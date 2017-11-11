import json
from trueskill import Rating, rate_1vs1


def calculate_places(racers_dict):
    leaderboards_list = [{'name': key, 'exposure': value.exposure, 'mu': value.mu} for key, value in
                         racers_dict.items()]
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
    if winner == '1':
        racers_list[player_1], racers_list[player_2] = rate_1vs1(racers_list[player_1], racers_list[player_2])
    elif winner == '2':
        racers_list[player_2], racers_list[player_1] = rate_1vs1(racers_list[player_2], racers_list[player_1])
    return racers_list


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
                for i in range(3):
                    calculate_mmr(race, racers)
            else:
                calculate_mmr(race, racers)

except FileNotFoundError:
    leaderboard = calculate_places(racers)
    with open('leaderboard.json', 'w') as output:
        json.dump(leaderboard, output, indent=2)
    print("Place    Name    TrueSkill")
    for record in leaderboard:
        print(f"{record['place']}   {record['name']}    {round(record['exposure'], 2)}")
