import pandas as pd


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

    if program_name == 'PHAS':
        # select the columns for PHAS program application discussions
        cols = ''

    else:
        # select the columns for MTST subprograms application discussions
        cols = ''

    df = get_heading(df, cols=cols)
    print(df['heading'].head())

    # do the XML/HTML creation here

    return 0
