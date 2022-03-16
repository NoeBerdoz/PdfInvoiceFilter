from pdf_filter import PdfFilter
import PySimpleGUI as sg


sg.theme('DarkAmber')  # Add a touch of color

# Construction of the window.
row1 = sg.Frame(' Scan & Filter PDF files ',
                [
                    [sg.Text(), sg.Column([
                        [sg.Text('Folder location:')],
                        # Take as input the chosen folder absolute path
                        [sg.In(enable_events=True, key="-FOLDER-"), sg.FolderBrowse()],
                        [sg.Text('List of files: ')],
                        [sg.Listbox(values=[], size=(55, 10), key='-FILES-')],
                        [sg.Button('Filter')]
                    ], size=(450, 300), pad=(0, 0))]
                ]
                )

layout = [
    [row1],
    [sg.Button('Quit')]
]

# Create the Window
window = sg.Window('Easy File Filter', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':  # if user closes window or clicks quit
        break

    # Update list to show all files in the directory
    if event == "-FOLDER-":
        pdf_filter = PdfFilter(values['-FOLDER-'])
        window['-FILES-'].update(PdfFilter.get_all_pdf(pdf_filter, values['-FOLDER-']))

    # Filter the PDF present in given folder
    if event == "Filter":
        pdf_filter = PdfFilter(values['-FOLDER-'] + "/")
        pdf_filter.run()




