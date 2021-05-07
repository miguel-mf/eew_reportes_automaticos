from reportSettings import *
file_name = "reporte.pdf"

title = 

pdf = PDF()
pdf.set_title(title)
pdf.set_author('Miguel Medina Flores')
pdf.print_chapter(1, '', '20k_c1.txt')
pdf.print_chapter(2, 'THE PROS AND CONS', '20k_c2.txt')
pdf.chapter_body(name)
pdf.output(file_name, 'F')
