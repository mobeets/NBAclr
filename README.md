# NBAclr

The idea is, given a feed of live basketball data (e.g. SportVU, or just play-by-play, or maybe even just scoring or stats), to generate interesting commentary by way of statistics.

For example, if Harden shoots the ball and misses, a relevant stat might be "Harden is 0 for 7 when Howard is standing more than 5 feet away from him."

These comments could be tweeted while a game is going on, for example.

Resources:

* [Track player movements in Python](http://savvastjortjoglou.com/nba-play-by-play-movements.html)
* [Shot tracker synced with SportVu](https://www.reddit.com/r/nba/comments/2laprb/shot_tracker_syncd_with_new_sportvu_data/)

Example:

1. The system is told that Charlie V made a 3-pointer with 10 seconds left on the shot clock.
2. Checking the info on stats.nba.com for Charlie V tells us that Charlie V takes and makes more threes during the interval of 15-7 seconds on the clock more than any other time.
3. The system tweets "Charlie V takes and makes most of his threes when there's 15-7 seconds left on the shot clock."


