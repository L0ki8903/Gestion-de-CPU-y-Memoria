"""
Módulo Visualizador
Genera:
1. Diagramas de Gantt con matplotlib (timeline de ejecución, cambios de contexto y estados ociosos).
2. Gráficos de barras comparativos de métricas (WT, RT, TAT, cambios de contexto, equidad).
3. Tablas comparativas formateadas en consola y exportación a CSV.
"""

import os
import matplotlib
matplotlib.use('Agg')  # Modo no interactivo para guardar directamente en archivo
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd


class Visualizador:
    """Clase para la generación de gráficos y exportación de reportes."""

    @staticmethod
    def _agrupar_timeline(timeline_gantt: list) -> list:
        """
        Agrupa bloques consecutivos idénticos para reducir la granularidad del gráfico.
        Ejemplo: [0-1 P1, 1-2 P1, 2-3 P1] se compacta a [0-3 P1].
        """
        if not timeline_gantt:
            return []

        agrupados = []
        actual = dict(timeline_gantt[0])

        for bloque in timeline_gantt[1:]:
            if bloque["pid"] == actual["pid"] and bloque["tipo"] == actual["tipo"]:
                actual["fin"] = bloque["fin"]
            else:
                agrupados.append(actual)
                actual = dict(bloque)
        agrupados.append(actual)
        return agrupados

    @classmethod
    def generar_diagrama_gantt(cls, timeline_gantt: list, titulo: str, ruta_salida: str):
        """
        Genera y guarda un diagrama de Gantt horizontal de la ejecución de la CPU.
        """
        bloques = cls._agrupar_timeline(timeline_gantt)
        if not bloques:
            print(f"[!] Timeline vacío para {titulo}, no se generó Gantt.")
            return

        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

        fig, ax = plt.subplots(figsize=(14, 4.5))

        # Paleta de colores para procesos y estados especiales
        colores_base = plt.cm.tab10.colors
        mapa_colores = {}
        idx_color = 0

        # Obtener lista única de procesos para asignar colores consistentes
        pids_procesos = sorted(list(set(b["pid"] for b in bloques if b["tipo"] == "CPU")))
        for pid in pids_procesos:
            mapa_colores[pid] = colores_base[idx_color % len(colores_base)]
            idx_color += 1

        mapa_colores["CS"] = "#E74C3C"      # Rojo suave / naranja para overhead de cambio de contexto
        mapa_colores["IDLE"] = "#BDC3C7"    # Gris claro para CPU ociosa

        tiempo_max = max(b["fin"] for b in bloques)

        # Dibujamos las barras del Gantt
        for b in bloques:
            inicio = b["inicio"]
            duracion = b["fin"] - b["inicio"]
            pid = b["pid"]
            tipo = b["tipo"]

            color = mapa_colores.get(pid, "#95A5A6")
            hatch = "//" if tipo == "CS" else (".." if tipo == "IDLE" else None)

            ax.broken_barh(
                [(inicio, duracion)], (10, 8),
                facecolors=color,
                edgecolor="black",
                linewidth=1,
                hatch=hatch
            )

            # Etiqueta de texto dentro del bloque si hay suficiente espacio
            if duracion >= 1:
                etiqueta = pid
                # Centrado del texto
                ax.text(
                    inicio + duracion / 2, 14, etiqueta,
                    ha='center', va='center',
                    color='white' if tipo in ["CPU", "CS"] else 'black',
                    fontweight='bold',
                    fontsize=9
                )

        # Configuración de ejes
        ax.set_ylim(0, 30)
        ax.set_xlim(0, max(tiempo_max, 10))
        ax.set_xlabel("Tiempo simulado (Ticks de reloj)", fontsize=11, fontweight="bold")
        ax.set_yticks([])  # Barra única continua estilo Gantt de CPU

        # Ticks en el eje X
        paso_ticks = 1 if tiempo_max <= 35 else (2 if tiempo_max <= 70 else 5)
        ax.set_xticks(range(0, tiempo_max + 1, paso_ticks))
        ax.grid(axis='x', linestyle='--', alpha=0.6)

        ax.set_title(f"Diagrama de Gantt — {titulo}", fontsize=13, fontweight="bold", pad=12)

        # Leyenda
        elementos_leyenda = []
        for pid in pids_procesos:
            elementos_leyenda.append(mpatches.Patch(color=mapa_colores[pid], label=f"Proceso {pid}"))
        if any(b["tipo"] == "CS" for b in bloques):
            elementos_leyenda.append(mpatches.Patch(facecolor=mapa_colores["CS"], edgecolor="black", hatch="//", label="Cambio Contexto (CS)"))
        if any(b["tipo"] == "IDLE" for b in bloques):
            elementos_leyenda.append(mpatches.Patch(facecolor=mapa_colores["IDLE"], edgecolor="black", hatch="..", label="CPU Ociosa (IDLE)"))

        ax.legend(handles=elementos_leyenda, bbox_to_anchor=(1.0, 1.25), loc='upper right', ncol=min(len(elementos_leyenda), 6), fontsize=8.5)

        plt.tight_layout()
        plt.savefig(ruta_salida, dpi=180)
        plt.close()

    @classmethod
    def generar_grafico_comparativo(cls, df_resumen: pd.DataFrame, titulo_escenario: str, ruta_salida: str):
        """
        Genera gráficos de barras comparativos para evaluar el rendimiento entre algoritmos:
        1. Tiempos promedio (WT, RT, TAT)
        2. Cambios de contexto y Equidad (Desviación Estándar de WT)
        """
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5))

        algoritmos = df_resumen["Algoritmo"].tolist()
        x = range(len(algoritmos))
        ancho = 0.25

        # Subgráfico 1: Tiempos promedio (WT, RT, TAT)
        ax1.bar([i - ancho for i in x], df_resumen["Promedio_WT"], width=ancho, label="Espera Prom. (WT)", color="#3498DB")
        ax1.bar([i for i in x], df_resumen["Promedio_RT"], width=ancho, label="Respuesta Prom. (RT)", color="#2ECC71")
        ax1.bar([i + ancho for i in x], df_resumen["Promedio_TAT"], width=ancho, label="Retorno Prom. (TAT)", color="#F39C12")

        ax1.set_title("Comparativa de Tiempos Promedio", fontweight="bold", fontsize=11)
        ax1.set_ylabel("Ticks de reloj", fontweight="bold")
        ax1.set_xticks(list(x))
        ax1.set_xticklabels(algoritmos, rotation=18, ha='right', fontsize=9)
        ax1.legend(fontsize=9)
        ax1.grid(axis='y', linestyle='--', alpha=0.6)

        # Subgráfico 2: Cambios de contexto y Equidad (Desv. Std. de WT)
        ancho2 = 0.35
        ax2.bar([i - ancho2/2 for i in x], df_resumen["Total_CS"], width=ancho2, label="Cambios de Contexto (CS)", color="#E74C3C")
        ax2.bar([i + ancho2/2 for i in x], df_resumen["DesvStd_WT (Equidad)"], width=ancho2, label="Desv. Std. WT (Iniquidad)", color="#9B59B6")

        ax2.set_title("Overhead (CS) vs Iniquidad (Desv. Std. WT)", fontweight="bold", fontsize=11)
        ax2.set_ylabel("Valor numérico", fontweight="bold")
        ax2.set_xticks(list(x))
        ax2.set_xticklabels(algoritmos, rotation=18, ha='right', fontsize=9)
        ax2.legend(fontsize=9)
        ax2.grid(axis='y', linestyle='--', alpha=0.6)

        fig.suptitle(f"Análisis Comparativo — {titulo_escenario}", fontsize=13, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(ruta_salida, dpi=180, bbox_inches="tight")
        plt.close()

    @classmethod
    def generar_grafico_comparativo_memoria(cls, df_memoria: pd.DataFrame, titulo_escenario: str, ruta_salida: str):
        """
        Genera gráfico comparativo entre estrategias de reemplazo (FIFO vs LRU):
        1. Aciertos (Hits) vs Fallos de página (Faults).
        2. Tasa de Aciertos (Hit Rate %) vs Tasa de Fallos (Page Fault Rate %).
        """
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

        estrategias = df_memoria["Estrategia"].tolist()
        x = range(len(estrategias))
        ancho = 0.35

        # Subgráfico 1: Aciertos y Fallos Absolutos
        ax1.bar([i - ancho/2 for i in x], df_memoria["Total_Aciertos"], width=ancho, label="Aciertos (Hits)", color="#2ECC71")
        ax1.bar([i + ancho/2 for i in x], df_memoria["Total_Fallos"], width=ancho, label="Fallos de Página (Faults)", color="#E74C3C")
        ax1.set_title("Conteo Absoluto de Aciertos vs Fallos", fontweight="bold", fontsize=11)
        ax1.set_ylabel("Cantidad de accesos", fontweight="bold")
        ax1.set_xticks(list(x))
        ax1.set_xticklabels(estrategias, fontsize=10, fontweight="bold")
        ax1.legend(fontsize=9)
        ax1.grid(axis='y', linestyle='--', alpha=0.6)

        # Subgráfico 2: Tasas Porcentuales (Hit Rate % vs Page Fault Rate %)
        ax2.bar([i - ancho/2 for i in x], df_memoria["Hit_Rate_HR (%)"], width=ancho, label="Tasa Aciertos (HR %)", color="#3498DB")
        ax2.bar([i + ancho/2 for i in x], df_memoria["Page_Fault_Rate_PFR (%)"], width=ancho, label="Tasa Fallos (PFR %)", color="#E67E22")
        ax2.set_title("Tasa de Aciertos (HR) vs Tasa de Fallos (PFR)", fontweight="bold", fontsize=11)
        ax2.set_ylabel("Porcentaje (%)", fontweight="bold")
        ax2.set_ylim(0, 105)
        ax2.set_xticks(list(x))
        ax2.set_xticklabels(estrategias, fontsize=10, fontweight="bold")
        ax2.legend(fontsize=9)
        ax2.grid(axis='y', linestyle='--', alpha=0.6)

        fig.suptitle(f"Evaluación de Gestión de Memoria (Paginación) — {titulo_escenario}", fontsize=13, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(ruta_salida, dpi=180, bbox_inches="tight")
        plt.close()

    @classmethod
    def generar_grafico_ocupacion_ram(cls, historial_ocupacion: list, titulo: str, ruta_salida: str):
        """
        Genera gráfico de línea que ilustra la ocupación de marcos físicos en RAM a lo largo del tiempo.
        """
        if not historial_ocupacion:
            return

        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

        tiempos = [h["tiempo"] for h in historial_ocupacion]
        ocupados = [h["marcos_ocupados"] for h in historial_ocupacion]
        total_marcos = historial_ocupacion[0]["total_marcos"]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.step(tiempos, ocupados, where='post', color="#8E44AD", linewidth=2, label="Marcos Ocupados")
        ax.axhline(total_marcos, color="#C0392B", linestyle="--", linewidth=1.5, label=f"Capacidad Total RAM ({total_marcos} marcos)")

        ax.set_title(f"Ocupación de Marcos Físicos en RAM en el Tiempo — {titulo}", fontweight="bold", fontsize=11)
        ax.set_xlabel("Tiempo simulado (ticks)", fontweight="bold")
        ax.set_ylabel("Número de marcos físicos ocupados", fontweight="bold")
        ax.set_ylim(0, total_marcos + 1)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(loc="lower right")

        plt.tight_layout()
        plt.savefig(ruta_salida, dpi=180)
        plt.close()
