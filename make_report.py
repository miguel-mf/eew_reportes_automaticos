from reportSettings import *
from plotUtil import *

file_name = "reporte.pdf"
title = "Reporte alerta temprana"
Fecha_Inicio = '04-12-2020'  # Formato: DD-MM-YYYY
Fecha_Termino = '11-05-2020' # Formato: DD-MM-YYYY
lonmin = -74
lonmax = -66
latmin = -26
latmax = -16.5

# TAMAÑO A4 = 210 x 297
# Palabras a reemplazar:
# PERIODO_PERIODO: mes, año, periodo
# PERIODO_TIEMPO: Nombre del mes, Año, XX/XX/XXXX - YY/YY/YYYY  
# CANTIDAD_SISMOS: Sismos >= 3.0
# CANTIDAD_SENSIBLES: Sismos >= 5.0

### GENERAR FIGURAS (TEMPORALES)
db = 'report_db.json'
figura_sismo = 'figura_sismo.pdf'
figura_histo = 'figura_histo.pdf'
plotEarthquakeAssoc(figura_sismo,latmin,latmax,lonmin,lonmax,tmin,tmax,db)
plotErrorHist(figura_histo,latmin,latmax,lonmin,lonmax,tmin,tmax,db)
### GENERAR DOCUMENTO 
pdf = PDF()
pdf.set_author('Miguel Medina Flores')
pdf.set_margins(left=20,right=20,top=20)
pdf.print_chapter(1, 'Contexto sísmico del norte de Chile', 'text/contexto1.txt')
pdf.logo('images/CSN.png', 0, 0, 55, 26.7)
pdf.image('images/Figura_Sismicidad.png', 20, 160, 170, 85)
pdf.caption('Figura 1: Catalogo CSN sismos M>4.0 desde 2013 hasta 2020 en el norte de Chile.',245)
pdf.texts('text/contexto2.txt', 270)

pdf.append_chapter(2, 'Sismicidad registrada y alertas emitidas', 'text/reporte1.txt')
#pdf.add_page()
pdf.image('images/Template.png', 15, 45, 85, 85) # SISMICIDAD REGISTRADA
pdf.image('images/Template.png', 110, 45, 85, 85) # SISMICIDAD ALERTADA
pdf.caption('Figure 2: Izquierda: Sismicidad registrada durante el PERIODO_PERIODO de PERIODO_TIEMPO. Derecha: Alertas emitidas asociadas a sismos.',130)
pdf.texts('text/reporte2.txt', 135) # Parrafo sobre las alertas emitidas y tiempos de alerta

#pdf.print_chapter(3, 'Exactitud de los eventos alertados', 'text/contexto1.txt')

#pdf.image('images/Template.png', 110, 45, 85, 85) # Errores de: magnitud, tiempo origen, distancia, profundidad

pdf.output(file_name, 'F')
### BORRAR FIGURAS
