import os


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


print(get_all_pdf(os.getcwd()+"/invoices"))
