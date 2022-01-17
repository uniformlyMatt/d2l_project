import pandas as pd
import csv
import re
import config

pd.options.mode.chained_assignment = None  # default='warn'


def write_html(df: pd.DataFrame, tempfolder: str):
    """ Accepts a pandas DataFrame and writes an html file """

    # open the html template
    with open(config.html_template, 'r') as html_file:
        html = html_file.read()

    # get the application fields from the html_fields.csv template
    with open(config.html_fields_template, 'r') as csvfile:
        fields = dict(list(csv.DictReader(csvfile))[0])

    # create column to store individual html markup
    df['html'] = html

    # replace the fields in the html column with the corresponding student data
    for field in fields.values():
        df['html'] = df.apply(lambda x: x['html'].replace(field, x[field]), axis=1)

    # write the html files for each student
    def save_html(filename: str, htmlfile: str):
        """ Accepts a filename and write htmlfile to it. """

        with open(tempfolder + '/{}'.format(filename), 'w') as file:
            file.write(htmlfile)

    df.apply(lambda x: save_html(x['html_filename'], x['html']), axis=1)

    return 0


def make_topics(topic_list: list):
    """ Makes D2L Topics to be posted under a Forum """

    with open(config.topic_template, 'r') as single_topic:
        topic = single_topic.read()

    # create one Topic for each item in topic_list
    topics = [
        topic.replace('TOPIC_ID_HERE', str(i)).replace('TOPIC_TITLE_HERE', tp) for i, tp in enumerate(topic_list)
    ]

    return ''.join(topics)


def make_discussions(path: str, subprogram=None) -> pd.DataFrame:
    """ Accepts a Microsoft Excel file path, builds pandas DataFrame with the 'heading' column,
        and creates the corresponding XML/HTML files for the D2L Discussions.

        Stores all HTML files in temp_folder until ready to zip.
    """

    df = pd.read_excel(path)

    # string extra spaces from the columns
    df.columns = list([col.strip() for col in list(df.columns)])

    # rename the columns to match the corresponding fields in the html template
    with open(config.html_fields_template, 'r') as csvfile:
        fields = dict(list(csv.DictReader(csvfile))[0])

    # change the name of the really long-named columns - these have been really problematic
    for col in df.columns:
        if len(col) > 32:
            if re.search('(combined)', col):
                df.rename(columns={col: 'combined_program'}, inplace=True)
            if re.search('(advanced credit)', col):
                df.rename(columns={col: 'advanced_credit'}, inplace=True)

    # rename columns to match the templates
    for key in fields.keys():
        df.rename(columns={key: fields[key]}, inplace=True)

    # use only the columns that we need
    df = df[fields.values()]

    # fill in missing values with empty string
    df.fillna('', inplace=True)

    # put names in proper case
    df['first_name'] = df['first_name'].str.title()
    df['last_name'] = df['last_name'].str.title()

    # convert student ID to string
    df['student_number'] = df['student_number'].apply(str)

    # copy the index column to an ID column
    df['ID'] = df.index
    df['ID'] = df['ID'].apply(str)

    # create a new column of discussion topics for all students
    with open(config.topic_template, 'r') as single_topic:
        text = single_topic.read()
    df['discussion_topic'] = text

    # create a filename column, replacing spaces with empty strings
    df['html_filename'] = df['first_name'].str.replace(' ', '') + df['last_name'].str.replace(' ', '') + df[
        'student_number'] + '.html'

    # replace the FILENAME in the discussion with the 'html_filename' values
    df['discussion_topic'] = df.apply(lambda x: x['discussion_topic'].replace('FILENAME', x['html_filename']), axis=1)

    # replace the fields in the discussion topic column with the corresponding student data
    for field in fields.values():
        df['discussion_topic'] = df.apply(lambda x: x['discussion_topic'].replace(field, x[field]), axis=1)

    # replace the ID tag in the XML markup
    df['discussion_topic'] = df.apply(lambda x: x['discussion_topic'].replace('TOPIC_ID_HERE', x['ID']), axis=1)

    return df


def make_forum(all_topics: str, year_of_application: str, tempfolder: str, program_name: str):
    """ Accepts a pandas DataFrame of student discussions and creates the D2L
        discussion forum object by filling in discussion_d2l_TemplateFile.txt
    """

    with open(config.forum_template, 'r') as forum_temp:
        forum = forum_temp.read()

    # all_topics = ''.join(df['discussion_topic'].to_list())
    forum = forum.replace("InsertTopicsHere", all_topics)
    forum = forum.replace("FORUM_TITLE", year_of_application + ' ' + program_name)

    with open('{}/discussion_d2l_1.xml'.format(tempfolder), 'w') as file:
        file.write(forum)

    return 0
