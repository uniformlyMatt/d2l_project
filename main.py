import pandas as pd
import interface


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


def run(path: str) -> int:
    """ Accepts a Microsoft Excel file path and builds pandas DataFrame with the 'heading' column """

    df = pd.read_excel(path)

    df = get_heading(df, cols=['Degree Plan Code', 'Person First Name'])
    print(df['heading'].head())

    return 0


if __name__ == '__main__':
    with interface.select_file() as file:
        print(file)

    # run(filepath)
