import interface
import discussions as disc
import config
import utils

if __name__ == '__main__':
    filepath, grad_program, subprograms = interface.main_loop()

    # select the year for creating the D2L application forum
    forum_year = interface.year_select()

    # create the individual XML discussions for each student - these are passed to make_forum
    df = disc.make_discussions(filepath)

    if grad_program == 'PHAS':
        # create the temporary folder
        tempfolder = utils.make_tempfolder(grad_program)

        # create the individual html files for each student
        disc.write_html(df, tempfolder=tempfolder)

        # create course manifest and course image XML files
        utils.create_manifest(grad_program, year=forum_year, tempfolder=tempfolder)
        utils.create_course_image(tempfolder=tempfolder)

        # create the D2L forum XML document
        disc.make_forum(df, year_of_application=forum_year, tempfolder=tempfolder)

        # collect all D2L forum XML and HTML files into one zip folder
        save_name = config.save_dir + 'D2L_import_{}_{}'.format(grad_program, forum_year)
        utils.zip_forum(save_name=save_name, tempfolder=tempfolder)
        # TODO: allow setting save path

    if grad_program == 'MTST' and subprograms:
        # use the program descriptions to convert the subprogram selection to academic program codes
        to_select = [config.mtst_programs_dict[sub] for sub in subprograms]

        for code in to_select:
            tempfolder = utils.make_tempfolder(code)

            # select only the students applying for the subprograms
            df_code = df[df['acad_plan'] == code]

            # create the individual html files for each student
            disc.write_html(df_code, tempfolder=tempfolder)

            # create course manifest and course image XML files
            utils.create_manifest(code, year=forum_year, tempfolder=tempfolder)
            utils.create_course_image(tempfolder=tempfolder)

            # create the D2L forum XML document
            disc.make_forum(df_code, year_of_application=forum_year, tempfolder=tempfolder)

            # collect all D2L forum XML and HTML files into one zip folder
            save_name = config.save_dir + 'D2L_import_{}_{}'.format(code, forum_year)
            utils.zip_forum(save_name=save_name, tempfolder=tempfolder)
