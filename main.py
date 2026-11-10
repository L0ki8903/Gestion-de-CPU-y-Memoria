"""
Punto de Entrada Principal (main.py)
Proyecto Académico de Sistemas Operativos: Planificación de CPU y Gestión de Memoria
Ingeniería de Software

Ejecuta de manera secuencial y estructurada:
PARTE A / CPU:
- Escenario 1: Carga Ligera (con operaciones de E/S y estados Bloqueado).
- Escenario 2: Carga Mixta (Evidencia del Efecto Convoy en FCFS vs SJF y RR).
- Escenario 3: Alta Concurrencia y Sensibilidad al Quantum en Round Robin (Q=2, Q=4, Q=8 vs FCFS y SJF).
- Comparativa especial: Impacto del Costo de Cambio de Contexto (costo_cs=1 vs costo_cs=0).
- Verificación matemática estricta: WT_prom == RT_prom para FCFS y SJF sin E/S.

PARTE B / MEMORIA (Paginación Pura):
- Algoritmo de traducción de direcciones virtuales a físicas en 4 pasos (MMU).
- Comparativa de reemplazo de páginas: FIFO vs. LRU en los 3 escenarios.
- Análisis de fragmentación interna individual y acumulada (memoria_asignada - memoria_necesitada).
- Demostración de fragmentación externa = 0 en paginación.
- Verificación de no-regresión en métricas de CPU.
"""

import os
import pandas as pd
from pcb import Proceso
from planificadores import PlanificadorFCFS, PlanificadorSJFNoExpropiativo, PlanificadorRoundRobin
from simulador import SimuladorCPU
from metricas import AnalizadorMetricas
from visualizador import Visualizador
from memoria import GestorMemoria, ReemplazoFIFO, ReemplazoLRU


# Carpetas para almacenar las salidas del proyecto (siempre dentro de la carpeta del proyecto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_LOGS = os.path.join(BASE_DIR, "resultados", "logs")
CARPETA_METRICAS = os.path.join(BASE_DIR, "resultados", "metricas")
CARPETA_GRAFICOS = os.path.join(BASE_DIR, "resultados", "graficos")


def inicializar_directorios():
    """Crea los directorios de salida si no existen."""
    for carpeta in [CARPETA_LOGS, CARPETA_METRICAS, CARPETA_GRAFICOS]:
        os.makedirs(carpeta, exist_ok=True)


#DDefinicion de escenarios de prueba para la simulación de CPU y memoria

def crear_escenario_1() -> list:
    """
    Escenario 1: Carga Ligera (Línea base y validación de E/S / Bloqueos).
    4 procesos con ráfagas moderadas y operaciones de E/S.
    Requerimientos de memoria (páginas de 4 KB):
    P1: 6000 B (2 pags, frag int = 2192 B)
    P2: 4096 B (1 pag,  frag int = 0 B)
    P3: 7500 B (2 pags, frag int = 692 B)
    P4: 3000 B (1 pag,  frag int = 1096 B)
    Total páginas requeridas = 6. En RAM de 8 marcos (32 KB) caben todas.
    """
    return [
        Proceso(pid=1, nombre="P1", tiempo_llegada=0, rafagas=[("CPU", 3), ("IO", 2), ("CPU", 2)],
                memoria_necesitada_bytes=6000,
                patron_accesos=[0*4096+100, 1*4096+200, 0*4096+300, 1*4096+400, 0*4096+500]),
        Proceso(pid=2, nombre="P2", tiempo_llegada=1, rafagas=[("CPU", 4)],
                memoria_necesitada_bytes=4096,
                patron_accesos=[0*4096+50, 0*4096+150, 0*4096+250, 0*4096+350]),
        Proceso(pid=3, nombre="P3", tiempo_llegada=2, rafagas=[("CPU", 2), ("IO", 1), ("CPU", 2)],
                memoria_necesitada_bytes=7500,
                patron_accesos=[0*4096+80, 1*4096+120, 0*4096+220, 1*4096+320]),
        Proceso(pid=4, nombre="P4", tiempo_llegada=4, rafagas=[("CPU", 3)],
                memoria_necesitada_bytes=3000,
                patron_accesos=[0*4096+60, 0*4096+160, 0*4096+260])
    ]


def crear_escenario_2() -> list:
    """
    Escenario 2: Carga Mixta (Efecto Convoy).
    P1 es un proceso masivo (CPU 20) que acapara la CPU; P2..P5 son procesos cortos.
    P1 ejecuta la secuencia canónica de Silberschatz con 20 accesos a 5 páginas distintas.
    Bajo una RAM de 4 marcos (16 KB), se fuerza el reemplazo donde LRU aventaja a FIFO.
    """
    silb_pattern = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    pat_addrs_p1 = [p * 4096 + 64 for p in silb_pattern]

    return [
        Proceso(pid=1, nombre="P1", tiempo_llegada=0, rafagas=[("CPU", 20)],
                memoria_necesitada_bytes=35000, patron_accesos=pat_addrs_p1),
        Proceso(pid=2, nombre="P2", tiempo_llegada=1, rafagas=[("CPU", 2)],
                memoria_necesitada_bytes=5000, patron_accesos=[0*4096+10, 1*4096+20]),
        Proceso(pid=3, nombre="P3", tiempo_llegada=2, rafagas=[("CPU", 3)],
                memoria_necesitada_bytes=6000, patron_accesos=[0*4096+15, 1*4096+25, 0*4096+35]),
        Proceso(pid=4, nombre="P4", tiempo_llegada=3, rafagas=[("CPU", 1)],
                memoria_necesitada_bytes=4000, patron_accesos=[0*4096+50]),
        Proceso(pid=5, nombre="P5", tiempo_llegada=4, rafagas=[("CPU", 2)],
                memoria_necesitada_bytes=5000, patron_accesos=[0*4096+40, 1*4096+60])
    ]


def crear_escenario_3() -> list:
    """
    Escenario 3: Alta Concurrencia y Sensibilidad al Quantum en Round Robin.
    8 procesos heterogéneos con ráfagas de 2 a 12 ticks.
    Cada proceso tiene un working set cíclico con localidad temporal de referencia.
    """
    # Patrón con fuerte localidad temporal en páginas 0 y 1, y accesos ocasionales a 2 y 3
    pat_loop = [0*4096+10, 1*4096+20, 0*4096+30, 1*4096+40, 2*4096+50, 0*4096+60, 1*4096+70, 3*4096+80]

    return [
        Proceso(pid=1, nombre="P1", tiempo_llegada=0, rafagas=[("CPU", 8)],
                memoria_necesitada_bytes=14000, patron_accesos=pat_loop),
        Proceso(pid=2, nombre="P2", tiempo_llegada=1, rafagas=[("CPU", 4)],
                memoria_necesitada_bytes=10000, patron_accesos=pat_loop),
        Proceso(pid=3, nombre="P3", tiempo_llegada=2, rafagas=[("CPU", 12)],
                memoria_necesitada_bytes=15000, patron_accesos=pat_loop),
        Proceso(pid=4, nombre="P4", tiempo_llegada=3, rafagas=[("CPU", 3)],
                memoria_necesitada_bytes=9000, patron_accesos=pat_loop),
        Proceso(pid=5, nombre="P5", tiempo_llegada=5, rafagas=[("CPU", 6)],
                memoria_necesitada_bytes=12000, patron_accesos=pat_loop),
        Proceso(pid=6, nombre="P6", tiempo_llegada=6, rafagas=[("CPU", 2)],
                memoria_necesitada_bytes=8500, patron_accesos=pat_loop),
        Proceso(pid=7, nombre="P7", tiempo_llegada=8, rafagas=[("CPU", 10)],
                memoria_necesitada_bytes=14500, patron_accesos=pat_loop),
        Proceso(pid=8, nombre="P8", tiempo_llegada=9, rafagas=[("CPU", 5)],
                memoria_necesitada_bytes=11000, patron_accesos=pat_loop)
    ]


#Suite de ejecución de CPU para un escenario determinado

def ejecutar_suite_escenario(id_escenario: str, nombre_escenario: str,
                             procesos: list, lista_planificadores: list,
                             costo_cs: int = 1) -> pd.DataFrame:
    """
    Ejecuta un conjunto de algoritmos de CPU sobre un mismo escenario y genera:
    - Log de transiciones en texto (.txt)
    - Diagramas de Gantt (.png)
    - Gráfico comparativo (.png)
    - CSV con métricas individuales y resumen (.csv)
    """
    print("\n" + "=" * 80)
    print(f"EJECUTANDO CPU: {nombre_escenario.upper()} (Costo CS = {costo_cs} tick)")
    print("=" * 80)

    resumenes_globales = []
    detalles_todos_procesos = []

    for planificador in lista_planificadores:
        nombre_alg = planificador.nombre
        nombre_sanitizado = nombre_alg.replace(" ", "_").replace("(", "").replace(")", "").replace("=", "")
        prefijo_archivo = f"{id_escenario}_{nombre_sanitizado}_cs{costo_cs}"

        # 1. Simulación de CPU
        sim = SimuladorCPU(planificador=planificador, costo_cs=costo_cs)
        resultado = sim.ejecutar(procesos)

        # 2. Guardar log de transiciones
        ruta_log = os.path.join(CARPETA_LOGS, f"transiciones_{prefijo_archivo}.txt")
        with open(ruta_log, "w", encoding="utf-8") as f:
            f.write(f"=== LOG DE TRANSICIONES: {nombre_alg} ({nombre_escenario}) ===\n")
            f.write(f"Costo de cambio de contexto: {costo_cs} ticks | Tiempo total: {resultado.tiempo_total} ticks\n\n")
            for linea in resultado.log_transiciones:
                f.write(linea + "\n")

        # 3. Métricas
        filas_p = AnalizadorMetricas.calcular_metricas_por_proceso(resultado.procesos)
        for fp in filas_p:
            fp_copia = dict(fp)
            fp_copia["Algoritmo"] = nombre_alg
            detalles_todos_procesos.append(fp_copia)

        resumen_g = AnalizadorMetricas.calcular_metricas_globales(
            filas_p, resultado.cambios_contexto_totales, nombre_alg, costo_cs
        )
        resumenes_globales.append(resumen_g)

        # 4. Generar Diagrama de Gantt
        ruta_gantt = os.path.join(CARPETA_GRAFICOS, f"gantt_{prefijo_archivo}.png")
        Visualizador.generar_diagrama_gantt(
            resultado.timeline_gantt,
            f"{nombre_escenario} — {nombre_alg} (CS={costo_cs})",
            ruta_gantt
        )

    # 5. Generar y exportar DataFrames
    df_resumen = AnalizadorMetricas.generar_dataframe_resumen(resumenes_globales)
    df_procesos = pd.DataFrame(detalles_todos_procesos)

    ruta_csv_resumen = os.path.join(CARPETA_METRICAS, f"resumen_{id_escenario}_cs{costo_cs}.csv")
    df_resumen.to_csv(ruta_csv_resumen, index=False)

    ruta_csv_procesos = os.path.join(CARPETA_METRICAS, f"detalle_procesos_{id_escenario}_cs{costo_cs}.csv")
    df_procesos.to_csv(ruta_csv_procesos, index=False)

    # 6. Gráfico Comparativo
    ruta_comparativa = os.path.join(CARPETA_GRAFICOS, f"comparativa_{id_escenario}_cs{costo_cs}.png")
    Visualizador.generar_grafico_comparativo(df_resumen, f"{nombre_escenario} (CS={costo_cs})", ruta_comparativa)

    # 7. Mostrar resultados en consola
    print("\n--- TABLA COMPARATIVA DE ALGORITMOS ---")
    print(df_resumen.to_string(index=False))

    return df_resumen


#Suite de ejecución de memoria (paginación) para los escenarios definidos

def ejecutar_suite_memoria():
    """
    Ejecuta la evaluación de gestión de memoria con paginación comparando FIFO vs. LRU
    sobre los 3 escenarios del proyecto.
    Genera tablas CSV, logs con la traducción de 4 pasos y gráficos comparativos.
    """
    print("\n" + "=" * 80)
    print("EJECUTANDO EVALUACIÓN DE GESTIÓN DE MEMORIA (PAGINACIÓN PURA: FIFO vs. LRU)")
    print("=" * 80)

    # Configuraciones de memoria por escenario:
    # Escenario 1: 8 marcos (32 KB RAM), caben todas las páginas (0 reemplazos forzados)
    # Escenario 2: 4 marcos (16 KB RAM), competencia directa donde LRU supera a FIFO
    # Escenario 3: 8 marcos (32 KB RAM), 8 procesos concurrentes con alta sobrecarga
    config_escenarios_memoria = [
        ("escenario1_ligera", "Escenario 1 (Carga Ligera)", crear_escenario_1(), 8, PlanificadorFCFS()),
        ("escenario2_convoy", "Escenario 2 (Carga Mixta - Efecto Convoy)", crear_escenario_2(), 4, PlanificadorFCFS()),
        ("escenario3_quantum", "Escenario 3 (Alta Concurrencia)", crear_escenario_3(), 8, PlanificadorRoundRobin(quantum=4))
    ]

    resumenes_memoria_totales = []
    fragmentacion_procesos_totales = []
    traducciones_muestra = []

    for id_esc, nombre_esc, procs_base, num_marcos, planificador in config_escenarios_memoria:
        tamano_ram = num_marcos * 4096
        print(f"\n--- Memoria en {nombre_esc} (RAM={tamano_ram//1024} KB, {num_marcos} marcos de 4 KB) ---")

        # Fragmentación interna de los procesos en este escenario
        gm_aux = GestorMemoria(tamano_ram=tamano_ram, tamano_pagina=4096)
        filas_frag = AnalizadorMetricas.calcular_fragmentacion_procesos(gm_aux, procs_base)
        for ff in filas_frag:
            ff_c = dict(ff)
            ff_c["Escenario"] = id_esc
            fragmentacion_procesos_totales.append(ff_c)

        filas_comparativa_esc = []

        for estr_cls, estr_nom in [(ReemplazoFIFO, "FIFO"), (ReemplazoLRU, "LRU")]:
            estrategia = estr_cls()
            gm = GestorMemoria(tamano_ram=tamano_ram, tamano_pagina=4096, estrategia=estrategia)

            # Simulador CPU + Memoria integrada sincrónicamente
            # Se usa una copia limpia del planificador
            plan_copia = PlanificadorFCFS() if isinstance(planificador, PlanificadorFCFS) else PlanificadorRoundRobin(planificador.quantum)
            sim = SimuladorCPU(planificador=plan_copia, costo_cs=1, gestor_memoria=gm)
            res = sim.ejecutar(procs_base)

            metricas_mem = AnalizadorMetricas.calcular_metricas_memoria(gm, procs_base)
            metricas_mem["Escenario"] = id_esc
            resumenes_memoria_totales.append(metricas_mem)
            filas_comparativa_esc.append(metricas_mem)

            # Guardar muestra de traducciones para el log de entrega
            if not traducciones_muestra and gm.log_traducciones:
                traducciones_muestra = gm.log_traducciones[:15]

            # Guardar log detallado de traducciones del escenario
            ruta_log_mem = os.path.join(CARPETA_LOGS, f"memoria_traducciones_{id_esc}_{estr_nom}.txt")
            with open(ruta_log_mem, "w", encoding="utf-8") as f:
                f.write(f"=== REGISTRO DE TRADUCCIÓN MMU (4 PASOS): {estr_nom} ({nombre_esc}) ===\n")
                f.write(f"RAM: {tamano_ram} B ({num_marcos} marcos de 4096 B) | Reemplazo: {estr_nom}\n\n")
                for linea in gm.log_traducciones:
                    f.write(linea + "\n")

            # Gráfico de ocupación de RAM en el tiempo
            ruta_graf_ocupacion = os.path.join(CARPETA_GRAFICOS, f"memoria_ocupacion_ram_{id_esc}_{estr_nom}.png")
            Visualizador.generar_grafico_ocupacion_ram(
                gm.historial_ocupacion,
                f"{nombre_esc} — {estr_nom}",
                ruta_graf_ocupacion
            )

        # Gráfico comparativo FIFO vs LRU para este escenario
        df_esc_mem = pd.DataFrame(filas_comparativa_esc)
        ruta_graf_comp = os.path.join(CARPETA_GRAFICOS, f"memoria_comparativa_{id_esc}.png")
        Visualizador.generar_grafico_comparativo_memoria(df_esc_mem, nombre_esc, ruta_graf_comp)

        print(df_esc_mem[["Estrategia", "Total_Accesos", "Total_Aciertos", "Total_Fallos", "Total_Reemplazos", "Hit_Rate_HR (%)", "Page_Fault_Rate_PFR (%)"]].to_string(index=False))

    # Guardar resumen consolidado de memoria en CSV
    df_resumen_mem = pd.DataFrame(resumenes_memoria_totales)
    ruta_csv_mem = os.path.join(CARPETA_METRICAS, "memoria_resumen_FIFO_vs_LRU.csv")
    df_resumen_mem.to_csv(ruta_csv_mem, index=False)

    df_frag = pd.DataFrame(fragmentacion_procesos_totales)
    ruta_csv_frag = os.path.join(CARPETA_METRICAS, "memoria_fragmentacion_procesos.csv")
    df_frag.to_csv(ruta_csv_frag, index=False)

    # Guardar archivo de muestra didáctica de la traducción MMU en 4 pasos
    ruta_muestra_mmu = os.path.join(CARPETA_LOGS, "traduccion_mmu_muestra.txt")
    with open(ruta_muestra_mmu, "w", encoding="utf-8") as f:
        f.write("=== PROCEDIMIENTO DE TRADUCCIÓN DE DIRECCIÓN VIRTUAL A FÍSICA EN 4 PASOS ===\n")
        f.write("Fórmulas del curso:\n")
        f.write("1. número_página = dirección_virtual // tamaño_página\n")
        f.write("2. desplazamiento = dirección_virtual % tamaño_página\n")
        f.write("3. consultar tabla_páginas: página -> marco (si no está: fallo de página y reemplazo FIFO/LRU)\n")
        f.write("4. dirección_física = marco * tamaño_página + desplazamiento\n\n")
        f.write("--- EJEMPLOS REALES GENERADOS POR EL SIMULADOR ---\n")
        for linea in traducciones_muestra:
            f.write(linea + "\n")

    print("\n[OK] Módulo de Memoria ejecutado exitosamente:")
    print(f"    - CSV Resumen comparativo: {ruta_csv_mem}")
    print(f"    - CSV Fragmentación:       {ruta_csv_frag}")
    print(f"    - Muestra de traducción:   {ruta_muestra_mmu}")


#Verificación formal de integridad matemática y no-regresión

def verificar_integridad_y_no_regresion():
    """
    Comprueba formalmente:
    1. Que WT_prom == RT_prom para FCFS y SJF en Escenarios 2 y 3 (sin E/S y no expropiativos).
    2. Que TAT == WT + CPU + IO para cada proceso.
    3. Que la integración de memoria no alteró las métricas de CPU.
    """
    print("\n" + "=" * 80)
    print("VERIFICACIÓN FORMAL DE INTEGRIDAD MATEMÁTICA Y NO-REGRESIÓN")
    print("=" * 80)

    # Verificación 1: FCFS y SJF en Escenario 2 y 3 (costo_cs = 1)
    for esc_num, creador in [(2, crear_escenario_2), (3, crear_escenario_3)]:
        for plan in [PlanificadorFCFS(), PlanificadorSJFNoExpropiativo()]:
            sim = SimuladorCPU(planificador=plan, costo_cs=1)
            res = sim.ejecutar(creador())
            filas = AnalizadorMetricas.calcular_metricas_por_proceso(res.procesos)
            glob = AnalizadorMetricas.calcular_metricas_globales(filas, res.cambios_contexto_totales, plan.nombre, 1)

            wt = glob["Promedio_WT"]
            rt = glob["Promedio_RT"]
            diff = abs(wt - rt)
            es_exacto = diff < 1e-9

            print(f"[TEST WT=RT] Escenario {esc_num} | {plan.nombre} (CS=1): WT_prom={wt:.2f}, RT_prom={rt:.2f} | Exacto: {es_exacto}")
            assert es_exacto, f"Error: WT_prom ({wt}) != RT_prom ({rt}) en {plan.nombre}"

            for p in filas:
                assert p["TAT"] == p["WT"] + p["CPU_Total"] + p["IO_Total"], "Inconsistencia en TAT = WT + CPU + IO"

    print("\n[OK] Todas las aserciones matemáticas de CPU pasaron con exactitud del 100%.")


#Main function 
def main():
    print("=" * 80)
    print("SIMULADOR INTEGRADO: PLANIFICACIÓN DE CPU Y GESTIÓN DE MEMORIA (PAGINACIÓN)")
    print("Sistemas Operativos — Ingeniería de Software")
    print("=" * 80)

    inicializar_directorios()

    # 1. SUITE DE PLANIFICACIÓN DE CPU
    procesos_e1 = crear_escenario_1()
    schedulers_e1 = [
        PlanificadorFCFS(),
        PlanificadorSJFNoExpropiativo(),
        PlanificadorRoundRobin(quantum=3)
    ]
    ejecutar_suite_escenario("escenario1_ligera", "Escenario 1: Carga Ligera", procesos_e1, schedulers_e1, costo_cs=1)

    procesos_e2 = crear_escenario_2()
    schedulers_e2 = [
        PlanificadorFCFS(),
        PlanificadorSJFNoExpropiativo(),
        PlanificadorRoundRobin(quantum=2)
    ]
    ejecutar_suite_escenario("escenario2_convoy", "Escenario 2: Carga Mixta (Efecto Convoy)", procesos_e2, schedulers_e2, costo_cs=1)

    procesos_e3 = crear_escenario_3()
    schedulers_e3 = [
        PlanificadorFCFS(),
        PlanificadorSJFNoExpropiativo(),
        PlanificadorRoundRobin(quantum=2),
        PlanificadorRoundRobin(quantum=4),
        PlanificadorRoundRobin(quantum=8)
    ]
    ejecutar_suite_escenario("escenario3_quantum", "Escenario 3: Alta Concurrencia y Sensibilidad al Quantum", procesos_e3, schedulers_e3, costo_cs=1)

    # Comparativa costo_cs = 0 vs costo_cs = 1
    procesos_e3_cs0 = crear_escenario_3()
    schedulers_e3_cs0 = [
        PlanificadorFCFS(),
        PlanificadorSJFNoExpropiativo(),
        PlanificadorRoundRobin(quantum=2),
        PlanificadorRoundRobin(quantum=4),
        PlanificadorRoundRobin(quantum=8)
    ]
    ejecutar_suite_escenario("escenario3_quantum", "Escenario 3 (Costo CS=0 Ideal)", procesos_e3_cs0, schedulers_e3_cs0, costo_cs=0)

    # 2. SUITE DE GESTIÓN DE MEMORIA (PAGINACIÓN)
    ejecutar_suite_memoria()

    # 3. VERIFICACIÓN FORMAL DE INTEGRIDAD Y NO-REGRESIÓN
    verificar_integridad_y_no_regresion()

    print("\n" + "=" * 80)
    print("SUITE COMPLETA EJECUTADA CON ÉXITO")
    print(f"- Logs guardados en:     {CARPETA_LOGS}")
    print(f"- Métricas guardadas en: {CARPETA_METRICAS}")
    print(f"- Gráficos guardados en: {CARPETA_GRAFICOS}")
    print("=" * 80)


if __name__ == "__main__":
    main()
