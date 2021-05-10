from reportSettings import *
file_name = "reporte.pdf"
title = "Reporte alerta temprana"

# Palabras a reemplazar:
# PERIODO_PERIODO: mes, año, periodo
# PERIODO_TIEMPO: Nombre del mes, Año, XX/XX/XXXX - YY/YY/YYYY  
# CANTIDAD_SISMOS: Sismos >= 3.0
# CANTIDAD_SENSIBLES: Sismos >= 5.0

pdf = PDF()
#pdf.titles(title)
pdf.set_author('Miguel Medina Flores')
pdf.print_chapter(1, 'Contexto sísmico del norte de Chile', 'text/contexto1.txt')
pdf.logo('images/CSN.png', 0, 0, 60, 30)
pdf.image('images/Figura_Sismicidad.png', 20, 135, 170, 85)
pdf.caption('Figura 1: Catalogo CSN sismos M>4.0 desde 2013 hasta 2020 en el norte de Chile.',220)
pdf.texts('text/contexto2.txt', 240)
pdf.output(file_name, 'F')
