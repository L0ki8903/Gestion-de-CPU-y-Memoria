"""
Generador de Presentacion PowerPoint (.pptx) para Sustentacion de Proyecto de SO
Tema: Gestion de Procesos y Planificacion de CPU, ampliado con Gestion de Memoria
Universidad Cooperativa de Colombia - 2026
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

DIRECTORIO_PROYECTO = r"C:\Users\Carlos Ibañez\.gemini\antigravity\scratch\proyecto_so_cpu"
DIRECTORIO_GRAFICOS = os.path.join(DIRECTORIO_PROYECTO, "resultados", "graficos")
RUTA_SALIDA_PPTX = os.path.join(DIRECTORIO_PROYECTO, "presentacion_sustentacion.pptx")
RUTA_GANTT_ESC2 = os.path.join(DIRECTORIO_GRAFICOS, "gantt_escenario2_convoy_Round_Robin_Q2_cs1.png")

# Paleta de Colores
BG_COLOR = RGBColor(11, 17, 32)        # #0B1120 Azul muy oscuro
CARD_BG = RGBColor(26, 36, 54)         # #1A2436 Slate azulado
CARD_BORDER = RGBColor(51, 65, 85)     # #334155 Borde slate
PRIMARY = RGBColor(56, 189, 248)       # #38BDF8 Cian
SECONDARY = RGBColor(129, 140, 248)    # #818CF8 Indigo
ACCENT = RGBColor(52, 211, 153)        # #34D399 Verde esmeralda
WARNING = RGBColor(251, 191, 36)       # #FBBF24 Amarillo
YELLOW = WARNING                       # Alias
DANGER = RGBColor(248, 113, 113)       # #F87171 Rojo
TEXT_TITLE = RGBColor(255, 255, 255)   # Blanco
TEXT_BODY = RGBColor(226, 232, 240)    # #E2E8F0 Gris claro
TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8 Gris medio
TEXT_DIM = RGBColor(100, 116, 139)     # #64748B Gris oscuro


def crear_slide_base(prs, tag_text, title_text, subtitle_text, slide_num, total_slides=8):
    """Crea una diapositiva con fondo uniforme, encabezado estandarizado y pie de pagina."""
    blank_layout = prs.slide_layouts[6]  # Layout en blanco
    slide = prs.slides.add_slide(blank_layout)

    # Fondo completo
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()

    # Si es la portada, omitimos el encabezado estandar
    if slide_num == 1:
        return slide

    # Header Top Bar Info
    tb_header = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
    tf_top = tb_header.text_frame
    tf_top.word_wrap = True
    p_top = tf_top.paragraphs[0]
    p_top.text = "UCC SANTA MARTA  •  INGENIERÍA DE SOFTWARE  •  SISTEMAS OPERATIVOS 2026"
    p_top.font.size = Pt(9.5)
    p_top.font.bold = True
    p_top.font.color.rgb = TEXT_DIM

    # Header Tag (Pill)
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(8.0), Inches(0.3))
    p_tag = tag_box.text_frame.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.size = Pt(10.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = PRIMARY

    # Header Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.733), Inches(0.55))
    p_title = title_box.text_frame.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_TITLE

    # Header Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.35))
    p_sub = sub_box.text_frame.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = TEXT_MUTED

    # Footer
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
    tf_foot = footer_box.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = f"Proyecto Final: Planificación de CPU & Gestión de Memoria                      Diapositiva {slide_num} de {total_slides}"
    p_foot.font.size = Pt(9.5)
    p_foot.font.color.rgb = TEXT_DIM

    return slide


def agregar_tarjeta(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Agrega una tarjeta redondeada con estilo glassmorphism oscuro."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape


# =========================================================================
# GENERADOR PRINCIPAL
# =========================================================================
def generar_presentacion_pptx():
    prs = Presentation()
    # Formato 16:9 Panoramico
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ---------------------------------------------------------------------
    # DIAPOSITIVA 1: PORTADA
    # ---------------------------------------------------------------------
    slide1 = crear_slide_base(prs, "", "", "", 1)

    # Tarjeta Central de Portada
    agregar_tarjeta(slide1, Inches(1.2), Inches(0.8), Inches(10.933), Inches(5.9), bg_color=CARD_BG, border_color=PRIMARY)

    # Contenido Portada
    tb_cov = slide1.shapes.add_textbox(Inches(1.6), Inches(1.1), Inches(10.133), Inches(2.2))
    tf = tb_cov.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "PROYECTO FINAL  •  SISTEMAS OPERATIVOS"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = PRIMARY
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "Gestión de Procesos y Planificación de CPU"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_TITLE
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "ampliado con Gestión de Memoria (Paginación Pura)"
    p2.font.size = Pt(18)
    p2.font.italic = True
    p2.font.color.rgb = SECONDARY
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "Simulador determinista de tiempo discreto ciclo a ciclo (reloj tick-by-tick) en Python 3 con FCFS, SJF no expropiativo, Round Robin, MMU en 4 pasos y reemplazo FIFO frente a LRU."
    p3.font.size = Pt(12)
    p3.font.color.rgb = TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER

    # Tarjetas de Integrantes y Docente
    autores = [
        ("Carlos Andrés Ibañez Barrios", "Estudiante Ponente", PRIMARY),
        ("Shaadon Jiménez Flores", "Estudiante Ponente", PRIMARY),
        ("Mag. Sergio Luis Lubo Argumedo", "Docente Evaluador", SECONDARY)
    ]

    for idx, (nombre, cargo, col) in enumerate(autores):
        c_left = Inches(1.8 + idx * 3.3)
        agregar_tarjeta(slide1, c_left, Inches(3.6), Inches(3.0), Inches(1.3), bg_color=RGBColor(18, 25, 41), border_color=col)
        tb_a = slide1.shapes.add_textbox(c_left, Inches(3.75), Inches(3.0), Inches(1.0))
        tf_a = tb_a.text_frame
        tf_a.word_wrap = True
        pa1 = tf_a.paragraphs[0]
        pa1.text = nombre
        pa1.font.size = Pt(12)
        pa1.font.bold = True
        pa1.font.color.rgb = TEXT_TITLE
        pa1.alignment = PP_ALIGN.CENTER

        pa2 = tf_a.add_paragraph()
        pa2.text = cargo
        pa2.font.size = Pt(10)
        pa2.font.color.rgb = col
        pa2.alignment = PP_ALIGN.CENTER

    # Bloque Institucional Inferior
    tb_inst = slide1.shapes.add_textbox(Inches(1.6), Inches(5.3), Inches(10.133), Inches(0.8))
    tf_inst = tb_inst.text_frame
    p_i1 = tf_inst.paragraphs[0]
    p_i1.text = "Universidad Cooperativa de Colombia  •  Facultad de Ingenierías  •  Pregrado de Ingeniería de Software"
    p_i1.font.size = Pt(11)
    p_i1.font.bold = True
    p_i1.font.color.rgb = TEXT_BODY
    p_i1.alignment = PP_ALIGN.CENTER

    p_i2 = tf_inst.add_paragraph()
    p_i2.text = "Santa Marta, Colombia  •  2026"
    p_i2.font.size = Pt(10)
    p_i2.font.color.rgb = TEXT_DIM
    p_i2.alignment = PP_ALIGN.CENTER

    # ---------------------------------------------------------------------
    # DIAPOSITIVA 2: FUNDAMENTACIÓN TEÓRICA
    # ---------------------------------------------------------------------
    slide2 = crear_slide_base(
        prs,
        "Fundamentación Teórica",
        "El Problema de la Asignación de Recursos en Sistemas Operativos",
        "La alternancia entre ráfagas de CPU-E/S y el aislamiento de memoria en entornos multiprogramados.",
        2
    )

    # Tarjeta Izquierda: CPU
    agregar_tarjeta(slide2, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.2))
    tb_c2 = slide2.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.3), Inches(4.0))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True

    p = tf_c2.paragraphs[0]
    p.text = "⚡ Planificación de CPU & Efecto Convoy"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    items_cpu = [
        ("Ciclo CPU-E/S:", " La ejecución de cualquier proceso alterna entre ráfagas de procesamiento y transferencias de entrada/salida. Desaprovechar los bloqueos degrada la utilización del procesador."),
        ("Efecto Convoy:", " En políticas no expropiativas, un proceso de cómputo largo retiene el CPU y condena a procesos breves a colas de espera desproporcionadas, inflando el TAT y RT."),
        ("Sobrecarga de Conmutación:", " Salvar y restaurar el PCB consume tiempo de CPU (costo_cs = 1 tick). Un diseño realista debe cuantificar este costo.")
    ]
    for tit, desc in items_cpu:
        p = tf_c2.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = f"• {tit}"
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = TEXT_TITLE
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(11.5)
        run2.font.color.rgb = TEXT_MUTED

    # Tarjeta Derecha: Memoria
    agregar_tarjeta(slide2, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.2))
    tb_m2 = slide2.shapes.add_textbox(Inches(7.0), Inches(2.1), Inches(5.3), Inches(4.0))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True

    p = tf_m2.paragraphs[0]
    p.text = "🧠 Gestión de Memoria & Paginación Pura"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    items_mem = [
        ("Fragmentación Externa (Eliminada):", " La asignación contigua deja huecos libres dispersos inutilizables. Con bloques de tamaño fijo (marcos/páginas), la fragmentación externa es 0 bytes."),
        ("Fragmentación Interna:", " Ocurre en el último marco asignado cuando la memoria demandada no es múltiplo de 4 KB: mem_asignada - mem_necesitada."),
        ("Traducción MMU:", " La Unidad de Manejo de Memoria desacopla la dirección virtual del marco físico en memoria RAM mediante tablas de páginas por proceso.")
    ]
    for tit, desc in items_mem:
        p = tf_m2.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = f"• {tit}"
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = TEXT_TITLE
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(11.5)
        run2.font.color.rgb = TEXT_MUTED

    # Barra Inferior de Objetivo
    agregar_tarjeta(slide2, Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.55), bg_color=RGBColor(16, 24, 40), border_color=PRIMARY)
    tb_obj = slide2.shapes.add_textbox(Inches(1.0), Inches(6.4), Inches(11.3), Inches(0.45))
    p_obj = tb_obj.text_frame.paragraphs[0]
    run_o1 = p_obj.add_run()
    run_o1.text = "🎯 Objetivo del Proyecto: "
    run_o1.font.bold = True
    run_o1.font.size = Pt(11)
    run_o1.font.color.rgb = PRIMARY
    run_o2 = p_obj.add_run()
    run_o2.text = "Construir un simulador determinista ciclo a ciclo en Python 3 que integre la planificación de CPU con la traducción MMU y políticas de reemplazo FIFO vs LRU."
    run_o2.font.size = Pt(11)
    run_o2.font.color.rgb = TEXT_BODY

    # ---------------------------------------------------------------------
    # DIAPOSITIVA 3: ARQUITECTURA DEL SIMULADOR & PCB
    # ---------------------------------------------------------------------
    slide3 = crear_slide_base(
        prs,
        "Diseño de la Solución",
        "Arquitectura Modular & Máquina de Estados del Proceso",
        "Simulador determinista de tiempo discreto ciclo a ciclo (reloj tick-by-tick).",
        3
    )

    # Tarjeta Izquierda: Máquina de Estados
    agregar_tarjeta(slide3, Inches(0.8), Inches(2.0), Inches(6.0), Inches(4.8))
    tb_est = slide3.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.6), Inches(4.6))
    tf_est = tb_est.text_frame
    tf_est.word_wrap = True

    p = tf_est.paragraphs[0]
    p.text = "🔄 Ciclo de Vida del Proceso (pcb.py)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    p = tf_est.add_paragraph()
    p.space_before = Pt(8)
    p.text = "Máquina formal estructurada en 5 estados:"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    # Estados visuales en texto
    estados_texto = [
        ("NUEVO", "Proceso creado; pendiente de admisión al sistema.", TEXT_DIM),
        ("LISTO", "En cola de espera para recibir despacho en procesador.", PRIMARY),
        ("EJECUCIÓN", "Ocupando la CPU; traduciendo referencias de memoria.", ACCENT),
        ("BLOQUEADO", "Esperando resolución de operación de E/S periférica.", DANGER),
        ("FINALIZADO", "Ráfagas concluidas; PCB archivado para métricas.", SECONDARY)
    ]
    for est, exp, col in estados_texto:
        p = tf_est.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"[{est}] "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = col
        r2 = p.add_run()
        r2.text = exp
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    p = tf_est.add_paragraph()
    p.space_before = Pt(10)
    p.text = "Atributos del PCB: PID, llegada, ráfaga CPU restante, operaciones E/S, tabla de páginas y métricas acumuladas (TAT, WT, RT, CS)."
    p.font.size = Pt(10.5)
    p.font.italic = True
    p.font.color.rgb = TEXT_DIM

    # Tarjeta Derecha: Módulos y Blindaje
    agregar_tarjeta(slide3, Inches(7.1), Inches(2.0), Inches(5.4), Inches(4.8))
    tb_mod = slide3.shapes.add_textbox(Inches(7.3), Inches(2.1), Inches(5.0), Inches(4.6))
    tf_mod = tb_mod.text_frame
    tf_mod.word_wrap = True

    p = tf_mod.paragraphs[0]
    p.text = "🧩 Organización Modular & Blindaje"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    modulos = [
        ("simulador.py", "Orquesta reloj discreto, colas y transiciones."),
        ("planificadores.py", "Implementa FCFS, SJF y Round Robin."),
        ("memoria.py", "Marcos físicos, tabla de páginas, MMU y reemplazo."),
        ("metricas.py", "Calcula TAT, WT, RT, equidad y fragmentación."),
        ("visualizador.py", "Genera diagramas de Gantt y curvas comparativas.")
    ]
    for mod, desc in modulos:
        p = tf_mod.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = f"• {mod}: "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = TEXT_TITLE
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Caja de Blindaje Hardware
    p = tf_mod.add_paragraph()
    p.space_before = Pt(12)
    p.text = "🛡️ Blindaje contra Violación de Segmento:"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = DANGER

    p = tf_mod.add_paragraph()
    p.text = "Si un proceso intenta acceder a una dirección virtual fuera de su espacio asignado, la MMU detona inmediatamente una excepción IndexError (Segmentation Fault) en lugar de recortar silenciosamente la dirección."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_BODY

    # ---------------------------------------------------------------------
    # DIAPOSITIVA 4: ALGORITMOS DE CPU COMPARADOS
    # ---------------------------------------------------------------------
    slide4 = crear_slide_base(
        prs,
        "Planificación de CPU",
        "Estrategias Comparadas: Criterios de Selección & Desempate",
        "Comparativa entre orden de llegada, duración de ráfaga y compartición temporal.",
        4
    )

    # 3 Columnas
    algoritmos = [
        ("1. FCFS", "No Expropiativo", YELLOW, [
            ("Mecanismo:", "Cola FIFO simple; atiende en estricto orden cronológico de arribo."),
            ("Desempate:", "Menor PID si coinciden en el mismo tick de llegada."),
            ("Sobrecarga:", "Mínima conmutación (N cambios de contexto en total)."),
            ("Debilidad:", "Severamente vulnerable al Efecto Convoy.")
        ]),
        ("2. SJF", "No Expropiativo", ACCENT, [
            ("Mecanismo:", "Selecciona el proceso con la ráfaga de CPU inmediata más corta."),
            ("Desempate:", "1) Menor ráfaga → 2) Menor llegada → 3) Menor PID."),
            ("Propiedad:", "Minimiza teóricamente el tiempo promedio de espera (WT)."),
            ("Debilidad:", "Riesgo de inanición para procesos de cómputo extenso.")
        ]),
        ("3. Round Robin", "Expropiativo (Quantum q)", PRIMARY, [
            ("Mecanismo:", "Asigna rodajas discretas (q). Si expira, el proceso es desalojado."),
            ("Desempate:", "Ante fin de quantum y nuevo arribo simultáneo, se encola primero al recién llegado."),
            ("Trade-off:", "Quantum pequeño eleva costo_cs; quantum grande degenera en FCFS.")
        ])
    ]

    for idx, (nombre, tipo, col, items) in enumerate(algoritmos):
        c_left = Inches(0.8 + idx * 4.0)
        agregar_tarjeta(slide4, c_left, Inches(2.0), Inches(3.7), Inches(3.9), border_color=col)
        tb_a = slide4.shapes.add_textbox(c_left + Inches(0.15), Inches(2.1), Inches(3.4), Inches(3.7))
        tf_a = tb_a.text_frame
        tf_a.word_wrap = True

        p = tf_a.paragraphs[0]
        p.text = nombre
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = TEXT_TITLE

        p_sub = tf_a.add_paragraph()
        p_sub.text = tipo
        p_sub.font.size = Pt(10.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = col

        for tit, desc in items:
            p = tf_a.add_paragraph()
            p.space_before = Pt(6)
            r1 = p.add_run()
            r1.text = f"{tit} "
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = TEXT_TITLE
            r2 = p.add_run()
            r2.text = desc
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = TEXT_MUTED

    # Fórmulas de Evaluación en Fila Inferior
    agregar_tarjeta(slide4, Inches(0.8), Inches(6.05), Inches(11.7), Inches(0.85), bg_color=RGBColor(16, 24, 40), border_color=SECONDARY)
    tb_form = slide4.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.3), Inches(0.75))
    tf_f = tb_form.text_frame
    tf_f.word_wrap = True

    p_f = tf_f.paragraphs[0]
    p_f.text = "📐 Fórmulas & Criterios Formales de Evaluación:"
    p_f.font.size = Pt(10.5)
    p_f.font.bold = True
    p_f.font.color.rgb = SECONDARY

    p_f2 = tf_f.add_paragraph()
    p_f2.text = "• TAT = T_fin - T_llegada    • WT = Ticks en LISTO    • RT = T_primer_despacho - T_llegada    • Inanición: WT/CPU >= 4.0x    • Consistencia: WT_prom == RT_prom (Sin E/S)"
    p_f2.font.size = Pt(10.5)
    p_f2.font.color.rgb = TEXT_BODY

    # ---------------------------------------------------------------------
    # DIAPOSITIVA 5: GESTIÓN DE MEMORIA & MMU
    # ---------------------------------------------------------------------
    slide5 = crear_slide_base(
        prs,
        "Gestión de Memoria",
        "Paginación Pura & Algoritmo Canónico de la MMU",
        "Unidad de Manejo de Memoria (MMU), marcos de 4 KB y políticas de reemplazo FIFO vs LRU.",
        5
    )

    # Tarjeta Izquierda: Algoritmo MMU
    agregar_tarjeta(slide5, Inches(0.8), Inches(2.0), Inches(5.9), Inches(4.8))
    tb_mmu = slide5.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.5), Inches(4.6))
    tf_mmu = tb_mmu.text_frame
    tf_mmu.word_wrap = True

    p = tf_mmu.paragraphs[0]
    p.text = "⚙️ Traducción Canónica en 4 Pasos (MMU)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    pasos = [
        ("Paso 1 (Página):", " p = dir_virtual // 4096"),
        ("Paso 2 (Desplazamiento):", " d = dir_virtual % 4096"),
        ("Paso 3 (Validación de Límites):", " Comprueba p < len(tabla). Si no se cumple → Detona IndexError (Segmentation Fault)."),
        ("Paso 4 (Dirección Física):", " dir_fisica = (id_marco * 4096) + d")
    ]
    for tit, desc in pasos:
        p = tf_mmu.add_paragraph()
        p.space_before = Pt(7)
        r1 = p.add_run()
        r1.text = tit
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = ACCENT
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Ejemplo numerico
    p = tf_mmu.add_paragraph()
    p.space_before = Pt(10)
    p.text = "Ejemplo Práctico de Simulación:"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_TITLE

    p = tf_mmu.add_paragraph()
    p.text = "• Solicitud: dir_virtual = 9500 bytes\n• Cálculo: p = 2 (9500 // 4096), d = 1308 (9500 % 4096)\n• Marco asignado: Marco #5\n• Resultado: dir_fisica = 5 * 4096 + 1308 = 21788 bytes"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_BODY

    # Tarjeta Derecha: Fragmentación y Reemplazo
    agregar_tarjeta(slide5, Inches(7.0), Inches(2.0), Inches(5.5), Inches(4.8))
    tb_frag = slide5.shapes.add_textbox(Inches(7.2), Inches(2.1), Inches(5.1), Inches(4.6))
    tf_frag = tb_frag.text_frame
    tf_frag.word_wrap = True

    p = tf_frag.paragraphs[0]
    p.text = "📦 Fragmentación & Algoritmos de Reemplazo"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    p = tf_frag.add_paragraph()
    p.space_before = Pt(6)
    r1 = p.add_run()
    r1.text = "• Fragmentación Externa: "
    r1.font.bold = True
    r1.font.size = Pt(11.5)
    r1.font.color.rgb = TEXT_TITLE
    r2 = p.add_run()
    r2.text = "0 bytes (la memoria física se asigna en bloques fijos de 4 KB)."
    r2.font.size = Pt(11)
    r2.font.color.rgb = TEXT_MUTED

    p = tf_frag.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = "• Fragmentación Interna: "
    r1.font.bold = True
    r1.font.size = Pt(11.5)
    r1.font.color.rgb = TEXT_TITLE
    r2 = p.add_run()
    r2.text = "mem_asignada - mem_necesitada (en el último marco).\n  Ej: Proceso pide 9000 B → 3 marcos (12288 B) → Desperdicio = 3288 B."
    r2.font.size = Pt(11)
    r2.font.color.rgb = TEXT_MUTED

    p = tf_frag.add_paragraph()
    p.space_before = Pt(12)
    p.text = "Políticas de Reemplazo ante Fallos:"
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_TITLE

    p = tf_frag.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = "• FIFO (First-In, First-Out): "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = YELLOW
    r2 = p.add_run()
    r2.text = "Desaloja la página cargada en el instante más antiguo. Ignora frecuencia y sufre la Anomalía de Bélády."
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = TEXT_MUTED

    p = tf_frag.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = "• LRU (Least Recently Used): "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = ACCENT
    r2 = p.add_run()
    r2.text = "Desaloja la página cuya última referencia sea la más remota en el tiempo. Fundamentado en el Principio de Localidad Temporal."
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = TEXT_MUTED

    # ---------------------------------------------------------------------
    # DIAPOSITIVA 6: ESCENARIOS EXPERIMENTALES DE PRUEBA
    # ---------------------------------------------------------------------
    slide6 = crear_slide_base(
        prs,
        "Experimentación",
        "Tres Escenarios Deterministas de Evaluación",
        "Batería de pruebas diseñada para tensionar CPU, provocar cambios de contexto y forzar reemplazos.",
        6
    )

    escenarios = [
        ("Escenario 1", "Carga Ligera con E/S", PRIMARY, [
            ("Procesos:", "4 procesos con transferencias periféricas."),
            ("P1 y P3:", "Alternan ráfagas de CPU con E/S intermedia, forzando estado BLOQUEADO."),
            ("P2 y P4:", "Procesos continuos de cómputo puro."),
            ("Memoria:", "8 marcos físicos (32 KB). Holgada, sin contención forzada."),
            ("Propósito:", "Comprobar liberación de CPU ante bloqueo y reactivación oportuna.")
        ]),
        ("Escenario 2", "Carga Mixta & Efecto Convoy", DANGER, [
            ("Proceso P1:", "Ráfaga monolítica de 20 ticks en t = 0."),
            ("P2 a P5:", "Procesos interactivos breves (1 a 3 ticks de CPU)."),
            ("Memoria:", "RAM limitada a 4 marcos (16 KB) para provocar colisiones."),
            ("Patrón:", "Cadena canónica de Silberschatz [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]."),
            ("Propósito:", "Diagnosticar Efecto Convoy y medir ventaja de LRU ante localidad.")
        ]),
        ("Escenario 3", "Alta Concurrencia & Sensibilidad", SECONDARY, [
            ("Procesos:", "8 procesos con ráfagas heterogéneas."),
            ("Barrido Quantum:", "Evaluación de Round Robin con q = 2, 4 y 8 ticks."),
            ("Sobrecarga CS:", "Comparativa costo_cs = 1 tick (real) vs costo_cs = 0 (ideal)."),
            ("Memoria:", "8 procesos compitiendo por 8 marcos físicos."),
            ("Propósito:", "Determinar el punto óptimo del quantum frente a la sobrecarga.")
        ])
    ]

    for idx, (nombre, subt, col, items) in enumerate(escenarios):
        c_left = Inches(0.8 + idx * 4.0)
        agregar_tarjeta(slide6, c_left, Inches(2.0), Inches(3.7), Inches(4.8), border_color=col)
        tb_e = slide6.shapes.add_textbox(c_left + Inches(0.15), Inches(2.1), Inches(3.4), Inches(4.6))
        tf_e = tb_e.text_frame
        tf_e.word_wrap = True

        p = tf_e.paragraphs[0]
        p.text = nombre
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = TEXT_TITLE

        p_sub = tf_e.add_paragraph()
        p_sub.text = subt
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = col

        for tit, desc in items:
            p = tf_e.add_paragraph()
            p.space_before = Pt(6)
            r1 = p.add_run()
            r1.text = f"• {tit} "
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = TEXT_TITLE
            r2 = p.add_run()
            r2.text = desc
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = TEXT_MUTED

    # ---------------------------------------------------------------------
    # DIAPOSITIVA 7: RESULTADOS OBTENIDOS & EVIDENCIA EMPÍRICA
    # ---------------------------------------------------------------------
    slide7 = crear_slide_base(
        prs,
        "Resultados Cuantitativos",
        "Evidencia Empírica: Resolución Práctica del Efecto Convoy",
        "Validación numérica y resolución práctica demostrada mediante simulación.",
        7
    )

    # Lado Izquierdo: Imagen del Diagrama de Gantt
    agregar_tarjeta(slide7, Inches(0.8), Inches(2.0), Inches(6.5), Inches(4.8))
    tb_gi = slide7.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(6.1), Inches(0.4))
    p = tb_gi.text_frame.paragraphs[0]
    p.text = "📊 Diagrama de Gantt: Escenario 2 (Round Robin q=2, cs=1)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    if os.path.exists(RUTA_GANTT_ESC2):
        slide7.shapes.add_picture(RUTA_GANTT_ESC2, Inches(1.0), Inches(2.6), width=Inches(6.1))
    
    tb_gc = slide7.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(6.1), Inches(0.9))
    tf_gc = tb_gc.text_frame
    tf_gc.word_wrap = True
    p = tf_gc.paragraphs[0]
    p.text = "Evidencia generada automáticamente por visualizador.py: El proceso monolítico P1 es desalojado preventivamente cada 2 ticks, permitiendo que P2 a P5 ejecuten casi de inmediato."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    # Lado Derecho: Metricas Reales y KPIs
    # KPI 1
    agregar_tarjeta(slide7, Inches(7.6), Inches(2.0), Inches(2.4), Inches(1.2), border_color=ACCENT)
    tb_k1 = slide7.shapes.add_textbox(Inches(7.7), Inches(2.05), Inches(2.2), Inches(1.1))
    tf_k1 = tb_k1.text_frame
    p = tf_k1.paragraphs[0]
    p.text = "-73.1% RT"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.alignment = PP_ALIGN.CENTER
    p2 = tf_k1.add_paragraph()
    p2.text = "RR (5.00) vs FCFS (18.60)"
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    # KPI 2
    agregar_tarjeta(slide7, Inches(10.15), Inches(2.0), Inches(2.35), Inches(1.2), border_color=PRIMARY)
    tb_k2 = slide7.shapes.add_textbox(Inches(10.25), Inches(2.05), Inches(2.15), Inches(1.1))
    tf_k2 = tb_k2.text_frame
    p = tf_k2.paragraphs[0]
    p.text = "46.43% Aciertos"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.alignment = PP_ALIGN.CENTER
    p2 = tf_k2.add_paragraph()
    p2.text = "LRU vs 39.29% FIFO"
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    # Tabla de Resultados Escenario 2
    agregar_tarjeta(slide7, Inches(7.6), Inches(3.4), Inches(4.9), Inches(3.4))
    tb_tbl = slide7.shapes.add_textbox(Inches(7.8), Inches(3.5), Inches(4.5), Inches(3.2))
    tf_tbl = tb_tbl.text_frame
    tf_tbl.word_wrap = True

    p = tf_tbl.paragraphs[0]
    p.text = "Métricas Reales: Escenario 2 (costo_cs = 1)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_TITLE

    filas = [
        ("FCFS", "TAT: 24.20 | WT: 18.60 | RT: 18.60", "4 CS (3 Inanición)"),
        ("SJF No Exprop.", "TAT: 23.40 | WT: 17.80 | RT: 17.80", "4 CS (0 Inanición)"),
        ("Round Robin (q=2)", "TAT: 21.20 | WT: 15.60 | RT: 5.00", "14 CS (0 Inanición)")
    ]
    for alg, met, cs in filas:
        p = tf_tbl.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {alg}\n  "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = PRIMARY if "Round" in alg else TEXT_BODY
        r2 = p.add_run()
        r2.text = f"{met}  [{cs}]"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = ACCENT if "Round" in alg else TEXT_MUTED

    p = tf_tbl.add_paragraph()
    p.space_before = Pt(8)
    p.text = "✓ Verificación Matemática: En FCFS y SJF (sin E/S), se verifica con exactitud absoluta WT_prom == RT_prom, confirmando que la sobrecarga antes del primer despacho computa en ambos tiempos."
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = TEXT_DIM

    # ---------------------------------------------------------------------
    # DIAPOSITIVA 8: CONCLUSIONES & CIERRE
    # ---------------------------------------------------------------------
    slide8 = crear_slide_base(
        prs,
        "Conclusiones del Proyecto",
        "Conclusiones & Lecciones de Ingeniería de Software",
        "Integración armónica entre la planificación de procesos y la gestión de memoria.",
        8
    )

    # Tarjeta Izquierda: Hallazgos Principales
    agregar_tarjeta(slide8, Inches(0.8), Inches(2.0), Inches(6.0), Inches(4.8))
    tb_ccl = slide8.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.6), Inches(4.6))
    tf_ccl = tb_ccl.text_frame
    tf_ccl.word_wrap = True

    p = tf_ccl.paragraphs[0]
    p.text = "💡 Hallazgos Principales de la Simulación"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    conclusiones = [
        ("Resolución del Efecto Convoy:", " Round Robin elimina la inanición estadística en procesos breves, reduciendo el tiempo de respuesta hasta en un 73.1% frente a FCFS."),
        ("Trade-off Crítico del Quantum:", " Quantums muy pequeños (q=2) disparan los cambios de contexto (18 CS en Esc. 3), mientras que quantums grandes (q=8) duplican el tiempo de respuesta inicial."),
        ("Principio de Localidad:", " LRU aventaja consistentemente a FIFO (46.43% vs 39.29% de aciertos) ante cadenas con recurrencia temporal, validando el principio formal de memoria virtual."),
        ("Consistencia Numérica Rigurosa:", " El simulador determinista ciclo a ciclo garantizó trazabilidad auditable y consistencia matemática exacta entre todas las métricas.")
    ]
    for tit, desc in conclusiones:
        p = tf_ccl.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {tit}"
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = TEXT_TITLE
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Tarjeta Derecha: Entregables y Agradecimiento
    agregar_tarjeta(slide8, Inches(7.1), Inches(2.0), Inches(5.4), Inches(4.8))
    tb_ent = slide8.shapes.add_textbox(Inches(7.3), Inches(2.1), Inches(5.0), Inches(4.6))
    tf_ent = tb_ent.text_frame
    tf_ent.word_wrap = True

    p = tf_ent.paragraphs[0]
    p.text = "📂 Entregables & Repositorio"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    entregables = [
        ("Código Fuente:", " pcb.py, planificadores.py, memoria.py, simulador.py, main.py"),
        ("Informe Técnico:", " informe_tecnico.pdf (7 páginas consolidadas)"),
        ("Revisión Preliminar:", " revision_preliminar.pdf (Normas APA 7ma ed.)"),
        ("Artefactos:", " Logs (.txt), Métricas (.csv) y Gráficos (.png)")
    ]
    for ent, arch in entregables:
        p = tf_ent.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = f"• {ent} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_TITLE
        r2 = p.add_run()
        r2.text = arch
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED

    # Repositorio
    p = tf_ent.add_paragraph()
    p.space_before = Pt(10)
    r1 = p.add_run()
    r1.text = "🔗 Repositorio Oficial: "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = PRIMARY
    r2 = p.add_run()
    r2.text = "[Link del repositorio: por agregar]"
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = TEXT_BODY

    # Bloque de Agradecimiento
    p = tf_ent.add_paragraph()
    p.space_before = Pt(14)
    p.text = "¡Muchas Gracias!"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.alignment = PP_ALIGN.CENTER

    p = tf_ent.add_paragraph()
    p.text = "Espacio abierto para preguntas del docente evaluador."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # Guardar Presentacion
    prs.save(RUTA_SALIDA_PPTX)
    print(f"[OK] Presentacion PowerPoint generada con exito en: {RUTA_SALIDA_PPTX}")

    # Copiar a artefactos
    dir_artefactos = r"C:\Users\Carlos Ibañez\.gemini\antigravity\brain\5c4c533d-4542-4431-b189-162cfbeaffb2"
    if os.path.exists(dir_artefactos):
        ruta_art = os.path.join(dir_artefactos, "presentacion_sustentacion.pptx")
        prs.save(ruta_art)
        print(f"[OK] Copia en directorio de artefactos guardada en: {ruta_art}")


if __name__ == "__main__":
    generar_presentacion_pptx()
