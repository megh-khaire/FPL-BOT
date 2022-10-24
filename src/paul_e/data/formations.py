import pandas as pd
from paul_e.constants.data import FORMATIONS_DATASET_LINK, POSSIBLE_FORMATIONS
from paul_e.data.seasons import gen_season_dataset


def get_total_points_for_position(position, n_players, gw_data):
    '''
    Calculates the total score of the players in the given position for the given formation

    Args:
        position (str): position for which total score is to be calculated
        n_players (int): number of players playing in the given position
        gw_data (pd.Dataframe): scores of all players in a game week

    Returns:
        int: total points scored by players in the given position during the GW
    '''
    top_n_players = gw_data[gw_data['position'] == position].nlargest(n_players, 'total_points')
    return top_n_players['total_points'].sum()


def get_points_for_all_formations(gw_data):
    '''
    Calculates the max score for all possible formations in a game week.

    Args:
        gw_data (pd.Dataframe): scores of all players in a game week

    Returns:
        pd.Dataframe: total scores for all possible formations in the game week.
    '''
    gw_points = []
    for formation in POSSIBLE_FORMATIONS:
        formation_points = {}
        formation_points['name'] = formation['NAME']
        formation_points['forwards'] = get_total_points_for_position('FWD', formation['FWD'], gw_data)
        formation_points['midfielders'] = get_total_points_for_position('MID', formation['MID'], gw_data)
        formation_points['defenders'] = get_total_points_for_position('DEF', formation['DEF'], gw_data)
        formation_points['total_points'] = formation_points['forwards'] + formation_points['midfielders'] + formation_points['defenders']
        gw_points.append(formation_points)
    return gw_points


def get_all_formation_points_for_season(year):
    '''
    Calculates the max score for all possible formations in a season.

    Args:
        year (str): season for which the total scores are to be calculated

    Returns:
        pd.Dataframe: total scores for all possible formations in the given season.
    '''
    print('Gathering formation stats for season: ' + year)
    season_points = pd.DataFrame()
    season_data = gen_season_dataset(year)
    for i in range(1, 39):
        gw_data = season_data[season_data['round'] == i][['element', 'name', 'position', 'total_points']]
        gw_data = gw_data.sort_values(['position', 'total_points'], ascending=False).groupby('position').head(5)
        gw_points = pd.DataFrame(get_points_for_all_formations(gw_data))
        gw_points.insert(len(gw_points.columns) - 1, 'round', i)
        season_points = season_points.append(gw_points)
    return season_points


def gen_formations_data(years):
    '''
    Creates a seperate csv file consisting of max points scored by all possible
    formations, per game week for all seasons.

    Args:
        years (list): Seasons for which formations data is to be extracted
    '''
    formations_dataset = pd.DataFrame()
    for year in years:
        season_points = get_all_formation_points_for_season(year)
        season_points.insert(len(season_points.columns) - 1, 'year', year)
        formations_dataset = formations_dataset.append(season_points)
    formations_dataset.to_csv(FORMATIONS_DATASET_LINK, mode='w', header=True)
