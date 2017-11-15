import json
from trueskill import Rating, rate_1vs1


def calculate_places(racers_dict):
    leaderboards_list = [{'name': key, 'exposure': value.exposure, 'mu': value.mu, 'sigma': value.sigma}
                         for key, value in racers_dict.items()]
    leaderboards_list.sort(key=lambda x: x['exposure'], reverse=True)
    for place, player in enumerate(leaderboards_list):
        player['place'] = place + 1
    return leaderboards_list


def calculate_mmr(matchup, racers_list):
    player_1 = matchup['player 1'].lower()
    player_2 = matchup['player 2'].lower()
    winner = matchup['winner']
    if player_1 not in racers_list:
        racers_list[player_1] = Rating(25)
    if player_2 not in racers_list:
        racers_list[player_2] = Rating(25)
    old_exposure_1 = racers_list[player_1].exposure
    old_exposure_2 = racers_list[player_2].exposure
    if winner == '1':
        racers_list[player_1], racers_list[player_2] = rate_1vs1(racers_list[player_1], racers_list[player_2])
        if debug:
            print(player_1 + ' ' + player_2 + ' ' + str(racers_list[player_1].exposure) + ' ' + str(
                racers_list[player_2].exposure) + ' +' + str(
                racers_list[player_1].exposure - old_exposure_1) + ' ' + str(
                racers_list[player_2].exposure - old_exposure_2))
    elif winner == '2':
        racers_list[player_2], racers_list[player_1] = rate_1vs1(racers_list[player_2], racers_list[player_1])
        if debug:
            print(player_2 + ' ' + player_1 + ' ' + str(racers_list[player_2].exposure) + ' ' + str(
                racers_list[player_1].exposure) + ' +' + str(
                racers_list[player_2].exposure - old_exposure_2) + ' ' + str(
                racers_list[player_1].exposure - old_exposure_1))
    return racers_list


def print_leaderboard(leaderboard_json):
    max_name_length = 0
    for record in leaderboard_json:
        if len(str(record['name'])) > max_name_length:
            max_name_length = len(str(record['name']))
    print('Place  ' + 'Name' + (max_name_length - 2) * ' ' + 'Trueskill')
    print('-' * 6 + '-' * max_name_length + '-' * 12)
    for record in leaderboard_json:
        place = str(record['place'])
        name = record['name']
        exposure = str(round(record['exposure'], 2))
        print('#' + place + (5 - len(place)) * ' ' + ' ' + name + (max_name_length - len(name) + 2) * ' ' + exposure)


debug = False  # Changing to True will cause printing out exposure change for each match up
racers = {}
try:
    n = 0
    while True:
        n = n + 1
        with open('tournaments/' + str(n) + '.json') as datafile:
            tournament_data = json.load(datafile)
        race_list = tournament_data['matchups']
        for race in race_list:
            if tournament_data['ruleset'] == 'seeded':
                if debug:
                    print('seeded')
                for i in range(4):
                    calculate_mmr(race, racers)
            elif tournament_data['ruleset'] == 'mixed':
                if debug:
                    print('mixed')
                for i in range(2):
                    calculate_mmr(race, racers)
            else:
                if debug:
                    print('unseeded')
                calculate_mmr(race, racers)

except FileNotFoundError:
    leaderboard = calculate_places(racers)
    with open('leaderboard.json', 'w') as output:
        json.dump(leaderboard, output, indent=2)
    print_leaderboard(leaderboard)
