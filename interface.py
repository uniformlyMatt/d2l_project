# import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog as fd
# from tkinter.messagebox import showinfo
#
# # create the root window
# root = tk.Tk()
# root.title('Tkinter Open File Dialog')
# root.resizable(False, False)
# root.geometry('300x150')
#
#
# def select_file():
#     filetypes = (
#         ('Microsoft Excel files', '*.xlsx'),
#         ('Comma-separated files', '*.csv'),
#         ('All files', '*.*')
#     )
#
#     filename = fd.askopenfilename(
#         title='Open a file',
#         initialdir='/home/matt/',
#         filetypes=filetypes)
#
#     showinfo(
#         title='Selected File',
#         message=filename
#     )
#
#
# # open button
# open_button = ttk.Button(
#     root,
#     text='Open a File',
#     command=select_file
# )
#
# open_button.pack(expand=True)
#
#
# # run the application
# root.mainloop()
import sys
import platform
import pandas as pd
import easygui as eg

mtst_programs = pd.read_csv('mtst_programs.csv')
current_os = platform.system()

# change default file open directory depending on operating system
if current_os == 'Windows':
    default_dir = "C:\\Users\\%USERNAME%\\Documents"
elif current_os == 'Linux':
    default_dir = "~/Documents"
else:
    default_dir = "Documents"


def program_select():
    """ buttonbox for selecting whether you are creating applications for MTST or PHAS """
    msg = """Select a graduate program..."""
    title = 'Program Selection'
    choices = ['MTST', 'PHAS', 'Cancel']
    filetypes = [['*.xls', '*.xlsx', 'Microsoft Excel files']]

    reply = eg.buttonbox(choices=choices, title=title, msg=msg)

    if reply == 'MTST':
        # do something
        filepath = eg.fileopenbox(filetypes=filetypes, default=default_dir)

        if filepath is None:
            raise RuntimeError

        return filepath
    elif reply == 'PHAS':
        # do something
        return eg.fileopenbox(filetypes=filetypes, default=default_dir)
    else:
        raise RuntimeError


def select_file():
    """ Uses a ccbox to proceed with the creation of Discussions for D2L applications """
    msg = """  This tool will help you create the necessary XML/HTML files\n
needed for uploading graduate applications as Discussions in\n 
D2L. To continue, you need to first select the graduate program\n 
for which you will upload applications. """
    title = "Simple D2L MTST/PHAS Application Upload Helper"

    if eg.ccbox(msg, title):     # show a Continue/Cancel dialog
        # user chose Continue
        file_path = program_select()
        return file_path
    else:  # user chose Cancel
        sys.exit(0)


def run_all():
    """ Create the GUI and guide the user through the creation of D2L Discussions """

    while True:
        try:
            select_file()
            break
        except RuntimeError:  # this happens when the user cancels the program_select dialog
            continue
