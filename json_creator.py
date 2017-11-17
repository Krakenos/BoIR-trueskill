import json
import requests


def json_parser(tournament, date):
    date_array = date.split('-', 2)
    matches = tournament['matches']
    participants = tournament['participants']
    parsed_json = {"name": tournament['name'],
                   "challonge": tournament['full_challonge_url'],
                   "date": date_array[2] + '-' + date_array[1] + '-' + date_array[0],
                   "organizer": "",
                   "description": "",
                   "ruleset": "",
                   "matchups": []
                   }
    for match in matches:
        match_data = match['match']
        if match_data['winner_id'] is None:
            parsed_json["matchups"].append({"winner": match_data['player1_id'],
                                            "loser": match_data['player2_id'],
                                            "score": "draw"})
        else:
            parsed_json["matchups"].append({"winner": match_data['winner_id'],
                                            "loser": match_data['loser_id'],
                                            "score": match_data['scores_csv']})
    for participant in participants:
        participant_id = participant['participant']['id']
        participant_name = participant['participant']['name']
        for match in parsed_json["matchups"]:
            if match['winner'] == participant_id:
                match['winner'] = participant_name
            if match['loser'] == participant_id:
                match['loser'] = participant_name
    print("json parsed successfully")
    return parsed_json


while True:
    api_key = ''
    print('Type q to exit')
    tourney_id = input('enter the tournament id:')
    if tourney_id == 'q':
        break
    tourney = requests.get('https://api.challonge.com/v1/tournaments/' + tourney_id + '.json',
                           params={'api_key': api_key, 'include_participants': 1, "include_matches": 1}).json()
    tourney_data = tourney['tournament']
    date = tourney_data['started_at'].split('T', 1)[0]  # YYYY-MM-DD
    json_var = json_parser(tourney_data, date)
    with open('tournaments/' + date + ' ' + tourney_data['name'] + '.json', 'w') as data_file:
        json.dump(json_var, data_file, indent=2)
