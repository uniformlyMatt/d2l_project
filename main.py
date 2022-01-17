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

    # create the temporary folder
    tempfolder = utils.make_tempfolder(grad_program)

    # create course manifest and course image XML files
    utils.create_manifest(grad_program, year=forum_year, tempfolder=tempfolder)
    utils.create_course_image(tempfolder=tempfolder)

    if grad_program == 'PHAS':
        # create the individual html files for each student
        disc.write_html(df, tempfolder=tempfolder)

        # create the D2L forum XML document
        disc.make_forum(df, year_of_application=forum_year, tempfolder=tempfolder)

        # collect all D2L forum XML and HTML files into one zip folder
        save_name = config.save_dir + 'D2L_import_{}_{}'.format(grad_program, forum_year)
        utils.zip_forum(save_name=save_name, tempfolder=tempfolder)
        # TODO: allow setting save path

    if grad_program == 'MTST' and subprograms:
        """ D2L doesn't have a way to upload individual students as threads under a forum, 
            so I need to create individual forums for each subprogram.
        """
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
            all_students = df_code['discussion_topic'].to_list()
            all_topics = ''.join(all_students)

            disc.make_forum(
                all_topics=all_topics,
                year_of_application=forum_year,
                tempfolder=tempfolder,
                program_name=code
            )

            # collect all D2L forum XML and HTML files into one zip folder
            save_name = config.save_dir + 'D2L_import_{}_{}'.format(code, forum_year)
            utils.zip_forum(save_name=save_name, tempfolder=tempfolder)

            # delete the temp folder
            utils.clear_temp(tempfolder)
