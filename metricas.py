"""
Módulo de Métricas
Calcula las métricas de rendimiento por proceso y globales:
- Turnaround Time (TAT - Tiempo de Retorno)
- Waiting Time (WT - Tiempo de Espera)
- Response Time (RT - Tiempo de Respuesta)
- Conteo de cambios de contexto
- Equidad: Desviación estándar de tiempos de espera
- Inanición (Starvation): Identificación de procesos con espera desproporcionada
- Generación de tablas resumen con pandas y exportación a CSV
"""

import math
import pandas as pd
from pcb import Proceso


class AnalizadorMetricas:
    """Clase utilitaria para computar y tabular métricas del simulador."""

    @staticmethod
    def calcular_metricas_por_proceso(procesos: list) -> list:
        """
        Calcula las métricas individuales para cada proceso simulado.
        :return: Lista de diccionarios con métricas por proceso.
        """
        filas = []
        for p in procesos:
            # Turnaround Time (TAT) = Tiempo de finalización - Tiempo de llegada
            tat = (p.tiempo_fin - p.tiempo_llegada) if p.tiempo_fin is not None else 0

            # Response Time (RT) = Tiempo de primera respuesta - Tiempo de llegada
            rt = (p.tiempo_inicio - p.tiempo_llegada) if p.tiempo_inicio is not None else 0

            # Waiting Time (WT) acumulado en cola de LISTOS
            wt = p.tiempo_espera

            # Verificación de integridad:
            # En teoría TAT = WT + CPU + IO.
            # Cuando costo_cs > 0, el tiempo que el proceso esperó en el cambio de contexto
            # también suma a su espera efectiva, lo cual es coherente.
            cpu_total = p.tiempo_cpu_ejecutado
            io_total = p.tiempo_io_ejecutado

            # Ratio de penalización = WT / CPU (indica cuántas veces su ráfaga tuvo que esperar)
            ratio_penalizacion = round(wt / cpu_total, 2) if cpu_total > 0 else 0.0

            filas.append({
                "PID": p.pid,
                "Nombre": p.nombre,
                "Llegada": p.tiempo_llegada,
                "CPU_Total": cpu_total,
                "IO_Total": io_total,
                "Inicio_CPU": p.tiempo_inicio,
                "Fin": p.tiempo_fin,
                "TAT": tat,
                "WT": wt,
                "RT": rt,
                "CS": p.cambios_contexto,
                "Ratio_WT_CPU": ratio_penalizacion
            })

        return filas

    @staticmethod
    def calcular_metricas_globales(filas_procesos: list, cambios_contexto_totales: int,
                                   nombre_algoritmo: str, costo_cs: int) -> dict:
        """
        Calcula promedios, dispersión y análisis de inanición para todo el conjunto de procesos.
        """
        n = len(filas_procesos)
        if n == 0:
            return {}

        avg_tat = sum(f["TAT"] for f in filas_procesos) / n
        avg_wt = sum(f["WT"] for f in filas_procesos) / n
        avg_rt = sum(f["RT"] for f in filas_procesos) / n

        # Desviación estándar poblacional del tiempo de espera (Métrica de equidad)
        # Menor valor = trato más parejo entre procesos
        varianza_wt = sum((f["WT"] - avg_wt) ** 2 for f in filas_procesos) / n
        std_wt = math.sqrt(varianza_wt)

        # Detección de Inanición / Espera excesiva:
        # Criterio 1: Ratio de penalización (WT / CPU) >= 4.0
        # Criterio 2: WT > avg_wt + 1.5 * std_wt (proceso atípico / outlier estadístico)
        procesos_inanicion = []
        for f in filas_procesos:
            motivos = []
            if f["Ratio_WT_CPU"] >= 4.0:
                motivos.append(f"Ratio WT/CPU={f['Ratio_WT_CPU']:.1f}x (>= 4.0)")
            if f["WT"] > (avg_wt + 1.5 * std_wt) and std_wt > 1.0:
                motivos.append(f"WT={f['WT']} > Umbral estadístico ({avg_wt + 1.5 * std_wt:.1f})")

            if motivos:
                procesos_inanicion.append({
                    "PID": f["PID"],
                    "Nombre": f["Nombre"],
                    "WT": f["WT"],
                    "Motivo": " | ".join(motivos)
                })

        return {
            "Algoritmo": nombre_algoritmo,
            "Costo_CS": costo_cs,
            "Procesos": n,
            "Promedio_TAT": round(avg_tat, 2),
            "Promedio_WT": round(avg_wt, 2),
            "Promedio_RT": round(avg_rt, 2),
            "Total_CS": cambios_contexto_totales,
            "DesvStd_WT (Equidad)": round(std_wt, 2),
            "Casos_Inanicion": len(procesos_inanicion),
            "Detalle_Inanicion": procesos_inanicion
        }

    @staticmethod
    def generar_dataframe_procesos(filas_procesos: list) -> pd.DataFrame:
        """Convierte las métricas por proceso en un DataFrame ordenado de pandas."""
        df = pd.DataFrame(filas_procesos)
        return df

    @staticmethod
    def generar_dataframe_resumen(resumenes_globales: list) -> pd.DataFrame:
        """Convierte una lista de resúmenes de algoritmos en una tabla comparativa."""
        # Omitimos el detalle dict para la tabla tabular limpia
        datos_tabla = []
        for r in resumenes_globales:
            copia = {k: v for k, v in r.items() if k != "Detalle_Inanicion"}
            datos_tabla.append(copia)
        return pd.DataFrame(datos_tabla)

    @staticmethod
    def calcular_metricas_memoria(gestor_memoria, procesos: list) -> dict:
        """
        Calcula las métricas consolidadas de gestión de memoria con paginación.
        """
        if gestor_memoria is None:
            return {}

        resumen = gestor_memoria.obtener_resumen_metricas()

        # Fragmentación interna acumulada
        frag_interna_total = sum(
            gestor_memoria.calcular_fragmentacion_interna(p) for p in procesos
        )
        resumen["Fragmentacion_Interna_Total_Bytes"] = frag_interna_total
        resumen["Num_Marcos_RAM"] = gestor_memoria.num_marcos
        resumen["Tamano_Pagina_Bytes"] = gestor_memoria.tamano_pagina
        return resumen

    @staticmethod
    def calcular_fragmentacion_procesos(gestor_memoria, procesos: list) -> list:
        """
        Detalla la fragmentación interna individual de cada proceso.
        Fórmula: memoria_asignada - memoria_necesitada
        """
        if gestor_memoria is None:
            return []

        filas = []
        for p in procesos:
            num_pags = math.ceil(p.memoria_necesitada_bytes / gestor_memoria.tamano_pagina)
            mem_asignada = num_pags * gestor_memoria.tamano_pagina
            frag_interna = mem_asignada - p.memoria_necesitada_bytes

            filas.append({
                "PID": p.pid,
                "Nombre": p.nombre,
                "Memoria_Necesitada_Bytes": p.memoria_necesitada_bytes,
                "Paginas_Asignadas": num_pags,
                "Memoria_Asignada_Bytes": mem_asignada,
                "Fragmentacion_Interna_Bytes": frag_interna
            })
        return filas
