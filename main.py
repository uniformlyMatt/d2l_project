import interface
import discussions as disc
import utils

if __name__ == '__main__':
    filepath, grad_program = interface.main_loop()

    # select the year for creating the D2L application forum
    forum_year = interface.year_select()

    if grad_program == 'PHAS':
        # create the individual XML discussions for each student - these are passed to make_forum
        df = disc.make_discussions(filepath, grad_program)

        # create the individual html files for each student
        disc.write_html(df)

        # create course manifest and course image XML files
        utils.create_manifest(grad_program, year=forum_year)
        utils.create_course_image()

        # create the D2L forum XML document
        disc.make_forum(df, year_of_application=forum_year, program=grad_program)

        # collect all D2L forum XML and HTML files into one zip folder
        utils.zip_forum(save_name='D2L_import_{}_{}'.format(grad_program, forum_year))
        # TODO: allow setting save path

    # TODO: what happens for MTST programs
