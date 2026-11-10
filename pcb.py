"""
Módulo PCB (Process Control Block)
Define la estructura del proceso y sus estados según el modelo de 5 estados:
NUEVO, LISTO, EJECUCION, BLOQUEADO y FINALIZADO.
Incluye atributos para gestión de memoria con paginación.
"""

from enum import Enum
import copy


class EstadoProceso(Enum):
    """Estados del ciclo de vida del proceso en el sistema operativo."""
    NUEVO = "NUEVO"
    LISTO = "LISTO"
    EJECUCION = "EJECUCION"
    BLOQUEADO = "BLOQUEADO"
    FINALIZADO = "FINALIZADO"


class Proceso:
    """
    Representa el Bloque de Control de Proceso (PCB).
    Almacena los atributos estáticos del proceso, sus métricas de ejecución
    y sus requerimientos de memoria virtual para paginación.
    """

    def __init__(self, pid: int, nombre: str, tiempo_llegada: int, rafagas: list,
                 memoria_necesitada_bytes: int = 4096, patron_accesos: list = None):
        """
        Constructor del PCB.
        :param pid: Identificador numérico único del proceso.
        :param nombre: Nombre amigable (ej. 'P1').
        :param tiempo_llegada: Instante t en que el proceso ingresa al sistema.
        :param rafagas: Lista de tuplas indicando ráfagas [("CPU", duracion), ("IO", duracion), ...]
        :param memoria_necesitada_bytes: Memoria requerida en bytes por el proceso.
        :param patron_accesos: Lista de direcciones virtuales a consultar durante las ráfagas de CPU.
        """
        if pid is None or not isinstance(pid, int) or pid < 0:
            raise ValueError(f"PID inválido '{pid}': debe ser un entero no negativo.")
        if tiempo_llegada < 0:
            raise ValueError(f"Tiempo de llegada inválido '{tiempo_llegada}' en proceso {nombre}: no puede ser negativo.")
        if not rafagas:
            raise ValueError(f"El proceso {nombre} (PID={pid}) debe contener al menos una ráfaga.")
        for tipo, duracion in rafagas:
            if tipo not in ("CPU", "IO"):
                raise ValueError(f"Tipo de ráfaga inválido '{tipo}' en proceso {nombre}: debe ser 'CPU' o 'IO'.")
            if not isinstance(duracion, int) or duracion <= 0:
                raise ValueError(f"Duración inválida en ráfaga ({tipo}, {duracion}) del proceso {nombre}: debe ser un entero mayor a 0.")

        self.pid = pid
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        
        # Guardamos copia de las ráfagas originales para poder clonar o reiniciar
        self.rafagas_originales = copy.deepcopy(rafagas)
        self.rafagas = copy.deepcopy(rafagas)
        
        # Puntero a la ráfaga actual y tiempo restante de dicha ráfaga
        self.indice_rafaga = 0
        self.tiempo_restante_rafaga_actual = self.rafagas[0][1]

        # Estado inicial
        self.estado = EstadoProceso.NUEVO

        # Marcas de tiempo (timestamps) para métricas
        self.tiempo_inicio = None    # Primer instante en que recibe CPU (para Response Time)
        self.tiempo_fin = None       # Instante en que pasa a FINALIZADO (para Turnaround Time)
        
        # Contadores acumulados
        self.tiempo_espera = 0           # Ciclos transcurridos en cola de LISTOS (Waiting Time)
        self.tiempo_cpu_ejecutado = 0     # Ciclos totales ejecutados en CPU
        self.tiempo_io_ejecutado = 0      # Ciclos totales pasados en BLOQUEADO por E/S
        self.cambios_contexto = 0        # Número de veces que fue despachado a la CPU

        # Atributos de memoria para paginación
        self.memoria_necesitada_bytes = memoria_necesitada_bytes
        self.patron_accesos = copy.deepcopy(patron_accesos if patron_accesos is not None else [])
        self.indice_acceso_memoria = 0

    def obtener_tipo_rafaga_actual(self) -> str:
        """Retorna 'CPU', 'IO' o 'FIN' si ya terminó todas las ráfagas."""
        if self.indice_rafaga < len(self.rafagas):
            return self.rafagas[self.indice_rafaga][0]
        return "FIN"

    def rafaga_cpu_total(self) -> int:
        """Calcula la suma total de todas las ráfagas de CPU asignadas."""
        return sum(duracion for tipo, duracion in self.rafagas_originales if tipo == "CPU")

    def rafaga_io_total(self) -> int:
        """Calcula la suma total de todas las ráfagas de E/S asignadas."""
        return sum(duracion for tipo, duracion in self.rafagas_originales if tipo == "IO")

    def obtener_siguiente_direccion_virtual(self, tamano_pagina: int = 4096) -> int:
        """
        Retorna la dirección virtual que el proceso solicita en el ciclo actual de CPU.
        Si se definió un patrón explícito, lo recorre cíclicamente. De lo contrario,
        itera ordenadamente sobre su espacio de páginas virtuales.
        """
        if self.patron_accesos:
            dir_v = self.patron_accesos[self.indice_acceso_memoria % len(self.patron_accesos)]
            self.indice_acceso_memoria += 1
            return dir_v
        
        # Comportamiento por defecto determinista: recorre las páginas que necesita
        num_pags = max(1, (self.memoria_necesitada_bytes + tamano_pagina - 1) // tamano_pagina)
        pag = self.tiempo_cpu_ejecutado % num_pags
        return (pag * tamano_pagina) + 128

    def es_finalizado(self) -> bool:
        """Indica si el proceso completó todas sus ráfagas de CPU y E/S."""
        return self.estado == EstadoProceso.FINALIZADO

    def clonar(self) -> 'Proceso':
        """
        Genera una copia fresca e independiente del proceso con sus métricas en cero.
        Permite simular el mismo conjunto de procesos en distintos algoritmos.
        """
        return Proceso(
            pid=self.pid,
            nombre=self.nombre,
            tiempo_llegada=self.tiempo_llegada,
            rafagas=self.rafagas_originales,
            memoria_necesitada_bytes=self.memoria_necesitada_bytes,
            patron_accesos=self.patron_accesos
        )

    def __repr__(self) -> str:
        return f"PCB({self.nombre}, Estado={self.estado.value}, Llegada={self.tiempo_llegada}, Memoria={self.memoria_necesitada_bytes}B)"
