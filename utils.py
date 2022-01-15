import os
import shutil


def create_manifest(grad_program: str, year: str):
    """ Create the D2L discussion manifest from the template """
    # create temporary folder
    try:
        os.mkdir('temp_folder')
    except FileExistsError:
        pass

    # copy the manifest and course image templates to the temp folder
    manifest_title = '{} Graduate Applications'.format(grad_program)
    with open('templates/imsmanifest.xml', 'r') as manifest_file:
        manifest = manifest_file.read()

    manifest = manifest.replace("PROGRAMHEADING", manifest_title)
    manifest = manifest.replace("YEAR", year)

    with open('temp_folder/imsmanifest.xml', 'w') as file:
        file.write(manifest)

    return 0


def create_course_image():
    """ Copies the course image template to the temp folder """
    shutil.copyfile('templates/courseimage_d2l.xml', 'temp_folder/courseimage_d2l.xml')

    return 0


def zip_forum(save_name: str):
    """ Collects all created files in the temp folder and zips them together """
    shutil.make_archive(save_name, 'zip', 'temp_folder')
