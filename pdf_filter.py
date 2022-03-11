import pdfquery
import os
import shutil


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


# Place the given invoice in its corresponding directory
def place_renamed_pdf(pdf_file):
    client_name = get_invoice_client(pdf_file)
    client_clean_name = client_name[1:]  # Remove first string ':'

    # If the client directory doesn't exist, create it
    if os.path.exists(working_dir + "\\" + client_clean_name) is False:
        os.mkdir(client_clean_name)

    # Copy the given invoice with its new name to the corresponding directory
    shutil.copyfile(pdf_file, working_dir + "\\" + client_clean_name + "\\" + client_clean_name + ".pdf")
