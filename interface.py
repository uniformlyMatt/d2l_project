import os
import sys
import platform
import pandas as pd
import easygui as eg

mtst_programs = pd.read_csv('mtst_programs.csv')
current_os = platform.system()

# change default file open directory depending on operating system
if current_os == 'Windows':
    default_dir = "C:\\Users\\%USERNAME%\\Documents\\{}*.xlsx"
elif current_os == 'Linux':
    current_user = os.getlogin()
    default_dir = "/home/"+current_user+"/Documents/{}*.xlsx"
else:
    default_dir = "Documents/{}*.xlsx"


def program_select():
    """ buttonbox for selecting whether you are creating applications for MTST or PHAS """
    msg = """Select a graduate program..."""
    title = 'Program Selection'
    choices = ['MTST', 'PHAS', 'Cancel']

    reply = eg.buttonbox(choices=choices, title=title, msg=msg)

    if reply in ['MTST', 'PHAS']:
        return reply
    else:  # if 'Cancel' is selected
        raise RuntimeError


def get_spreadsheet(program: str) -> str:
    """ Accepts the program name as a string and searches for the corresponding Excel workbook """
    filetypes = [[".xls", ".xlsx", "Microsoft Excel workbooks"]]

    if program == 'PHAS':
        file = eg.fileopenbox(
            default=default_dir.format(program),
            filetypes=filetypes
        )

        if file:
            return file
        else:  # if 'Cancel' is selected
            raise RuntimeError
    elif program == 'MTST':
        # select which MTST subprograms we are creating discussions for
        mult_choices = mtst_programs['Program Name'].to_list()
        msg = 'Choose the MTST programs for which you would like to generate D2L Discussions:'
        title = "Choose MTST Programs"
        subprograms = eg.multchoicebox(msg=msg, title=title, choices=mult_choices)


def splash_box():
    """ Uses a ccbox to proceed with the creation of Discussions for D2L applications """
    msg = """  This tool will help you create the necessary XML/HTML files\n
needed for uploading graduate applications as Discussions in\n 
D2L. To continue, you need to first select the graduate program\n 
for which you will upload applications. """
    title = "Simple D2L MTST/PHAS Application Upload Helper"

    if eg.ccbox(msg, title):  # show a Continue/Cancel dialog
        # user chose Continue
        grad_program = program_select()
        file_path = get_spreadsheet(grad_program)

        if file_path:
            return file_path, grad_program
        else:
            sys.exit(0)

    else:  # user chose Cancel
        sys.exit(0)


def main_loop():
    """ Create the GUI and guide the user through the creation of D2L Discussions """

    while True:
        try:
            file_path, program = splash_box()
            return file_path, program
        except RuntimeError:  # this happens when the user cancels the program_select dialog
            continue
