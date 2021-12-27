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

    df['heading'] = df[cols].agg('-'.join, axis=1)

    return df


def run(path: str) -> int:
    """ Accepts a Microsoft Excel file path and builds pandas DataFrame with the 'heading' column """

    df = pd.read_excel(path)
    print(df.columns)

    df = get_heading(df, cols=['Degree Plan Code', 'Person First Name'])

    df.info()
    df.head()

    return 0


if __name__ == '__main__':
    filepath = '~/Downloads/mtst.xlsx'

    run(filepath)
