"""
Script to extract per-minute data from http://basketballvalue.com play-by-plays.
Usage: python basketball.py (input_file output_file)
Author:  Elaine Angelino <elaine at eecs dot harvard dot edu>
Copyright 2011

source: http://www.eecs.harvard.edu/~elaine/sousvide/stories/basketball.html
"""

import sys
import tabular as tb

def aggregate_on_minutes(fin, fout):
	# load the play-by-play file
	# tb.tabarray automatically infers the delimiter ('\t'), column names in the
	# first row of the file, and data type of each column (str, int, or float)
	x = tb.tabarray(SVfile=fin)

	records = []
	prev_game_id = None
	prev_minutes_remaining = None
	prev_secs_remaining = None
	prev_time_remaining = None
	prev_rec = None

	# for each record in the play-by-play file
	for rec in x:
		# if we are at the start of a new game
		if (rec['GameID'] != prev_game_id):
			# record last minute of previous game
			if prev_rec is not None:
				records += [(game_id, year, month, day, team_1, team_2,
							 prev_minutes_remaining, prev_secs_remaining, prev_time_remaining, score_1, score_2)]

			# parse GameID information
			game_id = rec['GameID']
			year = int(game_id[:4])
			month = int(game_id[4:6])
			day = int(game_id[6:8])
			team_1 = game_id[8:11]
			team_2 = game_id[11:14]

			# initialize game score and minutes remaining
			minutes_remaining = 48
			secs_remaining = 0
			time_remaining = '00:48:00'
			score_1 = 0
			score_2 = 0

		else:
			minutes_remaining = int(rec['TimeRemaining'].split(':')[1])
			secs_remaining = int(rec['TimeRemaining'].split(':')[2])
			time_remaining = rec['TimeRemaining']

			# create a record for each minute of the game
			# if minutes_remaining != prev_minutes_remaining:
			if time_remaining != prev_time_remaining:
				records += [(game_id, year, month, day, team_1, team_2,
							 prev_minutes_remaining, prev_secs_remaining, prev_time_remaining, score_1, score_2)]

			# parse the play-by-play entry if it contains the current score
			# format:  '[ABC X-Y] Play-by-play details' where 'ABC' is the
			# identifier of the scoring team and 'X' is their current score, and
			# 'Y' is the current score of the other team
			entry = rec['Entry']
			if (entry[0] == '[') and (entry[5].isdigit()):

				# get the team identifier and scores
				team = entry[1:4]
				(a, b) = entry[5:].split(']')[0].split('-')

				# order the scores to match that of the teams in the GameID
				if (team == team_1):
					score_1 = a
					score_2 = b
				else:
					score_1 = b
					score_2 = a

		prev_game_id = rec['GameID']
		prev_minutes_remaining = minutes_remaining
		prev_secs_remaining = secs_remaining
		prev_time_remaining = time_remaining
		prev_rec = rec

	# create a tb.tabarray with our per-minute extracted data
	y = tb.tabarray(records=records,
					names=['GameID', 'Year', 'Month', 'Day', 'Team1', 'Team2',
						   'MinutesRemaining', 'SecondsRemaining', 'TimeRemaining', 'Score1', 'Score2'])

	# write out a delimited text file using tabular's default settings
	y.saveSV(fout)
