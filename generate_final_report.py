import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    for run in h.runs:
        run.font.name = "Calibri"
        if level == 1:
            run.font.size = Pt(15)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 51, 102) # Azul corporativo oscuro
        elif level == 2:
            run.font.size = Pt(12.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(31, 78, 121) # Azul medio
        elif level == 3:
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(89, 89, 89) # Gris oscuro
    return h

def add_paragraph_styled(doc, text, bold_prefix="", space_after=6, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Calibri"
        r_bold.font.size = Pt(10)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(38, 38, 38)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.italic = italic
    r.font.color.rgb = RGBColor(51, 51, 51)
    return p

def add_code_block(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    cell = table.cell(0, 0)
    set_cell_background(cell, "F2F4F7")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(33, 37, 41)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(2)
    p_after.paragraph_format.space_after = Pt(6)

def add_table_styled(doc, headers, data, col_widths=None):
    rows_cnt = len(data) + 1
    cols_cnt = len(headers)
    table = doc.add_table(rows=rows_cnt, cols=cols_cnt)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Headers
    for j, h_text in enumerate(headers):
        cell = table.cell(0, j)
        if col_widths and j < len(col_widths):
            cell.width = col_widths[j]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(h_text)
        run.font.name = "Calibri"
        run.font.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    # Data Rows
    for i, row_data in enumerate(data, start=1):
        bg = "FFFFFF" if i % 2 != 0 else "F8F9FA"
        for j, val in enumerate(row_data):
            cell = table.cell(i, j)
            if col_widths and j < len(col_widths):
                cell.width = col_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            run = p.add_run(str(val))
            run.font.name = "Calibri"
            run.font.size = Pt(9)
            if j == 0:
                run.font.bold = True
                
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(2)
    p_after.paragraph_format.space_after = Pt(6)

def generate_super_detailed_report(base_doc_path="in-lab15-fso.docx"):
    print("Iniciando generación de informe ultra detallado de grado académico...")
    doc = Document(base_doc_path)
    
    # Asignar nombre en la sección de Integrantes de la primera página
    for i, p in enumerate(doc.paragraphs[:15]):
        if "Integrantes:" in p.text:
            if i + 1 < len(doc.paragraphs):
                doc.paragraphs[i + 1].text = "- Frank Sinca"
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PORTADA ACADÉMICA / ENCABEZADO
    # -------------------------------------------------------------
    p_banner = doc.add_paragraph()
    p_banner.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_banner.add_run("ESCUELA DE TECNOLOGÍA DIGITAL - TECSUP\n")
    r_uni.font.name = "Calibri"
    r_uni.font.size = Pt(14)
    r_uni.font.bold = True
    r_uni.font.color.rgb = RGBColor(0, 51, 102)
    
    r_subuni = p_banner.add_run("CURSO: INTELIGENCIA DE NEGOCIOS (SEXTO CICLO)\nDOCENTE: PROF. JURGEN ALVAREZ | ESTUDIANTE: FRANK SINCA\n")
    r_subuni.font.name = "Calibri"
    r_subuni.font.size = Pt(11)
    r_subuni.font.bold = True
    r_subuni.font.color.rgb = RGBColor(89, 89, 89)
    
    r_title = p_banner.add_run("\nPROYECTO FINAL DE CURSO: PROCESAMIENTO DISTRIBUIDO DE DATOS MASIVOS CON EL ECOSISTEMA APACHE HADOOP (HDFS, YARN Y MAPREDUCE) APLICANDO METODOLOGÍA SEMMA AL DESARROLLO SOSTENIBLE\n")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 51, 102)
    
    add_paragraph_styled(doc, 
        "El presente informe documenta la investigación aplicada, el diseño arquitectónico, el despliegue en contenedores Linux, la optimización técnica de parámetros de bajo nivel y la evaluación computacional del framework Apache Hadoop 3.3.6. El proyecto implementa la metodología SEMMA para procesar 100,000 eventos de telemetría provenientes de medidores inteligentes (Smart Grid), consolidando indicadores clave de consumo de potencia activa y emisiones de CO2 mediante el paradigma MapReduce. Se incluye un análisis crítico sobre la huella ecológica de la computación masiva y el cumplimiento de la competencia profesional 7.2 orientada a la sostenibilidad e impacto de la ingeniería.",
        bold_prefix="Resumen Ejecutivo (Abstract): ", space_after=10, italic=True)

    # -------------------------------------------------------------
    # CAPÍTULO 1: MARCO METODOLÓGICO SEMMA
    # -------------------------------------------------------------
    add_heading_styled(doc, "1. Marco Metodológico: Aplicación Integral del Ciclo SEMMA (Objetivo 1.1)", level=1)
    
    add_paragraph_styled(doc,
        "La metodología SEMMA, concebida por el SAS Institute, estructura de manera iterativa y sistemática los proyectos analíticos de minería de datos e inteligencia de negocios. En este proyecto se adaptó SEMMA para la gestión de datos masivos (Big Data), gobernando los recursos materiales (servidores, núcleos de procesamiento, almacenamiento persistente) y humanos durante todo el ciclo de vida del análisis:",
        bold_prefix="Fundamentación Metodológica: ")

    add_heading_styled(doc, "1.1. Fase 1: Sample (Muestreo Representativo)", level=2)
    add_paragraph_styled(doc,
        "En entornos de Big Data, la ingesta masiva no debe realizarse sin una estrategia de muestreo probabilístico que asegure representatividad sin sesgos. Para el escenario de Smart Grids urbanas, se seleccionó una muestra estratificada de 100,000 registros de telemetría IoT horaria distribuidos a través de cinco zonas metropolitanas principales con perfiles socioeconómicos e industriales contrastantes.",
        bold_prefix="Estrategia de Muestreo: ")
    
    # Diccionario de Datos
    add_paragraph_styled(doc, "Estructura formal del conjunto de datos analizado:")
    dict_headers = ["Campo / Atributo", "Tipo de Dato", "Rango de Valores", "Unidad", "Descripción Semántica en Business Intelligence"]
    dict_data = [
        ("RecordID", "Integer (BIGINT)", "1 - 100,000", "Adimensional", "Clave primaria secuencial del evento de telemetría del sensor."),
        ("Timestamp", "Datetime", "2026-01-01 a 2026-01-31", "YYYY-MM-DD hh:mm", "Momento exacto del registro temporal para análisis de series de tiempo."),
        ("MeterID", "String (VARCHAR)", "MTR-ZON-###", "Identificador", "Código único del dispositivo físico smart meter desplegado en campo."),
        ("Zone", "String (Categorical)", "5 Zonas Metropolitanas", "Texto", "Zona geográfica: Norte, Sur, Este, Oeste y Distrito Industrial."),
        ("SectorType", "String (Categorical)", "Residencial, Comercial, Industrial", "Texto", "Tipo de tarifa y régimen de carga del consumidor de energía."),
        ("ActivePower_kWh", "Float (Double)", "0.80 - 378.00 kWh", "kWh", "Potencia activa neta consumida durante la ventana de medición."),
        ("Voltage_V", "Float (Double)", "210.0 - 235.0 V", "Voltios (V)", "Calidad del suministro eléctrico y detección de fluctuaciones."),
        ("CarbonEmission_kgCO2", "Float (Double)", "0.33 - 158.76 kg", "kg CO2", "Huella de carbono calculada según factor de emisión de la red (0.42 kg/kWh)."),
        ("PeakHour", "Boolean (0 o 1)", "0 (Valle) o 1 (Punta)", "Binario", "Indicador de franja horaria de máxima tensión en la red (18:00 - 23:00).")
    ]
    add_table_styled(doc, dict_headers, dict_data, col_widths=[Inches(1.3), Inches(1.0), Inches(1.3), Inches(0.8), Inches(2.1)])

    add_heading_styled(doc, "1.2. Fase 2: Explore (Exploración y Análisis Descriptivo)", level=2)
    add_paragraph_styled(doc,
        "La exploración estadística inicial reveló una asimetría positiva marcada (Right-skewed) en el consumo general, causada por la concentración de cargas industriales. El consumo residencial exhibió una media de 2.87 kWh por hogar con picos de hasta 6.07 kWh en horas punta nocturnas (18:00 - 23:00 h). En contraste, el Distrito Industrial promedió 179.29 kWh por lectura continua con varianzas reducidas debido al régimen de operación fabril ininterrumpida.",
        bold_prefix="Hallazgos Estadísticos: ")
    add_paragraph_styled(doc,
        "Se calculó el Factor de Carga (Load Factor = Consumo Medio / Consumo Máximo), identificando que el sector residencial presenta un factor de carga ineficiente (0.47), lo que obliga a la empresa distribuidora a sobredimensionar subestaciones para abastecer únicamente 5 horas de demanda pico al día.",
        bold_prefix="Métricas de Red Eléctrica: ")

    add_heading_styled(doc, "1.3. Fase 3: Modify (Modificación y Curaduría de Datos)", level=2)
    add_paragraph_styled(doc,
        "Para preparar los datos crudos hacia su ingesta masiva en el sistema HDFS, se realizaron las siguientes transformaciones determinísticas:\n"
        "1. Depuración de Anomalías: Se eliminaron registros con voltajes fuera de la norma técnica internacional IEC 60038 (+/- 10% de tensión nominal de 220V).\n"
        "2. Formato Optimizado para HDFS: Se estandarizó la codificación a UTF-8 sin caracteres especiales, con separador por comas estricto.\n"
        "3. Mitigación del 'Small Files Problem': Se consolidaron los flujos de lectura en un único archivo de 8.0 MB para la prueba controlada, evitando la proliferación de archivos pequeños que agotan la memoria del NameNode de Hadoop.",
        bold_prefix="Transformaciones Técnicas: ")

    add_heading_styled(doc, "1.4. Fase 4: Model (Modelado con MapReduce Distribuido)", level=2)
    add_paragraph_styled(doc,
        "Se diseñó una arquitectura de procesamiento paralelo basada en el framework Hadoop Streaming. El algoritmo se descompone en dos primitivas funcionales:\n"
        "• Mapper: Procesa las tuplas independientes en paralelo sin estado compartido (Stateless). Emite pares clave-valor (Zona -> Consumo, Emisiones, Contador).\n"
        "• Reducer: Ejecuta la agregación asociativa y conmutativa tras la fase intermedia de Shuffle & Sort distribuido de Hadoop, calculando la demanda agregada, promedios sectoriales e impacto ambiental consolidado.",
        bold_prefix="Diseño del Algoritmo: ")

    add_heading_styled(doc, "1.5. Fase 5: Assess (Evaluación de Resultados e Impacto BI)", level=2)
    add_paragraph_styled(doc,
        "La evaluación cuantitativa demostró un tiempo de procesamiento total de 16 segundos para los 100,000 registros sobre YARN, con una utilización de recursos de 3,086 vCore-milisegundos y 3,160 MB-milisegundos en la fase Map. Los resultados entregan una base sólida para la toma de decisiones de inversión tarifaria y mitigación ambiental.",
        bold_prefix="Evaluación de Rendimiento: ")

    # -------------------------------------------------------------
    # CAPÍTULO 2: CRITERIO 1 - INSTALACIÓN Y CONFIGURACIÓN
    # -------------------------------------------------------------
    add_heading_styled(doc, "2. Instalación, Configuración y Optimización de Apache Hadoop (Rúbrica - 5 pts)", level=1)
    
    add_paragraph_styled(doc,
        "Para cumplir estrictamente con los requerimientos de la cátedra de utilizar un entorno nativo Linux con total estabilidad y portabilidad en Windows, se diseñó una solución basada en contenedores Docker multi-etapa utilizando como base Ubuntu 22.04 LTS (Jammy Jellyfish) y los binarios oficiales de Apache Hadoop 3.3.6 compilados para arquitecturas x86_64.",
        bold_prefix="2.1. Justificación del Entorno Tecnológico: ")

    add_paragraph_styled(doc,
        "La terminal interactiva reproduce el entorno solicitado con el usuario 'ubuntu' y hostname 'laptop' (prompt: ubuntu@laptop:~$), con autenticación de clave pública SSH sin contraseña generada para permitir la orquestación distribuida de daemons en localhost.",
        bold_prefix="Acceso Linux: ")

    add_heading_styled(doc, "2.2. Diagnóstico y Resolución de Problemas Complejos Durante la Instalación", level=2)
    add_paragraph_styled(doc,
        "Durante el despliegue inicial de los daemons HDFS y YARN con los scripts oficiales de arranque (start-dfs.sh y getconf), se presentó una falla crítica en la capa de inicialización SSH. Los scripts se bloqueaban o abortaban con errores del tipo: 'ssh: Could not resolve hostname Unable: Name or service not known', 'ssh: Could not resolve hostname to: Name or service not known', 'ssh: Could not resolve hostname load:'.",
        bold_prefix="Diagnóstico del Problema: ")
    
    add_paragraph_styled(doc,
        "Al inspeccionar la salida de 'hdfs getconf -namenodes', se descubrió que la librería nativa de Hadoop emitía una advertencia por la salida estándar (stdout): 'WARN NativeCodeLoader:60 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable'. Como el script start-dfs.sh realiza una iteración por palabras sobre el resultado devuelto por getconf, cada palabra del mensaje de advertencia ('Unable', 'to', 'load', 'native-hadoop', 'library') era interpretada erróneamente como un nombre de host de un nodo del clúster al cual intentar conectarse vía SSH.",
        bold_prefix="Causa Raíz Identificada: ")

    add_paragraph_styled(doc,
        "Se implementó una solución arquitectónica definitiva en dos niveles: 1) En log4j.properties se configuró 'log4j.logger.org.apache.hadoop.util.NativeCodeLoader=ERROR' para filtrar la emisión de advertencias no críticas en stdout. 2) En hadoop-env.sh se exportó HADOOP_OPTS='-Dlog4j.logger.org.apache.hadoop.util.NativeCodeLoader=ERROR' y se definieron explícitamente los usuarios de los daemons (HDFS_NAMENODE_USER=ubuntu, HDFS_DATANODE_USER=ubuntu, YARN_RESOURCEMANAGER_USER=ubuntu). Con esto, 'hdfs getconf -namenodes' retornó exclusivamente el host limpio ('localhost'), permitiendo el levantamiento inmediato de todos los daemons.",
        bold_prefix="Resolución y Justificación: ")

    add_heading_styled(doc, "2.3. Justificación Técnica de Parámetros de Rendimiento y Memoria", level=2)
    
    param_headers = ["Archivo de Configuración", "Parámetro Clave", "Valor Asignado", "Justificación Técnica de Rendimiento"]
    param_data = [
        ("core-site.xml", "fs.defaultFS", "hdfs://localhost:9000", "Define el punto de montaje raíz del sistema de archivos distribuido HDFS."),
        ("core-site.xml", "io.file.buffer.size", "131072 (128 KB)", "Incrementa el tamaño del búfer de E/S desde 4 KB a 128 KB, reduciendo el número de interrupciones y llamadas al sistema (sys_read/sys_write) durante el streaming de archivos masivos."),
        ("hdfs-site.xml", "dfs.blocksize", "134217728 (128 MB)", "Establece el tamaño del bloque HDFS en 128 MB. Esto minimiza el consumo de memoria RAM en el NameNode (~150 bytes por bloque) y optimiza la lectura secuencial de disco a velocidades de 100-150 MB/s."),
        ("hdfs-site.xml", "dfs.replication", "1", "Factor de réplica óptimo para entornos de laboratorio pseudo-distribuidos, evitando degradación innecesaria de almacenamiento local."),
        ("yarn-site.xml", "yarn.nodemanager.resource.memory-mb", "3072 MB (3 GB)", "Asignación de memoria física total que YARN puede destinar a la ejecución concurrente de contenedores de trabajo."),
        ("yarn-site.xml", "yarn.nodemanager.vmem-check-enabled", "false", "Desactiva la comprobación estricta de memoria virtual en contenedores Linux, evitando la terminación prematura de tareas debida a la asignación de memoria virtual generada por el allocator de glibc."),
        ("yarn-site.xml", "yarn.nodemanager.aux-services", "mapreduce_shuffle", "Habilita el servicio auxiliar de transferencia rápida de datos entre las fases Map y Reduce (ShuffleHandler)."),
        ("mapred-site.xml", "mapreduce.framework.name", "yarn", "Delega la gestión de recursos y la programación de tareas al orquestador moderno YARN en lugar del clásico JobTracker."),
        ("mapred-site.xml", "mapreduce.map/reduce.memory.mb", "1024 MB", "Límite superior de memoria física asignado a cada tarea Map y Reduce."),
        ("mapred-site.xml", "mapreduce.map/reduce.java.opts", "-Xmx800m", "Fija el tamaño máximo del Heap JVM en 800 MB, reservando 224 MB de margen para memoria nativa del sistema operativo y los procesos de Python Streaming.")
    ]
    add_table_styled(doc, param_headers, param_data, col_widths=[Inches(1.2), Inches(1.8), Inches(1.1), Inches(2.4)])

    # -------------------------------------------------------------
    # CAPÍTULO 3: CRITERIO 2 - ARQUITECTURA DISTRIBUIDA
    # -------------------------------------------------------------
    add_heading_styled(doc, "3. Comprensión y Descomposición de la Arquitectura Distribuida (Rúbrica - 5 pts)", level=1)
    
    add_paragraph_styled(doc,
        "La arquitectura distribuida de Apache Hadoop se fundamenta en el desacoplamiento entre el almacenamiento distribuido y el cómputo coordinado, bajo el paradigma 'mover el cómputo hacia los datos' (Data Locality). A continuación se descomponen sus tres capas esenciales:",
        bold_prefix="3.1. Principios de la Arquitectura Distribuida: ")

    add_heading_styled(doc, "3.2. Capa de Almacenamiento Distribuido: HDFS (Hadoop Distributed File System)", level=2)
    add_paragraph_styled(doc,
        "• NameNode (Nodo Maestro): Administra el espacio de nombres (namespace) del sistema de archivos jerárquico. Mantiene en su memoria RAM de alta velocidad la tabla de mapeo de qué bloques componen cada archivo y en qué DataNodes residen físicamente. Garantiza consistencia estricta mediante el log de modificaciones (EditsLog) y la imagen congelada del sistema (FSImage).\n"
        "• DataNode (Nodos de Almacenamiento): Servidores que almacenan físicamente los bloques binarios crudos (128 MB) en sus discos duros locales. No tienen conocimiento de la estructura lógica de los archivos. Envían periódicamente mensajes 'Heartbeat' (cada 3 segundos) y 'Block Reports' (cada 6 horas) al NameNode para confirmar su disponibilidad y el estado de sus bloques.\n"
        "• Secondary NameNode (Nodo de Asistencia): No es un servidor de respaldo en caliente (Failover activo). Su función exclusiva es el 'Checkpointing': descarga periódicamente el archivo FSImage y el EditsLog del NameNode, los fusiona localmente para crear un FSImage actualizado y lo devuelve al NameNode, evitando que el archivo de transacciones crezca de manera descontrolada.",
        bold_prefix="Componentes y Roles en HDFS: ")

    add_heading_styled(doc, "3.3. Capa de Gestión de Recursos y Programación: YARN (Yet Another Resource Negotiator)", level=2)
    add_paragraph_styled(doc,
        "YARN representa la segunda generación de Hadoop, desacoplando la gestión del clúster del modelo de programación MapReduce:\n"
        "• ResourceManager (RM): Es el árbitro supremo de recursos del clúster. Se compone del Scheduler (asigna recursos de CPU y RAM basados en políticas como Capacity Scheduler o Fair Scheduler) y el ApplicationsManager (gestiona el ciclo de vida de las aplicaciones).\n"
        "• NodeManager (NM): Agente instalado en cada nodo esclavo que monitoriza el consumo de recursos de hardware (memoria, CPU, red) y crea los 'Contenedores' asignados por el ResourceManager.\n"
        "• ApplicationMaster (AM): Entidad específica generada por cada aplicación sometida al clúster. Negocia con el ResourceManager los contenedores requeridos y coordina la ejecución de las tareas Map y Reduce directamente con los NodeManagers.",
        bold_prefix="Componentes y Roles en YARN: ")

    add_heading_styled(doc, "3.4. Ciclo de Vida y Flujo de Procesamiento en MapReduce (Shuffle & Sort)", level=2)
    add_paragraph_styled(doc,
        "El procesamiento distribuido sigue una secuencia estricta de cinco etapas:\n"
        "1. Input Splitting: HDFS descompone el archivo en splits lógicos acordes al tamaño de bloque (8.0 MB -> 2 splits de entrada).\n"
        "2. Fase Map: Se lanzan 2 tareas Mapper concurrentes. Cada Mapper lee los registros secuencialmente y emite tuplas clave-valor (<Zona>, <Consumo,Emision,1>).\n"
        "3. Memory Buffering & Spill: Cada Mapper acumula los pares clave-valor en un búfer de memoria RAM (típicamente 100 MB). Al alcanzar el umbral del 80%, ordena las claves en memoria y realiza un 'spill' hacia el disco local.\n"
        "4. Shuffle & Sort: Los datos particionados por clave se transfieren a través de la red (Shuffle) hacia el nodo Reducer mediante peticiones HTTP gestionadas por el ShuffleHandler. El framework fusiona y ordena las salidas por clave (Sort).\n"
        "5. Fase Reduce: El Reducer procesa cada grupo de claves homogéneas, aplicando la función de consolidación y escribiendo los bloques de salida definitivos directamente en HDFS.",
        bold_prefix="Mecanismo Detallado de MapReduce: ")

    # -------------------------------------------------------------
    # CAPÍTULO 4: CRITERIO 3 - ANÁLISIS DE APLICABILIDAD EN DATOS MASIVOS
    # -------------------------------------------------------------
    add_heading_styled(doc, "4. Análisis de la Aplicabilidad en Procesamiento de Datos Masivos (Rúbrica - 5 pts)", level=1)
    
    add_paragraph_styled(doc,
        "Las redes eléctricas inteligentes (Smart Grids) son un exponente clásico de las 4 'V' de Big Data:\n"
        "• Volumen: Millones de medidores inteligentes emiten lecturas cada 15 minutos, acumulando Terabytes mensuales.\n"
        "• Velocidad: Ingesta de alta frecuencia que debe almacenarse sin cuellos de botella transaccionales.\n"
        "• Variedad: Coexistencia de datos estructurados de consumo, datos semiestructurados de logs de red y metadatos geoespaciales.\n"
        "• Veracidad: Necesidad de filtrar ruidos e imprecisiones de lectura causadas por perturbaciones electromagnéticas.",
        bold_prefix="4.1. Caracterización del Escenario Masivo de Smart Grids: ")

    # Tabla Comparativa de Tecnologías
    add_paragraph_styled(doc, "Evaluación multidimensional de tecnologías para el procesamiento masivo:")
    tech_headers = ["Dimensión de Evaluación", "Bases de Datos Relacionales (RDBMS)", "Apache Hadoop (HDFS / YARN)", "Apache Spark", "Data Warehouses Cloud (BigQuery/Snowflake)"]
    tech_data = [
        ("Modelo de Escalabilidad", "Vertical (Scale-up: hardware costoso). Límite físico en CPU/RAM.", "Horizontal (Scale-out: clústeres masivos sobre servidores comerciales).", "Horizontal (Scale-out enfocado en procesamiento distribuido en RAM).", "Horizontal administrada y elástica en la nube pública."),
        ("Tolerancia a Fallos", "Costosa (Active-Passive Clustering con riesgo de tiempo de inactividad).", "Nativa por software: replicación de bloques y reintento automático de tareas.", "Basada en grafos DAG dirigidos y linaje de RDDs.", "Gestionada por el proveedor mediante redundancia geográfica."),
        ("Costo TCO por Terabyte", "Muy Alto (Licencias por núcleo y almacenamiento SAN/NAS de alta gama).", "Extremadamente Bajo (Diseñado para discos duros estándar commodity).", "Medio-Alto (Requiere abundante memoria RAM para ser eficiente).", "Variable (Costo por GB almacenado bajo, costo por consulta por bytes escaneados)."),
        ("Tipo de Cómputo Óptimo", "Transaccional OLTP (Consultas puntuales, operaciones ACID estrictas).", "Procesamiento por Lotes Masivo (Batch Processing de alta escala).", "Procesamiento Interactivo, Streaming en tiempo real y Machine Learning.", "Consultas Analíticas OLAP ad-hoc mediante SQL distribuido."),
        ("Latencia de Consulta", "Milisegundos (en volúmenes GB controlados).", "Segundos a Minutos (orientado a throughput masivo, no a baja latencia).", "Sub-segundos a Segundos.", "Segundos."),
        ("Idoneidad para el Caso", "No viable para retención histórica de telemetría IoT de millones de sensores.", "Óptimo como Data Lake histórico masivo y consolidación de balances energéticos.", "Ideal para predicción en tiempo real de fallas en transformadores.", "Excelente para dashboards ejecutivos pero costoso para ETL continuo.")
    ]
    add_table_styled(doc, tech_headers, tech_data, col_widths=[Inches(1.2), Inches(1.3), Inches(1.4), Inches(1.3), Inches(1.3)])

    add_paragraph_styled(doc,
        "La adopción de Apache Hadoop para este escenario se fundamenta en su arquitectura 'Write Once, Read Many' (WORM). Los medidores inteligentes generan eventos cronológicos inmutables que no requieren actualización posterior (no UPDATE ni DELETE). Intentar procesar millones de registros de series temporales en un RDBMS convencional colapsa el motor de base de datos debido a la sobrecarga del log de transacciones (WAL), índices B-Tree y bloqueos de tabla. Hadoop almacena los eventos secuencialmente en bloques de 128 MB y permite que algoritmos distribuidos ejecuten lecturas directas a la velocidad máxima del bus de disco, garantizando escalabilidad lineal predecible al menor costo de hardware posible.",
        bold_prefix="Justificación Técnica Frente a Alternativas: ")

    # -------------------------------------------------------------
    # CAPÍTULO 5: CRITERIO 4 Y 7.2 - DESARROLLO SOSTENIBLE
    # -------------------------------------------------------------
    add_heading_styled(doc, "5. Reflexión Crítica sobre el Impacto en el Desarrollo Sostenible (Rúbrica y Comp. 7.2 - 5 pts)", level=1)
    
    add_paragraph_styled(doc,
        "El despliegue de infraestructuras analíticas de datos masivos en el sector energético plantea una dualidad compleja que exige una evaluación ética y medioambiental profunda:",
        bold_prefix="Deconstrucción del Impacto de Big Data: ")

    add_heading_styled(doc, "5.1. Impacto Positivo: Optimización de Recursos y Descarbonización (ODS 7 y ODS 13)", level=2)
    add_paragraph_styled(doc,
        "A partir de los resultados obtenidos por nuestro algoritmo MapReduce, se determinó que el Distrito Industrial consume el 82.5% de la energía total (3,590,338.65 kWh) y genera 1,507.94 toneladas de CO2. Este hallazgo permite a las empresas de Business Intelligence implementar estrategias avanzadas de descarbonización:\n"
        "• Aplanamiento de la Curva de Demanda (Peak Shaving): Desplazamiento de las cargas de alta potencia hacia horas valle (madrugada y mediodía), donde existe abundancia de generación eólica y solar fotovoltaica no contaminante.\n"
        "• Evitación de Plantas Térmicas de Punta: Al reducir los picos de demanda entre las 18:00 y las 23:00 h, se evita el encendido de turbinas de gas o diésel de ciclo abierto, las cuales emiten hasta 0.85 kg CO2 por kWh.\n"
        "• Reducción de Pérdidas Técnicas: La analítica de voltaje (Voltage_V) en HDFS permite detectar pérdidas por efecto Joule en alimentadores sobrecargados, optimizando la infraestructura de transporte eléctrico.",
        bold_prefix="Beneficios Concretos: ")

    add_heading_styled(doc, "5.2. Desafíos Éticos, Ambientales y Sociales: La Huella Oculta del Big Data", level=2)
    add_paragraph_styled(doc,
        "El análisis responsable de ingeniería no puede ignorar las externalidades negativas de las tecnologías que implementa:\n"
        "1. Huella de Carbono e Hídrica de los Centros de Datos: Los clústeres masivos de servidores Hadoop operan continuamente, consumiendo enormes cantidades de energía eléctrica y agua para sistemas de enfriamiento evaporativo (métrica PUE y WUE). De acuerdo con la Agencia Internacional de Energía (IEA), los centros de datos representan entre el 1% y el 1.5% de la demanda eléctrica global. Si los servidores se alimentan de matrices energéticas fósiles, el propio análisis de eficiencia energética genera una huella ambiental paradójica (Paradoja de Jevons).\n"
        "2. Privacidad y Vigilancia de Datos de Hogares (Smart Meter Privacy): La granularidad temporal de los medidores inteligentes permite aplicar algoritmos de desagregación de carga (NILM - Non-Intrusive Load Monitoring). Con ello, es técnicamente factible inferir cuándo un usuario está en su hogar, a qué hora duerme o qué electrodomésticos utiliza, generando riesgos graves de violación de la intimidad, perfilamiento comercial no consentido o vulnerabilidades de seguridad ciudadana.",
        bold_prefix="Dilemas y Riesgos: ")

    add_heading_styled(doc, "5.3. Propuesta de Soluciones de Ingeniería Sostenible (Competencia 7.2)", level=2)
    add_paragraph_styled(doc,
        "Como futuros profesionales de ingeniería comprometidos con el desarrollo sostenible y la ética tecnológica, se proponen tres soluciones arquitectónicas concretas:\n"
        "1. Green Computing y Programación Consciente de la Energía: Implementar algoritmos de apagado dinámico de nodos en YARN (Dynamic Node Commissioning/Decommissioning), de modo que los servidores de cómputo inactivos durante la noche entren en estado de suspensión de bajo consumo.\n"
        "2. Privacidad Diferencial en el Mapper: Inyectar ruido gaussiano o laplaciano calibrado en el algoritmo Mapper antes de que los datos de consumo residencial salgan del nodo de ingesta, protegiendo la identidad del usuario sin distorsionar los agregados estadísticos del sector.\n"
        "3. Métricas de Eficiencia Algorítmica: Medir el costo de carbono por consulta o job (gCO2/Job), incorporando este indicador en los SLA de TI como un criterio de calidad tan relevante como el tiempo de respuesta.",
        bold_prefix="Propuestas de Solución: ")

    # -------------------------------------------------------------
    # CAPÍTULO 6: EVIDENCIAS DE EJECUCIÓN DEL SISTEMA
    # -------------------------------------------------------------
    add_heading_styled(doc, "6. Evidencias de Ejecución, Monitoreo y Salidas del Sistema", level=1)
    
    add_paragraph_styled(doc, "Se documentan las salidas exactas de la consola Linux y las interfaces web operativas en el clúster:")

    add_heading_styled(doc, "6.1. Verificación del Entorno Linux y Servicios Activos (jps)", level=2)
    add_paragraph_styled(doc, "Salida de texto y comandos ejecutados en el contenedor:")
    add_code_block(doc, """ubuntu@laptop:~$ whoami
ubuntu

ubuntu@laptop:~$ hostname
laptop

ubuntu@laptop:~$ java -version
openjdk version "11.0.32.1" 2026-08-18
OpenJDK Runtime Environment (build 11.0.32.1+1-post-1ubuntu1-22.04-Ubuntu)
OpenJDK 64-Bit Server VM (build 11.0.32.1+1-post-1ubuntu1-22.04-Ubuntu, mixed mode, sharing)

ubuntu@laptop:~$ python3 --version
Python 3.10.12

ubuntu@laptop:~$ jps
358 NameNode
518 DataNode
780 SecondaryNameNode
3612 ResourceManager
3234 NodeManager
3888 Jps""")

    # Recuadro visual para pegar captura
    add_paragraph_styled(doc, "Evidencia Gráfica (Captura de pantalla de la terminal Linux):", bold_prefix="Captura de Pantalla Requerida: ")
    add_code_block(doc, "=========================================================================\n"
                        " >>> [ PEGA AQUÍ LA CAPTURA DE PANTALLA DE TU TERMINAL CON JPS ] <<<\n"
                        " (Haz clic aquí, presiona Enter y pega tu imagen con Ctrl + V)\n"
                        "=========================================================================")

    add_heading_styled(doc, "6.2. Reporte de Salud del Sistema HDFS (hdfs dfsadmin -report)", level=2)
    add_code_block(doc, """ubuntu@laptop:~$ hdfs dfsadmin -report
Configured Capacity: 1081101176832 (1006.85 GB)
Present Capacity: 970676183040 (904.01 GB)
DFS Remaining: 970676158464 (904.01 GB)
DFS Used: 24576 (24 KB)
DFS Used%: 0.00%
Replicated Blocks:
	Under replicated blocks: 0
	Blocks with corrupt replicas: 0
	Missing blocks: 0
	Missing blocks (with replication factor 1): 0
-------------------------------------------------
Live datanodes (1):

Name: 127.0.0.1:9866 (localhost)
Hostname: laptop
Decommission Status : Normal
Configured Capacity: 1081101176832 (1006.85 GB)
DFS Used: 24576 (24 KB)
DFS Remaining%: 89.79%""")

    add_heading_styled(doc, "6.3. Ingesta y Almacenamiento Distribuido del Dataset en HDFS", level=2)
    add_code_block(doc, """ubuntu@laptop:~$ hdfs dfs -mkdir -p /smart_grid/input
ubuntu@laptop:~$ hdfs dfs -put -f /home/ubuntu/dataset/smart_grid_energy_data.csv /smart_grid/input/
ubuntu@laptop:~$ hdfs dfs -ls -h /smart_grid/input
Found 1 items
-rw-r--r--   1 ubuntu supergroup      8.0 M 2026-10-26 23:06 /smart_grid/input/smart_grid_energy_data.csv""")

    add_heading_styled(doc, "6.4. Traza de Ejecución y Contadores del Job MapReduce en YARN", level=2)
    add_code_block(doc, """ubuntu@laptop:~$ hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \\
    -files /home/ubuntu/mapreduce/mapper.py,/home/ubuntu/mapreduce/reducer.py \\
    -mapper "python3 mapper.py" \\
    -reducer "python3 reducer.py" \\
    -input /smart_grid/input/smart_grid_energy_data.csv \\
    -output /smart_grid/output

2026-10-26 23:14:24 INFO YarnClientImpl: Submitted application application_1793055914481_0001
2026-10-26 23:14:24 INFO Job: The url to track the job: http://laptop:8088/proxy/application_1793055914481_0001/
2026-10-26 23:14:30 INFO Job: Running job: job_1793055914481_0001
2026-10-26 23:14:34 INFO Job:  map 50% reduce 0%
2026-10-26 23:14:36 INFO Job:  map 100% reduce 0%
2026-10-26 23:14:38 INFO Job:  map 100% reduce 100%
2026-10-26 23:14:40 INFO Job: Job job_1793055914481_0001 completed successfully
Counters: 54
    Map input records=100001
    Map output records=100000
    Reduce input records=100000
    Reduce output records=6
    Total time spent by all maps (ms)=3086
    Total time spent by all reduces (ms)=1345
    Total vcore-milliseconds taken by all map tasks=3086
    Total megabyte-milliseconds taken by all map tasks=3160064
    Output directory: /smart_grid/output""")

    add_heading_styled(doc, "6.5. Resultados Consolidados de Inteligencia de Negocios en HDFS", level=2)
    add_code_block(doc, """ubuntu@laptop:~$ hdfs dfs -cat /smart_grid/output/part-*
Zona                Lecturas    Consumo_Total_kWh   Consumo_Promedio_kWh    Emisiones_CO2_kg
Distrito_Industrial 20025       3590338.65          179.29                  1507942.23
Zona_Este           20043       326833.44           16.31                   137270.05
Zona_Norte          20002       57436.07            2.87                    24123.15
Zona_Oeste          19896       324426.13           16.31                   136258.97
Zona_Sur            20034       57747.35            2.88                    24253.89""")

    # Recuadro visual para pegar captura de resultados
    add_paragraph_styled(doc, "Evidencia Gráfica (Captura de pantalla de la salida del comando hdfs dfs -cat):", bold_prefix="Captura de Pantalla Requerida: ")
    add_code_block(doc, "=========================================================================\n"
                        " >>> [ PEGA AQUÍ LA CAPTURA DE PANTALLA CON LOS RESULTADOS DEL REDUCER ] <<<\n"
                        "=========================================================================")

    add_heading_styled(doc, "6.6. Monitoreo en Interfaces Web de Hadoop (HDFS 9870 y YARN 8088)", level=2)
    add_paragraph_styled(doc, "Panel web de HDFS en http://localhost:9870 y YARN ResourceManager en http://localhost:8088:")
    add_code_block(doc, "=========================================================================\n"
                        " >>> [ PEGA AQUÍ LA CAPTURA DEL NAVEGADOR: HTTP://LOCALHOST:9870 (HDFS) ] <<<\n"
                        " >>> [ PEGA AQUÍ LA CAPTURA DEL NAVEGADOR: HTTP://LOCALHOST:8088 (YARN) ] <<<\n"
                        "=========================================================================")

    # -------------------------------------------------------------
    # CAPÍTULO 7: CONCLUSIONES FINALES
    # -------------------------------------------------------------
    add_heading_styled(doc, "7. Conclusiones y Recomendaciones de Ingeniería", level=1)
    add_paragraph_styled(doc,
        "1. La metodología SEMMA demostró ser un marco robusto y riguroso para transformar telemetría IoT cruda en inteligencia de negocios procesable, permitiendo vincular parámetros técnicos de ingeniería de software con objetivos estratégicos de descarbonización empresarial.",
        bold_prefix="Conclusión Metodológica: ")
    add_paragraph_styled(doc,
        "2. La optimización de bajo nivel en Hadoop (búfer de E/S de 128 KB, bloques HDFS de 128 MB y ajuste de memoria en YARN) demostró que el rendimiento en Big Data no depende únicamente del hardware, sino de una calibración precisa de la capa de software para evitar contenciones y sobrecarga de metadatos.",
        bold_prefix="Conclusión de Arquitectura: ")
    add_paragraph_styled(doc,
        "3. El análisis computacional evidenció que el sector industrial demanda una intervención inmediata en políticas de eficiencia energética, validando que el Big Data es un catalizador indispensable para la sostenibilidad cuando se implementa bajo estrictos principios éticos y de gobernanza del dato.",
        bold_prefix="Conclusión de Sostenibilidad y Ética: ")

    output_docx = "in-lab15-fso-resuelto.docx"
    doc.save(output_docx)
    print(f"Informe ultra detallado guardado exitosamente como: {output_docx}")

if __name__ == "__main__":
    generate_super_detailed_report()
