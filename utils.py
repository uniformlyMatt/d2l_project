import os
import shutil
import config


def make_tempfolder(grad_program: str) -> str:
    """ Accepts the grad program and creates a temp folder """

    tempfolder = 'temp_folder_{}'.format(grad_program)

    try:
        os.mkdir(tempfolder)
    except FileExistsError:  # if the directory already exists
        pass

    return tempfolder


def create_manifest(grad_program: str, year: str, tempfolder: str):
    """ Create the D2L discussion manifest from the template """

    # copy the manifest and course image templates to the temp folder
    manifest_title = '{} Graduate Applications'.format(grad_program)
    with open(config.manifest_template, 'r') as manifest_file:
        manifest = manifest_file.read()

    manifest = manifest.replace("PROGRAMHEADING", manifest_title)
    manifest = manifest.replace("YEAR", year)

    with open(tempfolder + '/imsmanifest.xml', 'w') as file:
        file.write(manifest)

    return 0


def create_course_image(tempfolder: str):
    """ Copies the course image template to the temp folder """
    shutil.copyfile(config.course_image_template, '{}/courseimage_d2l.xml'.format(tempfolder))

    return 0


def zip_forum(save_name: str, tempfolder: str):
    """ Collects all created files in the temp folder and zips them together """
    shutil.make_archive(save_name, 'zip', tempfolder)


def clear_temp(tempfolder: str):
    """ Deletes the temporary folder and its contents """
    shutil.rmtree(tempfolder)
