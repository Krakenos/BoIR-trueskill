import json
import glob
from trueskill import Rating, rate_1vs1


def calculate_places(racers_dict):
    leaderboards_list = [{'name': key, 'exposure': value.exposure, 'mu': value.mu, 'sigma': value.sigma}
                         for key, value in racers_dict.items()]
    leaderboards_list.sort(key=lambda x: x['exposure'], reverse=True)
    for place, player in enumerate(leaderboards_list):
        player['place'] = place + 1
    return leaderboards_list


def calculate_mmr(matchup, racers_list):
    winner = matchup['winner'].lower()
    loser = matchup['loser'].lower()
    if winner not in racers_list:
        racers_list[winner] = Rating(25)
    if loser not in racers_list:
        racers_list[loser] = Rating(25)
    old_exposure_1 = racers_list[winner].exposure
    old_exposure_2 = racers_list[loser].exposure
    if not (matchup['score'] == 'draw'):
        racers_list[winner], racers_list[loser] = rate_1vs1(racers_list[winner], racers_list[loser])
    if debug:
        print(winner + ' ' + loser + ' ' + str(racers_list[winner].exposure) + ' ' + str(
            racers_list[loser].exposure) + ' +' + str(
            racers_list[winner].exposure - old_exposure_1) + ' ' + str(
            racers_list[loser].exposure - old_exposure_2))

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


def dump_json(filename, data):
    with open(filename, 'w') as output:
        json.dump(data, output, indent=2)


debug = False  # Changing to True will cause printing out exposure change for each match up
racers = {}
seeded_racers = {}
unseeded_racers = {}
for infile in sorted(glob.glob('tournaments/*.json')):
    with open(infile) as datafile:
        tournament_data = json.load(datafile)
    race_list = tournament_data['matchups']
    for race in race_list:
        if tournament_data['ruleset'] == 'seeded':
            if debug:
                print('seeded')
            for i in range(4):
                calculate_mmr(race, racers)
            calculate_mmr(race, seeded_racers)
        elif tournament_data['ruleset'] == 'mixed':
            if debug:
                print('mixed')
            for i in range(2):
                calculate_mmr(race, racers)
            calculate_mmr(race, unseeded_racers)
        elif tournament_data['ruleset'] == 'other':
            continue
        else:
            if debug:
                print('unseeded')
            calculate_mmr(race, racers)
            calculate_mmr(race, unseeded_racers)

leaderboard = calculate_places(racers)
seeded_leaderboard = calculate_places(seeded_racers)
unseeded_leaderboard = calculate_places(unseeded_racers)
dump_json('leaderboard.json', leaderboard)
dump_json('seeded_leaderboard.json', seeded_leaderboard)
dump_json('unseeded_leaderboard.json', unseeded_leaderboard)
print_leaderboard(leaderboard)
