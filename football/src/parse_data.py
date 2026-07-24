from pathlib import Path
import pandas as pd
import json
import argparse

def parse_competitions(comp_file):
    comp_file = Path(comp_file)

    with open(comp_file, 'r') as f:
        comp_data = json.load(f)

    comp_list = []
    seasons_list = []

    for comp in comp_data:
        comp_dict = {
            'competition_id': comp['competition_id'],
            'competition_name': comp['competition_name'],
            'country_name': comp['country_name']
        }
        comp_list.append(comp_dict)

        seasons_dict = {
            'season_id': comp['season_id'],
            'season_name': comp['season_name'],
            'competition_id': comp['competition_id']
        }

        seasons_list.append(seasons_dict)

    comp_df = pd.DataFrame(comp_list)
    seasons_df = pd.DataFrame(seasons_list)

    comp_df["competition_name"] = comp_df["competition_name"].str.replace(r"^\d+\.\s*", "", regex=True)

    seasons_df = seasons_df.drop_duplicates(subset=["season_id"])
    comp_df = comp_df.drop_duplicates(subset=["competition_id"])

    return (comp_df, seasons_df)


def parse_lineups(lineups_dir):
    lineups_dir = Path(lineups_dir)

    players_list = []
    countries_list = []
    lineups_list = []
    positions_list = []
    cards_list = []

    for item in lineups_dir.iterdir():
        if item.suffix == ".json":
            match_id = int(item.stem)

            with open(item, 'r') as f:
                data = json.load(f)

            for team in data:
                for player in team['lineup']:
                    country = player.get("country") or {}

                    player_dict = {
                        'player_id': player['player_id'],
                        'player_name': player['player_name'],
                        'country_id': country.get('id')
                         }
                    lineup_dict = {
                        'match_id': match_id,
                        'team_id': team['team_id'],
                        'player_id': player['player_id'],
                        'jersey_number': player['jersey_number']
                         }
                    countries_dict = {
                        'country_id': country.get('id'),
                        'country_name': country.get('name')
                        }
                    players_list.append(player_dict)
                    lineups_list.append(lineup_dict)
                    countries_list.append(countries_dict)

                    for position in player["positions"]:
                        position_dict = {
                            'match_id': match_id,
                            'player_id': player['player_id'],
                            'position_id': position['position_id'],
                            'position_name': position['position'],
                            'from_time': position['from'],
                            'to_time': position['to'],
                            'from_period': position['from_period'],
                            'to_period': position['to_period'],
                            'start_reason': position['start_reason'],
                            'end_reason': position['end_reason']
                        }
                        positions_list.append(position_dict)
                    for card in player["cards"]:
                        cards_dict = {
                            'match_id': match_id,
                            'player_id': player['player_id'],
                            'card_time': card['time'],
                            'card_type': card['card_type'],
                            'reason': card['reason'],
                            'period': card['period']
                         }
                        cards_list.append(cards_dict)

    players_df = pd.DataFrame(players_list)
    lineups_df = pd.DataFrame(lineups_list)
    countries_df = pd.DataFrame(countries_list)
    positions_df = pd.DataFrame(positions_list)
    cards_df = pd.DataFrame(cards_list)

    players_df = players_df.drop_duplicates(subset=['player_id']).reset_index(drop=True)

    countries_df = countries_df.dropna(subset=["country_id"])
    countries_df = countries_df.drop_duplicates(subset=['country_id']).reset_index(drop=True)

    return (players_df, countries_df, lineups_df, positions_df, cards_df)


def parse_matches(matches_dir):
    matches_dir = Path(matches_dir)

    matches_list = []
    teams_list = []
    managers_list = []
    team_managers_list = []

    for item in matches_dir.rglob("*.json"):
        with open(item, 'r') as f:
            match_data = json.load(f)

        for match in match_data:
            matches_dict = {
                'match_id': match['match_id'],
                'match_date': match['match_date'],
                'match_week': match['match_week'],
                'home_score': match['home_score'],
                'away_score': match['away_score'],
                'home_team_id': match['home_team']['home_team_id'],
                'away_team_id': match['away_team']['away_team_id'],
                'competition_id': match['competition']['competition_id'],
                'season_id': match['season']['season_id'],
                'competition_stage': match['competition_stage']['id']
            }
            matches_list.append(matches_dict)

            for team_key, team_id_key, team_name_key in [('home_team', 'home_team_id', 'home_team_name'), ('away_team', 'away_team_id', 'away_team_name')]:
                team = match[team_key]

                teams_dict = {
                    'team_id': team[team_id_key],
                    'team_name': team[team_name_key]
                }
                teams_list.append(teams_dict)

                for manager in team.get('managers', []):
                    managers_dict = {
                        'manager_id': manager['id'],
                        'manager_name': manager['name'],
                        'nickname': manager['nickname'],
                        'date_of_birth': manager['dob'],
                        'country_id': manager['country']['id'],
                        'country_name': manager['country']['name']
                    }
                    managers_list.append(managers_dict)

                    team_managers_dict = {
                        'match_id': match["match_id"],
                        'team_id': team[team_id_key],
                        'manager_id': manager['id']
                    }
                    team_managers_list.append(team_managers_dict)

    matches_df = pd.DataFrame(matches_list)
    teams_df = pd.DataFrame(teams_list)
    managers_df = pd.DataFrame(managers_list)
    team_managers_df = pd.DataFrame(team_managers_list)

    teams_df = teams_df.drop_duplicates(subset=['team_id']).reset_index(drop=True)
    managers_df = managers_df.drop_duplicates(subset=["manager_id"]).reset_index(drop=True)

    return (matches_df, teams_df, managers_df, team_managers_df)


def parse_all(data_dir):
    data_dir = Path(data_dir)

    comp_df, seasons_df = parse_competitions(data_dir/"competitions.json")
    players_df, countries_df, lineups_df, positions_df, cards_df = parse_lineups(data_dir/"lineups")
    matches_df, teams_df, managers_df, team_managers_df = parse_matches(data_dir/"matches")

    return {
        'competitions': comp_df,
        'seasons': seasons_df,
        'matches': matches_df,
        'teams': teams_df,
        'managers': managers_df,
        'team_managers': team_managers_df,
        'players': players_df,
        'countries': countries_df,
        'lineups': lineups_df,
        'player_positions': positions_df,
        'cards': cards_df
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse StatsBomb football data")

    parser.add_argument("--data-dir", required=True, help="Path to the raw StatsBomb data directory")

    args = parser.parse_args()

    tables = parse_all(args.data_dir)

    for table_name, dataframe in tables.items():
        print(table_name, dataframe.shape)
