"""
Generador de Documento: revision_preliminar.pdf
Cumple con las normas APA 7ma edición para trabajos académicos de pregrado:
- Portada institucional limpia (sin líneas de grado)
- Fuente Times New Roman 12pt
- Interlineado doble en el cuerpo (leading=24)
- Márgenes de 1 pulgada (72 pt) en los cuatro lados
- Numeración de página en la esquina superior derecha
- Jerarquía de títulos APA 7 para las 9 secciones
- Bloque de código corto en Courier con fondo gris en Sección 4
- Repositorio o Carpeta de Trabajo con estructura en Sección 7
- Evidencia visual real (Diagrama de Gantt) en Sección 9
- Referencias en sangría francesa
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

# Rutas del proyecto
DIRECTORIO_PROYECTO = r"C:\Users\Carlos Ibañez\.gemini\antigravity\scratch\proyecto_so_cpu"
RUTA_PDF = os.path.join(DIRECTORIO_PROYECTO, "revision_preliminar.pdf")
RUTA_GANTT = os.path.join(DIRECTORIO_PROYECTO, "resultados", "graficos", "gantt_escenario2_convoy_Round_Robin_Q2_cs1.png")


class CanvasAPA7(canvas.Canvas):
    """
    Canvas personalizado para normas APA 7ma edición.
    Inserta la numeración de página en la esquina superior derecha en todas las páginas.
    Margen derecho: 72 pt (x = 612 - 72 = 540 pt)
    Margen superior: 36 pt desde el borde superior (y = 792 - 36 = 756 pt)
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
            self.saveState()
            self.setFont("Times-Roman", 12)
            # Numeración de página APA 7 en esquina superior derecha
            self.drawRightString(540, 756, str(self._pageNumber))
            self.restoreState()
            super().showPage()
        super().save()


def crear_estilos_apa():
    """Define los estilos tipográficos siguiendo estrictamente la 7ma edición de APA."""
    return {
        # Estilos de Portada
        "PortadaTitulo": ParagraphStyle(
            "PortadaTitulo",
            fontName="Times-Italic",
            fontSize=13,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=0
        ),
        "PortadaTexto": ParagraphStyle(
            "PortadaTexto",
            fontName="Times-Roman",
            fontSize=12,
            leading=20,
            alignment=TA_CENTER,
            textColor=colors.black
        ),
        "PortadaInstitucion": ParagraphStyle(
            "PortadaInstitucion",
            fontName="Times-Roman",
            fontSize=12,
            leading=19,
            alignment=TA_CENTER,
            textColor=colors.black
        ),

        # Títulos APA 7
        # Nivel 1: Centrado, Negrita, Cada Palabra con Mayúscula
        "APA_Nivel1": ParagraphStyle(
            "APA_Nivel1",
            fontName="Times-Bold",
            fontSize=12,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceBefore=12,
            spaceAfter=12,
            keepWithNext=True
        ),
        # Nivel 2: Alineado a la izquierda, Negrita, Cada Palabra con Mayúscula
        "APA_Nivel2": ParagraphStyle(
            "APA_Nivel2",
            fontName="Times-Bold",
            fontSize=12,
            leading=24,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceBefore=10,
            spaceAfter=8,
            keepWithNext=True
        ),
        # Nivel 3: Alineado a la izquierda, Negrita y Cursiva
        "APA_Nivel3": ParagraphStyle(
            "APA_Nivel3",
            fontName="Times-BoldItalic",
            fontSize=12,
            leading=24,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceBefore=8,
            spaceAfter=6,
            keepWithNext=True
        ),

        # Cuerpo del Texto: Doble espacio (leading=24), sangría de primera línea 0.5 in (36 pt)
        "APA_Cuerpo": ParagraphStyle(
            "APA_Cuerpo",
            fontName="Times-Roman",
            fontSize=12,
            leading=24,
            alignment=TA_LEFT,
            firstLineIndent=36,
            textColor=colors.black,
            spaceAfter=0
        ),
        # Cuerpo sin sangría inicial (para continuaciones o párrafos tras tablas/figuras)
        "APA_CuerpoSinSangria": ParagraphStyle(
            "APA_CuerpoSinSangria",
            fontName="Times-Roman",
            fontSize=12,
            leading=24,
            alignment=TA_LEFT,
            firstLineIndent=0,
            textColor=colors.black,
            spaceAfter=0
        ),

        # Bloque de Código Monoespaciado (Sección 4)
        "CodigoBloque": ParagraphStyle(
            "CodigoBloque",
            fontName="Courier",
            fontSize=10,
            leading=16,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1A1A1A")
        ),

        # Bloque de Estructura de Directorios (Sección 7)
        "ArbolBloque": ParagraphStyle(
            "ArbolBloque",
            fontName="Courier",
            fontSize=8,
            leading=11.5,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1A1A1A")
        ),

        # Título y Notas de Figura en APA 7
        "FiguraNumero": ParagraphStyle(
            "FiguraNumero",
            fontName="Times-Bold",
            fontSize=12,
            leading=18,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=2,
            keepWithNext=True
        ),
        "FiguraTitulo": ParagraphStyle(
            "FiguraTitulo",
            fontName="Times-Italic",
            fontSize=12,
            leading=18,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=8,
            keepWithNext=True
        ),
        "FiguraNota": ParagraphStyle(
            "FiguraNota",
            fontName="Times-Roman",
            fontSize=10,
            leading=16,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceBefore=6,
            spaceAfter=12
        ),

        # Referencias en Sangría Francesa (hanging indent: leftIndent=36, firstLineIndent=-36)
        "APA_Referencia": ParagraphStyle(
            "APA_Referencia",
            fontName="Times-Roman",
            fontSize=12,
            leading=24,
            alignment=TA_LEFT,
            leftIndent=36,
            firstLineIndent=-36,
            textColor=colors.black,
            spaceAfter=0
        )
    }


def construir_portada_tesis(estilos):
    """
    Construye la portada formal tipo tesis según las especificaciones del usuario:
    - Título en cursiva en la parte superior.
    - Integrantes por orden alfabético de apellido.
    - Docente (Mag. Sergio Luis Lubo Argumedo).
    - Sin la línea de 'Trabajo de grado...'.
    - Bloque institucional final centrado.
    """
    elementos = []
    
    # Espaciado superior inicial
    elementos.append(Spacer(1, 40))

    # Título en cursiva
    p_titulo = Paragraph(
        "<i>Gestión de Procesos y Planificación de CPU, ampliado con Gestión de Memoria</i>",
        estilos["PortadaTitulo"]
    )
    elementos.append(p_titulo)
    elementos.append(Spacer(1, 140))

    # Integrantes en orden alfabético de apellido
    p_integrantes = Paragraph(
        "Carlos Andrés Ibañez Barrios<br/>"
        "Shaadon Jiménez Flores",
        estilos["PortadaTexto"]
    )
    elementos.append(p_integrantes)
    elementos.append(Spacer(1, 110))

    # Docente evaluador
    p_docente = Paragraph(
        "Docente<br/>"
        "Mag. Sergio Luis Lubo Argumedo",
        estilos["PortadaTexto"]
    )
    elementos.append(p_docente)
    elementos.append(Spacer(1, 140))

    # Bloque institucional final centrado
    p_inst = Paragraph(
        "Universidad Cooperativa de Colombia<br/>"
        "Facultad de Ingenierías<br/>"
        "Pregrado de Ingeniería de Software<br/>"
        "Santa Marta, Colombia<br/>"
        "2026",
        estilos["PortadaInstitucion"]
    )
    elementos.append(p_inst)
    elementos.append(PageBreak())

    return elementos


def generar_documento_revision():
    """Compila el documento completo revision_preliminar.pdf."""
    # Márgenes de 1 pulgada (72 pt) en los cuatro costados
    doc = SimpleDocTemplate(
        RUTA_PDF,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    estilos = crear_estilos_apa()
    story = []

    # 1. PORTADA
    story.extend(construir_portada_tesis(estilos))

    # ANCHO ÚTIL DE PÁGINA: 612 - 72 - 72 = 468 pt
    ancho_util = 468

    # =========================================================================
    # SECCIÓN 1: DESCRIPCIÓN DEL PROBLEMA
    # =========================================================================
    story.append(Paragraph("1. Descripción del Problema", estilos["APA_Nivel1"]))
    story.append(Paragraph(
        "El tema seleccionado corresponde a la Opción 1 del proyecto final: Gestión de Procesos y Planificación de CPU, "
        "ampliada a solicitud del docente para incluir Gestión de Memoria con paginación.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "En los sistemas computacionales multiprogramados, el procesador (CPU) y la memoria principal (RAM) "
        "son los recursos físicos más restringidos y demandados por los programas en ejecución. Cuando múltiples "
        "procesos compiten por el tiempo del procesador, la ausencia de una política disciplinada de planificación "
        "provoca patologías graves en el sistema. Entre ellas destaca el denominado efecto convoy, donde un proceso "
        "con una ráfaga de cómputo extensa monopoliza el procesador y condena a múltiples procesos breves a esperas "
        "inaceptables, incrementando los tiempos de retorno y degradando la interactividad percibida por los usuarios "
        "(Silberschatz et al., 2018).",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "De manera simultánea, la asignación tradicional contigua en memoria principal genera fragmentación externa, "
        "una condición donde la memoria libre total es teóricamente suficiente para albergar un proceso, pero se encuentra "
        "dispersa en múltiples particiones pequeñas y no contiguas que impiden su asignación (Tanenbaum & Bos, 2015). "
        "Para subsanar esta debilidad, los sistemas operativos modernos recurren a la memoria virtual paginada. Sin embargo, "
        "este mecanismo traslada el problema hacia la gestión de tablas de páginas, la minimización de la fragmentación interna "
        "en los marcos de memoria y la selección de políticas óptimas de reemplazo ante fallos de página. El presente proyecto "
        "aborda la construcción y evaluación de un simulador ciclo a ciclo en Python 3 que integra ambos subsistemas para analizar "
        "cuantitativamente su desempeño.",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # SECCIÓN 2: JUSTIFICACIÓN Y FUNDAMENTACIÓN TEÓRICA
    # =========================================================================
    story.append(Paragraph("2. Justificación y Fundamentación Teórica", estilos["APA_Nivel1"]))
    story.append(Paragraph(
        "La planificación de la CPU se fundamenta en la naturaleza empírica del ciclo de ráfagas CPU-E/S, el cual "
        "establece que la ejecución de cualquier proceso consiste en una alternancia periódica entre cómputo en procesador "
        "y espera por operaciones de transferencia en periféricos (Silberschatz et al., 2018). Un planificador a corto "
        "plazo eficiente debe aprovechar los intervalos en que un proceso se bloquea por E/S para despachar a otro proceso listo, "
        "elevando el coeficiente de utilización del hardware y garantizando una asignación equitativa del procesador.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "Por su parte, la paginación pura divide el espacio de direcciones virtuales del proceso en bloques de tamaño fijo "
        "denominados páginas, mientras que la memoria física se particiona en bloques del mismo tamaño denominados marcos. "
        "La Unidad de Manejo de Memoria (MMU) efectúa la traducción dinámica de direcciones mediante una tabla de páginas, "
        "eliminando por diseño la fragmentación externa (Stallings, 2018). No obstante, cuando la memoria física es inferior "
        "a la demanda agregada de los procesos, la presencia de fallos de página exige algoritmos de reemplazo basados en el "
        "principio de localidad de referencia. El algoritmo Least Recently Used (LRU) asume que las páginas referenciadas "
        "recientemente volverán a ser utilizadas a corto plazo, aventajando al esquema elemental First-In, First-Out (FIFO), "
        "el cual desaloja páginas basándose únicamente en su orden cronológico de ingreso a la memoria física.",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # SECCIÓN 3: OBJETIVOS DEL PROYECTO
    # =========================================================================
    story.append(Paragraph("3. Objetivos del Proyecto", estilos["APA_Nivel1"]))
    story.append(Paragraph("3.1. Objetivo General", estilos["APA_Nivel2"]))
    story.append(Paragraph(
        "Diseñar, implementar y evaluar un simulador determinista de tiempo discreto ciclo a ciclo (reloj tick-by-tick) "
        "en Python 3 que integre la planificación de procesos en CPU (FCFS, SJF no expropiativo y Round Robin) y la gestión "
        "de memoria virtual con paginación pura (traducción MMU en 4 pasos, cálculo de fragmentación y reemplazo FIFO frente a LRU), "
        "analizando cuantitativamente el rendimiento, la sobrecarga por conmutación y la equidad distributiva sobre tres escenarios reproducibles.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph("3.2. Objetivos Específicos", estilos["APA_Nivel2"]))
    story.append(Paragraph(
        "1. Modelar el ciclo de vida del proceso mediante un Bloque de Control de Proceso (PCB) explícito estructurado "
        "bajo cinco estados formales: NUEVO, LISTO, EJECUCION, BLOQUEADO y FINALIZADO, con trazabilidad completa de eventos en logs auditables.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "2. Implementar el costo temporal de cambio de contexto como parámetro configurable (costo_cs = 1 tick y costo_cs = 0), "
        "asegurando consistencia matemática rigurosa entre el tiempo de espera y el tiempo de respuesta en entornos no expropiativos.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "3. Desarrollar la Unidad de Manejo de Memoria (MMU) simulada con el procedimiento estándar de 4 pasos para traducir "
        "direcciones virtuales a físicas y detectar fallos de página y violaciones de segmento (Segmentation Fault).",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "4. Evaluar empíricamente la efectividad de las políticas de reemplazo FIFO y LRU, comprobando la ventaja de LRU ante patrones "
        "con localidad temporal y analizando el fenómeno de homogeneización derivado de la rotación temporal en Round Robin.",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # SECCIÓN 4: DISEÑO GENERAL DE LA SOLUCIÓN
    # =========================================================================
    story.append(Paragraph("4. Diseño General de la Solución", estilos["APA_Nivel1"]))
    story.append(Paragraph(
        "La solución se concibe bajo una arquitectura modular de tiempo discreto en Python 3, sin dependencias externas "
        "más allá de matplotlib y pandas para la presentación tabular y gráfica. Cada avance unitario del reloj entero del simulador "
        "(t = 0, 1, 2, ...) gobierna sincrónicamente la admisión de nuevos procesos, la ejecución en procesador, la traducción "
        "de referencias de memoria y la resolución de transferencias de E/S.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "El sistema se organiza en seis módulos cohesivos: pcb.py (administra los atributos del proceso y su máquina de estados), "
        "planificadores.py (implementa la clase base intercambiable y los algoritmos FCFS, SJF y Round Robin), memoria.py (contiene "
        "la estructura de marcos físicos, tablas de páginas por proceso, MMU y estrategias FIFO y LRU), simulador.py (orquesta las colas "
        "y el reloj discreto), metricas.py (computa TAT, WT, RT, equidad y fragmentación) y visualizador.py (construye los diagramas de Gantt).",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "Durante la fase de cómputo en CPU, la MMU ejecuta en cada ciclo el procedimiento canónico de 4 pasos para resolver la "
        "dirección física correspondiente, validando estrictamente que el número de página no exceda los límites asignados al proceso:",
        estilos["APA_Cuerpo"]
    ))

    # BLOQUE DE CÓDIGO CORTO (Courier, fondo gris claro, 2-4 líneas)
    codigo_mmu = (
        "# Procedimiento canonico de traduccion en 4 pasos (MMU)\n"
        "num_pagina = dir_virtual // self.tamano_pagina\n"
        "desplazamiento = dir_virtual % self.tamano_pagina\n"
        "dir_fisica = (id_marco * self.tamano_pagina) + desplazamiento"
    )
    t_codigo = Table([[Paragraph(codigo_mmu.replace("\n", "<br/>"), estilos["CodigoBloque"])]], colWidths=[ancho_util])
    t_codigo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F3F4")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(Spacer(1, 4))
    story.append(t_codigo)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Si el número de página calculado excede el tamaño de la tabla del proceso, el sistema detona inmediatamente una "
        "excepción de violación de segmento (Segmentation Fault / IndexError) y registra el evento en el log de la MMU, emulando "
        "con precisión el comportamiento de las trampas de hardware en arquitecturas reales.",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # SECCIÓN 5: ALGORITMOS Y ESTRATEGIAS COMPARADAS
    # =========================================================================
    story.append(Paragraph("5. Algoritmos y Estrategias Comparadas", estilos["APA_Nivel1"]))
    story.append(Paragraph(
        "En el subsistema de procesador se seleccionaron tres estrategias clásicas con distintas propiedades de equidad y sobrecarga. "
        "En primer término, First-Come, First-Served (FCFS) opera como una cola FIFO no expropiativa simple, atendiendo a los procesos en "
        "estricto orden cronológico de arribo. En segundo lugar, Shortest Job First (SJF) en su variante no expropiativa selecciona en cada "
        "despacho al proceso cuya ráfaga de CPU inmediata sea la más breve, aplicando como reglas deterministas de desempate el menor tiempo "
        "de llegada y el menor identificador numérico (PID). Finalmente, Round Robin (RR) asigna la CPU en rodajas de tiempo discretas denominadas "
        "quantum (q). Si el quantum concluye antes de terminar la ráfaga, el proceso es expropiado preventivamente. Ante la concurrencia simultánea "
        "entre el vencimiento de quantum de un proceso activo y el arribo de un nuevo proceso a la cola de listos, la política adoptada "
        "posiciona primero al proceso entrante, optimizando su tiempo de respuesta inicial.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "En el subsistema de memoria se confrontan dos algoritmos de reemplazo de páginas con un tamaño de marco fijado en 4 KB (4096 bytes). "
        "El algoritmo FIFO mantiene un registro del instante de carga de cada marco y desaloja la página de mayor antigüedad temporal. En contraste, "
        "el algoritmo LRU actualiza la estampa de tiempo en cada lectura o escritura a la dirección física, seleccionando como víctima a la página "
        "cuyo acceso previo sea el más remoto en la línea de tiempo del reloj simulado.",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # SECCIÓN 6: ESCENARIOS Y MÉTRICAS DE PRUEBA
    # =========================================================================
    story.append(Paragraph("6. Escenarios y Métricas de Prueba", estilos["APA_Nivel1"]))
    story.append(Paragraph(
        "La evaluación cuantitativa se estructura en tres escenarios experimentales deterministas almacenados en la suite de pruebas. "
        "El Escenario 1 (Carga Ligera con E/S) evalúa cuatro procesos donde dos de ellos (P1 y P3) realizan operaciones de entrada y salida "
        "intermedias, forzando la transición al estado BLOQUEADO en una memoria holgada de 8 marcos (32 KB). El Escenario 2 (Carga Mixta y Efecto Convoy) "
        "introduce un proceso monolítico P1 con ráfaga de 20 ticks en t = 0 seguido por cuatro procesos cortos de 1 a 3 ticks; simultáneamente en memoria, "
        "P1 ejecuta el patrón de referencias de Silberschatz en una RAM limitada a 4 marcos (16 KB) para provocar colisiones de reemplazo. "
        "El Escenario 3 (Alta Concurrencia) involucra ocho procesos heterogéneos y evalúa la sensibilidad de Round Robin con quantum q = 2, 4 y 8 ticks, "
        "contrastando corridas con sobrecarga real (costo_cs = 1) frente a costo ideal (costo_cs = 0).",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "Las métricas computadas en cada corrida comprenden: el Tiempo de Retorno (Turnaround Time, TAT = T_fin - T_llegada), el Tiempo de Espera "
        "(Waiting Time, WT = Ticks en estado LISTO), el Tiempo de Respuesta (Response Time, RT = T_inicio - T_llegada), la Desviación Estándar de WT "
        "(métrica formal de equidad distributiva) y el indicador de inanición estadística (alertas emitidas si la razón WT/CPU supera o iguala 4.0x). "
        "En memoria se calcula la Tasa de Aciertos (Hit Rate, HR = Aciertos / Accesos * 100%), la Tasa de Fallos (Page Fault Rate, PFR = 100% - HR) y la "
        "Fragmentación Interna acumulada (memoria asignada menos memoria requerida).",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # SECCIÓN 7: REPOSITORIO O CARPETA DE TRABAJO
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("7. Repositorio o Carpeta de Trabajo", estilos["APA_Nivel1"]))
    story.append(Paragraph(
        "El código fuente completo, los scripts de automatización, las trazas de auditoría y los documentos "
        "técnicos que integran la solución se encuentran organizados bajo control de versiones. El acceso al repositorio "
        "del proyecto se encuentra disponible a través del siguiente enlace oficial: <b>[Link del repositorio: por agregar]</b>.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "La estructura interna del directorio de trabajo sigue una arquitectura modular y reproducible, diseñada "
        "para desacoplar la lógica de simulación, la gestión de memoria, las herramientas de medición y los artefactos de salida generados:",
        estilos["APA_Cuerpo"]
    ))
    story.append(Spacer(1, 4))

    arbol_carpetas = (
        "proyecto_so_cpu/\n"
        "|-- pcb.py                     # Modelo del proceso y maquina de estados (5 estados)\n"
        "|-- planificadores.py          # Politicas de CPU: FCFS, SJF y Round Robin\n"
        "|-- memoria.py                 # Paginacion, MMU (4 pasos) y reemplazo FIFO / LRU\n"
        "|-- simulador.py               # Motor determinista de simulacion ciclo a ciclo\n"
        "|-- metricas.py                # Calculo de TAT, WT, RT, equidad y fragmentacion\n"
        "|-- visualizador.py            # Generacion de graficos y diagramas de Gantt\n"
        "|-- main.py                    # Orquestador general y suite de pruebas de escenarios\n"
        "|-- generar_pdf.py             # Generador del informe tecnico formal\n"
        "|-- generar_revision_preliminar.py # Generador del presente documento de revision APA 7\n"
        "|-- informe_tecnico.pdf        # Documento del informe tecnico consolidado en PDF\n"
        "|-- README.md                  # Documentacion de arquitectura, instalacion y ejecucion\n"
        "|-- .gitignore                 # Exclusion de cache (__pycache__/) y artefactos locales\n"
        "`-- resultados/\n"
        "    |-- logs/                  # Trazas de auditoria ciclo a ciclo por escenario (.txt)\n"
        "    |-- metricas/              # Tablas de resultados consolidadas en formato CSV\n"
        "    `-- graficos/              # Diagramas de Gantt y graficas comparativas (.png)"
    )
    t_arbol = Table([[Paragraph(arbol_carpetas.replace("\n", "<br/>").replace(" ", "&nbsp;"), estilos["ArbolBloque"])]], colWidths=[ancho_util])
    t_arbol.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F3F4")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t_arbol)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Esta organización garantiza que cualquier ejecución a través de main.py regenere de forma limpia "
        "y determinista la totalidad de los datos analizados, permitiendo verificar de manera inmediata la consistencia "
        "entre los logs de eventos, las tablas métricas consolidadas y las representaciones visuales.",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # SECCIÓN 8: PLAN DE TRABAJO Y CRONOGRAMA
    # =========================================================================
    story.append(Paragraph("8. Plan de Trabajo y Cronograma", estilos["APA_Nivel1"]))
    story.append(Paragraph(
        "El desarrollo del proyecto se organizó en cinco fases secuenciales estructuradas para garantizar entregables verificables y mitigar riesgos técnicos. "
        "La Fase 1 comprendió la auditoría conceptual y diseño de la máquina de estados y PCB. La Fase 2 abarcó la implementación y verificación del motor "
        "de planificación de CPU, logrando la consistencia exacta WT == RT en entornos no expropiativos. La Fase 3 se centró en la arquitectura de memoria "
        "virtual con paginación pura y la implementación de las clases de reemplazo FIFO y LRU. La Fase 4 contempló la auditoría de no-regresión y el blindaje "
        "contra excepciones (validaciones de quantum positivo, ráfagas no nulas y detección de Segmentation Fault). Finalmente, la Fase 5 comprende la "
        "redacción del informe técnico final, compilación de gráficos y preparación de la sustentación oral.",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # SECCIÓN 9: AVANCE FUNCIONAL INICIAL O PRUEBA DE CONCEPTO
    # =========================================================================
    story.append(Paragraph("9. Avance Funcional Inicial o Prueba de Concepto", estilos["APA_Nivel1"]))
    story.append(Paragraph(
        "A la fecha de la presente entrega, el simulador se encuentra totalmente implementado y operativo a través del orquestador main.py. "
        "El sistema ejecuta con éxito la totalidad de las pruebas de CPU y memoria, generando automáticamente los registros de transiciones en texto, "
        "los archivos tabulares consolidados en formato CSV y las representaciones visuales correspondientes.",
        estilos["APA_Cuerpo"]
    ))
    story.append(Paragraph(
        "Como evidencia empírica directa de funcionamiento, la Figura 1 ilustra el Diagrama de Gantt generado por el simulador para el Escenario 2 "
        "bajo la política Round Robin con quantum q = 2 ticks y sobrecarga de cambio de contexto costo_cs = 1 tick. En el diagrama se aprecia con "
        "claridad el desalojo preventivo del proceso monolítico P1, los intervalos intercalados de sobrecarga (etiquetados como CS) y la rápida atención "
        "de los procesos interactivos breves (P2 a P5), logrando una reducción del 73.1% en el tiempo de respuesta frente al algoritmo FCFS.",
        estilos["APA_Cuerpo"]
    ))

    # EVIDENCIA VISUAL REAL (Diagrama de Gantt)
    if os.path.exists(RUTA_GANTT):
        ancho_img = ancho_util
        alto_img = 150  # Proporción aproximada 3.1:1
        story.append(Spacer(1, 6))
        story.append(KeepTogether([
            Paragraph("Figura 1", estilos["FiguraNumero"]),
            Paragraph("<i>Diagrama de Gantt del Escenario 2 bajo Planificación Round Robin (q = 2, costo_cs = 1).</i>", estilos["FiguraTitulo"]),
            Image(RUTA_GANTT, width=ancho_img, height=alto_img),
            Paragraph("<i>Nota.</i> Registro cronológico de ejecución generado automáticamente por visualizador.py en resultados/graficos/. "
                      "Evidencia la alternancia equitativa entre procesos y los ticks de penalización por cambio de contexto.", estilos["FiguraNota"])
        ]))
        story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Asimismo, las pruebas de aserción automatizadas incorporadas al final de la ejecución de main.py certificaron que en los algoritmos no "
        "expropiativos sin E/S el tiempo de espera promedio coincide exactamente con el tiempo de respuesta promedio (FCFS: WT = 18.60, RT = 18.60; "
        "SJF: WT = 17.80, RT = 17.80), y que en el módulo de memoria LRU superó a FIFO alcanzando una tasa de aciertos del 46.43% frente al 39.29% "
        "en el Escenario 2, confirmando la solidez de la prueba de concepto desarrollada.",
        estilos["APA_Cuerpo"]
    ))

    # =========================================================================
    # REFERENCIAS (APA 7MA EDICIÓN, SANGRÍA FRANCESA)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("Referencias", estilos["APA_Nivel1"]))
    story.append(Spacer(1, 8))

    referencias_apa = [
        "Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). <i>Operating system concepts</i> (10th ed.). John Wiley & Sons.",
        "Stallings, W. (2018). <i>Operating systems: Internals and design principles</i> (9th ed.). Pearson.",
        "Tanenbaum, A. S., & Bos, H. (2015). <i>Modern operating systems</i> (4th ed.). Pearson."
    ]

    for ref in referencias_apa:
        story.append(Paragraph(ref, estilos["APA_Referencia"]))
        story.append(Spacer(1, 6))

    # Compilación final
    doc.build(story, canvasmaker=CanvasAPA7)
    print(f"[OK] Documento de revision preliminar generado con exito en: {RUTA_PDF}")


if __name__ == "__main__":
    generar_documento_revision()
