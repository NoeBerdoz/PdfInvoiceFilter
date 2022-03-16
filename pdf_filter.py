import pdfquery
import os
import shutil
import re


class PdfFilter:

    def __init__(self, directory):
        self.working_dir = directory

    # Get the invoice's client data
    # TODO Manage exceptions
    # -> not found
    # -> permission error because file is open by user
    def get_invoice_data(self, pdf_file):

        pdf = pdfquery.PDFQuery(pdf_file)
        pdf.load()
        pdf.tree.write('pdfXML.txt', pretty_print = True)

        # 150.0, 678.82, 271.93, 688.82 is the client data position
        xml_company_data = pdf.pq('LTTextLineHorizontal:overlaps_bbox("150.0, 678.82, 271.93, 688.82")')
        # REGEX = ':' character match -> '() capturing group
        # -> [] character matches -> {1, } one to infinite time of it until '</'
        all_companies = re.findall(r": ([A-Za-z0-9áàâäéèêëíìîïóòôöúùûüÁÀÂÄÉÈÊËÍÌÎÏÓÒÔÖÚÙÛÜ \-\.\,\_\t\n\r]{1,})<\/", str(xml_company_data))
        company = all_companies[0]

        # 150.0, 726.602, 302.118, 737.602 is the invoice number data position
        xml_invoice_data = pdf.pq('LTTextLineHorizontal:overlaps_bbox("150.0, 726.602, 302.118, 737.602")')
        # REGEX = ':' character match -> '() capturing group -> [0-9] number character matches -> {8} eight time of it
        all_invoice_number = re.findall(r": ([0-9]{8})/@-\d \*\*", str(xml_invoice_data))
        invoice_number = all_invoice_number[0]

        pdf.file.close()

        # Return a dictionary with the scrapped data
        return {'company': company, 'invoice_number': invoice_number}

    # Get only pdf files in directory
    def get_all_pdf(self, path):
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
    def place_renamed_pdf(self, pdf_file):
        invoice_data = self.get_invoice_data(pdf_file)

        # Remove whitespace for path name compatibility
        if invoice_data['company'][-1:] == ' ':
            invoice_data['company'] = invoice_data['company'][:-1]  # Remove last string ' '

        # If the client directory doesn't exist, create it
        if os.path.exists(self.working_dir + invoice_data['company']) is False:
            os.mkdir(self.working_dir + invoice_data['company'])

        # Copy the given invoice with its new name to the corresponding directory
        shutil.copyfile(pdf_file, self.working_dir + invoice_data['company'] + "/" + invoice_data['invoice_number'] + ' ' + invoice_data['company'] + ".pdf")

    def run(self):
        given_input = self.working_dir
        all_pdf_files = self.get_all_pdf(given_input)
        # Place all pdf files in the working directory
        for pdf_file in all_pdf_files:
            self.place_renamed_pdf(given_input + pdf_file)
