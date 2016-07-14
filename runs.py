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


Now that I think about it, though, you can just calculate N different runs from the last N scores, and highlight the one with the biggest scoring difference.

So say N=5. Then as the game goes on, you've got 5 scoring runs for the last 5 times a team scored. And one of those is going to have the highest point differential, and thus be the most interesting.
You can then have a second tuning parameter that checks if this point differential is over some threshold.

xs = [2 4 6 8 10]; # nmins
v1 = [12.47 22.55 32.23 41.51 50.52]; # var(pts_home - pts_away)
# n.b. distribution is basically exactly normal: N(0, v1)
could fit a linear trend to xs and v1 to predict it for any nmins...
"""

import time
import numpy as np
import pandas as pd
SECS_PER_GAME = 4*12*60 + 5*60

class Runs:
    def __init__(self, nback=5, ptdiff_thresh=None, secs_thresh=0):
        self.rows = []
        self.nback = nback
        self.ptdiff_thresh = ptdiff_thresh
        self.secs_thresh = secs_thresh

    def update(self, row):
        self.rows.append(row)
        msgs = self.get_runs()
        return self.write_msgs(row, msgs)

    def write_msgs(self, row, msgs):
        if len(msgs) == 0:
            return
        outs = []
        for m in msgs:
            isT1 = m[0] > m[1]
            tm = row['Team1'] if isT1 else row['Team2']
            sc1 = m[0] if isT1 else m[1]
            sc2 = m[1] if isT1 else m[0]
            mmss = time.strftime("%M:%S", time.gmtime(m[2]))
            out = '{0} is on a {1}-{2} run in the last {3}.'.format(tm, int(sc1), int(sc2), mmss)
            outs.append(out)
        return outs

    def get_runs(self):
        rs = self.rows[:-self.nback:-1] # take last n and reverse
        ts = np.array([r['SecondsElapsed'] for r in rs])
        pts1 = np.array([r['pts_home'] for r in rs])
        pts2 = np.array([r['pts_away'] for r in rs])
        
        ps1 = pts1.cumsum()
        ps2 = pts2.cumsum()
        ts1 = np.hstack([0, np.abs(np.diff(ts))]).cumsum()
        out = np.array(zip(ps1, ps2, ts1, ps1-ps2))
        (P1i, P2i, Ti, PDi) = (0,1,2,3)

        # filter out anything but max
        v = np.abs(out[:,PDi]).max()
        ix = out[:,PDi] >= v
        out = out[ix,:]

        # filter out too low a pt differential
        if self.ptdiff_thresh is not None:
            ix = np.abs(out[:,PDi]) > self.ptdiff_thresh
            out = out[ix,:]

        # filter too short of a time
        out = out[out[:,Ti] > self.secs_thresh,:]

        # filter out nans
        ix = np.isnan(out).any(axis=1)
        out = out[~ix]

        return out

def load_game(d, score_keys, time_key):
    d = d.drop_duplicates(subset=score_keys)
    d = d.drop_duplicates(subset=time_key, keep='last') # e.g., free-throws

    # find points scored, indexed by elapsed_secs
    pdiff = lambda d: d[score_keys[0]].values - d[score_keys[1]].values
    d['pts_diff'] = pdiff(d)
    d['pts_home'] = d[score_keys[0]].diff()
    d['pts_away'] = d[score_keys[1]].diff()
    return d

def load_example(infile, score_keys=['Score1', 'Score2']):
    df = pd.read_csv(infile, delimiter='\t')
    df['SecondsElapsed'] = 60*df['MinutesRemaining'] + df['SecondsRemaining']
    for (game_id, dfc) in df.groupby('GameID'):
        dfg = load_game(dfc, score_keys=score_keys, time_key='SecondsElapsed')
        return dfg.T.to_dict().values()

def test():
    rows = load_example('data/input/playbyplay20120510040.tsv')
    R = Runs(nback=8, ptdiff_thresh=5)
    for (i, row) in enumerate(rows):
        msg = R.update(row)
        if msg:
            print '\n'.join(msg)
            print '-------'
        if i > 500:
            return

if __name__ == '__main__':
    test()

