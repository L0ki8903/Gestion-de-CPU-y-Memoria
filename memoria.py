"""
Módulo de Gestión de Memoria con Paginación
Implementa:
- MarcoFisico (Frames de memoria física RAM).
- TablaPaginas y EntradaTablaPagina (por proceso).
- Estrategias de reemplazo: ReemplazoFIFO y ReemplazoLRU.
- GestorMemoria con el procedimiento de traducción de direcciones virtuales
  a físicas en 4 pasos según las diapositivas del curso.
- Cálculo de fragmentación interna y externa.
"""

import math
from pcb import Proceso


class MarcoFisico:
    """Representa un marco (frame) de tamaño fijo en la memoria RAM física."""

    def __init__(self, id_marco: int):
        self.id_marco = id_marco
        self.pid_ocupante = None
        self.pagina_ocupante = None
        self.tiempo_carga = -1     # Instante en que se cargó la página (para FIFO)
        self.ultimo_acceso = -1    # Instante del último acceso de lectura/escritura (para LRU)
        self.libre = True

    def asignar(self, pid: int, pagina: int, t: int):
        """Asigna el marco físico a una página de un proceso."""
        self.pid_ocupante = pid
        self.pagina_ocupante = pagina
        self.tiempo_carga = t
        self.ultimo_acceso = t
        self.libre = False

    def liberar(self):
        """Libera el marco físico haciéndolo disponible para cualquier proceso."""
        self.pid_ocupante = None
        self.pagina_ocupante = None
        self.tiempo_carga = -1
        self.ultimo_acceso = -1
        self.libre = True

    def __repr__(self) -> str:
        if self.libre:
            return f"Marco {self.id_marco}: [LIBRE]"
        return f"Marco {self.id_marco}: [PID={self.pid_ocupante}, Pag={self.pagina_ocupante}]"


class EntradaTablaPagina:
    """Entrada individual de la tabla de páginas de un proceso."""

    def __init__(self, pagina_virtual: int):
        self.pagina_virtual = pagina_virtual
        self.marco_fisico = None
        self.presente = False      # Bit de presencia (True si está en RAM, False si requiere fallo)


class TablaPaginas:
    """Tabla de páginas de un proceso. Mapea páginas virtuales a marcos físicos."""

    def __init__(self, pid: int, num_paginas: int):
        self.pid = pid
        self.num_paginas = num_paginas
        self.entradas = {
            pag: EntradaTablaPagina(pag) for pag in range(num_paginas)
        }

    def mapear(self, pagina_virtual: int, id_marco: int):
        """Asocia una página virtual a un marco físico cargado en RAM."""
        if pagina_virtual in self.entradas:
            self.entradas[pagina_virtual].marco_fisico = id_marco
            self.entradas[pagina_virtual].presente = True

    def desmapear(self, pagina_virtual: int):
        """Invalida la entrada cuando la página es desalojada de la RAM (víctima de reemplazo)."""
        if pagina_virtual in self.entradas:
            self.entradas[pagina_virtual].marco_fisico = None
            self.entradas[pagina_virtual].presente = False

    def obtener_marco(self, pagina_virtual: int) -> int:
        """Retorna el marco físico si la página está presente, o None si no lo está."""
        entrada = self.entradas.get(pagina_virtual)
        if entrada and entrada.presente:
            return entrada.marco_fisico
        return None

    def esta_presente(self, pagina_virtual: int) -> bool:
        """Verifica si la página se encuentra actualmente en memoria principal."""
        entrada = self.entradas.get(pagina_virtual)
        return entrada.presente if entrada else False


class EstrategiaReemplazo:
    """Clase base intercambiable para los algoritmos de reemplazo de páginas."""

    def __init__(self, nombre: str):
        self.nombre = nombre

    def registrar_acceso(self, marco: MarcoFisico, t: int):
        """Actualiza metadatos del marco tras un acceso (relevante para LRU)."""
        pass

    def seleccionar_victima(self, marcos_ocupados: list) -> MarcoFisico:
        """Selecciona el marco que será desalojado para cargar una nueva página."""
        raise NotImplementedError


class ReemplazoFIFO(EstrategiaReemplazo):
    """
    Algoritmo First-In, First-Out (FIFO).
    Reemplaza la página que lleva más tiempo cargada en la RAM (menor tiempo_carga).
    """

    def __init__(self):
        super().__init__("FIFO")

    def registrar_acceso(self, marco: MarcoFisico, t: int):
        # En FIFO el orden de llegada no cambia con accesos subsecuentes
        pass

    def seleccionar_victima(self, marcos_ocupados: list) -> MarcoFisico:
        # Víctima: menor tiempo_carga; desempate por menor id_marco
        return min(marcos_ocupados, key=lambda m: (m.tiempo_carga, m.id_marco))


class ReemplazoLRU(EstrategiaReemplazo):
    """
    Algoritmo Least Recently Used (LRU).
    Reemplaza la página menos recientemente usada (menor ultimo_acceso).
    """

    def __init__(self):
        super().__init__("LRU")

    def registrar_acceso(self, marco: MarcoFisico, t: int):
        # En LRU se actualiza la estampa del último acceso en cada referencia
        marco.ultimo_acceso = t

    def seleccionar_victima(self, marcos_ocupados: list) -> MarcoFisico:
        # Víctima: menor ultimo_acceso; desempate por menor id_marco
        return min(marcos_ocupados, key=lambda m: (m.ultimo_acceso, m.id_marco))


class GestorMemoria:
    """
    Administrador central de memoria y MMU simulada.
    Implementa:
    - Paginación pura de tamaño fijo.
    - Traducción de direcciones virtuales a físicas en 4 pasos exactos.
    - Manejo de fallos de página y reemplazo de páginas (FIFO / LRU).
    - Monitoreo de fragmentación interna y externa.
    """

    def __init__(self, tamano_ram: int = 32768, tamano_pagina: int = 4096,
                 estrategia: EstrategiaReemplazo = None):
        """
        :param tamano_ram: Tamaño total de la RAM física en bytes (por defecto 32 KB).
        :param tamano_pagina: Tamaño de página y marco en bytes (por defecto 4 KB).
        :param estrategia: Instancia de EstrategiaReemplazo (ReemplazoFIFO o ReemplazoLRU).
        """
        self.tamano_ram = tamano_ram
        self.tamano_pagina = tamano_pagina
        self.num_marcos = tamano_ram // tamano_pagina
        self.estrategia = estrategia if estrategia is not None else ReemplazoFIFO()

        # Marcos físicos de la RAM
        self.marcos = [MarcoFisico(i) for i in range(self.num_marcos)]

        # Tablas de páginas activas por PID: {pid: TablaPaginas}
        self.tablas_paginas = {}

        # Contadores de rendimiento
        self.total_accesos = 0
        self.total_aciertos = 0
        self.total_fallos = 0
        self.total_reemplazos = 0

        # Registro de ocupación y logs
        self.historial_ocupacion = []  # Lista de dicts {tiempo, marcos_ocupados, pct_ocupacion}
        self.log_traducciones = []

    def inicializar_proceso(self, proceso: Proceso):
        """
        Crea la tabla de páginas del proceso en la transición NUEVO -> LISTO.
        Calcula el número de páginas necesarias según su memoria requerida.
        """
        num_paginas = math.ceil(proceso.memoria_necesitada_bytes / self.tamano_pagina)
        self.tablas_paginas[proceso.pid] = TablaPaginas(proceso.pid, num_paginas)

    def liberar_proceso(self, proceso: Proceso):
        """
        Libera todos los marcos ocupados por el proceso en la transición EJECUCION -> FINALIZADO.
        """
        for marco in self.marcos:
            if marco.pid_ocupante == proceso.pid:
                marco.liberar()
        if proceso.pid in self.tablas_paginas:
            del self.tablas_paginas[proceso.pid]

    def traducir_direccion(self, proceso: Proceso, dir_virtual: int, t: int) -> tuple:
        """
        PROCEDIMIENTO DE TRADUCCIÓN DE 4 PASOS (según diapositivas del profesor):
        1. Calcular número de página = dirección_virtual // tamaño_página
        2. Calcular desplazamiento = dirección_virtual % tamaño_página
        3. Consultar la tabla de páginas: página -> marco (si no está, fallo de página y reemplazo)
        4. dirección_física = marco * tamaño_página + desplazamiento

        :return: (dir_fisica, es_fallo, id_marco)
        """
        self.total_accesos += 1
        tabla = self.tablas_paginas.get(proceso.pid)
        if tabla is None:
            self.inicializar_proceso(proceso)
            tabla = self.tablas_paginas[proceso.pid]

        # PASO 1: Calcular número de página
        num_pagina = dir_virtual // self.tamano_pagina

        # PASO 2: Calcular desplazamiento
        desplazamiento = dir_virtual % self.tamano_pagina

        # Validación estricta de límites de memoria (Detección de Segmentation Fault)
        if num_pagina >= tabla.num_paginas:
            mensaje_error = (
                f"VIOLACIÓN DE SEGMENTO (Segmentation Fault): PID {proceso.pid} ({proceso.nombre}) "
                f"intentó acceder a Dir.Virtual {dir_virtual} (Página {num_pagina}), "
                f"pero su espacio asignado solo comprende {tabla.num_paginas} páginas [0-{tabla.num_paginas - 1}]."
            )
            self.log_traducciones.append(f"[t={t:03d}] PID {proceso.pid} | {mensaje_error}")
            raise IndexError(mensaje_error)

        # PASO 3: Consultar la tabla de páginas
        es_fallo = False
        id_marco = tabla.obtener_marco(num_pagina)

        if id_marco is not None:
            # ACIERTO (HIT): La página ya está en RAM
            self.total_aciertos += 1
            marco = self.marcos[id_marco]
            self.estrategia.registrar_acceso(marco, t)
        else:
            # FALLO DE PÁGINA (PAGE FAULT): La página no está en RAM
            self.total_fallos += 1
            es_fallo = True

            # Buscar marco libre
            marcos_libres = [m for m in self.marcos if m.libre]
            if marcos_libres:
                marco = marcos_libres[0]
            else:
                # Reemplazo de páginas: la RAM está llena, elegir víctima según FIFO o LRU
                marcos_ocupados = [m for m in self.marcos if not m.libre]
                marco = self.estrategia.seleccionar_victima(marcos_ocupados)
                
                # Desmapear la página antigua del proceso víctima
                if marco.pid_ocupante in self.tablas_paginas:
                    self.tablas_paginas[marco.pid_ocupante].desmapear(marco.pagina_ocupante)
                self.total_reemplazos += 1

            # Cargar la nueva página en el marco seleccionado
            marco.asignar(proceso.pid, num_pagina, t)
            tabla.mapear(num_pagina, marco.id_marco)
            id_marco = marco.id_marco

        # PASO 4: dirección_física = marco * tamaño_página + desplazamiento
        dir_fisica = (id_marco * self.tamano_pagina) + desplazamiento

        # Registrar log detallado de traducción
        evento = "FALLO" if es_fallo else "ACIERTO"
        linea_log = (
            f"[t={t:03d}] PID {proceso.pid} ({proceso.nombre}) | "
            f"Dir.Virtual={dir_virtual:05d} -> "
            f"Paso 1: Pag={num_pagina} | "
            f"Paso 2: Offset={desplazamiento:04d} | "
            f"Paso 3: Marco={id_marco} ({evento}) | "
            f"Paso 4: Dir.Fisica={dir_fisica:05d}"
        )
        self.log_traducciones.append(linea_log)

        # Registrar ocupación de RAM en este instante
        marcos_usados = sum(1 for m in self.marcos if not m.libre)
        self.historial_ocupacion.append({
            "tiempo": t,
            "marcos_ocupados": marcos_usados,
            "total_marcos": self.num_marcos,
            "pct_ocupacion": round((marcos_usados / self.num_marcos) * 100, 2)
        })

        return (dir_fisica, es_fallo, id_marco)

    def calcular_fragmentacion_interna(self, proceso: Proceso) -> int:
        """
        Fórmula de las diapositivas:
        memoria_asignada - memoria_necesitada
        Donde memoria_asignada = num_paginas * tamano_pagina
        """
        num_paginas = math.ceil(proceso.memoria_necesitada_bytes / self.tamano_pagina)
        memoria_asignada = num_paginas * self.tamano_pagina
        return memoria_asignada - proceso.memoria_necesitada_bytes

    def obtener_resumen_metricas(self) -> dict:
        """Genera el diccionario resumen con las métricas de memoria."""
        pfr = (self.total_fallos / self.total_accesos * 100) if self.total_accesos > 0 else 0.0
        hr = (self.total_aciertos / self.total_accesos * 100) if self.total_accesos > 0 else 0.0
        return {
            "Estrategia": self.estrategia.nombre,
            "Total_Accesos": self.total_accesos,
            "Total_Aciertos": self.total_aciertos,
            "Total_Fallos": self.total_fallos,
            "Total_Reemplazos": self.total_reemplazos,
            "Hit_Rate_HR (%)": round(hr, 2),
            "Page_Fault_Rate_PFR (%)": round(pfr, 2),
            "Fragmentacion_Externa_Bytes": 0  # 0 bytes en paginación pura
        }
