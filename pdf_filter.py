import pdfquery
import os


working_dir = os.getcwd()


# Get the invoice's client data
def get_invoice_client(pdf_file):
    pdf = pdfquery.PDFQuery(pdf_file)
    pdf.load()
    pdf.tree.write('pdfXML.txt', pretty_print = True)
    # 150.0, 678.82, 271.93, 688.82 is the client data position
    company = pdf.pq('LTTextLineHorizontal:overlaps_bbox("150.0, 678.82, 271.93, 688.82")').text()
    pdf.file.close()
    return company


# Get only pdf files in directory
def get_all_pdf(path):
    file_names = []
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                name_extension_split = os.path.splitext(entry.name)
                if name_extension_split[1] == ".pdf":
                    file_names.append(entry.name)
            return file_names

    except FileNotFoundError:
        return ['No files found in ' + path]
