import pandas as pd
import interface
import os
import discussions as disc
import utils
import shutil

if __name__ == '__main__':
    filepath, grad_program = interface.main_loop()

    # TODO: allow year selection
    # create course manifest and course image XML files
    utils.create_manifest(grad_program, year='2022')
    utils.create_course_image()

    # create the individual XML discussions for each student
    df = disc.make_discussions(filepath, grad_program)

    # create the D2L forum XML document
    disc.make_forum(df, year_of_application=2022, program=grad_program)
