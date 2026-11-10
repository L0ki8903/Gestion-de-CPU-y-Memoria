"""
Generador de Diapositivas HTML Dinamicas para Sustentacion de Proyecto de SO
Tema: Gestion de Procesos y Planificacion de CPU, ampliado con Gestion de Memoria
Universidad Cooperativa de Colombia - 2026
"""

import os
import base64

DIRECTORIO_PROYECTO = r"C:\Users\Carlos Ibañez\.gemini\antigravity\scratch\proyecto_so_cpu"
DIRECTORIO_GRAFICOS = os.path.join(DIRECTORIO_PROYECTO, "resultados", "graficos")
RUTA_SALIDA_HTML = os.path.join(DIRECTORIO_PROYECTO, "presentacion_sustentacion.html")

def obtener_imagen_base64(nombre_archivo):
    ruta = os.path.join(DIRECTORIO_GRAFICOS, nombre_archivo)
    if os.path.exists(ruta):
        with open(ruta, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

def generar_html_presentacion():
    # Cargar imagenes clave en base64
    img_gantt_rr = obtener_imagen_base64("gantt_escenario2_convoy_Round_Robin_Q2_cs1.png")
    img_comparativa_esc2 = obtener_imagen_base64("comparativa_escenario2_convoy_cs1.png")
    img_memoria_esc2 = obtener_imagen_base64("memoria_comparativa_escenario2_convoy.png")

    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sustentación: Planificación de CPU & Gestión de Memoria - UCC 2026</title>
  <style>
    :root {
      --bg: #0B1120;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border: rgba(148, 163, 184, 0.15);
      --primary: #38BDF8;
      --primary-glow: rgba(56, 189, 248, 0.25);
      --secondary: #818CF8;
      --accent: #34D399;
      --warning: #FBBF24;
      --danger: #F87171;
      --text: #F1F5F9;
      --text-muted: #94A3B8;
      --text-dim: #64748B;
      --font: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      --code-font: 'Fira Code', 'Courier New', Courier, monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      user-select: none;
    }

    /* Fondo abstracto con gradientes sutiles */
    .bg-gradient-glow {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: 
        radial-gradient(circle at 15% 20%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(129, 140, 248, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.6) 0%, transparent 100%);
      pointer-events: none;
      z-index: 0;
    }

    /* Barra Superior */
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 28px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      z-index: 10;
    }

    .logo-badge {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .badge-pill {
      background: rgba(56, 189, 248, 0.12);
      color: var(--primary);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .header-title {
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 500;
    }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-icon {
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 6px 10px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .btn-icon:hover {
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      border-color: rgba(56, 189, 248, 0.4);
    }

    /* Contenedor Principal de Diapositivas */
    main {
      flex: 1;
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      z-index: 1;
    }

    .slide {
      position: absolute;
      width: 100%;
      max-width: 1240px;
      height: calc(100vh - 140px);
      max-height: 740px;
      opacity: 0;
      transform: translateY(16px) scale(0.985);
      pointer-events: none;
      transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1), transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding-right: 6px;
    }

    .slide.active {
      opacity: 1;
      transform: translateY(0) scale(1);
      pointer-events: all;
    }

    /* Scrollbar estilizado */
    .slide::-webkit-scrollbar {
      width: 6px;
    }
    .slide::-webkit-scrollbar-thumb {
      background: rgba(148, 163, 184, 0.2);
      border-radius: 4px;
    }

    /* Tipografía de Diapositivas */
    .slide-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--primary);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 6px;
    }

    .slide-title {
      font-size: 28px;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.25;
      margin-bottom: 6px;
      background: linear-gradient(135deg, #FFFFFF 60%, #94A3B8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .slide-subtitle {
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 18px;
    }

    /* Grid y Tarjetas */
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      flex: 1;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      flex: 1;
    }

    .card {
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      transition: border-color 0.2s ease, transform 0.2s ease;
    }

    .card:hover {
      border-color: rgba(56, 189, 248, 0.35);
    }

    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }

    .card-title {
      font-size: 16px;
      font-weight: 700;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .card-body {
      color: var(--text-muted);
      font-size: 13.5px;
      line-height: 1.55;
      flex: 1;
    }

    /* Badges & Chips */
    .chip {
      display: inline-block;
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(148, 163, 184, 0.15);
      color: var(--text);
    }
    .chip.cyan { background: rgba(56, 189, 248, 0.15); color: var(--primary); border: 1px solid rgba(56, 189, 248, 0.3); }
    .chip.indigo { background: rgba(129, 140, 248, 0.15); color: var(--secondary); border: 1px solid rgba(129, 140, 248, 0.3); }
    .chip.green { background: rgba(52, 211, 153, 0.15); color: var(--accent); border: 1px solid rgba(52, 211, 153, 0.3); }
    .chip.yellow { background: rgba(251, 191, 36, 0.15); color: var(--warning); border: 1px solid rgba(251, 191, 36, 0.3); }
    .chip.red { background: rgba(248, 113, 113, 0.15); color: var(--danger); border: 1px solid rgba(248, 113, 113, 0.3); }

    /* Listas y viñetas */
    ul.feature-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    ul.feature-list li {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      font-size: 13px;
      line-height: 1.5;
      color: var(--text-muted);
    }

    ul.feature-list li strong {
      color: #FFFFFF;
    }

    .bullet-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--primary);
      margin-top: 6px;
      flex-shrink: 0;
    }

    /* Tablas elegantes */
    .styled-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 8px;
    }

    .styled-table th {
      background: rgba(15, 23, 42, 0.8);
      color: #FFFFFF;
      font-weight: 600;
      text-align: left;
      padding: 8px 10px;
      border-bottom: 1px solid var(--card-border);
    }

    .styled-table td {
      padding: 8px 10px;
      border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    }

    .styled-table tr:hover td {
      background: rgba(56, 189, 248, 0.04);
      color: var(--text);
    }

    /* Bloques de código */
    .code-block {
      background: #060B14;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 14px;
      font-family: var(--code-font);
      font-size: 12px;
      line-height: 1.55;
      color: #E2E8F0;
      overflow-x: auto;
    }

    .code-block .keyword { color: #F472B6; }
    .code-block .var { color: #38BDF8; }
    .code-block .comment { color: #64748B; font-style: italic; }
    .code-block .num { color: #FBBF24; }

    /* Tabs interactivos dentro de diapositiva */
    .tab-bar {
      display: flex;
      gap: 6px;
      margin-bottom: 14px;
      background: rgba(15, 23, 42, 0.6);
      padding: 4px;
      border-radius: 10px;
      width: fit-content;
      border: 1px solid var(--card-border);
    }

    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 7px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .tab-btn.active {
      background: var(--primary);
      color: #0B1120;
    }

    .tab-pane {
      display: none;
    }

    .tab-pane.active {
      display: block;
      animation: fadeIn 0.25s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Calculadora interactiva MMU en Slide 5 */
    .mmu-box {
      background: #060B14;
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .mmu-input-row {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .mmu-input {
      background: #1E293B;
      border: 1px solid var(--card-border);
      color: #FFFFFF;
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 13px;
      font-family: var(--code-font);
      width: 140px;
    }

    .mmu-step-card {
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 12px;
    }

    /* Contenedor de Imagenes de Graficos */
    .chart-container {
      background: #060B14;
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      max-height: 380px;
      overflow: hidden;
    }

    .chart-container img {
      max-width: 100%;
      max-height: 340px;
      object-fit: contain;
      border-radius: 6px;
    }

    /* Barra Inferior de Navegación */
    footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 28px;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      border-top: 1px solid var(--card-border);
      z-index: 10;
    }

    .nav-btn-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .nav-btn {
      background: #1E293B;
      border: 1px solid var(--card-border);
      color: #FFFFFF;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .nav-btn:hover:not(:disabled) {
      background: var(--primary);
      color: #0B1120;
      border-color: var(--primary);
    }

    .nav-btn:disabled {
      opacity: 0.35;
      cursor: not-allowed;
    }

    /* Barra de Progreso y Puntos */
    .progress-track {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: rgba(148, 163, 184, 0.25);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .dot.active {
      background: var(--primary);
      box-shadow: 0 0 10px var(--primary);
      transform: scale(1.25);
    }

    .slide-counter {
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 600;
      min-width: 85px;
      text-align: right;
    }

    /* Drawer de Notas del Presentador */
    #notes-drawer {
      position: fixed;
      bottom: 60px;
      right: 28px;
      width: 360px;
      max-height: 240px;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 12px;
      padding: 14px 16px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.6);
      transform: translateY(300px);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 50;
      font-size: 12.5px;
      line-height: 1.5;
      color: #CBD5E1;
      overflow-y: auto;
    }

    #notes-drawer.open {
      transform: translateY(0);
    }

    #notes-drawer h4 {
      color: var(--primary);
      font-size: 13px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Diapositiva Portada Especial */
    .cover-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      height: 100%;
      gap: 20px;
    }

    .cover-title {
      font-size: 38px;
      font-weight: 800;
      line-height: 1.2;
      max-width: 900px;
      background: linear-gradient(135deg, #FFFFFF 30%, #38BDF8 80%, #818CF8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .cover-authors {
      display: flex;
      gap: 24px;
      margin: 10px 0;
    }

    .author-card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 10px 18px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }

    .author-name {
      font-size: 14px;
      font-weight: 700;
      color: #FFFFFF;
    }

    .author-role {
      font-size: 11px;
      color: var(--primary);
    }

    /* Atajos en pie */
    .shortcuts-hint {
      font-size: 11px;
      color: var(--text-dim);
    }
  </style>
</head>
<body>

  <div class="bg-gradient-glow"></div>

  <!-- ENCABEZADO -->
  <header>
    <div class="logo-badge">
      <span class="badge-pill">UCC Santa Marta</span>
      <span class="header-title">Ingeniería de Software &bull; Sistemas Operativos 2026</span>
    </div>
    <div class="header-controls">
      <button class="btn-icon" onclick="toggleNotes()" title="Ver notas de apoyo para sustentación [Tecla N]">
        <span>📝</span> Notas
      </button>
      <button class="btn-icon" onclick="toggleFullscreen()" title="Pantalla completa [Tecla F]">
        <span>⛶</span> Pantalla Completa
      </button>
    </div>
  </header>

  <!-- CONTENEDOR DE DIAPOSITIVAS -->
  <main id="slides-container">

    <!-- ========================================================================= -->
    <!-- SLIDE 1: PORTADA -->
    <!-- ========================================================================= -->
    <div class="slide active" id="slide-1" data-notes="Bienvenida: Saludar al profesor Sergio Luis Lubo Argumedo. Presentar a los integrantes en orden alfabético. Enfatizar que abordamos la Opción 1: Planificación de CPU ampliada con Gestión de Memoria por paginación en un simulador determinista ciclo a ciclo.">
      <div class="cover-container">
        <span class="chip cyan" style="font-size: 12px; padding: 6px 14px;">Proyecto Final de Sistemas Operativos</span>
        
        <h1 class="cover-title">
          Gestión de Procesos y Planificación de CPU
          <span style="display: block; font-size: 26px; font-weight: 500; color: #94A3B8; margin-top: 8px;">
            ampliado con Gestión de Memoria (Paginación Pura)
          </span>
        </h1>

        <p style="color: var(--text-muted); max-width: 720px; font-size: 15px;">
          Simulador determinista de tiempo discreto ciclo a ciclo (tick-by-tick) con FCFS, SJF no expropiativo, Round Robin, MMU canónica en 4 pasos y reemplazo FIFO frente a LRU.
        </p>

        <div class="cover-authors">
          <div class="author-card">
            <span class="author-name">Carlos Andrés Ibañez Barrios</span>
            <span class="author-role">Estudiante Ponente</span>
          </div>
          <div class="author-card">
            <span class="author-name">Shaadon Jiménez Flores</span>
            <span class="author-role">Estudiante Ponente</span>
          </div>
          <div class="author-card" style="border-color: rgba(129, 140, 248, 0.4);">
            <span class="author-name">Mag. Sergio Luis Lubo Argumedo</span>
            <span class="author-role" style="color: var(--secondary);">Docente Evaluador</span>
          </div>
        </div>

        <div style="font-size: 12px; color: var(--text-dim);">
          Universidad Cooperativa de Colombia &bull; Facultad de Ingenierías &bull; 2026
        </div>

        <button class="nav-btn" style="background: var(--primary); color: #0B1120; border: none; font-size: 14px; padding: 10px 24px; margin-top: 10px;" onclick="goToSlide(1)">
          Iniciar Sustentación &rarr;
        </button>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SLIDE 2: DESCRIPCIÓN DEL PROBLEMA & FUNDAMENTACIÓN -->
    <!-- ========================================================================= -->
    <div class="slide" id="slide-2" data-notes="Explicar los dos problemas fundamentales: 1) Monopolio del procesador por ráfagas largas (Efecto Convoy) y necesidad de expropiación. 2) La memoria contigua causa fragmentación externa (huecos dispersos). La paginación la elimina fijando bloques (marcos/páginas), pero introduce fragmentación interna.">
      <div class="slide-tag">Fundamentación Teórica</div>
      <h2 class="slide-title">El Problema de la Asignación de Recursos</h2>
      <p class="slide-subtitle">La alternancia entre ráfagas de CPU-E/S y el aislamiento de memoria en sistemas multiprogramados.</p>

      <div class="grid-2">
        <!-- Tarjeta CPU -->
        <div class="card">
          <div class="card-header">
            <span class="card-title"><span>⚡</span> Planificación de CPU</span>
            <span class="chip red">Efecto Convoy</span>
          </div>
          <div class="card-body">
            <ul class="feature-list">
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Ciclo CPU-E/S:</strong> Los procesos alternan periódicamente entre ráfagas de cómputo y transferencias periféricas. Desaprovechar los bloqueos degrada la utilización.</div>
              </li>
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Efecto Convoy:</strong> Un proceso con una ráfaga masiva retiene la CPU, forzando a procesos breves a colas de espera desproporcionadas en algoritmos no expropiativos.</div>
              </li>
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Sobrecarga de Conmutación:</strong> Salvar y restaurar el estado del procesador (PCB) consume tiempo real de cómputo (<code>costo_cs</code>).</div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Tarjeta Memoria -->
        <div class="card">
          <div class="card-header">
            <span class="card-title"><span>🧠</span> Gestión de Memoria</span>
            <span class="chip yellow">Paginación Pura</span>
          </div>
          <div class="card-body">
            <ul class="feature-list">
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Fragmentación Externa (Eliminada):</strong> La asignación contigua deja memoria libre dispersa en huecos inutilizables. En paginación la fragmentación externa es <strong>0 bytes</strong>.</div>
              </li>
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Fragmentación Interna:</strong> Ocurre en la última página asignada si la memoria solicitada no es múltiplo exacto de 4 KB: <code>mem_asignada - mem_necesitada</code>.</div>
              </li>
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Traducción MMU:</strong> La Unidad de Manejo de Memoria desacopla la dirección virtual del marco físico en memoria RAM.</div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top: 14px; padding: 12px 18px; background: rgba(56, 189, 248, 0.05); border-color: rgba(56, 189, 248, 0.25);">
        <div style="font-size: 13px; color: var(--text);">
          <strong style="color: var(--primary);">Objetivo del Proyecto:</strong> Diseñar un simulador determinista de tiempo discreto en Python 3 que articule la planificación de procesos con la traducción dinámica de páginas y reemplazo FIFO vs LRU.
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SLIDE 3: ARQUITECTURA DEL SIMULADOR & PCB -->
    <!-- ========================================================================= -->
    <div class="slide" id="slide-3" data-notes="Destacar el diseño del simulador: Reloj entero discreto t=0,1,2... PCB con 5 estados formales. Manejo determinista de costo_cs. Detección rigurosa de Segmentation Fault (IndexError) si se intenta acceder a una página no válida.">
      <div class="slide-tag">Diseño de la Solución</div>
      <h2 class="slide-title">Arquitectura Modular & Máquina de Estados</h2>
      <p class="slide-subtitle">Simulador determinista de tiempo discreto ciclo a ciclo (reloj tick-by-tick).</p>

      <div class="grid-2">
        <!-- Ciclo de Vida del PCB -->
        <div class="card">
          <div class="card-header">
            <span class="card-title"><span>🔄</span> Máquina de 5 Estados del PCB</span>
            <span class="chip cyan">pcb.py</span>
          </div>
          <div class="card-body">
            <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px;">
              <div style="display: flex; gap: 8px; align-items: center; justify-content: space-between;">
                <span class="chip" style="background: rgba(148,163,184,0.2);">NUEVO</span>
                <span style="font-size: 11px; color: var(--text-dim);">&rarr; admisión &rarr;</span>
                <span class="chip cyan">LISTO</span>
                <span style="font-size: 11px; color: var(--text-dim);">&harr; despacho / expropiación &harr;</span>
                <span class="chip green">EJECUCIÓN</span>
              </div>
              <div style="display: flex; gap: 8px; align-items: center; justify-content: center; margin: 4px 0;">
                <span style="font-size: 11px; color: var(--danger);">&uarr; E/S terminada</span>
                <span class="chip red" style="margin: 0 16px;">BLOQUEADO</span>
                <span style="font-size: 11px; color: var(--warning);">&larr; solicita E/S</span>
              </div>
              <div style="text-align: right;">
                <span style="font-size: 11px; color: var(--text-dim);">&rarr; ráfaga completada &rarr;</span>
                <span class="chip" style="background: rgba(52,211,153,0.2); color: var(--accent); font-weight: 700;">FINALIZADO</span>
              </div>
            </div>
            <p style="font-size: 12.5px; color: var(--text-muted);">
              Cada proceso encapsula PID, llegada, ráfagas restantes de CPU y E/S, tabla de páginas, y métricas acumuladas (TAT, WT, RT).
            </p>
          </div>
        </div>

        <!-- Módulos del Sistema -->
        <div class="card">
          <div class="card-header">
            <span class="card-title"><span>🧩</span> Cohesión Modular</span>
            <span class="chip indigo">Arquitectura</span>
          </div>
          <div class="card-body">
            <table class="styled-table">
              <tr>
                <th>Módulo</th>
                <th>Responsabilidad Principal</th>
              </tr>
              <tr>
                <td><code>simulador.py</code></td>
                <td>Orquestación del reloj discreto, colas y transiciones.</td>
              </tr>
              <tr>
                <td><code>planificadores.py</code></td>
                <td>Políticas de CPU: FCFS, SJF no expropiativo, Round Robin.</td>
              </tr>
              <tr>
                <td><code>memoria.py</code></td>
                <td>Marcos físicos, tabla de páginas, MMU y reemplazos.</td>
              </tr>
              <tr>
                <td><code>metricas.py</code></td>
                <td>Cálculo de TAT, WT, RT, equidad y fragmentación.</td>
              </tr>
              <tr>
                <td><code>visualizador.py</code></td>
                <td>Generación automática de diagramas de Gantt y curvas.</td>
              </tr>
            </table>
          </div>
        </div>
      </div>

      <!-- Blindaje contra fallos -->
      <div class="card" style="margin-top: 14px; padding: 12px 18px; border-color: rgba(248, 113, 113, 0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="font-size: 13px;">
            <strong style="color: var(--danger);">🛡️ Blindaje y Robustez:</strong> Si un proceso referencia una página inexistente, la MMU detona un <code>IndexError</code> emulando una <em>Violación de Segmento (Segmentation Fault)</em> en lugar de un recorte silencioso.
          </div>
          <span class="chip red">Excepción Hardware</span>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SLIDE 4: ALGORITMOS DE CPU COMPARADOS -->
    <!-- ========================================================================= -->
    <div class="slide" id="slide-4" data-notes="Explicar las tres políticas: FCFS (orden de arribo), SJF (menor ráfaga, con desempate determinista por llegada y PID), y Round Robin (con quantum y regla de desempate priorizando al proceso entrante). Mencionar la fórmula de inanición WT/CPU >= 4.0x.">
      <div class="slide-tag">Planificación de CPU</div>
      <h2 class="slide-title">Estrategias de Selección & Criterios de Desempate</h2>
      <p class="slide-subtitle">Comparativa entre orden de llegada, duración de ráfaga y compartición temporal.</p>

      <!-- Tabs de Algoritmos -->
      <div class="tab-bar">
        <button class="tab-btn active" onclick="switchCpuTab('tab-fcfs', this)">1. FCFS</button>
        <button class="tab-btn" onclick="switchCpuTab('tab-sjf', this)">2. SJF No Expropiativo</button>
        <button class="tab-btn" onclick="switchCpuTab('tab-rr', this)">3. Round Robin (RR)</button>
        <button class="tab-btn" onclick="switchCpuTab('tab-formulas', this)">📐 Fórmulas de Evaluación</button>
      </div>

      <!-- Tab FCFS -->
      <div id="tab-fcfs" class="tab-pane active">
        <div class="grid-2">
          <div class="card">
            <div class="card-header">
              <span class="card-title">First-Come, First-Served</span>
              <span class="chip yellow">No Expropiativo</span>
            </div>
            <div class="card-body">
              <ul class="feature-list">
                <li><div class="bullet-dot"></div><div><strong>Mecanismo:</strong> Atiende los procesos en estricto orden cronológico de arribo a la cola de listos (FIFO pura).</div></li>
                <li><div class="bullet-dot"></div><div><strong>Desempate:</strong> Si dos procesos arriban en el mismo tick, se desempata por menor PID numérico.</div></li>
                <li><div class="bullet-dot"></div><div><strong>Sobrecarga:</strong> Mínima cantidad de cambios de contexto (N cambios en total).</div></li>
                <li><div class="bullet-dot"></div><div><strong>Debilidad:</strong> Severamente propenso al efecto convoy ante procesos pesados iniciales.</div></li>
              </ul>
            </div>
          </div>
          <div class="card">
            <div class="card-header"><span class="card-title">Comportamiento en Simulación</span></div>
            <div class="card-body">
              <div class="code-block">
<span class="comment"># Regla de despacho FCFS</span>
<span class="keyword">def</span> <span class="var">seleccionar_siguiente</span>(self, cola_listos):
    <span class="keyword">return</span> cola_listos[<span class="num">0</span>]  <span class="comment"># Cabeza de la cola</span>
              </div>
              <p style="margin-top: 10px; font-size: 12.5px;">Sin expropiación, el proceso activo corre hasta agotar su ráfaga completa o bloquearse por solicitud de E/S.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab SJF -->
      <div id="tab-sjf" class="tab-pane">
        <div class="grid-2">
          <div class="card">
            <div class="card-header">
              <span class="card-title">Shortest Job First (SJF)</span>
              <span class="chip green">No Expropiativo</span>
            </div>
            <div class="card-body">
              <ul class="feature-list">
                <li><div class="bullet-dot"></div><div><strong>Mecanismo:</strong> Selecciona de la cola de listos al proceso con la ráfaga de CPU inmediata más corta.</div></li>
                <li><div class="bullet-dot"></div><div><strong>Desempate Jerárquico:</strong> 1) Menor duración de ráfaga &rarr; 2) Menor tiempo de llegada &rarr; 3) Menor PID.</div></li>
                <li><div class="bullet-dot"></div><div><strong>Propiedad:</strong> Minimiza teóricamente el tiempo promedio de espera (WT promedio).</div></li>
                <li><div class="bullet-dot"></div><div><strong>Debilidad:</strong> Riesgo de inanición para procesos de cómputo largo si ingresan continuamente trabajos cortos.</div></li>
              </ul>
            </div>
          </div>
          <div class="card">
            <div class="card-header"><span class="card-title">Criterio Determinista</span></div>
            <div class="card-body">
              <div class="code-block">
<span class="comment"># Criterio determinista SJF</span>
cola_listos.sort(key=<span class="keyword">lambda</span> p: (
    p.rafaga_cpu_actual,
    p.tiempo_llegada,
    p.pid
))
              </div>
              <p style="margin-top: 10px; font-size: 12.5px;">Garantiza reproducibilidad absoluta en cada corrida de simulación.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab RR -->
      <div id="tab-rr" class="tab-pane">
        <div class="grid-2">
          <div class="card">
            <div class="card-header">
              <span class="card-title">Round Robin (RR)</span>
              <span class="chip cyan">Expropiativo (Quantum q)</span>
            </div>
            <div class="card-body">
              <ul class="feature-list">
                <li><div class="bullet-dot"></div><div><strong>Mecanismo:</strong> Cada proceso recibe una rodaja fija de CPU (q). Si expira, es desalojado preventivamente.</div></li>
                <li><div class="bullet-dot"></div><div><strong>Desempate Crítico:</strong> Si un proceso agota su quantum en el mismo instante en que arriba un nuevo proceso, <strong>se inserta primero el nuevo proceso</strong>, favoreciendo el tiempo de respuesta inicial.</div></li>
                <li><div class="bullet-dot"></div><div><strong>Trade-off:</strong> Quantum muy pequeño dispara el costo de conmutación (<code>costo_cs</code>); quantum muy grande degenera en FCFS.</div></li>
              </ul>
            </div>
          </div>
          <div class="card">
            <div class="card-header"><span class="card-title">Control de Quantum</span></div>
            <div class="card-body">
              <div class="code-block">
<span class="comment"># Vencimiento de Quantum en simulador</span>
<span class="keyword">if</span> ticks_quantum == self.quantum:
    proceso.cambiar_estado(Estado.LISTO)
    self.cola_listos.append(proceso)
    self.aplicar_overhead_cs()
              </div>
              <p style="margin-top: 10px; font-size: 12.5px;">Inyecta el tick de overhead configurable en la línea de tiempo.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Formulas -->
      <div id="tab-formulas" class="tab-pane">
        <div class="grid-3">
          <div class="card">
            <div class="card-header"><span class="card-title">Tiempos</span></div>
            <div class="card-body">
              <p><strong>Turnaround (TAT):</strong></p>
              <div class="code-block" style="margin: 6px 0;">TAT = T_fin - T_llegada</div>
              <p style="margin-top: 8px;"><strong>Waiting Time (WT):</strong></p>
              <div class="code-block" style="margin: 6px 0;">WT = Ticks en estado LISTO</div>
              <p style="margin-top: 8px;"><strong>Response Time (RT):</strong></p>
              <div class="code-block" style="margin: 6px 0;">RT = T_primer_despacho - T_llegada</div>
            </div>
          </div>
          <div class="card">
            <div class="card-header"><span class="card-title">Equidad & Inanición</span></div>
            <div class="card-body">
              <p><strong>Desviación Estándar de WT:</strong></p>
              <div class="code-block" style="margin: 6px 0;">σ_WT = sqrt(Σ(WT_i - μ)^2 / N)</div>
              <p style="margin-top: 8px;"><strong>Criterio de Inanición:</strong></p>
              <div class="code-block" style="margin: 6px 0;">Alerta si: WT_i / CPU_i >= 4.0x</div>
            </div>
          </div>
          <div class="card">
            <div class="card-header"><span class="card-title">Consistencia</span></div>
            <div class="card-body">
              <p><strong>Ley Matemática No Expropiativa:</strong></p>
              <div class="code-block" style="margin: 6px 0; color: var(--accent);">WT_prom == RT_prom (Sin E/S)</div>
              <p style="font-size: 12px; margin-top: 8px;">
                Cualquier overhead de conmutación antes del primer despacho computa en ambos tiempos con idéntico impacto.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SLIDE 5: GESTIÓN DE MEMORIA & CALCULADORA MMU -->
    <!-- ========================================================================= -->
    <div class="slide" id="slide-5" data-notes="Mostrar la MMU en 4 pasos y la calculadora interactiva en vivo: cambiar el valor de la dirección virtual (ej. 8500) para mostrar cómo calcula página 2, offset 308, y dirección física en marco. Explicar FIFO vs LRU (localidad temporal) y fragmentación interna.">
      <div class="slide-tag">Gestión de Memoria</div>
      <h2 class="slide-title">Paginación Pura & Traducción Canónica en 4 Pasos</h2>
      <p class="slide-subtitle">Unidad de Manejo de Memoria (MMU), marcos de 4 KB y políticas FIFO vs LRU.</p>

      <div class="grid-2">
        <!-- Procedimiento Canónico MMU -->
        <div class="card">
          <div class="card-header">
            <span class="card-title"><span>⚙️</span> Algoritmo Canónico de la MMU</span>
            <span class="chip cyan">4 Pasos</span>
          </div>
          <div class="card-body">
            <ol style="padding-left: 18px; display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
              <li><strong>Número de página:</strong> <code>p = dir_virtual // 4096</code></li>
              <li><strong>Desplazamiento (offset):</strong> <code>d = dir_virtual % 4096</code></li>
              <li><strong>Validación de límites:</strong> Comprueba <code>p < len(tabla)</code>. Si no &rarr; <span class="chip red" style="font-size: 10px;">Segmentation Fault</span></li>
              <li><strong>Dirección física:</strong> <code>dir_fisica = (marco * 4096) + d</code></li>
            </ol>

            <div style="margin-top: 14px; padding: 10px; background: rgba(15,23,42,0.6); border-radius: 8px; border: 1px solid var(--card-border);">
              <div style="font-size: 12px; color: var(--text);">
                <strong>Fragmentación Interna:</strong> <code>mem_asignada - mem_necesitada</code>.<br/>
                <span style="color: var(--text-dim);">Ejemplo: Proceso pide 9000 bytes &rarr; Ocupa 3 marcos (12288 bytes) &rarr; Desperdicio = 3288 bytes.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Calculadora MMU Interactiva en Vivo -->
        <div class="card" style="border-color: rgba(56, 189, 248, 0.4);">
          <div class="card-header">
            <span class="card-title"><span>💻</span> Demostración Interactiva de la MMU</span>
            <span class="chip green">En Vivo</span>
          </div>
          <div class="card-body">
            <div class="mmu-box">
              <div class="mmu-input-row">
                <label style="font-size: 12px; color: var(--text-muted);">Dirección Virtual:</label>
                <input type="number" id="mmu-virtual-input" class="mmu-input" value="9500" min="0" max="32767" oninput="calcularMmuLive()">
                <span class="chip" style="font-size: 11px;">bytes</span>
              </div>

              <div class="mmu-step-card" id="mmu-res-p">Paso 1 (Página): <strong>p = 2</strong> (9500 // 4096)</div>
              <div class="mmu-step-card" id="mmu-res-d">Paso 2 (Desplazamiento): <strong>d = 1308</strong> (9500 % 4096)</div>
              <div class="mmu-step-card" id="mmu-res-v">Paso 3 (Validación): <strong style="color: var(--accent);">Válida (Marco asignado #5)</strong></div>
              <div class="mmu-step-card" style="background: rgba(56, 189, 248, 0.15); border-color: rgba(56, 189, 248, 0.4);" id="mmu-res-f">
                Paso 4 (Dirección Física): <strong style="color: var(--primary);">21788</strong> (5 &times; 4096 + 1308)
              </div>
            </div>

            <p style="font-size: 11.5px; color: var(--text-dim); margin-top: 8px;">
              *Ingresa valores mayores a 16384 para probar la detección de fallo de límites.
            </p>
          </div>
        </div>
      </div>

      <!-- Comparativa FIFO vs LRU -->
      <div class="grid-2" style="margin-top: 14px;">
        <div class="card" style="padding: 12px 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">FIFO (First-In, First-Out)</div>
          <p style="font-size: 12px; color: var(--text-muted);">Desaloja la página cargada en el instante más antiguo. Ignora si es frecuentemente accedida. Sufre la Anomalía de Bélády.</p>
        </div>
        <div class="card" style="padding: 12px 16px; border-color: rgba(52, 211, 153, 0.3);">
          <div style="font-size: 13px; font-weight: 700; color: var(--accent); margin-bottom: 4px;">LRU (Least Recently Used)</div>
          <p style="font-size: 12px; color: var(--text-muted);">Desaloja la página cuya última referencia sea la más remota. Se fundamenta en el <strong>Principio de Localidad Temporal</strong>.</p>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SLIDE 6: ESCENARIOS EXPERIMENTALES DE PRUEBA -->
    <!-- ========================================================================= -->
    <div class="slide" id="slide-6" data-notes="Presentar los 3 escenarios: Escenario 1 (E/S y bloqueo), Escenario 2 (Efecto convoy con P1 de 20 ticks + patrón de memoria de Silberschatz en 4 marcos), y Escenario 3 (Sensibilidad de quantum q=2, 4, 8 con costo_cs=1 vs 0).">
      <div class="slide-tag">Experimentación</div>
      <h2 class="slide-title">Tres Escenarios Experimentales Deterministas</h2>
      <p class="slide-subtitle">Diseñados para tensionar el procesador y forzar reemplazos en memoria RAM.</p>

      <div class="grid-3">
        <!-- Escenario 1 -->
        <div class="card">
          <div class="card-header">
            <span class="card-title">Escenario 1</span>
            <span class="chip cyan">Carga Ligera</span>
          </div>
          <div class="card-body">
            <p style="font-size: 12.5px; color: var(--text); margin-bottom: 8px;"><strong>4 Procesos con E/S intercalada:</strong></p>
            <ul class="feature-list" style="font-size: 12px;">
              <li><div class="bullet-dot"></div><div><strong>P1:</strong> CPU=3, E/S=2, CPU=2.</div></li>
              <li><div class="bullet-dot"></div><div><strong>P2:</strong> CPU=4 puro.</div></li>
              <li><div class="bullet-dot"></div><div><strong>P3:</strong> CPU=1, E/S=3, CPU=2.</div></li>
              <li><div class="bullet-dot"></div><div><strong>P4:</strong> CPU=2 puro.</div></li>
            </ul>
            <div style="margin-top: 10px; padding: 8px; background: rgba(15,23,42,0.6); border-radius: 6px; font-size: 11.5px;">
              <strong>Memoria:</strong> 8 marcos (32 KB). Holgada, sin contención forzada.
            </div>
          </div>
        </div>

        <!-- Escenario 2 -->
        <div class="card" style="border-color: rgba(248, 113, 113, 0.4);">
          <div class="card-header">
            <span class="card-title">Escenario 2</span>
            <span class="chip red">Efecto Convoy</span>
          </div>
          <div class="card-body">
            <p style="font-size: 12.5px; color: var(--text); margin-bottom: 8px;"><strong>Proceso Monolítico vs Cortos:</strong></p>
            <ul class="feature-list" style="font-size: 12px;">
              <li><div class="bullet-dot"></div><div><strong>P1:</strong> CPU=20 ticks (arriba en t=0).</div></li>
              <li><div class="bullet-dot"></div><div><strong>P2 a P5:</strong> CPU corta (1 a 3 ticks).</div></li>
              <li><div class="bullet-dot"></div><div><strong>Patrón Memoria:</strong> Cadena canónica de Silberschatz: <code>[7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]</code>.</div></li>
            </ul>
            <div style="margin-top: 10px; padding: 8px; background: rgba(248,113,113,0.1); border-radius: 6px; font-size: 11.5px; color: var(--danger);">
              <strong>Memoria:</strong> RAM limitada a 4 marcos (16 KB) para provocar colisiones continuas.
            </div>
          </div>
        </div>

        <!-- Escenario 3 -->
        <div class="card">
          <div class="card-header">
            <span class="card-title">Escenario 3</span>
            <span class="chip indigo">Sensibilidad Quantum</span>
          </div>
          <div class="card-body">
            <p style="font-size: 12.5px; color: var(--text); margin-bottom: 8px;"><strong>8 Procesos Heterogéneos:</strong></p>
            <ul class="feature-list" style="font-size: 12px;">
              <li><div class="bullet-dot"></div><div><strong>Barrido de Quantum:</strong> Evaluado con q = 2, 4, 8 ticks.</div></li>
              <li><div class="bullet-dot"></div><div><strong>Comparativa de Sobrecarga:</strong> <code>costo_cs = 1</code> (real) frente a <code>costo_cs = 0</code> (ideal).</div></li>
              <li><div class="bullet-dot"></div><div><strong>Tráfico de Memoria:</strong> 8 procesos compitiendo por 8 marcos físicos.</div></li>
            </ul>
            <div style="margin-top: 10px; padding: 8px; background: rgba(129,140,248,0.1); border-radius: 6px; font-size: 11.5px; color: var(--secondary);">
              Permite aislar matemáticamente el costo de la expropiación.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SLIDE 7: RESULTADOS OBTENIDOS & EVIDENCIA EMPÍRICA -->
    <!-- ========================================================================= -->
    <div class="slide" id="slide-7" data-notes="Esta es la diapositiva central de resultados: Mostrar el Gantt del Escenario 2, donde Round Robin desaloja a P1 y permite que P2-P5 respondan de inmediato (reducción del 73.1% en Response Time). Señalar la victoria de LRU (46.4% aciertos vs 39.3% de FIFO) por localidad temporal.">
      <div class="slide-tag">Resultados Cuantitativos</div>
      <h2 class="slide-title">Evidencia Empírica de Simulación</h2>
      <p class="slide-subtitle">Validación numérica y resolución práctica del Efecto Convoy.</p>

      <div class="grid-2">
        <!-- Gantt Visual Real -->
        <div class="card">
          <div class="card-header">
            <span class="card-title"><span>📊</span> Diagrama de Gantt: Escenario 2 (Round Robin q=2, cs=1)</span>
            <span class="chip green">Generado por visualizador.py</span>
          </div>
          <div class="chart-container">
            __IMG_GANTT_TAG__
          </div>
          <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 8px;">
            El proceso monolítico P1 es desalojado en rodajas de 2 ticks. P2 a P5 ingresan de inmediato al procesador.
          </p>
        </div>

        <!-- Métricas Clave y Comparativa Memoria -->
        <div style="display: flex; flex-direction: column; gap: 14px;">
          <!-- 3 Tarjetas de Impacto -->
          <div class="grid-2">
            <div class="card" style="padding: 12px; border-color: rgba(52, 211, 153, 0.4);">
              <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Reducción Response Time</div>
              <div style="font-size: 26px; font-weight: 800; color: var(--accent); margin: 4px 0;">-73.1%</div>
              <div style="font-size: 11px; color: var(--text-dim);">RR (5.00) vs FCFS (18.60)</div>
            </div>

            <div class="card" style="padding: 12px; border-color: rgba(56, 189, 248, 0.4);">
              <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted);">Superioridad de LRU</div>
              <div style="font-size: 26px; font-weight: 800; color: var(--primary); margin: 4px 0;">46.43%</div>
              <div style="font-size: 11px; color: var(--text-dim);">Aciertos LRU vs 39.29% FIFO</div>
            </div>
          </div>

          <!-- Tabla de Resultados Reales del Escenario 2 -->
          <div class="card">
            <div class="card-header">
              <span class="card-title" style="font-size: 14px;">Métricas Reales: Escenario 2 (Convoy)</span>
              <span class="chip cyan">costo_cs = 1</span>
            </div>
            <table class="styled-table">
              <tr>
                <th>Algoritmo</th>
                <th>TAT Prom</th>
                <th>WT Prom</th>
                <th>RT Prom</th>
                <th>Cambios Contexto</th>
              </tr>
              <tr>
                <td><strong>FCFS</strong></td>
                <td>24.20</td>
                <td>18.60</td>
                <td>18.60</td>
                <td>4 (Inanición en P2,P3,P5)</td>
              </tr>
              <tr>
                <td><strong>SJF</strong></td>
                <td>23.40</td>
                <td>17.80</td>
                <td>17.80</td>
                <td>4</td>
              </tr>
              <tr style="background: rgba(56, 189, 248, 0.08);">
                <td><strong>Round Robin (q=2)</strong></td>
                <td>21.20</td>
                <td>15.60</td>
                <td style="color: var(--accent); font-weight: 700;">5.00</td>
                <td>14 (0 Inanición)</td>
              </tr>
            </table>
            <p style="font-size: 11px; color: var(--text-dim); margin-top: 8px;">
              *Verificado: En FCFS y SJF (sin E/S), se cumple exactamente la identidad matemática <code>WT_prom == RT_prom</code>.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- SLIDE 8: CONCLUSIONES & CIERRE -->
    <!-- ========================================================================= -->
    <div class="slide" id="slide-8" data-notes="Cierre de la sustentación: Destacar los 4 aportes principales: 1) Solución del convoy mediante RR. 2) Compromiso entre interactividad y sobrecarga (costo_cs). 3) Ventaja de LRU fundamentada en la localidad temporal. 4) Software auditable y reproducible. Invitar a preguntas.">
      <div class="slide-tag">Conclusiones del Proyecto</div>
      <h2 class="slide-title">Conclusiones & Lecciones de Ingeniería</h2>
      <p class="slide-subtitle">Integración armónica entre la planificación de CPU y la paginación de memoria.</p>

      <div class="grid-2">
        <div class="card">
          <div class="card-header"><span class="card-title"><span>💡</span> Hallazgos Principales</span></div>
          <div class="card-body">
            <ul class="feature-list">
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Resolución del Convoy:</strong> Round Robin elimina la inanición estadística en procesos cortos y reduce el tiempo de respuesta hasta en un <strong>73.1%</strong> frente a FCFS.</div>
              </li>
              <li>
                <div class="bullet-dot"></div>
                <div><strong>El Trade-off del Quantum:</strong> Quantums muy pequeños (q=2) disparan los cambios de contexto (18 CS en Escenario 3), mientras que quantums grandes (q=8) duplican el tiempo de respuesta.</div>
              </li>
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Localidad de Referencia:</strong> LRU aventaja consistentemente a FIFO ante patrones con repetición temporal, confirmando las predicciones de la literatura formal.</div>
              </li>
              <li>
                <div class="bullet-dot"></div>
                <div><strong>Consistencia Numérica:</strong> La auditoría determinista ciclo a ciclo certificó la rigurosidad matemática en todas las transiciones del PCB.</div>
              </li>
            </ul>
          </div>
        </div>

        <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div class="card-header"><span class="card-title"><span>📂</span> Entregables & Repositorio</span></div>
            <div class="card-body">
              <table class="styled-table">
                <tr><td>Código Fuente</td><td><code>main.py</code>, <code>pcb.py</code>, <code>planificadores.py</code>, <code>memoria.py</code>, <code>simulador.py</code></td></tr>
                <tr><td>Informe Técnico</td><td><code>informe_tecnico.pdf</code> (7 páginas consolidadas)</td></tr>
                <tr><td>Revisión Preliminar</td><td><code>revision_preliminar.pdf</code> (Formato APA 7ma ed.)</td></tr>
                <tr><td>Artefactos</td><td>Logs (.txt), Métricas (.csv) y Gráficos (.png)</td></tr>
              </table>
              <div style="margin-top: 14px; padding: 10px; background: rgba(56, 189, 248, 0.08); border-radius: 8px; border: 1px dashed rgba(56, 189, 248, 0.3);">
                <span style="font-size: 12px; color: var(--primary);"><strong>Repositorio Oficial:</strong> [Link del repositorio: por agregar]</span>
              </div>
            </div>
          </div>

          <div style="text-align: center; padding: 16px; background: rgba(30, 41, 59, 0.4); border-radius: 10px; margin-top: 10px;">
            <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">¡Muchas Gracias!</div>
            <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">Espacio abierto para preguntas del jurado docente.</div>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- DRAWER DE NOTAS DEL PRESENTADOR (ACCESIBLE CON 'N') -->
  <div id="notes-drawer">
    <h4>
      <span>Notas de Sustentación</span>
      <button onclick="toggleNotes()" style="background:none; border:none; color:var(--text-dim); cursor:pointer; font-size:14px;">✕</button>
    </h4>
    <p id="notes-text">Notas para el ponente...</p>
  </div>

  <!-- PIE DE PÁGINA / CONTROLES -->
  <footer>
    <div class="nav-btn-group">
      <button class="nav-btn" id="btn-prev" onclick="prevSlide()">
        <span>&larr;</span> Anterior
      </button>
      <button class="nav-btn" id="btn-next" onclick="nextSlide()">
        Siguiente <span>&rarr;</span>
      </button>
      <span class="shortcuts-hint" style="margin-left: 10px;">(Teclas: &larr; / &rarr; / Espacio / F: Pantalla Completa / N: Notas)</span>
    </div>

    <!-- Barra de Puntos -->
    <div class="progress-track" id="dots-container"></div>

    <div class="slide-counter" id="slide-counter">Diapositiva 1 / 8</div>
  </footer>

  <!-- SCRIPT DE NAVEGACIÓN Y DINAMISMO -->
  <script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    const dotsContainer = document.getElementById('dots-container');
    const counterEl = document.getElementById('slide-counter');
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const notesText = document.getElementById('notes-text');
    const notesDrawer = document.getElementById('notes-drawer');

    // Inicializar Dots de navegación
    slides.forEach((_, idx) => {
      const dot = document.createElement('div');
      dot.className = `dot ${idx === 0 ? 'active' : ''}`;
      dot.title = `Ir a diapositiva ${idx + 1}`;
      dot.onclick = () => goToSlide(idx);
      dotsContainer.appendChild(dot);
    });

    function updateSlide() {
      slides.forEach((slide, idx) => {
        slide.classList.toggle('active', idx === currentSlide);
      });

      const dots = document.querySelectorAll('.dot');
      dots.forEach((dot, idx) => {
        dot.classList.toggle('active', idx === currentSlide);
      });

      counterEl.textContent = `Diapositiva ${currentSlide + 1} / ${totalSlides}`;
      btnPrev.disabled = currentSlide === 0;
      btnNext.disabled = currentSlide === totalSlides - 1;

      // Actualizar notas
      const currentSlideEl = slides[currentSlide];
      const notes = currentSlideEl.getAttribute('data-notes') || 'Sin notas adicionales para esta diapositiva.';
      notesText.textContent = notes;
    }

    function goToSlide(idx) {
      if (idx >= 0 && idx < totalSlides) {
        currentSlide = idx;
        updateSlide();
      }
    }

    function nextSlide() {
      if (currentSlide < totalSlides - 1) {
        currentSlide++;
        updateSlide();
      }
    }

    function prevSlide() {
      if (currentSlide > 0) {
        currentSlide--;
        updateSlide();
      }
    }

    // Atajos de Teclado
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') return; // Evitar disparar al escribir en la calculadora MMU
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'Backspace') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'Home') {
        goToSlide(0);
      } else if (e.key === 'End') {
        goToSlide(totalSlides - 1);
      } else if (e.key.toLowerCase() === 'f') {
        toggleFullscreen();
      } else if (e.key.toLowerCase() === 'n') {
        toggleNotes();
      }
    });

    // Pantalla Completa
    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }

    // Alternar Notas
    function toggleNotes() {
      notesDrawer.classList.toggle('open');
    }

    // Tabs interactivos en Slide 4
    function switchCpuTab(tabId, btn) {
      const parent = btn.parentElement;
      parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      document.querySelectorAll('#slide-4 .tab-pane').forEach(p => p.classList.remove('active'));
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');
    }

    // Calculadora MMU interactiva en Slide 5
    function calcularMmuLive() {
      const input = document.getElementById('mmu-virtual-input');
      let val = parseInt(input.value);
      if (isNaN(val) || val < 0) val = 0;

      const tamanoPagina = 4096;
      const numPagina = Math.floor(val / tamanoPagina);
      const desplazamiento = val % tamanoPagina;

      // Simulamos que el proceso tiene asignadas 4 páginas (0 a 3) mapeadas a marcos [5, 2, 7, 1]
      const tablaMarcos = [5, 2, 7, 1];
      const resP = document.getElementById('mmu-res-p');
      const resD = document.getElementById('mmu-res-d');
      const resV = document.getElementById('mmu-res-v');
      const resF = document.getElementById('mmu-res-f');

      resP.innerHTML = `Paso 1 (Página): <strong>p = ${numPagina}</strong> (${val} // 4096)`;
      resD.innerHTML = `Paso 2 (Desplazamiento): <strong>d = ${desplazamiento}</strong> (${val} % 4096)`;

      if (numPagina < tablaMarcos.length) {
        const marco = tablaMarcos[numPagina];
        const dirFisica = (marco * tamanoPagina) + desplazamiento;
        resV.innerHTML = `Paso 3 (Validación): <strong style="color: var(--accent);">Válida (Marco #${marco})</strong>`;
        resF.innerHTML = `Paso 4 (Dirección Física): <strong style="color: var(--primary);">${dirFisica}</strong> (${marco} &times; 4096 + ${desplazamiento})`;
        resF.style.borderColor = 'rgba(56, 189, 248, 0.4)';
        resF.style.background = 'rgba(56, 189, 248, 0.15)';
      } else {
        resV.innerHTML = `Paso 3 (Validación): <strong style="color: var(--danger);">¡FALLO! Página fuera de límite (p >= ${tablaMarcos.length})</strong>`;
        resF.innerHTML = `Paso 4 (Excepción): <strong style="color: var(--danger);">Segmentation Fault (IndexError detonado)</strong>`;
        resF.style.borderColor = 'rgba(248, 113, 113, 0.5)';
        resF.style.background = 'rgba(248, 113, 113, 0.15)';
      }
    }

    // Iniciar con notas en primera diapositiva
    updateSlide();
  </script>
</body>
</html>
"""

    img_tag = f"<img src='{img_gantt_rr}' alt='Gantt Round Robin'>" if img_gantt_rr else "<p style='color:var(--text-dim)'>[Gráfico no encontrado]</p>"
    html_final = html_template.replace("__IMG_GANTT_TAG__", img_tag)

    with open(RUTA_SALIDA_HTML, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"[OK] Presentacion HTML generada exitosamente en: {RUTA_SALIDA_HTML}")

    # Copiar tambien al directorio de artefactos
    dir_artefactos = r"C:\Users\Carlos Ibañez\.gemini\antigravity\brain\5c4c533d-4542-4431-b189-162cfbeaffb2"
    if os.path.exists(dir_artefactos):
        ruta_artefacto = os.path.join(dir_artefactos, "presentacion_sustentacion.html")
        with open(ruta_artefacto, "w", encoding="utf-8") as f:
            f.write(html_final)
        print(f"[OK] Copia en artefactos guardada en: {ruta_artefacto}")

if __name__ == "__main__":
    generar_html_presentacion()
