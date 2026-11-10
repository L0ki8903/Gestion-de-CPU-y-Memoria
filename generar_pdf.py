"""
Script para generar el Informe Técnico formal en PDF:
"Gestión de Procesos, Planificación de CPU y Gestión de Memoria con Paginación"
Curso: Sistemas Operativos (Ingeniería de Software)

Compila un documento formal, exhaustivo y elegante con:
- Portada institucional con placeholders para los 4 integrantes.
- Tablas 1 a 4 completamente recalculadas tras la corrección del bug de WT.
- Redacción rigurosa y corregida (efecto convoy, trade-off de CS vs TAT, artefactos de ratio de inanición).
- Detalle individual de los 8 procesos del Escenario 3.
- Sección completa e integrada de Gestión de Memoria con Paginación:
  * Procedimiento de traducción MMU en 4 pasos (fórmulas del curso).
  * Comparación formal FIFO vs. LRU (con victoria medible de LRU en Escenario 2).
  * Fragmentación interna y externa (demostración de 0 bytes externos).
- Gráficos comparativos y diagramas de Gantt embebidos.
- Declaración explícita de la simplificación del modelo de memoria (observador sincrónico sin latencia de disco).
- Nota metodológica de uso de IA (requisito ético de la sección 8 del enunciado).
- Referencias bibliográficas canónicas (Silberschatz, Tanenbaum, Stallings, Love).
"""

import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PDF = os.path.join(BASE_DIR, "informe_tecnico.pdf")
CARPETA_GRAFICOS = os.path.join(BASE_DIR, "resultados", "graficos")
CARPETA_METRICAS = os.path.join(BASE_DIR, "resultados", "metricas")


class NumberedCanvas(canvas.Canvas):
    """
    Canvas de doble pasada para calcular el total de páginas
    y estampar encabezados y pies de página formales en cada hoja.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#5D6D7E"))

            # Encabezado superior
            self.drawString(42, 755, "Sistemas Operativos - Informe Tecnico: CPU y Gestion de Memoria (Paginacion)")
            self.setStrokeColor(colors.HexColor("#BDC3C7"))
            self.setLineWidth(0.6)
            self.line(42, 748, 570, 748)

            # Pie de página inferior
            self.line(42, 45, 570, 45)
            self.drawString(42, 32, "Ingenieria de Software - Simulacion de Procesos, Schedulers y Paginacion MMU")
            texto_pag = f"Pagina {self._pageNumber} de {page_count}"
            self.drawRightString(570, 32, texto_pag)

            self.restoreState()


def crear_estilos():
    """Genera la paleta de estilos tipográficos con jerarquía visual coherente."""
    color_primario = colors.HexColor("#1B365D")    # Azul marino institucional
    color_secundario = colors.HexColor("#2C3E50")  # Gris azulado oscuro
    color_texto = colors.HexColor("#2C3E50")

    estilos = {
        "PortadaTitulo": ParagraphStyle(
            "PortadaTitulo",
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            textColor=color_primario,
            alignment=TA_CENTER
        ),
        "PortadaSubtitulo": ParagraphStyle(
            "PortadaSubtitulo",
            fontName="Helvetica",
            fontSize=11.5,
            leading=15.5,
            textColor=color_secundario,
            alignment=TA_CENTER
        ),
        "PortadaMeta": ParagraphStyle(
            "PortadaMeta",
            fontName="Helvetica",
            fontSize=9.5,
            leading=14.5,
            textColor=colors.HexColor("#34495E"),
            alignment=TA_CENTER
        ),
        "H1": ParagraphStyle(
            "H1",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=color_primario,
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True
        ),
        "H2": ParagraphStyle(
            "H2",
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12.5,
            textColor=color_secundario,
            spaceBefore=7,
            spaceAfter=3,
            keepWithNext=True
        ),
        "H3": ParagraphStyle(
            "H3",
            fontName="Helvetica-Bold",
            fontSize=8.8,
            leading=11.5,
            textColor=colors.HexColor("#4A235A"),
            spaceBefore=5,
            spaceAfter=2,
            keepWithNext=True
        ),
        "Cuerpo": ParagraphStyle(
            "Cuerpo",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=color_texto,
            alignment=TA_JUSTIFY,
            spaceAfter=3.5
        ),
        "CuerpoBullet": ParagraphStyle(
            "CuerpoBullet",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=color_texto,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=2
        ),
        "Destacado": ParagraphStyle(
            "Destacado",
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#1A5276"),
            alignment=TA_JUSTIFY,
            spaceBefore=2,
            spaceAfter=3
        ),
        "TablaHeader": ParagraphStyle(
            "TablaHeader",
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=9,
            textColor=colors.white,
            alignment=TA_CENTER
        ),
        "TablaCelda": ParagraphStyle(
            "TablaCelda",
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            textColor=color_texto,
            alignment=TA_CENTER
        ),
        "TablaCeldaLeft": ParagraphStyle(
            "TablaCeldaLeft",
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            textColor=color_texto,
            alignment=TA_LEFT
        ),
        "Caption": ParagraphStyle(
            "Caption",
            fontName="Helvetica-Oblique",
            fontSize=7.2,
            leading=9,
            textColor=colors.HexColor("#5D6D7E"),
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=5
        )
    }
    return estilos


def crear_tabla_desde_df(df: pd.DataFrame, estilos, anchos=None) -> Table:
    """Convierte un DataFrame de pandas en una tabla estilizada de ReportLab."""
    encabezados = [Paragraph(str(col), estilos["TablaHeader"]) for col in df.columns]
    filas = [encabezados]

    for _, row in df.iterrows():
        fila_actual = []
        for col_idx, valor in enumerate(row):
            texto = str(valor)
            if col_idx == 0:
                p = Paragraph(texto, estilos["TablaCeldaLeft"])
            else:
                p = Paragraph(texto, estilos["TablaCelda"])
            fila_actual.append(p)
        filas.append(fila_actual)

    t = Table(filas, colWidths=anchos)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5D8DC")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#1B365D")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def construir_portada(estilos) -> list:
    """Genera la portada formal del informe con placeholders para los integrantes."""
    elementos = []
    elementos.append(Spacer(1, 35))

    elementos.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor("#1B365D"), spaceAfter=14))

    p_inst = Paragraph(
        "UNIVERSIDAD - FACULTAD DE INGENIERIA Y CIENCIAS BASICAS<br/>"
        "PROGRAMA DE INGENIERIA DE SOFTWARE",
        estilos["PortadaMeta"]
    )
    elementos.append(p_inst)
    elementos.append(Spacer(1, 16))

    p_curso = Paragraph("CURSO: SISTEMAS OPERATIVOS", estilos["PortadaSubtitulo"])
    elementos.append(p_curso)
    elementos.append(Spacer(1, 25))

    p_titulo = Paragraph(
        "INFORME TECNICO INTEGRAL DE PROYECTO<br/>"
        "Planificacion de CPU y Gestion de Memoria con Paginacion",
        estilos["PortadaTitulo"]
    )
    elementos.append(p_titulo)
    elementos.append(Spacer(1, 12))

    p_sub = Paragraph(
        "Simulacion Ciclo a Ciclo de Procesos (FCFS, SJF, Round Robin),<br/>"
        "Overhead de Cambio de Contexto, Evaluacion de Equidad e Inanicion,<br/>"
        "y Paginacion Pura con Traduccion MMU de 4 Pasos (Reemplazo FIFO vs. LRU)",
        estilos["PortadaSubtitulo"]
    )
    elementos.append(p_sub)
    elementos.append(Spacer(1, 35))

    elementos.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#BDC3C7"), spaceAfter=20))

    meta_texto = (
        "<b>INTEGRANTES DEL EQUIPO (GRUPO DE PROYECTO):</b><br/><br/>"
        "• [Estudiante 1 - Codigo: ____________________]<br/>"
        "• [Estudiante 2 - Codigo: ____________________]<br/>"
        "• [Estudiante 3 - Codigo: ____________________]<br/>"
        "• [Estudiante 4 - Codigo: ____________________]<br/><br/>"
        "<b>DOCENTE EVALUADOR:</b> [Nombre del Docente del Curso]<br/>"
        "<b>FECHA DE ENTREGA:</b> Noviembre de 2026<br/>"
        "<b>STACK TECNICO:</b> Python 3.11, Matplotlib, Pandas (Simulacion Pura sin Frameworks)"
    )
    elementos.append(Paragraph(meta_texto, estilos["PortadaMeta"]))
    elementos.append(Spacer(1, 30))
    elementos.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1B365D"), spaceAfter=10))

    elementos.append(PageBreak())
    return elementos


def generar_informe_pdf():
    """Compila el informe completo cumpliendo todas las secciones obligatorias."""
    doc = SimpleDocTemplate(
        RUTA_PDF,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=44,
        bottomMargin=44
    )

    estilos = crear_estilos()
    story = []

    # PORTADA
    story.extend(construir_portada(estilos))

    ancho_doc = 532

    # =========================================================================
    # 1. DESCRIPCIÓN DEL PROBLEMA
    # =========================================================================
    story.append(Paragraph("1. Descripcion del Problema", estilos["H1"]))
    story.append(Paragraph(
        "En los sistemas computacionales modernos, la Unidad Central de Procesamiento (CPU) y la Memoria Principal (RAM) "
        "constituyen los dos recursos fisicos mas criticos y limitados. Dado que el numero de tareas concurrentes excede "
        "ampliamente la cantidad de nucleos fisicos y la capacidad contigua de la memoria, el sistema operativo (SO) "
        "enfrenta el desafio de <b>multiplexar tanto el tiempo de CPU como el espacio de memoria</b> de forma transparente, "
        "segura y determinista.",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "A nivel de procesador, la ausencia de una politica de planificacion adecuada provoca patologias severas como el "
        "<b>Efecto Convoy</b>, degradacion de interactividad y sobrecarga administrativa (<i>overhead</i>) por conmutaciones de contexto. "
        "En paralelo, a nivel de memoria, la asignacion contigua tradicional genera <b>fragmentacion externa</b> (memoria libre dispersa "
        "en huecos inservibles). Para superarlo, el SO implementa <b>paginacion</b>, dividiendo el espacio virtual en paginas y la RAM en "
        "marcos fijos, lo cual elimina la fragmentacion externa pero introduce <b>fragmentacion interna</b> y la necesidad de politicas "
        "optimas de reemplazo de paginas (FIFO vs. LRU) ante fallos de pagina (<i>page faults</i>).",
        estilos["Cuerpo"]
    ))

    # =========================================================================
    # 2. OBJETIVO DEL PROYECTO
    # =========================================================================
    story.append(Paragraph("2. Objetivo del Proyecto", estilos["H1"]))
    story.append(Paragraph(
        "<b>Objetivo General:</b> Disenar, implementar y evaluar un simulador ciclo a ciclo (reloj discreto <i>tick-by-tick</i>) "
        "en Python 3 que integre en un unico motor de ejecucion la <b>planificacion de CPU</b> (FCFS, SJF no expropiativo, Round Robin) "
        "y la <b>gestion de memoria con paginacion pura</b> (MMU con traduccion en 4 pasos, calculo de fragmentacion y reemplazo FIFO vs. LRU), "
        "evaluando cuantitativamente rendimiento, equidad, sobrecarga y aciertos de memoria sobre tres escenarios reproducibles.",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph("<b>Objetivos Especificos:</b>", estilos["H2"]))
    story.append(Paragraph("• Modelar el Bloque de Control de Proceso (PCB) bajo cinco estados formales: NUEVO, LISTO, EJECUCION, BLOQUEADO y FINALIZADO, con log de transiciones auditables.", estilos["CuerpoBullet"]))
    story.append(Paragraph("• Incorporar el costo temporal de cambio de contexto (<i>costo_cs</i>) asegurando consistencia matematica estricta (WT = RT en algoritmos no expropiativos sin E/S).", estilos["CuerpoBullet"]))
    story.append(Paragraph("• Implementar la Unidad de Manejo de Memoria (MMU) simulada con el procedimiento canónico de 4 pasos para traducir direcciones virtuales a fisicas.", estilos["CuerpoBullet"]))
    story.append(Paragraph("• Contrastar experimentalmente las estrategias de reemplazo de paginas FIFO y LRU, demostrando la ventaja de LRU ante patrones de acceso con localidad temporal.", estilos["CuerpoBullet"]))
    story.append(Paragraph("• Cuantificar la fragmentacion interna (memoria asignada - memoria necesitada) y constatar la ausencia de fragmentacion externa en paginacion.", estilos["CuerpoBullet"]))

    # =========================================================================
    # 3. FUNDAMENTACIÓN DEL MECANISMO SELECCIONADO
    # =========================================================================
    story.append(Paragraph("3. Fundamentacion del Mecanismo Seleccionado", estilos["H1"]))
    story.append(Paragraph(
        "La coexistencia coordinada de la planificacion de CPU a corto plazo y la paginacion en memoria responde al principio clasico "
        "del <b>Ciclo de Rafagas CPU-E/S</b> (Silberschatz et al., 2018). Los procesos alternan entre computo en procesador y transferencia "
        "de datos de E/S. Un planificador eficaz solapa estas fases: mientras un proceso espera E/S en estado BLOQUEADO, la CPU se cede a "
        "otro proceso listo, elevando el aprovechamiento del hardware.",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "Asimismo, la paginacion desacopla el espacio de direcciones logico del espacio fisico: el proceso percibe una memoria virtual "
        "contigua, mientras la MMU mapea dinamicamente sus paginas a marcos fisicos no contiguos en la RAM. Esto erradica la compactacion "
        "pesada de memoria y, mediante la carga bajo demanda, permite ejecutar procesos cuya demanda virtual supera la memoria fisica disponible.",
        estilos["Cuerpo"]
    ))

    # =========================================================================
    # 4. DISEÑO DE LA SOLUCIÓN
    # =========================================================================
    story.append(Paragraph("4. Diseno de la Solucion", estilos["H1"]))
    story.append(Paragraph(
        "La arquitectura del simulador es de <b>tiempo discreto determinista (tick-by-tick)</b>. Cada avance del reloj entero "
        "(<i>t = 0, 1, 2, ...</i>) orquesta las admisiones, la ejecucion de instrucciones, la traduccion de direcciones de memoria "
        "y el avance de los dispositivos de E/S.",
        estilos["Cuerpo"]
    ))

    story.append(Paragraph("4.1. PCB, Maquina de Estados y Modulos", estilos["H2"]))
    story.append(Paragraph(
        "El ciclo de vida del proceso implementa una maquina de estados finitos:<br/>"
        "• <b>NUEVO -> LISTO:</b> Admision del proceso. Se crea su Tabla de Paginas calculando "
        "<i>num_paginas = ceil(memoria_necesitada / tamano_pagina)</i>.<br/>"
        "• <b>LISTO -> EJECUCION:</b> Despacho a CPU tras el intervalo de cambio de contexto (<i>costo_cs</i>).<br/>"
        "• <b>EJECUCION (Acceso a Memoria):</b> En cada tick de CPU, la MMU traduce la direccion virtual. Si la pagina no esta en RAM, "
        "ocurre un <b>fallo de pagina</b>, cargando la pagina en un marco libre o aplicando reemplazo (FIFO / LRU).<br/>"
        "• <b>EJECUCION -> BLOQUEADO:</b> Transicion voluntaria por solicitud de E/S al completar una rafaga de CPU intermedia.<br/>"
        "• <b>BLOQUEADO -> LISTO:</b> Desbloqueo al finalizar el conteo de ciclos de E/S.<br/>"
        "• <b>EJECUCION -> LISTO:</b> Desalojo preventivo por expiracion de quantum en Round Robin.<br/>"
        "• <b>EJECUCION -> FINALIZADO:</b> Al concluir sus rafagas, se liberan todos los marcos fisicos que el proceso ocupaba en RAM.",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "El sistema se organiza en 6 archivos modulares: <code>pcb.py</code> (PCB y estados), <code>planificadores.py</code> (algoritmos CPU), "
        "<code>memoria.py</code> (marcos, tablas, MMU y reemplazo), <code>simulador.py</code> (reloj y colas), <code>metricas.py</code> (cálculos matemáticos) "
        "y <code>visualizador.py</code> (graficación automatizada).",
        estilos["Cuerpo"]
    ))

    # =========================================================================
    # 5. ALGORITMOS, ESTRATEGIAS O CONFIGURACIONES COMPARADAS
    # =========================================================================
    story.append(Paragraph("5. Algoritmos, Estrategias o Configuraciones Comparadas", estilos["H1"]))
    story.append(Paragraph(
        "<b>A. Planificacion de CPU:</b><br/>"
        "• <b>FCFS (First-Come, First-Served):</b> Cola FIFO pura no expropiativa. Atiende por orden de llegada; desempate por menor PID.<br/>"
        "• <b>SJF (Shortest Job First No Expropiativo):</b> Selecciona el proceso con menor duracion en su rafaga actual de CPU. "
        "Desempate: 1) menor tiempo de llegada (FCFS local); 2) menor PID.<br/>"
        "• <b>Round Robin (RR con quantum q):</b> Expropiativo por tiempo. Rota en rodajas de <i>q</i> ticks. En caso de colision simultanea "
        "entre fin de quantum y nueva llegada, se encola primero el proceso entrante para favorecer su tiempo de respuesta (RT).",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "<b>B. Gestion de Memoria (Paginacion Pura y Reemplazo):</b><br/>"
        "• <b>Procedimiento de Traduccion MMU (4 Pasos de las Diapositivas):</b><br/>"
        "  1. <i>numero_pagina = direccion_virtual // tamano_pagina</i><br/>"
        "  2. <i>desplazamiento = direccion_virtual % tamano_pagina</i><br/>"
        "  3. Consultar <code>tabla_paginas</code>: si no esta en RAM -> fallo de pagina y seleccion de victima (FIFO / LRU).<br/>"
        "  4. <i>direccion_fisica = marco * tamano_pagina + desplazamiento</i>.<br/>"
        "• <b>FIFO (First-In, First-Out):</b> Reemplaza la pagina que lleva mas tiempo cargada en la RAM (menor <i>tiempo_carga</i>).<br/>"
        "• <b>LRU (Least Recently Used):</b> Reemplaza la pagina menos recientemente accedida (menor <i>ultimo_acceso</i>).",
        estilos["Cuerpo"]
    ))

    # =========================================================================
    # 6. ESCENARIOS Y MÉTRICAS DE PRUEBA
    # =========================================================================
    story.append(Paragraph("6. Escenarios y Metricas de Prueba", estilos["H1"]))
    story.append(Paragraph(
        "Se estructuraron tres escenarios reproducibles con parametros exactos (almacenados en <code>resultados/logs/</code> y <code>resultados/metricas/</code>):",
        estilos["Cuerpo"]
    ))

    datos_escenarios = [
        ["Escenario", "Objetivo Experimental", "Procesos y Parametros de Rafaga", "Memoria Asignada (4 KB/pag)"],
        [
            "1. Carga Ligera\n(con E/S)",
            "Linea base, transicion a BLOQUEADO y validacion de MMU sin sobrecarga.",
            "P1 (Llegada 0, CPU 3, IO 2, CPU 2)\nP2 (Llegada 1, CPU 4)\nP3 (Llegada 2, CPU 2, IO 1, CPU 2)\nP4 (Llegada 4, CPU 3)",
            "P1: 6000 B (2 pags)\nP2: 4096 B (1 pag)\nP3: 7500 B (2 pags)\nP4: 3000 B (1 pag)\nTotal: 6 pags en RAM 32 KB"
        ],
        [
            "2. Carga Mixta\n(Efecto Convoy)",
            "Demostrar efecto convoy en CPU y ventaja de LRU sobre FIFO en memoria.",
            "P1 (Llegada 0, CPU 20) [Monolitico]\nP2 (Llegada 1, CPU 2); P3 (Llegada 2, CPU 3)\nP4 (Llegada 3, CPU 1); P5 (Llegada 4, CPU 2)",
            "P1: 35000 B (9 pags, bucle Silberschatz)\nP2, P5: 5000 B (2 pags c/u)\nP3: 6000 B; P4: 4000 B\nRAM limitada: 4 marcos (16 KB)"
        ],
        [
            "3. Alta Concurrencia\ny Sensibilidad q",
            "Trade-off de quantum en CPU y competencia de 8 procesos por marcos de RAM.",
            "P1 (Llegada 0, CPU 8); P2 (Llegada 1, CPU 4)\nP3 (Llegada 2, CPU 12); P4 (Llegada 3, CPU 3)\nP5 (Llegada 5, CPU 6); P6 (Llegada 6, CPU 2)\nP7 (Llegada 8, CPU 10); P8 (Llegada 9, CPU 5)",
            "P1: 14 KB; P2: 10 KB; P3: 15 KB;\nP4: 9 KB; P5: 12 KB; P6: 8.5 KB;\nP7: 14.5 KB; P8: 11 KB\nTotal: 27 pags en RAM 32 KB (8 marcos)"
        ]
    ]
    t_esc = Table(datos_escenarios, colWidths=[80, 135, 175, 142])
    t_esc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5D8DC")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#1B365D")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8F9FA")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_esc)
    story.append(Spacer(1, 4))

    story.append(Paragraph("6.1. Formulas Matematicas de las Metricas", estilos["H2"]))
    story.append(Paragraph(
        "• <b>Turnaround Time (TAT):</b> <i>TAT_i = T_fin,i - T_llegada,i</i>; Promedio: <i>TAT_prom = (1/N) * sum(TAT_i)</i>.<br/>"
        "• <b>Waiting Time (WT):</b> Ciclos acumulados en LISTO: <i>WT_i = TAT_i - T_CPU,i - T_IO,i</i>.<br/>"
        "• <b>Response Time (RT):</b> Latencia hasta primer despacho: <i>RT_i = T_primer_despacho,i - T_llegada,i</i>.<br/>"
        "• <b>Equidad (Desv. Estandar de WT):</b> <i>sigma_WT = raiz[ (1/N) * sum( (WT_i - WT_prom)^2 ) ]</i>.<br/>"
        "• <b>Inanicion Estadistica:</b> Alerta si ratio <i>WT_i / T_CPU,i &gt;= 4.0</i> y/o <i>WT_i &gt; WT_prom + 1.5 * sigma_WT</i>.<br/>"
        "• <b>Tasa de Aciertos y Fallos de Memoria:</b> <i>Hit Rate (HR) = (Aciertos / Total Accesos) * 100%</i>; <i>PFR = 100% - HR</i>.<br/>"
        "• <b>Fragmentacion Interna:</b> <i>IF_i = (Paginas_Asignadas_i * Tamano_Pagina) - Memoria_Necesitada_i</i>. Total = sum(IF_i).",
        estilos["Cuerpo"]
    ))

    # =========================================================================
    # 7. RESULTADOS OBTENIDOS
    # =========================================================================
    story.append(Paragraph("7. Resultados Obtenidos", estilos["H1"]))
    story.append(Paragraph(
        "A continuacion se presentan las tablas consolidadas reales generadas por el simulador tras la correccion del bug de WT "
        "(archivos <code>resumen_*.csv</code> y <code>memoria_resumen_*.csv</code>):",
        estilos["Cuerpo"]
    ))

    csv_e1 = os.path.join(CARPETA_METRICAS, "resumen_escenario1_ligera_cs1.csv")
    csv_e2 = os.path.join(CARPETA_METRICAS, "resumen_escenario2_convoy_cs1.csv")
    csv_e3_cs1 = os.path.join(CARPETA_METRICAS, "resumen_escenario3_quantum_cs1.csv")
    csv_e3_cs0 = os.path.join(CARPETA_METRICAS, "resumen_escenario3_quantum_cs0.csv")

    anchos_tabla = [112, 42, 44, 52, 52, 52, 42, 66, 56]

    if os.path.exists(csv_e1):
        df_e1 = pd.read_csv(csv_e1)
        story.append(Paragraph("<b>Tabla 1: Escenario 1 - Carga Ligera con E/S (costo_cs = 1 tick, recalculado)</b>", estilos["H2"]))
        story.append(crear_tabla_desde_df(df_e1, estilos, anchos_tabla))
        story.append(Spacer(1, 3))

    if os.path.exists(csv_e2):
        df_e2 = pd.read_csv(csv_e2)
        story.append(Paragraph("<b>Tabla 2: Escenario 2 - Carga Mixta / Efecto Convoy (costo_cs = 1 tick, recalculado)</b>", estilos["H2"]))
        story.append(crear_tabla_desde_df(df_e2, estilos, anchos_tabla))
        story.append(Spacer(1, 3))

    if os.path.exists(csv_e3_cs1):
        df_e3_cs1 = pd.read_csv(csv_e3_cs1)
        story.append(Paragraph("<b>Tabla 3: Escenario 3 - Alta Concurrencia (costo_cs = 1 tick con overhead, recalculado)</b>", estilos["H2"]))
        story.append(crear_tabla_desde_df(df_e3_cs1, estilos, anchos_tabla))
        story.append(Spacer(1, 3))

    if os.path.exists(csv_e3_cs0):
        df_e3_cs0 = pd.read_csv(csv_e3_cs0)
        story.append(Paragraph("<b>Tabla 4: Escenario 3 - Costo Ideal Teorico (costo_cs = 0 ticks, recalculado)</b>", estilos["H2"]))
        story.append(crear_tabla_desde_df(df_e3_cs0, estilos, anchos_tabla))
        story.append(Spacer(1, 5))

    # Tablas de Memoria
    csv_mem = os.path.join(CARPETA_METRICAS, "memoria_resumen_FIFO_vs_LRU.csv")
    if os.path.exists(csv_mem):
        df_mem = pd.read_csv(csv_mem)
        # Reordenar columnas para visualización clara
        cols_mostrar = ["Escenario", "Estrategia", "Total_Accesos", "Total_Aciertos", "Total_Fallos", "Total_Reemplazos", "Hit_Rate_HR (%)", "Page_Fault_Rate_PFR (%)", "Fragmentacion_Interna_Total_Bytes"]
        df_mem_sub = df_mem[cols_mostrar]
        story.append(Paragraph("<b>Tabla 5: Evaluacion Comparativa de Memoria (Paginacion: FIFO vs. LRU)</b>", estilos["H2"]))
        story.append(crear_tabla_desde_df(df_mem_sub, estilos, [100, 52, 45, 45, 45, 52, 60, 65, 68]))
        story.append(Spacer(1, 5))

    # Gráficos embebidos
    img_comparativa_e2 = os.path.join(CARPETA_GRAFICOS, "comparativa_escenario2_convoy_cs1.png")
    img_mem_e2 = os.path.join(CARPETA_GRAFICOS, "memoria_comparativa_escenario2_convoy.png")
    if os.path.exists(img_comparativa_e2) and os.path.exists(img_mem_e2):
        story.append(KeepTogether([
            Paragraph("7.1. Graficos Comparativos: Rendimiento de CPU y Rendimiento de Memoria", estilos["H2"]),
            Image(img_comparativa_e2, width=500, height=185),
            Paragraph("Figura 1: Tiempos promedio y conmutaciones en Escenario 2 (Efecto Convoy en CPU).", estilos["Caption"]),
            Spacer(1, 3),
            Image(img_mem_e2, width=500, height=185),
            Paragraph("Figura 2: Comparativa de Aciertos y Fallos de Memoria (FIFO vs LRU) en Escenario 2.", estilos["Caption"])
        ]))

    # =========================================================================
    # 8. ANÁLISIS E INTERPRETACIÓN
    # =========================================================================
    story.append(Paragraph("8. Analisis e Interpretacion", estilos["H1"]))

    story.append(Paragraph("8.1. Escenario 1: Carga Ligera con E/S y Comportamiento de Round Robin (Q=3)", estilos["H2"]))
    story.append(Paragraph(
        "En la Tabla 1, el Escenario 1 modela un entorno balanceado donde los procesos P1 y P3 intercalan ráfagas de cómputo con ráfagas de E/S. "
        "<b>SJF (no expropiativo)</b> alcanza el menor tiempo de retorno medio (<b>TAT = 12.75 ticks</b>) y menor tiempo de espera medio (<b>WT = 8.00 ticks</b>), "
        "pero a costa de postergar al proceso largo P2 (CPU=4), el cual sufre un tiempo de espera de 16 ticks que dispara una alerta de inanición "
        "por ratio (<b>4.00x</b>). En contraste, <b>FCFS</b> distribuye el acceso de forma secuencial (TAT=13.75, WT=9.00) sin registrar alertas de inanición.",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "Por su parte, <b>Round Robin (Q=3)</b> prioriza la reactividad inicial logrando el mejor tiempo de respuesta promedio (<b>RT = 4.00 ticks</b>, "
        "frente a 4.50 en FCFS y 6.75 en SJF). Tras la corrección estricta del bug de sobrecarga de conmutación de contexto, el tiempo de espera "
        "promedio de Round Robin se recalculó en <b>11.50 ticks</b> (subiendo de 10.50 a 11.50 ticks debido a los ticks de conmutación antes del despacho), "
        "y su desviación estándar aumentó ligeramente de <b>2.96 a 3.20</b>, reflejando una dispersión levemente mayor en los tiempos de espera individuales. "
        "Es importante destacar que Round Robin <b>mantuvo exactamente 0 casos de inanición</b> (0 de 4 procesos), ya que ningún proceso alcanzó el umbral "
        "crítico de ratio de 4.0x (el ratio máximo fue de 3.75x en P3). La penalización en TAT promedio (16.25 ticks) evidencia el costo directo de sus "
        "6 cambios de contexto en un entorno con ráfagas cortas.",
        estilos["Cuerpo"]
    ))

    story.append(Paragraph("8.2. Escenario 2: Demostracion Cuantitativa del Efecto Convoy y Mitigacion en Round Robin", estilos["H2"]))
    story.append(Paragraph(
        "En la Tabla 2, FCFS exhibe el <b>Efecto Convoy</b> en su expresion mas clasica: el proceso monolitico P1 (CPU=20) acapara "
        "la CPU en <i>t=0</i>, obligando a los cuatro procesos cortos (P2 a P5, de 1 a 3 ticks) a esperar en la cola de listos. "
        "Esto eleva el tiempo de espera promedio a <b>18.60 ticks</b> (identico a su tiempo de respuesta tras la correccion del bug de conmutacion) "
        "y genera 4 alertas criticas de ratio (P4 espera 25 ticks para ejecutar 1 sola unidad, ratio <b>25.0x</b>).",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "<b>Round Robin (q=2) reduce notablemente el efecto convoy y mejora la equidad distributiva:</b> el tiempo de respuesta promedio "
        "se desploma de 18.60 a solo <b>5.00 ticks</b> (reduccion del 73.1%), y el tiempo de retorno medio baja de 24.20 a <b>15.40 ticks</b>, "
        "con una desviacion estandar de espera de <b>4.45</b> frente al 9.54 de FCFS. Es crucial senalar que Round Robin registra 3 alertas "
        "de ratio (P3, P4, P5 con ratio &gt;= 4.0x): <i>estas alertas constituyen indicadores estadisticos de riesgo por rafaga breve, "
        "no una demostracion de inanicion indefinida</i>, ya que todos los procesos reciben CPU deterministicamente en su turno.",
        estilos["Cuerpo"]
    ))

    story.append(Paragraph("8.3. Escenario 3: Trade-Off de Quantum en CPU y Separacion entre Conteo de CS y Retardo Real de TAT", estilos["H2"]))
    story.append(Paragraph(
        "En el Escenario 3 (Tablas 3 y 4), se aprecian con exactitud las lecciones clasicas de planificacion:<br/>"
        "1. <b>Separacion entre Conteo de CS y Retardo en TAT:</b> Round Robin con <i>q=2</i> registra <b>25 cambios de contexto</b>. "
        "No obstante, el incremento real en el tiempo de retorno promedio al pasar de costo ideal (CS=0) a costo real (CS=1) es de "
        "<b>16.76 ticks</b> (<i>TAT_{CS=1} = 45.38</i> vs <i>TAT_{CS=0} = 28.62</i>), debido a que el overhead de cada conmutacion se solapa "
        "y distribuye temporalmente entre las distintas llegadas y terminaciones de los 8 procesos.<br/>"
        "2. <b>Explicacion de las 7 Alertas de Inanicion en RR (Q=2):</b> Pese a ser el algoritmo mas reactivo (RT = 9.62), registra el mayor "
        "numero de alertas de inanicion (7 de 8 procesos). Esto ocurre porque el criterio formal de ratio (<i>WT_i / CPU_i &gt;= 4.0</i>) castiga "
        "fuertemente a los procesos cuando el overhead acumulado de 25 conmutaciones eleva el tiempo de espera global. Es un "
        "<b>artefacto cuantitativo de la metrica de penalizacion</b>, no inanicion clasica en el sentido de exclusion indefinida.<br/>"
        "3. <b>Sensibilidad al Quantum y Convergencia Asintotica:</b> Con <i>q=4</i>, los cambios de contexto descienden a 14 y el TAT a 34.62 ticks. "
        "Con <i>q=8</i>, Round Robin reduce los CS a 9, estabilizando el TAT en 31.00 ticks (frente a 26.38 en CS=0) y convergiendo hacia FCFS "
        "(TAT=28.50), confirmando el teorema formal <i>lim_{q -> inf} RR(q) = FCFS</i>.",
        estilos["Cuerpo"]
    ))

    story.append(Paragraph("8.4. Analisis de Gestion de Memoria: Demostracion de Superioridad de LRU sobre FIFO", estilos["H2"]))
    story.append(Paragraph(
        "En la Tabla 5 y la Figura 2, el <b>Escenario 2</b> constituye el laboratorio ideal para evaluar el reemplazo de paginas: "
        "P1 ejecuta de forma continua durante 20 ticks sobre un espacio de 9 paginas con una RAM física limitada a 4 marcos (16 KB). "
        "Al acceder P1 a su working set con localidad temporal, <b>LRU supera claramente a FIFO</b>:<br/>"
        "• <b>Tasa de Aciertos (Hit Rate):</b> LRU alcanza <b>46.43%</b> frente a <b>39.29%</b> de FIFO (<b>diferencia medible de +7.14% a favor de LRU</b>).<br/>"
        "• <b>Fallos y Reemplazos:</b> LRU solo sufre 15 fallos y 4 reemplazos, mientras FIFO incurre en 17 fallos y 6 reemplazos.<br/>"
        "• <i>Explicacion teorica:</i> FIFO expulsa la pagina que llego primero, castigando a las paginas calientes que el bucle re-accede constantemente. "
        "LRU actualiza el estampa de <i>ultimo_acceso</i> en cada referencia, protegiendo las paginas activas y expulsando las de menor frecuencia.",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "<b>Analisis del Resultado Identico en Escenario 3:</b> En el Escenario 3 con Round Robin (q=4) y 8 marcos, tanto FIFO como LRU arrojaron "
        "21 aciertos y 29 fallos (42.0% HR). La auditoria revela una razon teorica solida: bajo Round Robin con 8 procesos que rotan rapidamente "
        "cada 4 ticks, cuando un proceso es desalojado y permanece inactivo en la cola de listos, sus paginas son <i>simultaneamente las que llevan mas "
        "tiempo cargadas (criterio FIFO) y las menos recientemente usadas (criterio LRU)</i>. En consecuencia, el orden de llegada coincide con el orden "
        "de recencia (<i>Arrival Order == Recency Order</i>), forzando a ambos algoritmos a elegir exactamente las mismas paginas victimas.",
        estilos["Cuerpo"]
    ))

    # =========================================================================
    # 9. RIESGOS Y RESPONSABILIDADES PROFESIONALES
    # =========================================================================
    story.append(Paragraph("9. Riesgos y Responsabilidades Profesionales", estilos["H1"]))
    story.append(Paragraph(
        "• <b>Rendimiento y Saturacion:</b> Emplear planificadores sin desalojo (FCFS) o quantums minusculos con alto costo de conmutacion "
        "provoca degradacion de servicio severa, latencias inaceptables y desperdicio de ciclos utiles de CPU.<br/>"
        "• <b>Estabilidad y Ataques DoS:</b> Algoritmos no expropiativos permiten que un proceso con un bucle infinito no intencionado "
        "(<code>while(true)</code>) monopolice el nucleo fisico, inmovilizando el sistema operativo.<br/>"
        "• <b>Seguridad de Memoria y Canales Laterales:</b> El reemplazo de paginas y las diferencias en tiempos de conmutacion pueden ser "
        "explotados mediante ataques de canal lateral (<i>timing attacks</i> tipo Meltdown/Spectre). La MMU y el despachador deben asegurar "
        "aislamiento criptografico e invalidacion estricta de lineas de cache y TLB.<br/>"
        "• <b>Equidad e Inanicion en Sistemas Criticos:</b> En entornos de aviacion, telemedicina o control de reactores, postergar indefinidamente "
        "procesos de baja prioridad o procesos pesados en favor de tareas breves puede ocasionar fallos humanos y materiales irreparables.",
        estilos["Cuerpo"]
    ))

    # =========================================================================
    # 10. LIMITACIONES, MEJORAS Y CONCLUSIONES
    # =========================================================================
    story.append(Paragraph("10. Limitaciones, Mejoras y Conclusiones", estilos["H1"]))

    story.append(Paragraph("10.1. Limitaciones del Modelo Actual", estilos["H2"]))
    story.append(Paragraph(
        "1. <b>Simplificacion del Modelo de Memoria (Observador Sincronico):</b> En el simulador actual, los fallos de pagina y la traduccion "
        "MMU se resuelven de forma logica y sincrona en el mismo ciclo de instruccion, <b>sin agregar tiempo de bloqueo por E/S de disco "
        "adicional a la linea de tiempo de CPU</b> (TAT, WT y RT permanecen desacoplados). Esta simplificacion deliberada permite aislar "
        "rigurosamente las metricas de CPU sin introducir ruido de disco, manteniendo el alcance formativo del curso.<br/>"
        "2. <b>Validacion Estricta de Limites y Manejo de Violacion de Segmento (Segmentation Fault):</b> La MMU valida en su Paso 1 que el "
        "numero de pagina solicitado no exceda el limite asignado en la Tabla de Paginas (<i>num_pagina &lt; num_paginas</i>). Mientras que los accesos "
        "a paginas validas no presentes en RAM detonan un fallo de pagina recuperable con carga bajo demanda, cualquier acceso fuera del espacio "
        "virtual asignado dispara una excepcion de <b>Violacion de Segmento (Segmentation Fault / IndexError)</b> con registro explicito en el log de MMU, "
        "impidiendo corrupciones de memoria y evitando recortar o enmascarar silenciosamente referencias ilegales.<br/>"
        "3. <b>Monoprocesador:</b> No se modela multiprocesamiento simetrico (SMP), afinidad de nucleos ni topologias NUMA.<br/>"
        "4. <b>Costo de Conmutacion Fijo:</b> <i>costo_cs</i> se computa como 1 tick constante, sin modelar fallos dinamicos de cache L1/L2/L3.",
        estilos["Cuerpo"]
    ))

    story.append(Paragraph("10.2. Propuestas de Mejora y Trabajo Futuro", estilos["H2"]))
    story.append(Paragraph(
        "• Integrar un modelo asincrono donde el fallo de pagina suspenda al proceso a estado BLOQUEADO durante una latencia fija de disco (ej. 10 ticks).<br/>"
        "• Implementar el algoritmo de reloj (Segunda Oportunidad) y el algoritmo optimo de Belady (OPT) para confrontar cotas superiores.<br/>"
        "• Incorporar Colas Multinivel con Retroalimentacion (MLFQ) y envejecimiento (<i>aging</i>) para erradicar la inanicion en SJF.",
        estilos["Cuerpo"]
    ))

    story.append(Paragraph("10.3. Conclusiones", estilos["H2"]))
    story.append(Paragraph(
        "1. Se demostro matematicamente la consistencia del calculo de tiempos: en algoritmos no expropiativos sin E/S, <b>WT_prom == RT_prom</b> "
        "con precision del 100%, garantizando que <i>TAT = WT + CPU + IO</i>.<br/>"
        "2. <b>Round Robin reduce sustancialmente el Efecto Convoy</b> y distribuye equitativamente el procesador frente a FCFS, aunque requiere "
        "calibrar cuidadosamente el quantum para no inflar la sobrecarga de cambio de contexto.<br/>"
        "3. La paginacion pura elimina formalmente la fragmentacion externa (0 bytes), confinándola a la fragmentacion interna en el ultimo marco. "
        "Asimismo, se comprobo que <b>LRU supera a FIFO</b> en presencia de localidad temporal, protegiendo las paginas activas.",
        estilos["Cuerpo"]
    ))

    # =========================================================================
    # NOTA METODOLÓGICA (Exigencia explícita del enunciado)
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("Nota Metodologica sobre el Uso de Inteligencia Artificial", estilos["H2"]))
    texto_nota = (
        "En cumplimiento de los lineamientos eticos del curso de Sistemas Operativos (Seccion 8 del enunciado), se declara formalmente "
        "el uso asistido de herramientas de Inteligencia Artificial Generativa (IA) como soporte metodologico en la estructuracion de "
        "scripts de simulacion, graficacion y formateo de datos. El equipo de estudiantes diseno los escenarios de prueba, audito cada "
        "modulo, corrigio las formulas matematicas de conmutacion y espera, verifico y comprendio los resultados empiricos de CPU y memoria, "
        "y asume plena responsabilidad intelectual y academica por el contenido de este informe."
    )
    t_box = Table([[Paragraph(texto_nota, estilos["Destacado"])]], colWidths=[ancho_doc])
    t_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EBF5FB")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#2980B9")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 5))

    # =========================================================================
    # 11. REFERENCIAS UTILIZADAS
    # =========================================================================
    story.append(Paragraph("11. Referencias Utilizadas", estilos["H1"]))
    story.append(Paragraph(
        "[1] Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). <i>Operating System Concepts</i> (10th ed.). "
        "Hoboken, NJ: John Wiley & Sons. (Capitulos 5: 'CPU Scheduling' y 9-10: 'Main Memory & Virtual Memory').",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "[2] Tanenbaum, A. S., & Bos, H. (2015). <i>Modern Operating Systems</i> (4th ed.). "
        "Boston, MA: Pearson. (Capitulos 2: 'Processes and Threads' y 3: 'Memory Management').",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "[3] Stallings, W. (2018). <i>Operating Systems: Internals and Design Principles</i> (9th ed.). "
        "New York, NY: Pearson. (Capitulos 7-8: 'Memory Management & Virtual Memory' y 9: 'Uniprocessor Scheduling').",
        estilos["Cuerpo"]
    ))
    story.append(Paragraph(
        "[4] Love, R. (2010). <i>Linux Kernel Development</i> (3rd ed.). "
        "Upper Saddle River, NJ: Addison-Wesley Professional. (Capitulos 4: 'Process Scheduling' y 12: 'Memory Management').",
        estilos["Cuerpo"]
    ))

    # Compilar PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Informe tecnico completo y actualizado generado en: {RUTA_PDF}")


if __name__ == "__main__":
    generar_informe_pdf()
