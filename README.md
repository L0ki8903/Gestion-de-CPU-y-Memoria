# Simulador Integrado de Planificación de CPU y Gestión de Memoria (Paginación)

**Curso:** Sistemas Operativos — Ingeniería de Software  
**Lenguaje:** Python 3 (versión 3.8+)  
**Dependencias:** `matplotlib`, `pandas`, `reportlab`

---

## 1. Descripción del Proyecto

Este proyecto implementa un simulador ciclo a ciclo (reloj discreto *tick-by-tick*) en Python 3 que unifica en un único motor de ejecución:
1. **Planificación de Procesos en CPU:**
   - Modelado explícito del Bloque de Control de Proceso (PCB) bajo 5 estados: `NUEVO`, `LISTO`, `EJECUCION`, `BLOQUEADO` y `FINALIZADO`.
   - Comparación de 3 algoritmos: **FCFS**, **SJF (No Expropiativo)** y **Round Robin** (con quantum $q$ configurable).
   - Cálculo de métricas individuales y promedios: Turnaround Time ($TAT$), Waiting Time ($WT$) y Response Time ($RT$).
   - Conteo riguroso de cambios de contexto ($CS$) con costo configurable (`costo_cs = 1` o `0`).
   - Análisis de equidad (desviación estándar $\sigma_{WT}$) e indicadores de inanición (*starvation*).
2. **Gestión de Memoria con Paginación Pura:**
   - Procedimiento canónico de traducción de la Unidad de Manejo de Memoria (MMU) en 4 pasos:
     1. $P\text{á}gina = DirVirtual // Tama\tilde{n}oP\text{á}gina$
     2. $Desplazamiento = DirVirtual \% Tama\tilde{n}oP\text{á}gina$
     3. Consulta a la tabla de páginas y detección de fallo de página (*page fault*).
     4. $DirF\text{í}sica = Marco \times Tama\tilde{n}oP\text{á}gina + Desplazamiento$
   - Manejo de fallos de página y reemplazo global comparando **FIFO** vs. **LRU**.
   - Cuantificación de fragmentación interna ($MemoriaAsignada - MemoriaNecesitada$) y verificación empírica de ausencia de fragmentación externa ($0\text{ bytes}$).

---

## 2. Estructura de Archivos del Proyecto

```text
proyecto_so_cpu/
│
├── pcb.py             # Clase Proceso (PCB), enum EstadoProceso y validaciones de robustez
├── planificadores.py  # Algoritmos de CPU (FCFS, SJF No Expropiativo, Round Robin)
├── memoria.py         # Tablas de páginas, marcos físicos, MMU de 4 pasos, FIFO y LRU
├── simulador.py       # Motor de simulación discreta tick a tick, colas y costo_cs
├── metricas.py        # Fórmulas de métricas de CPU, equidad, inanición y memoria
├── visualizador.py    # Generación de diagramas de Gantt y gráficos comparativos (.png)
├── main.py            # Orquestador: corre los 3 escenarios de CPU y la suite de memoria
├── generar_pdf.py     # Compilador ReportLab del Informe Técnico oficial en PDF
├── generar_revision_preliminar.py # Compilador APA 7ma ed. de la Revisión Preliminar
├── informe_tecnico.pdf # Informe Técnico final completo generado (7 páginas)
├── revision_preliminar.pdf # Documento oficial de Revisión Preliminar en formato APA 7
├── README.md          # Guía técnica de instalación, ejecución y arquitectura
└── resultados/        # Directorio generado automáticamente con las salidas
    ├── logs/          # Logs detallados ciclo a ciclo (.txt) de transiciones y MMU
    ├── metricas/      # Tablas en formato CSV (.csv) con métricas consolidadas
    └── graficos/      # Gráficos y diagramas de Gantt en alta resolución (.png)
```

---

## 3. Instalación de Dependencias

Se requiere Python 3 instalado en el sistema. Para instalar las librerías necesarias, ejecuta:

```bash
pip install matplotlib pandas reportlab
```

---

## 4. Instrucciones de Ejecución

### 4.1. Ejecución de la Suite Completa de Simulación (CPU y Memoria)

Para ejecutar todos los escenarios, regenerar los logs de transiciones, los CSVs de métricas y los gráficos comparativos:

```bash
python main.py
```

Al finalizar, la consola mostrará las tablas tabulares de los 3 escenarios de CPU, la comparativa de costo $CS=0$ vs $CS=1$, la comparativa de memoria FIFO vs LRU y las pruebas de aserción de consistencia matemática ($\overline{WT} == \overline{RT}$).

### 4.2. Compilación de Documentos Académicos en PDF

- **Informe Técnico Completo (7 páginas):**
  ```bash
  python generar_pdf.py
  ```
  Genera `informe_tecnico.pdf` con las 11 secciones formales, tablas de resultados y gráficos.

- **Documento de Revisión Preliminar (Normas APA 7ma edición):**
  ```bash
  python generar_revision_preliminar.py
  ```
  Genera `revision_preliminar.pdf` con portada institucional, las 8 secciones académicas requeridas, código ilustrativo, evidencia visual real (Gantt) y referencias en sangría francesa.

---

## 5. Escenarios de Prueba Modelados

1. **Escenario 1 — Carga Ligera con E/S:**
   - 4 procesos con ráfagas moderadas.
   - P1 y P3 realizan operaciones de E/S intermedias, transitando al estado `BLOQUEADO`.
   - Evaluación de línea base de la MMU en memoria holgada (8 marcos, 32 KB).
2. **Escenario 2 — Carga Mixta (Efecto Convoy y Localidad Temporal):**
   - Proceso monolítico P1 ($CPU=20$) en $t=0$, seguido de procesos cortos (P2 a P5). Demuestra el efecto convoy en FCFS.
   - En memoria, P1 ejecuta el patrón de referencias de Silberschatz en una RAM limitada (4 marcos, 16 KB), evidenciando la superioridad de LRU ($HR=46.43\%$) frente a FIFO ($HR=39.29\%$).
3. **Escenario 3 — Alta Concurrencia y Sensibilidad al Quantum:**
   - 8 procesos heterogéneos con ráfagas de 2 a 12 ticks.
   - Comparación de Round Robin con $Q=2, 4, 8$ bajo $costo\_cs=1$ y $costo\_cs=0$.
   - Demostración de cómo la rotación de Round Robin con memoria saturada iguala el orden de llegada y recencia en FIFO y LRU.

---

## 6. Fórmulas de las Métricas

- **Tiempo de Retorno (Turnaround Time, $TAT$):**
  $$TAT_i = T_{fin,i} - T_{llegada,i}$$
- **Tiempo de Espera (Waiting Time, $WT$):**
  $$WT_i = \text{Ticks acumulados en estado LISTO} = TAT_i - T_{CPU,i} - T_{IO,i}$$
- **Tiempo de Respuesta (Response Time, $RT$):**
  $$RT_i = T_{primer\_despacho,i} - T_{llegada,i}$$
- **Equidad ($\sigma_{WT}$):**
  $$\sigma_{WT} = \sqrt{\frac{1}{N}\sum_{i=1}^N (WT_i - \overline{WT})^2}$$
- **Criterio de Inanición (*Starvation*):**
  Se emite alerta estadística si $\frac{WT_i}{T_{CPU,i}} \ge 4.0$ o si $WT_i > \overline{WT} + 1.5 \cdot \sigma_{WT}$.
- **Tasa de Aciertos de Memoria (Hit Rate, $HR$):**
  $$HR = \frac{\text{Aciertos}}{\text{Total de Accesos}} \times 100\%$$
- **Fragmentación Interna ($IF$):**
  $$IF_i = (\text{Páginas Asignadas}_i \times \text{Tamaño Página}) - \text{Memoria Necesitada}_i$$

---

## 7. Manejo de Errores y Robustez

El simulador cuenta con validaciones estrictas en tiempo de construcción y ejecución:
- **Lista de procesos vacía:** Lanza `ValueError("No se puede ejecutar la simulación: la lista de procesos a simular está vacía.")`.
- **Quantum inválido ($\le 0$):** Lanza `ValueError("El quantum debe ser un número entero mayor a 0.")`.
- **Ráfaga nula o negativa ($\le 0$):** Lanza `ValueError("Duración inválida en ráfaga (tipo, duracion): debe ser un entero mayor a 0.")`.
- **Costo de cambio de contexto negativo ($< 0$):** Lanza `ValueError("El costo de cambio de contexto no puede ser negativo.")`.
