# BoIR-trueskill

This is a series of Python 3.6.1 scripts to compile a [TrueSkill](http://trueskill.org/) leaderboard for [The Binding of Isaac: Afterbirth+](http://store.steampowered.com/app/250900/The_Binding_of_Isaac_Rebirth/) based on tournament match-ups.

The "json_creator.py" script will import brackets from [Challonge](http://challonge.com/). For this to work, you'll need to first copy the `.env_template` file to `.env` and then paste in your Challonge API key into the API_KEY variable.

The "main.py" script will go through the JSON files in the "tournaments" directory in order, calculating TrueSkill as it goes along.
