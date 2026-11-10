"""
Módulo Simulador de CPU
Implementa el motor de simulación con reloj discreto ciclo a ciclo (tick-by-tick).
Gestiona:
- Transiciones de estado con log detallado.
- Despacho y expropiación según el planificador activo.
- Colas de listos y bloqueados (E/S).
- Costo configurable de cambio de contexto (costo_cs).
- Generación de timeline para el diagrama de Gantt.
"""

from pcb import Proceso, EstadoProceso
from planificadores import PlanificadorBase, PlanificadorRoundRobin


class ResultadoSimulacion:
    """Contenedor para los resultados completos de una corrida de simulación."""

    def __init__(self, nombre_algoritmo: str, costo_cs: int, procesos: list,
                 timeline_gantt: list, log_transiciones: list,
                 cambios_contexto_totales: int, tiempo_total: int,
                 gestor_memoria=None):
        self.nombre_algoritmo = nombre_algoritmo
        self.costo_cs = costo_cs
        self.procesos = procesos
        self.timeline_gantt = timeline_gantt
        self.log_transiciones = log_transiciones
        self.cambios_contexto_totales = cambios_contexto_totales
        self.tiempo_total = tiempo_total
        self.gestor_memoria = gestor_memoria


class SimuladorCPU:
    """
    Motor de simulación de planificación de CPU y gestión de memoria con paginación.
    """

    def __init__(self, planificador: PlanificadorBase, costo_cs: int = 1,
                 gestor_memoria=None):
        """
        :param planificador: Instancia de PlanificadorBase (FCFS, SJF, RR).
        :param costo_cs: Costo en ticks de reloj por cambio de contexto (0 = instantáneo, 1 = 1 tick, etc.).
        :param gestor_memoria: Instancia opcional de GestorMemoria para simular paginación.
        """
        if costo_cs < 0:
            raise ValueError(f"El costo de cambio de contexto ({costo_cs}) no puede ser negativo.")
        self.planificador = planificador
        self.costo_cs = costo_cs
        self.gestor_memoria = gestor_memoria

    def _registrar_transicion(self, logs: list, t: int, proceso: Proceso,
                              estado_origen: EstadoProceso, estado_destino: EstadoProceso,
                              motivo: str):
        """Registra una transición en el log con formato estructurado."""
        proceso.estado = estado_destino
        mensaje = (
            f"[t={t:03d}] PID {proceso.pid} ({proceso.nombre}): "
            f"{estado_origen.value} -> {estado_destino.value} | Motivo: {motivo}"
        )
        logs.append(mensaje)

    def ejecutar(self, procesos_originales: list) -> ResultadoSimulacion:
        """
        Ejecuta la simulación hasta que todos los procesos hayan finalizado.
        :param procesos_originales: Lista de objetos Proceso (se clonarán para no alterar el original).
        :return: Objeto ResultadoSimulacion con métricas y logs.
        """
        if not procesos_originales:
            raise ValueError("No se puede ejecutar la simulación: la lista de procesos a simular está vacía.")

        # Clonamos los procesos para asegurar aislamiento entre pruebas
        procesos = [p.clonar() for p in procesos_originales]

        tiempo_actual = 0
        proceso_en_cpu = None
        ultimo_proceso_cpu = None
        cola_bloqueados = []
        timeline_gantt = []
        log_transiciones = []
        cambios_contexto_totales = 0

        # Control del cambio de contexto
        ticks_cs_restante = 0
        proceso_en_cambio = None

        # Control de Round Robin
        ticks_quantum_restante = 0
        proceso_pendiente_reencolar = None

        # Límite de seguridad contra bucles infinitos (por si un input es inválido)
        limite_ticks = 100000

        while tiempo_actual < limite_ticks:
            # 1. ADMISIÓN DE NUEVOS PROCESOS (Llegadas en tiempo_actual)
            # Se ordenan por PID para consistencia en llegadas simultáneas
            nuevos_llegados = [p for p in procesos if p.tiempo_llegada == tiempo_actual and p.estado == EstadoProceso.NUEVO]
            nuevos_llegados.sort(key=lambda p: p.pid)

            for p in nuevos_llegados:
                self._registrar_transicion(
                    log_transiciones, tiempo_actual, p,
                    EstadoProceso.NUEVO, EstadoProceso.LISTO,
                    "Llegada al sistema"
                )
                if self.gestor_memoria is not None:
                    self.gestor_memoria.inicializar_proceso(p)
                self.planificador.encolar(p)

            # 2. REENCOLAR PROCESO CUYO QUANTUM EXPIRÓ EN EL TICK ANTERIOR
            # Se reencola después de los nuevos llegados para favorecer el tiempo de respuesta
            if proceso_pendiente_reencolar is not None:
                self.planificador.reencolar_por_quantum(proceso_pendiente_reencolar)
                proceso_pendiente_reencolar = None

            # 3. AVANCE Y DESBLOQUEO DE PROCESOS EN E/S (BLOQUEADOS)
            # Procesamos E/S en este tick
            desbloqueados = []
            for p in list(cola_bloqueados):
                p.tiempo_restante_rafaga_actual -= 1
                p.tiempo_io_ejecutado += 1

                if p.tiempo_restante_rafaga_actual == 0:
                    # Terminó su ráfaga de E/S
                    p.indice_rafaga += 1
                    if p.indice_rafaga < len(p.rafagas):
                        p.tiempo_restante_rafaga_actual = p.rafagas[p.indice_rafaga][1]

                    cola_bloqueados.remove(p)
                    desbloqueados.append(p)

            # Reingreso de procesos desbloqueados a la cola de listos
            desbloqueados.sort(key=lambda p: p.pid)
            for p in desbloqueados:
                self._registrar_transicion(
                    log_transiciones, tiempo_actual, p,
                    EstadoProceso.BLOQUEADO, EstadoProceso.LISTO,
                    "Fin de operación de E/S"
                )
                self.planificador.encolar(p)

            # 4. GESTIÓN DE CPU Y CAMBIO DE CONTEXTO
            tick_consumido_por_cs = False
            proceso_esperando_cs = None  # Proceso en LISTO que sufre el overhead de CS antes de ejecutar

            if ticks_cs_restante > 0:
                # La CPU está ocupada realizando el overhead del cambio de contexto
                timeline_gantt.append({
                    "inicio": tiempo_actual,
                    "fin": tiempo_actual + 1,
                    "tipo": "CS",
                    "pid": "CS",
                    "detalle": f"Overhead cambio contexto hacia {proceso_en_cambio.nombre}"
                })
                ticks_cs_restante -= 1
                tick_consumido_por_cs = True
                proceso_esperando_cs = proceso_en_cambio

                if ticks_cs_restante == 0:
                    # El cambio de contexto terminó al final de este tick
                    proceso_en_cpu = proceso_en_cambio
                    proceso_en_cambio = None
                    self._registrar_transicion(
                        log_transiciones, tiempo_actual + 1, proceso_en_cpu,
                        EstadoProceso.LISTO, EstadoProceso.EJECUCION,
                        "CPU asignada tras cambio de contexto"
                    )
                    if isinstance(self.planificador, PlanificadorRoundRobin):
                        ticks_quantum_restante = self.planificador.quantum

            elif proceso_en_cpu is None:
                # La CPU está libre: intentar despachar el siguiente proceso listo
                if not self.planificador.esta_vacia():
                    siguiente = self.planificador.despachar()

                    # Evaluamos si hay cambio de contexto:
                    # Ocurre si había un proceso previo ejecutando y es diferente al nuevo.
                    #
                    # TODO (Debate para informe): ¿El primer despacho del sistema (de CPU inactiva
                    # a primer proceso) debe cobrar costo_cs? En este modelo solo cobramos cuando
                    # se conmuta entre dos procesos distintos (último != None y último != nuevo).
                    es_cambio = (ultimo_proceso_cpu is not None and ultimo_proceso_cpu.pid != siguiente.pid)

                    if es_cambio:
                        cambios_contexto_totales += 1
                        siguiente.cambios_contexto += 1

                        if self.costo_cs > 0:
                            # Inicia periodo de penalización por cambio de contexto
                            tick_consumido_por_cs = True
                            proceso_esperando_cs = siguiente
                            timeline_gantt.append({
                                "inicio": tiempo_actual,
                                "fin": tiempo_actual + 1,
                                "tipo": "CS",
                                "pid": "CS",
                                "detalle": f"Overhead cambio contexto hacia {siguiente.nombre}"
                            })

                            if self.costo_cs == 1:
                                # Si costo_cs == 1, el overhead termina al final de este mismo tick
                                proceso_en_cpu = siguiente
                                self._registrar_transicion(
                                    log_transiciones, tiempo_actual + 1, proceso_en_cpu,
                                    EstadoProceso.LISTO, EstadoProceso.EJECUCION,
                                    "CPU asignada tras cambio de contexto"
                                )
                                if isinstance(self.planificador, PlanificadorRoundRobin):
                                    ticks_quantum_restante = self.planificador.quantum
                            else:
                                proceso_en_cambio = siguiente
                                ticks_cs_restante = self.costo_cs - 1
                        else:
                            # costo_cs == 0: Cambio instantáneo
                            proceso_en_cpu = siguiente
                            self._registrar_transicion(
                                log_transiciones, tiempo_actual, proceso_en_cpu,
                                EstadoProceso.LISTO, EstadoProceso.EJECUCION,
                                "CPU asignada (cambio instantáneo)"
                            )
                            if isinstance(self.planificador, PlanificadorRoundRobin):
                                ticks_quantum_restante = self.planificador.quantum
                    else:
                        # No hay cambio de contexto (primer proceso o reingreso directo)
                        proceso_en_cpu = siguiente
                        self._registrar_transicion(
                            log_transiciones, tiempo_actual, proceso_en_cpu,
                            EstadoProceso.LISTO, EstadoProceso.EJECUCION,
                            "CPU asignada (despacho inicial/continuación)"
                        )
                        if isinstance(self.planificador, PlanificadorRoundRobin):
                            ticks_quantum_restante = self.planificador.quantum
                else:
                    # No hay procesos en cola de listos y no hay proceso en CPU -> OCIOSO (IDLE)
                    # Solo registramos IDLE si no todos han terminado
                    if not all(p.es_finalizado() for p in procesos):
                        timeline_gantt.append({
                            "inicio": tiempo_actual,
                            "fin": tiempo_actual + 1,
                            "tipo": "IDLE",
                            "pid": "IDLE",
                            "detalle": "CPU Ociosa (sin procesos listos)"
                        })

            # 5. EJECUCIÓN EN CPU (Si hay un proceso activo en este tick)
            if proceso_en_cpu is not None and not tick_consumido_por_cs:
                # Registrar tiempo de primera respuesta si aún no se ha marcado
                if proceso_en_cpu.tiempo_inicio is None:
                    proceso_en_cpu.tiempo_inicio = tiempo_actual

                # Registrar tick en Gantt
                timeline_gantt.append({
                    "inicio": tiempo_actual,
                    "fin": tiempo_actual + 1,
                    "tipo": "CPU",
                    "pid": proceso_en_cpu.nombre,
                    "detalle": f"Ejecutando ráfaga CPU ({proceso_en_cpu.nombre})"
                })

                # Consumo de ráfaga
                proceso_en_cpu.tiempo_restante_rafaga_actual -= 1
                proceso_en_cpu.tiempo_cpu_ejecutado += 1

                # Simulación de acceso a memoria con paginación durante la instrucción
                if self.gestor_memoria is not None:
                    dir_v = proceso_en_cpu.obtener_siguiente_direccion_virtual(self.gestor_memoria.tamano_pagina)
                    self.gestor_memoria.traducir_direccion(proceso_en_cpu, dir_v, tiempo_actual)

                if isinstance(self.planificador, PlanificadorRoundRobin):
                    ticks_quantum_restante -= 1

                # Comprobación de eventos al finalizar el ciclo de CPU:
                if proceso_en_cpu.tiempo_restante_rafaga_actual == 0:
                    # La ráfaga de CPU actual terminó
                    proceso_en_cpu.indice_rafaga += 1

                    if proceso_en_cpu.indice_rafaga < len(proceso_en_cpu.rafagas):
                        tipo_siguiente = proceso_en_cpu.rafagas[proceso_en_cpu.indice_rafaga][0]
                        if tipo_siguiente == "IO":
                            proceso_en_cpu.tiempo_restante_rafaga_actual = proceso_en_cpu.rafagas[proceso_en_cpu.indice_rafaga][1]
                            self._registrar_transicion(
                                log_transiciones, tiempo_actual + 1, proceso_en_cpu,
                                EstadoProceso.EJECUCION, EstadoProceso.BLOQUEADO,
                                "Solicitud de operación de E/S"
                            )
                            cola_bloqueados.append(proceso_en_cpu)
                            ultimo_proceso_cpu = proceso_en_cpu
                            proceso_en_cpu = None
                    else:
                        # El proceso completó todas sus ráfagas
                        proceso_en_cpu.tiempo_fin = tiempo_actual + 1
                        self._registrar_transicion(
                            log_transiciones, tiempo_actual + 1, proceso_en_cpu,
                            EstadoProceso.EJECUCION, EstadoProceso.FINALIZADO,
                            "Todas las ráfagas completadas"
                        )
                        if self.gestor_memoria is not None:
                            self.gestor_memoria.liberar_proceso(proceso_en_cpu)
                        ultimo_proceso_cpu = proceso_en_cpu
                        proceso_en_cpu = None

                elif isinstance(self.planificador, PlanificadorRoundRobin) and ticks_quantum_restante == 0:
                    # Expiró el quantum de Round Robin y aún le queda ráfaga de CPU
                    self._registrar_transicion(
                        log_transiciones, tiempo_actual + 1, proceso_en_cpu,
                        EstadoProceso.EJECUCION, EstadoProceso.LISTO,
                        f"Expiración de quantum (Q={self.planificador.quantum})"
                    )
                    proceso_pendiente_reencolar = proceso_en_cpu
                    ultimo_proceso_cpu = proceso_en_cpu
                    proceso_en_cpu = None

            # 6. INCREMENTO DE TIEMPO DE ESPERA (WAITING TIME)
            # Se incrementa en 1 tick para todo proceso en estado LISTO.
            # Nota: Los procesos que acaban de desbloquearse en este mismo tick (desbloqueados)
            # estuvieron ejecutando E/S durante este ciclo, por lo que su tiempo de espera
            # en cola de listos comienza formalmente en el siguiente ciclo (t + 1).
            for p in self.planificador.obtener_cola():
                if p not in desbloqueados:
                    p.tiempo_espera += 1

            # Si hay un proceso sufriendo el overhead del cambio de contexto hacia él,
            # está formalmente esperando en estado LISTO y debe acumular tiempo de espera
            if proceso_esperando_cs is not None:
                proceso_esperando_cs.tiempo_espera += 1

            # 7. AVANZAR EL RELOJ
            tiempo_actual += 1

            # Condición de término: todos los procesos en FINALIZADO y colas vacías
            todos_terminados = all(p.es_finalizado() for p in procesos)
            if (todos_terminados and not cola_bloqueados and
                    proceso_en_cpu is None and ticks_cs_restante == 0 and
                    proceso_pendiente_reencolar is None):
                break

        return ResultadoSimulacion(
            nombre_algoritmo=self.planificador.nombre,
            costo_cs=self.costo_cs,
            procesos=procesos,
            timeline_gantt=timeline_gantt,
            log_transiciones=log_transiciones,
            cambios_contexto_totales=cambios_contexto_totales,
            tiempo_total=tiempo_actual,
            gestor_memoria=self.gestor_memoria
        )
