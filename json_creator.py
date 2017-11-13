import json
import requests


def json_parser(matches, participants, tourney_id):
    parsed_json = {'name': tourney_id,
                   'challonge': 'http://challonge.com/' + tourney_id,
                   'ruleset': '',
                   'matchups': []
                   }
    for match in matches:
        match_data = match['match']
        parsed_json['matchups'].append({'player 1': match_data['player1_id'],
                                        'player 2': match_data['player2_id'],
                                        'winner': match_data['winner_id']})
    for participant in participants:
        participant_id = participant['participant']['id']
        participant_name = participant['participant']['name']

        for match in parsed_json['matchups']:
            if match['player 1'] == participant_id:
                match['player 1'] = participant_name
                if match['winner'] == participant_id:
                    match['winner'] = '1'
            if match['player 2'] == participant_id:
                match['player 2'] = participant_name
                if match['winner'] == participant_id:
                    match['winner'] = '2'
    print('json parsed successfully')
    return parsed_json


n = 0
while True:
    n = n + 1
    k = str(n)
    api_key = ''
    print('Type q to exit')
    tourney_id = input('enter the tournament id:')
    if tourney_id == 'q':
        break
    participants = requests.get('https://api.challonge.com/v1/tournaments/' + tourney_id + '/participants.json',
                                params={'api_key': api_key}).json()
    matches = requests.get('https://api.challonge.com/v1/tournaments/' + tourney_id + '/matches.json',
                           params={'api_key': api_key}).json()
    json_var = json_parser(matches, participants, tourney_id)
    with open('tournaments/' + k + '_unasigned.json', 'w') as data_file:
        json.dump(json_var, data_file, indent=2)
