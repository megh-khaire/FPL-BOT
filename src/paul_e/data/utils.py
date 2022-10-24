import pandas as pd


def get_file_data(filename, drop_columns=[], columns=[]):
    '''
    Returns the content of the given file.

    Args:
        filename (str): path of the file
        drop_columns (list): columns to be skipped
        columns (list): columns to be loaded

    Returns:
        pd.Dataframe: contents loaded from the file
    '''
    if columns:
        return pd.read_csv(filename, usecols=columns, encoding='latin1')
    else:
        return pd.read_csv(filename, usecols=lambda x: x not in drop_columns, encoding='latin1')


def fetch_team_mapping(year):
    '''
    Returns a mapping between team code and name, and team code
    and fixture difficulty for all teams in the given year.

    Args:
        year (str): year (season) for which the mapping is required

    Returns:
        dict: maps team code with team name
    '''
    team_cols = ['id', 'name', 'difficulty']
    team_data_filename = f'resources/teams/{year}_teams.csv'
    team_data = get_file_data(team_data_filename, columns=team_cols)
    team_data = team_data.set_index('id').to_dict('dict')
    return team_data
