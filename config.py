import pandas as pd
import os
import platform

# define the template folder
templates_folder = 'templates/{}'

html_template = templates_folder.format('template.html')
manifest_template = templates_folder.format('imsmanifest.xml')
mtst_program_descriptions = templates_folder.format('mtst_programs.csv')
discussion_template = templates_folder.format('DiscussionTemplate.txt')
forum_template = templates_folder.format('D2LForumTemplate.txt')
html_fields_template = templates_folder.format('html_fields.csv')
course_image_template = templates_folder.format('courseimage_d2l.xml')

# load the MTST program descriptions
mtst_programs = pd.read_csv(mtst_program_descriptions)
mtst_programs_dict = dict(zip(mtst_programs['Program Name'], mtst_programs['Program Code']))

# change default file open directory depending on operating system
current_os = platform.system()
if current_os == 'Windows':
    default_dir = "C:\\Users\\%USERNAME%\\Documents\\{}*.xlsx"
    save_dir = "C:\\Users\\%USERNAME%\\Documents\\"
elif current_os == 'Linux':
    current_user = os.getlogin()
    default_dir = "/home/"+current_user+"/Documents/{}*.xlsx"
    save_dir = "/home/"+current_user+"/Documents/"
else:
    default_dir = "Documents/{}*.xlsx"
    save_dir = "/Documents/"
