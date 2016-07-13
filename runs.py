"""
data source: http://basketballvalue.com/downloads.php

t in (0,48)
A run, R(t,d)=(Pf, Pa), a function of the current time and an elapsed time, returns a scoring pair of points for and points against.

Can build up a histogram of empirical values of R, call it Rp, for all values of d. Rp(d) is a function of d only.

The demon reports if the current val of R(t,d) during a game passes some percentile of the empirical distribution Rp(d).

BUT wait!
It turns out scoring in the last X minutes is basically perfectly symmetric. So really our run detection is just going to be an AND: Team1 has scored _less_ than some amount, while Team2 has score _more_ than some amount.

So for the last X mins, the mean number of points scored is ~Y

 X: Y
 -----
 2: 5
 4: 9
 6: 13
 8: 18
 10: 22

which is basically Y = round(2.2*X)
"""
