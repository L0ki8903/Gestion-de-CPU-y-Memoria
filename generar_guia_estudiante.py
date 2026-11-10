"""
Generador de Documento PDF: guia_sustentacion_expositor.pdf
Documento complementario y pedagogico para el estudiante / expositor.
Contiene:
- Glosario integral de siglas, abreviaciones y terminos tecnicos.
- Explicacion paso a paso de la Planificacion de CPU y Gestion de Memoria.
- Guia de lectura e interpretacion de los resultados reales de consola.
- Banco de preguntas tipicas del profesor con respuestas de 10/10.
- Guion y chuleta ejecutiva de sustentacion.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

DIRECTORIO_PROYECTO = r"C:\Users\Carlos Ibañez\.gemini\antigravity\scratch\proyecto_so_cpu"
RUTA_SALIDA_PDF = os.path.join(DIRECTORIO_PROYECTO, "guia_sustentacion_expositor.pdf")


class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para numerar paginas 'Pagina X de Y' y membrete elegante."""
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

    def draw_page_decorations(self, total_pages):
        self.saveState()
        # No dibujar en la portada (Pagina 1)
        if self._pageNumber > 1:
            # Header sutil
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(54, 750, "GUÍA DEL EXPOSITOR: SISTEMAS OPERATIVOS (UCC 2026)")
            self.setFont("Helvetica", 8)
            self.drawRightString(558, 750, "CPU & MEMORIA VIRTUAL")

            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

            # Footer
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 45, 558, 45)

            self.setFont("Helvetica", 8.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 32, "Manual Pedagógico de Sustentación Oral — Proyecto Final")
            self.drawRightString(558, 32, f"Página {self._pageNumber} de {total_pages}")

        self.restoreState()


def crear_estilos():
    base = getSampleStyleSheet()

    azul_oscuro = colors.HexColor("#0F172A")
    azul_primario = colors.HexColor("#0284C7")
    indigo = colors.HexColor("#4F46E5")
    gris_texto = colors.HexColor("#334155")
    gris_oscuro = colors.HexColor("#1E293B")

    return {
        "DocTitle": ParagraphStyle(
            "DocTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=azul_oscuro,
            alignment=TA_CENTER
        ),
        "DocSub": ParagraphStyle(
            "DocSub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=13,
            leading=18,
            textColor=azul_primario,
            alignment=TA_CENTER
        ),
        "MetaText": ParagraphStyle(
            "MetaText",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748B"),
            alignment=TA_CENTER
        ),
        "SecTitle": ParagraphStyle(
            "SecTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=azul_oscuro,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True
        ),
        "SubSecTitle": ParagraphStyle(
            "SubSecTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=indigo,
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=gris_texto,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        ),
        "BulletText": ParagraphStyle(
            "BulletText",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=gris_texto,
            leftIndent=12,
            spaceAfter=3
        ),
        "CalloutText": ParagraphStyle(
            "CalloutText",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=13,
            textColor=gris_oscuro
        ),
        "TableHead": ParagraphStyle(
            "TableHead",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=colors.white,
            alignment=TA_CENTER
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=gris_oscuro
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBold",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=azul_oscuro
        ),
        "Pregunta": ParagraphStyle(
            "Pregunta",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#0F766E"),
            spaceBefore=8,
            spaceAfter=2,
            keepWithNext=True
        ),
        "Respuesta": ParagraphStyle(
            "Respuesta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13.5,
            textColor=gris_texto,
            spaceAfter=6,
            leftIndent=10
        )
    }


def callout_box(texto, estilos, bg="#F0F9FF", border="#0284C7", icono="💡"):
    contenido = [
        Paragraph(f"<b>{icono} Clave para la Sustentación:</b> {texto}", estilos["CalloutText"])
    ]
    t = Table([[contenido]], colWidths=[504])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor(border)),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def construir_guia_pdf():
    doc = SimpleDocTemplate(
        RUTA_SALIDA_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    est = crear_estilos()
    story = []

    # =========================================================================
    # PORTADA DE LA GUÍA
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("GUÍA MAESTRA DEL EXPOSITOR", est["DocTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Manual Pedagógico para la Comprensión y Sustentación Oral del Proyecto", est["DocSub"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Tema:</b> Planificación de CPU &bull; Gestión de Memoria Virtual con Paginación Pura<br/>"
        "<b>Estudiantes:</b> Carlos Andrés Ibañez Barrios &bull; Shaadon Jiménez Flores<br/>"
        "<b>Docente:</b> Mag. Sergio Luis Lubo Argumedo<br/>"
        "Universidad Cooperativa de Colombia &bull; Facultad de Ingenierías &bull; Santa Marta &bull; 2026",
        est["MetaText"]
    ))
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284C7"), spaceAfter=14))

    # Introducción
    story.append(Paragraph(
        "<b>¿Para qué sirve este documento?</b><br/>"
        "A diferencia del <i>Informe Técnico</i> (formal, denso y lleno de código), este manual fue redactado "
        "en lenguaje claro y didáctico para que <b>entiendas exactamente qué hace cada parte del sistema</b>, "
        "qué significan todos los números que viste en la terminal, cómo responder las preguntas difíciles del "
        "profesor y cómo explicar con autoridad técnica cada decisión de diseño tomada en el simulador.",
        est["Body"]
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 1: GLOSARIO DE SIGLAS Y ABREVIACIONES
    # =========================================================================
    story.append(Paragraph("1. Glosario Maestro de Abreviaciones, Siglas y Fórmulas", est["SecTitle"]))
    story.append(Paragraph(
        "En los exámenes y sustentaciones de Sistemas Operativos, dominar la terminología exacta transmite seguridad y rigor. "
        "A continuación se presenta la totalidad de siglas empleadas en las tablas de resultados:",
        est["Body"]
    ))

    data_glosario = [
        [Paragraph("Sigla", est["TableHead"]),
         Paragraph("Nombre Formal", est["TableHead"]),
         Paragraph("Significado Intuitivo (¿Qué representa?)", est["TableHead"]),
         Paragraph("Fórmula o Criterio", est["TableHead"])],

        [Paragraph("TAT", est["TableCellBold"]),
         Paragraph("Turnaround Time<br/>(Tiempo de Retorno)", est["TableCell"]),
         Paragraph("El tiempo total desde que el proceso llega al sistema hasta que finaliza por completo su última ráfaga.", est["TableCell"]),
         Paragraph("<b>TAT = T_fin - T_llegada</b>", est["TableCell"])],

        [Paragraph("WT", est["TableCellBold"]),
         Paragraph("Waiting Time<br/>(Tiempo de Espera)", est["TableCell"]),
         Paragraph("El tiempo que el proceso pasa 'haciendo fila' en la cola de LISTOS esperando que le den CPU.", est["TableCell"]),
         Paragraph("<b>WT = Ticks en estado LISTO</b><br/>= TAT - T_CPU - T_IO", est["TableCell"])],

        [Paragraph("RT", est["TableCellBold"]),
         Paragraph("Response Time<br/>(Tiempo de Respuesta)", est["TableCell"]),
         Paragraph("Tiempo que tarda el proceso en recibir la CPU por <b>primera vez</b>. Mide la agilidad interactiva del sistema.", est["TableCell"]),
         Paragraph("<b>RT = T_primer_despacho - T_llegada</b>", est["TableCell"])],

        [Paragraph("CS", est["TableCellBold"]),
         Paragraph("Context Switch<br/>(Cambio de Contexto)", est["TableCell"]),
         Paragraph("Acción del SO de guardar el estado (PCB) del proceso actual en memoria y restaurar el del siguiente.", est["TableCell"]),
         Paragraph("<b>costo_cs = 1 tick</b> (real)<br/>costo_cs = 0 tick (ideal)", est["TableCell"])],

        [Paragraph("σ_WT", est["TableCellBold"]),
         Paragraph("Desviación Estándar de WT (Equidad)", est["TableCell"]),
         Paragraph("Mide qué tan dispersas están las esperas entre procesos. Un valor bajo significa que el trato fue parejo.", est["TableCell"]),
         Paragraph("<b>sqrt(Σ(WT_i - μ)^2 / N)</b>", est["TableCell"])],

        [Paragraph("Inanición", est["TableCellBold"]),
         Paragraph("Starvation<br/>(Inanición Estadística)", est["TableCell"]),
         Paragraph("Alerta cuando un proceso espera desproporcionadamente más de lo que dura su propio cómputo.", est["TableCell"]),
         Paragraph("<b>Alerta si: WT / T_CPU ≥ 4.0</b>", est["TableCell"])],

        [Paragraph("PCB", est["TableCellBold"]),
         Paragraph("Process Control Block<br/>(Bloque de Control)", est["TableCell"]),
         Paragraph("Estructura de datos que almacena el 'carnet de identidad' del proceso: PID, estado, ráfagas y tabla de páginas.", est["TableCell"]),
         Paragraph("Clase <b>Proceso</b> en pcb.py", est["TableCell"])],

        [Paragraph("MMU", est["TableCellBold"]),
         Paragraph("Memory Management Unit<br/>(Unidad de Manejo)", est["TableCell"]),
         Paragraph("Dispositivo de hardware simulado que convierte direcciones virtuales en direcciones físicas en RAM.", est["TableCell"]),
         Paragraph("<b>dir_fisica = (marco * 4096) + offset</b>", est["TableCell"])],

        [Paragraph("HR", est["TableCellBold"]),
         Paragraph("Hit Rate<br/>(Tasa de Aciertos)", est["TableCell"]),
         Paragraph("Porcentaje de veces que la página solicitada ya estaba cargada en memoria RAM sin necesidad de disco.", est["TableCell"]),
         Paragraph("<b>HR = (Aciertos / Total) * 100%</b>", est["TableCell"])],

        [Paragraph("PFR", est["TableCellBold"]),
         Paragraph("Page Fault Rate<br/>(Tasa de Fallos)", est["TableCell"]),
         Paragraph("Porcentaje de accesos donde la página NO estaba en RAM y el SO tuvo que traerla (Fallo de Página).", est["TableCell"]),
         Paragraph("<b>PFR = 100% - HR</b>", est["TableCell"])],

        [Paragraph("IF", est["TableCellBold"]),
         Paragraph("Fragmentación Interna", est["TableCell"]),
         Paragraph("Espacio desperdiciado dentro del último marco asignado porque el proceso pidió menos de 4096 bytes.", est["TableCell"]),
         Paragraph("<b>mem_asignada - mem_necesitada</b>", est["TableCell"])],

        [Paragraph("EF", est["TableCellBold"]),
         Paragraph("Fragmentación Externa", est["TableCell"]),
         Paragraph("Memoria libre total suficiente pero dispersa en huecos. En paginación pura <b>es exactamente 0</b>.", est["TableCell"]),
         Paragraph("<b>0 bytes</b> (por diseño de marcos fijos)", est["TableCell"])]
    ]

    t_glo = Table(data_glosario, colWidths=[55, 110, 185, 154])
    t_glo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_glo)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 2: PLANIFICACIÓN DE CPU
    # =========================================================================
    story.append(Paragraph("2. ¿Cómo Funciona la Planificación de CPU? (Explicación Intuitiva)", est["SecTitle"]))
    story.append(Paragraph(
        "El procesador solo puede ejecutar las instrucciones de <b>un solo proceso a la vez</b>. Cuando varios programas "
        "quieren correr simultáneamente, el sistema operativo necesita una política para decidir a quién le toca el turno. "
        "Nuestro simulador implementa las 3 estrategias clásicas:",
        est["Body"]
    ))

    story.append(Paragraph("2.1. Los 3 Algoritmos Explicados de Forma Simple", est["SubSecTitle"]))
    story.append(Paragraph(
        "<b>1. FCFS (First-Come, First-Served):</b><br/>"
        "• <i>Metáfora:</i> Es la fila tradicional del banco. Quien llega primero, se atiende primero.<br/>"
        "• <i>Ventaja:</i> Muy fácil de programar y casi no gasta tiempo cambiando de contexto.<br/>"
        "• <i>El gran peligro (Efecto Convoy):</i> Si el primer cliente de la fila va a pagar 50 facturas (un proceso gigante de CPU=20), "
        "los clientes de atrás que solo iban a retirar un recibo de 1 minuto tienen que esperar 20 minutos parados. Eso arruina la interactividad.",
        est["Body"]
    ))

    story.append(Paragraph(
        "<b>2. SJF No Expropiativo (Shortest Job First):</b><br/>"
        "• <i>Metáfora:</i> En la fila rápida del supermercado, quien tiene menos artículos pasa primero.<br/>"
        "• <i>Ventaja:</i> Minimiza matemáticamente el tiempo de espera promedio general.<br/>"
        "• <i>Desempate:</i> Si dos procesos tienen la misma ráfaga, pasa el que llegó primero; si llegaron al mismo tiempo, el de menor PID.<br/>"
        "• <i>Peligro:</i> Si siguen llegando procesos cortitos todo el tiempo, un proceso largo nunca recibe CPU (Inanición).",
        est["Body"]
    ))

    story.append(Paragraph(
        "<b>3. Round Robin con Quantum q:</b><br/>"
        "• <i>Metáfora:</i> Un reloj de ajedrez donde cada jugador tiene exactamente <i>q</i> segundos de turno. Si no termina su jugada en ese tiempo, "
        "se le pausa y pasa al final de la fila.<br/>"
        "• <i>Ventaja:</i> Nadie monopoliza la CPU. Todos los procesos reciben atención rápidamente (bajísimo Tiempo de Respuesta RT).<br/>"
        "• <i>Regla de desempate clave:</i> Si un proceso agota su quantum en el mismo instante en que llega un nuevo proceso, el simulador "
        "<b>le da prioridad al nuevo proceso</b>, colocándolo de primero en la cola para que su tiempo de respuesta inicial sea excelente.",
        est["Body"]
    ))

    story.append(Spacer(1, 4))
    story.append(callout_box(
        "<b>El cambio de contexto no es gratis:</b> Salvar los registros y el estado del PCB de un proceso que sale y cargar el del nuevo "
        "consume cómputo real. En el simulador esto se modela como <code>costo_cs = 1 tick</code>. Si el quantum es muy pequeño (ej. q=2), "
        "el procesador pasa demasiado tiempo conmutando en lugar de trabajar.",
        estilos=est, bg="#FEF3C7", border="#D97706", icono="⚠️"
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 3: GESTIÓN DE MEMORIA CON PAGINACIÓN PURA
    # =========================================================================
    story.append(Paragraph("3. ¿Cómo Funciona la Gestión de Memoria? (Paginación y MMU)", est["SecTitle"]))
    story.append(Paragraph(
        "En los sistemas primitivos, a un proceso se le asignaba un bloque continuo de memoria RAM. Si los procesos se abrían y cerraban, "
        "la RAM quedaba llena de huecos dispersos que no alcanzaban para nadie (<b>Fragmentación Externa</b>). "
        "La solución moderna es la <b>Paginación Pura</b>:",
        est["Body"]
    ))

    story.append(Paragraph("3.1. Páginas, Marcos y el Algoritmo MMU en 4 Pasos", est["SubSecTitle"]))
    story.append(Paragraph(
        "• <b>Páginas:</b> Bloques lógicos de tamaño fijo (4 KB = 4096 bytes) en el espacio del programa.<br/>"
        "• <b>Marcos (Frames):</b> Bloques del mismo tamaño fijo (4 KB) pero en la memoria física real (RAM).<br/>"
        "• <b>La MMU:</b> Cada vez que la CPU quiere leer una dirección virtual, ejecuta este algoritmo canónico de 4 pasos:",
        est["Body"]
    ))

    data_mmu = [
        [Paragraph("Paso", est["TableHead"]),
         Paragraph("Operación MMU", est["TableHead"]),
         Paragraph("Ejemplo Numérico Real (dir_virtual = 9500 B)", est["TableHead"])],
        [Paragraph("1", est["TableCellBold"]),
         Paragraph("<b>Número de Página (p):</b><br/>p = dir_virtual // 4096", est["TableCell"]),
         Paragraph("9500 // 4096 = <b>Página 2</b>", est["TableCell"])],
        [Paragraph("2", est["TableCellBold"]),
         Paragraph("<b>Desplazamiento / Offset (d):</b><br/>d = dir_virtual % 4096", est["TableCell"]),
         Paragraph("9500 % 4096 = <b>1308 bytes</b> de desplazamiento", est["TableCell"])],
        [Paragraph("3", est["TableCellBold"]),
         Paragraph("<b>Validación de Límites:</b><br/>Verificar si p < len(tabla_paginas)", est["TableCell"]),
         Paragraph("Si el proceso tiene 3 páginas, 2 < 3 → <b>Válida (Marco #5)</b>.<br/>Si pide página 6 → <b>Detona Segmentation Fault</b>.", est["TableCell"])],
        [Paragraph("4", est["TableCellBold"]),
         Paragraph("<b>Dirección Física Final:</b><br/>dir_fisica = (id_marco * 4096) + d", est["TableCell"]),
         Paragraph("(5 * 4096) + 1308 = <b>21,788 bytes</b> en la RAM real.", est["TableCell"])]
    ]
    t_mmu = Table(data_mmu, colWidths=[35, 230, 239])
    t_mmu.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_mmu)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2. Fragmentación y Políticas de Reemplazo (FIFO vs LRU)", est["SubSecTitle"]))
    story.append(Paragraph(
        "• <b>Fragmentación Externa = 0 bytes:</b> Como cualquier página de 4 KB cabe en cualquier marco de 4 KB disponible, "
        "no importa si están separados. No hay huecos desperdiciados.<br/>"
        "• <b>Fragmentación Interna:</b> Si un proceso pide 9,000 bytes, necesita 3 páginas de 4096 (12,288 bytes). La diferencia "
        "<code>12,288 - 9,000 = 3,288 bytes</code> se desperdicia dentro del último marco asignado.<br/>"
        "• <b>Reemplazo ante Fallo de Página (Page Fault):</b> Cuando la RAM se llena y se pide una página nueva, hay que expulsar a una víctima:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;→ <b>FIFO:</b> Desaloja la página que llegó primero a la RAM (la más vieja). Es ciega, pues puede botar una página que el proceso está usando intensamente.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;→ <b>LRU:</b> Desaloja la página que lleva más tiempo sin ser usada (la menos recientemente referenciada). Se basa en el <b>Principio de Localidad Temporal</b>.",
        est["Body"]
    ))

    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 4: CÓMO EXPLICAR LOS RESULTADOS REALES DE LA TERMINAL
    # =========================================================================
    story.append(Paragraph("4. Guía de Lectura: ¿Qué Significan los Resultados que Obtuviste?", est["SecTitle"]))
    story.append(Paragraph(
        "Aquí está el análisis directo de los números exactos que salieron en tu terminal al ejecutar <code>main.py</code>. "
        "Léelo con atención para saber qué decirle al profesor cuando mire cada tabla:",
        est["Body"]
    ))

    story.append(Paragraph("4.1. Escenario 1: Carga Ligera (Con E/S y Bloqueos)", est["SubSecTitle"]))
    story.append(Paragraph(
        "• <b>FCFS:</b> TAT=13.75, WT=9.00, RT=4.50, CS=5, Inanición=0.<br/>"
        "• <b>SJF:</b> TAT=12.75, WT=8.00, RT=6.75, CS=5, Inanición=1.<br/>"
        "• <b>Round Robin (Q=3):</b> TAT=16.25, WT=11.50, RT=4.00, CS=6, Inanición=0.<br/>"
        "<b>¿Cómo explicarlo?</b><br/>"
        "1. <i>SJF es el rey de la eficiencia promedio:</i> Logra el menor tiempo de retorno (12.75) y menor espera (8.00) porque despacha de primero a los procesos cortos.<br/>"
        "2. <i>Round Robin es el rey de la interactividad:</i> Aunque su TAT es mayor por conmutar turnos, su tiempo de respuesta es el más rápido de todos (RT=4.00).<br/>"
        "3. <i>¿Por qué aquí WT es mayor que RT?</i> Porque P1 y P3 realizan transferencias de E/S. Pasan a <code>BLOQUEADO</code> y, cuando regresan a <code>LISTO</code>, "
        "tienen que volver a esperar en la fila, acumulando más tiempo de espera (WT) que el que tardaron en su primer despacho (RT).",
        est["Body"]
    ))

    story.append(Paragraph("4.2. Escenario 2: El Efecto Convoy (La Prueba de Fuego)", est["SubSecTitle"]))
    story.append(Paragraph(
        "• <b>FCFS:</b> TAT=24.20, WT=18.60, RT=18.60, CS=4, Inanición=4.<br/>"
        "• <b>SJF:</b> TAT=23.40, WT=17.80, RT=17.80, CS=4, Inanición=4.<br/>"
        "• <b>Round Robin (Q=2):</b> TAT=15.40, WT=9.80, RT=5.00, CS=7, Inanición=3.<br/>"
        "<b>¿Cómo explicarlo?</b><br/>"
        "1. <i>El colapso de FCFS:</i> El proceso P1 (ráfaga de 20 ticks) acapara el procesador en t=0. Los procesos cortos P2, P3, P4 y P5 quedan atrapados "
        "esperando casi 20 ticks solo para empezar. Su tiempo de respuesta es altísimo (18.60) y 4 de los 5 procesos caen en inanición.<br/>"
        "2. <i>El rescate de Round Robin:</i> Al cortarle la CPU a P1 cada 2 ticks (Q=2), los procesos cortos terminan rapidísimo. El tiempo de respuesta cae "
        "de 18.60 a <b>5.00 ticks</b> (¡una reducción brutal del <b>73.1%</b>!) y el TAT promedio baja de 24.20 a 15.40.<br/>"
        "3. <i>En Memoria (LRU vence a FIFO):</i> La memoria se limitó a 4 marcos para forzar reemplazos sobre el patrón canónico de Silberschatz. "
        "<b>LRU logró 46.43% de aciertos frente al 39.29% de FIFO</b> (13 aciertos contra 11, y solo 4 reemplazos contra 6). Esto demuestra que recordar "
        "las páginas usadas recientemente ahorra fallos de página.",
        est["Body"]
    ))

    story.append(Paragraph("4.3. Escenario 3: La Sensibilidad al Quantum y el Costo del Context Switch", est["SubSecTitle"]))
    story.append(Paragraph(
        "• <b>Con costo real (CS=1 tick):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;→ RR Q=2: TAT=45.38, WT=39.12, RT=9.62, <b>CS=25</b>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;→ RR Q=4: TAT=34.62, WT=28.38, RT=14.75, <b>CS=14</b>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;→ RR Q=8: TAT=31.00, WT=24.75, RT=19.50, <b>CS=9</b>.<br/>"
        "• <b>En mundo ideal sin costo de hardware (CS=0 tick):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;→ RR Q=2: TAT=28.62, WT=22.38, RT=5.75, <b>CS=25</b>.<br/>"
        "<b>¿Cómo explicarlo?</b><br/>"
        "Este escenario enseña el <b>Trade-off fundamental del Quantum</b>:<br/>"
        "Si usas un quantum muy pequeño (Q=2), la CPU cambia 25 veces de proceso. En un sistema real (CS=1), esos 25 cambios le roban 25 ticks a la CPU, "
        "inflando el TAT de 28.62 a 45.38. Si usas Q=8, los cambios bajan a 9 y el TAT mejora a 31.00, pero el tiempo de respuesta empeora a 19.50 porque se parece a FCFS.",
        est["Body"]
    ))

    story.append(Spacer(1, 4))
    story.append(callout_box(
        "<b>La prueba matemática de los tests verdes [TEST WT=RT]:</b><br/>"
        "En el Escenario 2, FCFS dio WT=18.60 y RT=18.60 (iguales). SJF dio WT=17.80 y RT=17.80 (iguales).<br/>"
        "<i>¿Por qué?</i> Porque como son algoritmos no expropiativos y los procesos no hacen E/S, una vez que un proceso entra a la CPU "
        "corre hasta morir. Todo lo que esperó antes de entrar (RT) es exactamente todo lo que esperó en toda su vida (WT). "
        "Que ambos números den exactamente idénticos prueba que tu simulador cuenta la sobrecarga de conmutación con cero error.",
        estilos=est, bg="#ECFDF5", border="#059669", icono="✅"
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECCIÓN 5: BANCO DE PREGUNTAS DEL PROFESOR Y CÓMO RESPONDERLAS
    # =========================================================================
    story.append(Paragraph("5. Banco de Preguntas Típicas del Jurado y Respuestas de 10/10", est["SecTitle"]))
    story.append(Paragraph(
        "Estas son las preguntas más comunes que un profesor de Sistemas Operativos suele hacer en este proyecto. "
        "Aprende el concepto detrás de cada respuesta:",
        est["Body"]
    ))

    preguntas = [
        ("Profesor: ¿Por qué en el Escenario 2 el tiempo de espera promedio (WT) es matemáticamente igual al tiempo de respuesta (RT) en FCFS y SJF?",
         "Respuesta: Porque en el Escenario 2 los algoritmos son NO expropiativos y los procesos tienen cómputo puro sin operaciones de E/S. "
         "Esto significa que un proceso solo espera una vez en la cola de listos; en el momento en que es despachado a la CPU, ejecuta hasta terminar sin volver a esperar jamás. "
         "Por ende, el tiempo transcurrido hasta su primer despacho (RT) es idéntico a su tiempo de espera total acumulado (WT)."),

        ("Profesor: ¿Y por qué en el Escenario 1 esa igualdad WT == RT ya no se cumple?",
         "Respuesta: Porque en el Escenario 1 los procesos P1 y P3 realizan operaciones de E/S intermedias. Cuando piden E/S pasan a estado BLOQUEADO y, "
         "al terminar la transferencia periférica, regresan a la cola de LISTOS. Esa segunda espera se suma al WT total, haciendo que WT sea mayor que el RT inicial."),

        ("Profesor: ¿Qué pasa si el quantum (q) de Round Robin se hace extremadamente grande?",
         "Respuesta: Si el quantum es mayor o igual que la ráfaga más larga de todos los procesos, ningún proceso será expropiado por límite de tiempo. "
         "En ese límite matemático, Round Robin degenera exactamente en el algoritmo FCFS (First-Come, First-Served)."),

        ("Profesor: ¿Por qué LRU le ganó a FIFO en el Escenario 2, pero en el Escenario 3 empataron?",
         "Respuesta: En el Escenario 2, el proceso P1 ejecutó el patrón de referencias de Silberschatz en una memoria restringida a 4 marcos. Ese patrón tiene "
         "localidad temporal (reutiliza páginas consultadas recientemente). LRU protege esas páginas calientes, mientras que FIFO las desaloja por ser viejas. "
         "En cambio, en el Escenario 3 hay 8 procesos rotando rápidamente en Round Robin; esa rotación constante satura la RAM y hace que el orden cronológico "
         "de llegada a la memoria (FIFO) coincida con el orden de recencia (LRU)."),

        ("Profesor: ¿Cómo garantiza su simulador que no exista fragmentación externa en memoria?",
         "Respuesta: Por la propia definición de la Paginación Pura. La memoria física se divide en marcos de tamaño fijo (4096 bytes) y el espacio virtual en páginas del mismo tamaño. "
         "Cualquier página libre puede colocarse en cualquier marco disponible sin importar que no sean contiguos. Al no requerir memoria contigua, la fragmentación externa es estrictamente 0 bytes."),

        ("Profesor: ¿Qué hace su simulador si un proceso intenta acceder a una dirección virtual fuera de su rango asignado?",
         "Respuesta: El simulador no recorta en silencio la dirección. En el Paso 3 del algoritmo de la MMU, valida si el número de página calculado excede el tamaño "
         "de la tabla de páginas del proceso. Si lo excede, detona inmediatamente una excepción formal IndexError etiquetada como 'Violación de Segmento (Segmentation Fault)', "
         "emulando con precisión las trampas de hardware reales de un sistema operativo.")
    ]

    for preg, resp in preguntas:
        story.append(Paragraph(preg, est["Pregunta"]))
        story.append(Paragraph(resp, est["Respuesta"]))

    story.append(Spacer(1, 8))

    # =========================================================================
    # SECCIÓN 6: CHULETA RESUMEN PARA LA SUSTENTACIÓN
    # =========================================================================
    story.append(Paragraph("6. 'Chuleta' Resumen: Guion de 2 Minutos para Abrir tu Exposición", est["SecTitle"]))
    story.append(Paragraph(
        "Si te piden resumir tu proyecto en 2 minutos frente al salón o al profesor, di exactamente esto:",
        est["Body"]
    ))

    story.append(callout_box(
        "<i>'Buenos días profesor. Nuestro proyecto consistió en construir un simulador ciclo a ciclo en Python 3 que unifica dos subsistemas fundamentales: "
        "la Planificación de CPU y la Gestión de Memoria Virtual por Paginación Pura.<br/><br/>"
        "En la parte de CPU demostramos empíricamente el <b>Efecto Convoy</b> en el Escenario 2: con FCFS, un proceso largo acaparó el procesador obligando "
        "a los procesos cortos a esperar 18.6 ticks. Al aplicar <b>Round Robin (Q=2)</b>, el tiempo de respuesta cayó un <b>73.1%</b> (a 5 ticks), resolviendo la interactividad.<br/><br/>"
        "También modelamos el costo real de cambio de contexto (costo_cs = 1 tick), demostrando el trade-off del quantum: quantums muy pequeños aumentan "
        "los cambios de contexto (25 CS en el Escenario 3) y disparan el TAT a 45.38 ticks.<br/><br/>"
        "En la parte de Memoria implementamos la traducción MMU en 4 pasos, comprobamos ausencia de fragmentación externa (0 bytes), calculamos la fragmentación interna "
        "y demostramos cómo el algoritmo <b>LRU superó a FIFO logrando un 46.43% de aciertos frente a 39.29%</b> gracias al principio de localidad temporal.'</i>",
        estilos=est, bg="#F8FAFC", border="#475569", icono="🗣️"
    ))

    # Compilacion del PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Guia de sustentacion generada exitosamente en: {RUTA_SALIDA_PDF}")


if __name__ == "__main__":
    construir_guia_pdf()
