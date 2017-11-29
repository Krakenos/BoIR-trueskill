import json
import glob
from trueskill import Rating, rate_1vs1

debug = False  # Changing to True will cause printing out exposure change for each match up
current_file = ''  # Global variable to track which file is being processed, used in name_check function


def main():
    racers = {}
    seeded_racers = {}
    unseeded_racers = {}

    # Looping through every file in the tournaments folder
    for infile in sorted(glob.glob('tournaments/*.json')):
        global current_file
        current_file = infile
        with open(infile) as datafile:
            tournament_data = json.load(datafile)
        race_list = tournament_data['matchups']

        # Looping through every race in the tournament
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

    mixed_leaderboard = calculate_places(racers)
    seeded_leaderboard = calculate_places(seeded_racers)
    unseeded_leaderboard = calculate_places(unseeded_racers)
    dump_json('leaderboards/mixed_leaderboard.json', mixed_leaderboard)
    dump_json('leaderboards/seeded_leaderboard.json', seeded_leaderboard)
    dump_json('leaderboards/unseeded_leaderboard.json', unseeded_leaderboard)
    print_leaderboard(mixed_leaderboard)


def calculate_places(racers_dict):
    # Creating leaderboard, sorting by exposure value
    leaderboards_list = [{'name': key, 'exposure': value.exposure, 'mu': value.mu, 'sigma': value.sigma}
                         for key, value in racers_dict.items()]
    leaderboards_list.sort(key=lambda x: x['exposure'], reverse=True)
    for place, player in enumerate(leaderboards_list):
        player['place'] = place + 1
    return leaderboards_list


def name_check(name, racers_dict):
    for key, value in racers_dict.items():
        if name.lower() == key.lower():
            if name != key:
                print(f'WARNING: expected name {key} got {name} in {current_file} file')
            return key
    return name


def calculate_mmr(matchup, racers_list):
    winner = name_check(matchup['winner'], racers_list)
    loser = name_check(matchup['loser'], racers_list)
    if winner not in racers_list:  # If the person doesn't have existing rating, assign rating of 25
        racers_list[winner] = Rating(25)
    if loser not in racers_list:
        racers_list[loser] = Rating(25)

    old_exposure_1 = racers_list[winner].exposure  # Variables for debug purpose
    old_exposure_2 = racers_list[loser].exposure

    if not (matchup['score'] == 'draw'):  # We want to ignore draws because they most likely are mistake in the json.

        # Adjusting trueskill
        racers_list[winner], racers_list[loser] = rate_1vs1(racers_list[winner], racers_list[loser])

    if debug:

        # Printing out every change in the exposure value
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


if __name__ == '__main__':
    main()
