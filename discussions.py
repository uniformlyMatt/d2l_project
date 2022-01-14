import pandas as pd
import shutil
import os
import csv
import re


def get_heading(df: pd.DataFrame, cols=None):
    """ Accepts a pandas DataFrame and list of columns
        and creates a new 'heading' column.

        :df:
            pandas DataFrame
        :cols:
            list of columns used to make the 'heading'

        :returns: df with 'heading' column added
    """

    # change missing entries to empty strings
    df[cols] = df[cols].fillna('')

    df['heading'] = df[cols].agg('-'.join, axis=1)

    return df


def write_html(df: pd.DataFrame):
    """ Accepts a pandas DataFrame and writes an html file """

    # open the html template
    with open('templates/template.html', 'r') as html_file:
        HTML = html_file.read()

    # create column to store individual html markup
    df['html'] = HTML


def make_discussions(path: str, program_name: str) -> pd.DataFrame:
    """ Accepts a Microsoft Excel file path, builds pandas DataFrame with the 'heading' column,
        and creates the corresponding XML/HTML files for the D2L Discussions.

        Stores all HTML files in temp_folder until ready to zip.
    """

    df = pd.read_excel(path)

    # string extra spaces from the columns
    df.columns = list([col.strip() for col in list(df.columns)])

    # rename the columns to match the corresponding fields in the html template
    with open('templates/html_fields.csv', 'r') as csvfile:
        fields = dict(list(csv.DictReader(csvfile))[0])

    # change the name of the really long-named columns - these have been really problematic
    for col in df.columns:
        if len(col) > 32:
            if re.search('(combined)', col):
                df.rename(columns={col: 'combined_program'}, inplace=True)
            if re.search('(advanced credit)', col):
                df.rename(columns={col: 'advanced_credit'}, inplace=True)

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
    with open('templates/DiscussionTemplate.txt', 'r') as single_topic:
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
    df['discussion_topic'] = df.apply(lambda x: x['discussion_topic'].replace('IDnumberHERE', x['ID']), axis=1)

    return df


def make_forum(df: pd.DataFrame, year_of_application: int, program: str):
    """ Accepts a pandas DataFrame of student discussions and creates the D2L
        discussion forum object by filling in discussion_d2l_TemplateFile.txt
    """

    with open('templates/discussion_d2l_TemplateFile.txt', 'r') as all_students:
        forum = all_students.read()

    all_topics = ''.join(df['discussion_topic'].to_list())
    forum = forum.replace("InsertTopicHere", all_topics)
    forum = forum.replace("TOPIC_TITLE", str(year_of_application) + " Applications")

    with open('temp_folder/d2l_discussion_{}.xml'.format(program), 'w') as file:
        file.write(forum)

    return 0
