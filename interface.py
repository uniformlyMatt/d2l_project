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

import easygui as eg

msg = """This tool will help you create the necessary XML/HTML files\n
needed for uploading graduate applications as Discussions in D2L.\n
To continue, you need to first select the Microsoft Excel workbook\n
where the applicant information is found. 
"""
title = "Simple D2L MTST/PHAS Application Upload Helper"


def select_file():
    if eg.ccbox(msg, title):     # show a Continue/Cancel dialog
        # user chose Continue
        return eg.fileopenbox()
    else:  # user chose Cancel
        import sys
        sys.exit(0)
