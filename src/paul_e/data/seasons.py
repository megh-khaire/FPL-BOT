import numpy as np
import pandas as pd
import paul_e.constants.data as pcd
import paul_e.data.utils as pdu


def set_player_specific_features(dataset, year):
    '''
    Adds player position and team code to the given dataset.

    Args:
        dataset (pd.Dataframe): compiled data for a single season
        year (str): year (season) the data belongs to

    Returns:
        pd.Dataframe: modified dataframe containing player specific features
    '''
    player_features = ['id', 'team', 'element_type']
    player_data_file = f'{pcd.RAW_DATASET_LINK}/{year}/players_raw.csv'
    player_data = pdu.get_file_data(player_data_file, columns=player_features)
    # Convert team code to name
    team_codes_to_name = pdu.fetch_team_mapping(year)
    player_data['team'] = player_data["team"].map(team_codes_to_name)
    # Create a dictionary of player data
    player_data = player_data.set_index('id').to_dict('dict')
    # Extract team dictionary
    team_dict = player_data['team']
    # Insert team column
    dataset.insert(len(dataset.columns) - 1, "team", np.nan)
    dataset['team'] = dataset['element'].map(team_dict)
    # Extract position dictionary
    position_dict = player_data['element_type']
    # Insert position column
    dataset.insert(len(dataset.columns) - 1, "position", np.nan)
    dataset['position'] = dataset['element'].map(position_dict)
    dataset['position'] = dataset['position'].map(pcd.POSITIONS)
    # Drop null entries
    dataset.dropna(inplace=True)
    dataset.reset_index(drop=True, inplace=True)
    return dataset


def remove_2019_20_irregularities(dataset):
    '''
    Removes irregularities from the 2019-20 PL season dataset

    Args:
        dataset (pd.Dataframe): 2019-20 PL season dataset

    Returns:
        pd.Dataframe: modified dataframe without irregularities
    '''
    print("Removing irregularities from season 2019-20")
    dataset['round'] = dataset['round'].apply(lambda x: x - 9 if x > 29 else x)
    return dataset


def perform_season_specific_modifications(dataset, year):
    '''
    Performs year specific modifications to the dataset

    - For year 2019-20 removes all COVID affected GWs

    Args:
        dataset (pd.Dataframe): compiled data for a single season
        year (str): year (season) the data belongs to

    Returns:
        pd.Dataframe: modified dataframe with year specific changes
    '''
    if year == '2019-20':
        return remove_2019_20_irregularities(dataset)
    else:
        return dataset


def clean_initial_data(dataset, points_val=38, min_val=525):
    '''
    Groups dataset by id and removes players with total_points less than points_val
    and total minutes less than min_val. Removes entries where players have been
    rested for the match.

    Args:
        dataset (pd.Dataframe): compiled data for a single season
        points_val (int): Minimum required season points
        min_val (int): Minimum required season playtime (in minutes)

    Returns:
      pd.Dataframe: cleaned dataframe
    '''
    aggregated_dataset = dataset.groupby(['element'])[['total_points', 'minutes']].sum()
    # Create a list of all players with total points less than required
    points_deficit = aggregated_dataset.query(f"total_points < {points_val}").index.values.tolist()
    # Create a list of all players with total minutes less than required
    minutes_deficit = aggregated_dataset.query(f"minutes < {min_val}").index.values.tolist()
    # Remove deficit players from dataframe
    deficit_elements = list(set(points_deficit + minutes_deficit))
    print("Total players removed: ", len(deficit_elements))
    dataset = dataset[~(dataset['element'].isin(deficit_elements))]
    # Remove all entries where players have been rested for the GW
    dataset.reset_index(drop=True, inplace=True)
    return dataset


def gen_initial_dataset(years):
    '''
    For each season creates a seperate csv file consisting of data
    compiled from each gameweek

    Args:
      years (list): Seasons for which raw data is to be extracted
    '''
    for year in years:
        print("Gathering stats for season: " + year)
        seasons_dataset_file = f'{pcd.INITIAL_DATASET_LINK}/{year}_season_stats.csv'
        dataset = pd.DataFrame()
        for i in range(1, 39):
            if year == '2019-20' and i > 29:
                initial_dataset_link = f"{pcd.RAW_DATASET_LINK}/{year}/gws/gw{i+9}.csv"
            else:
                initial_dataset_link = f"{pcd.RAW_DATASET_LINK}/{year}/gws/gw{i}.csv"
            gw_data = pdu.get_file_data(initial_dataset_link, drop_columns=pcd.GENERATED_DATA_COLUMNS)
            gw_data.insert(len(gw_data.columns) - 1, "year", year)
            dataset = dataset.append(gw_data)
        dataset = perform_season_specific_modifications(dataset, year)
        dataset = clean_initial_data(dataset)
        dataset = set_player_specific_features(dataset, year)
        dataset.to_csv(seasons_dataset_file, mode='w', header=True)


gen_initial_dataset(pcd.YEARS)
