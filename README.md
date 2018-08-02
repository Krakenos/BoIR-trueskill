# The Binding of Isaac: Rebirth / Afterbirth / Afterbirth+ Tournament Leaderboards

This is a [historical archive](https://github.com/Krakenos/BoIR-trueskill/tree/master/tournaments) of every *[The Binding of Isaac: Rebirth*](http://store.steampowered.com/app/250900/The_Binding_of_Isaac_Rebirth/) tournament that has ever been played.

Furthermore, by using the [TrueSkill algorithm](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/NIPS2006_0688.pdf) on every 1v1 matchup, we can create a leaderboard for the top players.

The three leaderboards are as follows:

* [Seeded](https://github.com/Krakenos/BoIR-trueskill/blob/master/leaderboards/seeded_leaderboard.json)
  * This only uses matchups from [seeded](https://github.com/Zamiell/isaac-racing-client/blob/master/mod/CHANGES-RACES.md#seeded) tournaments.
* [Unseeded](https://github.com/Krakenos/BoIR-trueskill/blob/master/leaderboards/unseeded_leaderboard.json)
  * This only uses matchups from [unseeded](https://github.com/Zamiell/isaac-racing-client/blob/master/mod/CHANGES-RACES.md#unseeded) tournaments.
* [Mixed](https://github.com/Krakenos/BoIR-trueskill/blob/master/leaderboards/mixed_leaderboard.json)
  * This uses matchups from both seeded and unseeded, but seeded matchups are [weighted more](https://github.com/Krakenos/BoIR-trueskill/blob/master/leaderboard_creator.py#L10).

## More Information

* The scripts used are written in Python 3.6.1.
* The "tournament_json_creator.py" script will import brackets from [Challonge](http://challonge.com/). For this to work, you'll need to first copy the `.env_template` file to `.env` and then paste in your Challonge API key into the `API_KEY` variable.
* The "leaderboard_creator.py" script will go through the JSON files in the "tournaments" directory in order, calculating TrueSkill as it goes along.
