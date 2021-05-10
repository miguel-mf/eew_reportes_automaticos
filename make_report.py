from reportSettings import *
file_name = "reporte.pdf"
title = "Reporte alerta temprana"

# TAMAÑO A4 = 210 x 297
# Palabras a reemplazar:
# PERIODO_PERIODO: mes, año, periodo
# PERIODO_TIEMPO: Nombre del mes, Año, XX/XX/XXXX - YY/YY/YYYY  
# CANTIDAD_SISMOS: Sismos >= 3.0
# CANTIDAD_SENSIBLES: Sismos >= 5.0


### GENERAR FIGURAS (TEMPORALES)


pdf = PDF()
#pdf.titles(title)
pdf.set_author('Miguel Medina Flores')
pdf.print_chapter(1, 'Contexto sísmico del norte de Chile', 'text/contexto1.txt')
pdf.logo('images/CSN.png', 0, 0, 55, 26.7)
pdf.image('images/Figura_Sismicidad.png', 20, 135, 170, 85)
pdf.caption('Figura 1: Catalogo CSN sismos M>4.0 desde 2013 hasta 2020 en el norte de Chile.',220)
pdf.texts('text/contexto2.txt', 240)

pdf.append_chapter(2, 'Funcionamiento del sistema de alerta temprana', 'text/reporte1.txt')
pdf.image('images/Template.png', 15, 200, 85, 85) # SISMICIDAD REGISTRADA
pdf.image('images/Template.png', 105, 200, 85, 85) # SISMICIDAD ALERTADA
pdf.caption('Figure 2: Izquierda: Sismicidad registrada durante el mes de Octubre 2020. Derecha: Alertas emitidas asociadas a sismos.',286)

pdf.output(file_name, 'F')



### BORRAR FIGURAS
