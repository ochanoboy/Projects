import PyPDF2
import sys

pdf_file = sys.argv[1]
wtr_file = sys.argv[2]
watermarked_pdf = sys.argv[3]

template = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))
watermark = PyPDF2.PdfFileReader(open(wtr_file, 'rb'))
output = PyPDF2.PdfFileWriter()

for i in range(template.getNumPages()):
    page = template.getPage(i)
    page.mergePage(watermark.getPage(0))
    output.addPage(page)
   
    with open(watermarked_pdf, 'wb') as file:
        output.write(file)