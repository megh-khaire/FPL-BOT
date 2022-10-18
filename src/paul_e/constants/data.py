RAW_DATASET_LINK = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data"

INITIAL_DATASET_LINK = "resources/seasons/initial"

FORMATIONS_DATASET_LINK = "resources/formations/max_formation_scores.csv"

YEARS = ['2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22']

POSITIONS = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}

INIT_DATA_COLUMNS = ["element", "name", "round", "assists", "goals_scored", "goals_conceded", "bonus", "bps", "clean_sheets", "red_cards", "yellow_cards", "saves",
                     "minutes", "value", "creativity", "ict_index", "influence", "selected", "threat", "transfers_in", "transfers_out", "total_points"]

AVG_DATA_COLUMNS = ["assists", "goals_scored", "clean_sheets", "saves", "goals_conceded", "bonus", "red_cards", "yellow_cards", "minutes", "total_points"]

GENERATED_DATA_COLUMNS = ["team", "position"]

FINAL_DATA_COLUMNS = ["element", "name", "round", "year", "value", "selected", "transfers_in", "transfers_out", "minutes", "goals_scored", "assists", "clean_sheets",
                      "goals_conceded", "yellow_cards", "red_cards", "saves", "bonus", "bps", "influence", "creativity", "threat", "ict_index", "was_home",
                      "opponent_team", "team", "position", "fixture_difficulty", "total_points", "next_gw_points"]

POSSIBLE_FORMATIONS = [{"NAME": "3-4-3", "DEF": 3, "MID": 4, "FWD": 3},
                       {"NAME": "3-5-2", "DEF": 3, "MID": 5, "FWD": 2},
                       {"NAME": "4-3-3", "DEF": 4, "MID": 3, "FWD": 3},
                       {"NAME": "4-4-2", "DEF": 4, "MID": 4, "FWD": 2},
                       {"NAME": "4-5-1", "DEF": 4, "MID": 5, "FWD": 1},
                       {"NAME": "5-2-3", "DEF": 5, "MID": 2, "FWD": 3},
                       {"NAME": "5-3-2", "DEF": 5, "MID": 3, "FWD": 2},
                       {"NAME": "5-4-1", "DEF": 5, "MID": 4, "FWD": 1}]
