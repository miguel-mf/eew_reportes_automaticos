from reportSettings import *
file_name = "reporte.pdf"
title = "Reporte sismicidad"
from fpdf import FPDF
class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 9)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        #self.set_draw_color(0, 80, 180)
        #self.set_fill_color(230, 230, 0)
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)
    def chapter_body(self, name):
        # Read text file
        with open(name, 'rb') as fh:
            txt = fh.read().decode('utf-8')
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 7, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 7)
    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)
    def logo(self, name, x, y, w, h):
        self.image(name, x, y, w, h)
    def texts(self, name, y):
        with open(name, 'rb') as fh:
            txt = fh.read().decode('utf-8')
        self.set_xy(10.0,80.0)
        self.set_text_color(0,0,0)
        self.set_font('Times', '', 12)
        self.multi_cell(0,7,txt)
    def titles(self, title):
        self.add_page()
        self.set_xy(0.0,0.0)
        self.set_text_color(0,0,0)
        self.set_font('Times', 'B', 14)
        self.cell(w=210.0, h=40.0, txt=title, border=0)

title = "Reporte alerta temprana"
pdf = PDF()
pdf.titles(title)
pdf.logo('CSN.png', 0, 0, 60, 30)
pdf.set_author('Miguel Medina Flores')
pdf.print_chapter(1, 'Contexto sísmico del norte de Chile', 'textos/contexto1.txt')
pdf.texts('textos/contexto2.txt', 240)
#pdf.print_chapter(2, 'THE PROS AND CONS', 'contexto2.txt')
pdf.output(file_name, 'F')
