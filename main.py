import pandas as pd
import interface
import os
import discussions as disc

if __name__ == '__main__':
    html_fields_template_path = 'templates/html_fields.csv'

    # disc.build_html_template(html_fields_template_path)

    filepath, grad_program = interface.main_loop()

    # create temporary folder to gather all discussion files
    os.mkdir('temp_folder')

    # create the individual html files for each student
    disc.make_discussions(filepath, grad_program)
