from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth

### INPUT ###
Titulo = ""
file_name = "test.pdf"
#############

width, height = A4
canvas = Canvas(file_name, pagesize=A4)
canvas.setFont("Helvetica-Bold", 14)
text_width = stringWidth(Titulo)
text = canvas.beginText((width - text_width) / 2.0, height - 50)
text.textLines(Titulo)
#canvas.drawImage("logo.png", 50, height - 200)

canvas.setFont("Helvetica", 12)
text = canvas.beginText(50, height - 200)
text.textLines("Reporte automático \n Texto de prueba.")
