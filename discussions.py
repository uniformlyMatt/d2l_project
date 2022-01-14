import pandas as pd
import shutil


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


def make_discussions(path: str, program_name: str) -> int:
    """ Accepts a Microsoft Excel file path, builds pandas DataFrame with the 'heading' column,
        and creates the corresponding XML/HTML files for the D2L Discussions.
    """

    df = pd.read_excel(path)

    # the data from these columns will replace the corresponding fields in 'DiscussionTemplate.txt'
    cols = ['Person First Name', 'Person Last Name', 'Acad Prog Code', 'Academic Plan 1 Code']
    fields = ['FirstName', 'LastName', 'StudentNumber', 'AcadProgram', 'AcademicPlan']
    html_save_name = ''

    # if program_name == 'PHAS':
    #     # select the columns for PHAS program application discussions
    #     fields = ['Person First Name', 'Person Last Name', 'Student ID', 'Academic Plan 1 Code']
    #
    # else:
    #     # select the columns for MTST subprograms application discussions
    #     fields = ''

    df = get_heading(df, cols=cols)

    # convert student number to string
    df['Student ID'] = df['Student ID'].apply(str)

    # create a new column of discussion topics for all students
    with open('DiscussionTemplate.txt', 'r') as single_topic:
        df['discussion_topic'] = single_topic.read()

    print(df)

    # replace the fields in the discussion topic column with the corresponding student data
    for col, field in zip(cols, fields):
        df['discussion_topic'] = df.apply(lambda x: x['discussion_topic'].replace(field, x[col]))

    print(df)
    return 0
