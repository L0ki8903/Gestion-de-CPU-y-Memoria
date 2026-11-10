"""
Módulo de Planificadores de CPU (Schedulers)
Implementa la clase base y los 3 algoritmos requeridos:
1. FCFS (First-Come, First-Served)
2. SJF No Expropiativo (Shortest Job First)
3. Round Robin (con quantum configurable)
"""

from collections import deque
from pcb import Proceso


class PlanificadorBase:
    """Clase base simple para los algoritmos de planificación."""

    def __init__(self, nombre: str):
        self.nombre = nombre

    def encolar(self, proceso: Proceso):
        """Agrega un proceso que acaba de pasar a estado LISTO."""
        raise NotImplementedError

    def despachar(self) -> Proceso:
        """Extrae y retorna el siguiente proceso a recibir CPU."""
        raise NotImplementedError

    def reencolar_por_quantum(self, proceso: Proceso):
        """Reingresa a la cola un proceso que agotó su quantum (relevante para Round Robin)."""
        self.encolar(proceso)

    def esta_vacia(self) -> bool:
        """Verifica si no hay procesos listos para ejecutar."""
        raise NotImplementedError

    def obtener_cola(self) -> list:
        """Retorna una lista con los procesos actualmente en la cola de listos (para monitoreo/depuración)."""
        raise NotImplementedError


class PlanificadorFCFS(PlanificadorBase):
    """
    Planificador First-Come, First-Served (FCFS).
    El primer proceso en llegar a la cola de listos es el primero en ser atendido.
    Es un algoritmo estrictamente no expropiativo.
    """

    def __init__(self):
        super().__init__("FCFS")
        self.cola = deque()

    def encolar(self, proceso: Proceso):
        self.cola.append(proceso)

    def despachar(self) -> Proceso:
        if self.cola:
            return self.cola.popleft()
        return None

    def esta_vacia(self) -> bool:
        return len(self.cola) == 0

    def obtener_cola(self) -> list:
        return list(self.cola)


class PlanificadorSJFNoExpropiativo(PlanificadorBase):
    """
    Planificador Shortest Job First (SJF) No Expropiativo.
    Selecciona de la cola de listos el proceso con la ráfaga de CPU actual más corta.
    Una vez asignada la CPU, no se expropia hasta que termine la ráfaga o se bloquee por E/S.
    """

    def __init__(self):
        super().__init__("SJF (No Expropiativo)")
        self.lista_listos = []

    def encolar(self, proceso: Proceso):
        self.lista_listos.append(proceso)

    def despachar(self) -> Proceso:
        if not self.lista_listos:
            return None

        # CRITERIO DE SELECCIÓN Y DESEMPATE:
        # 1. Menor duración de la ráfaga de CPU actual (o restante de la ráfaga actual).
        # 2. Desempate 1: Menor tiempo de llegada al sistema (FCFS local).
        # 3. Desempate 2: Menor PID para desempatar determinísticamente.
        #
        # TODO (Debate para informe): ¿Se debe ordenar por la ráfaga de CPU actual o por
        # el total acumulado de ráfagas restantes del proceso? En sistemas operativos reales
        # con E/S, el planificador solo conoce la duración estimada de la próxima ráfaga de CPU.
        # Aquí usamos la duración de la ráfaga actual (tiempo_restante_rafaga_actual).
        self.lista_listos.sort(
            key=lambda p: (p.tiempo_restante_rafaga_actual, p.tiempo_llegada, p.pid)
        )
        return self.lista_listos.pop(0)

    def esta_vacia(self) -> bool:
        return len(self.lista_listos) == 0

    def obtener_cola(self) -> list:
        return list(self.lista_listos)


class PlanificadorRoundRobin(PlanificadorBase):
    """
    Planificador Round Robin (RR).
    Asigna la CPU por un intervalo de tiempo fijo (quantum).
    Si el proceso no termina durante su quantum, es expropiado y colocado al final de la cola.
    """

    def __init__(self, quantum: int):
        if quantum <= 0:
            raise ValueError("El quantum debe ser un número entero mayor a 0.")
        super().__init__(f"Round Robin (Q={quantum})")
        self.quantum = quantum
        self.cola = deque()

    def encolar(self, proceso: Proceso):
        """Encola procesos nuevos o desbloqueados."""
        self.cola.append(proceso)

    def reencolar_por_quantum(self, proceso: Proceso):
        """
        Reencola un proceso cuyo quantum expiró.
        TODO (Debate para informe): En caso de llegada simultánea de un proceso nuevo
        y expiración de quantum de otro, ¿quién entra antes a la cola?
        Nuestra política (acordada en el plan) favorece a los nuevos procesos para
        optimizar su tiempo de respuesta (RT). El simulador aplica esta prioridad.
        """
        self.cola.append(proceso)

    def despachar(self) -> Proceso:
        if self.cola:
            return self.cola.popleft()
        return None

    def esta_vacia(self) -> bool:
        return len(self.cola) == 0

    def obtener_cola(self) -> list:
        return list(self.cola)
