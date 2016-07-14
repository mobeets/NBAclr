import sys
import os.path
import pandas as pd
import numpy as np
from dateutil import parser
from scipy.io import savemat

SECS_PER_GAME = 4*12*60 + 5*60

def old(d):
    dtp = lambda x: parser.parse(x)
    d['elapsed_secs_qtr'] = d['elapsed'].apply(lambda x: dtp(x).minute*60 + dtp(x).second)
    d['elapsed_secs'] = (d['period']-1)*12*60 + d['elapsed_secs_qtr']

def load_game(d, score_keys, time_key):
    # parse time; convert to total secs elapsed
    d = d.drop_duplicates(subset=score_keys)
    d = d.drop_duplicates(subset=time_key, keep='last') # e.g., free-throws

    # find points scored, indexed by elapsed_secs
    pdiff = lambda d: d[score_keys[0]].values - d[score_keys[1]].values
    d['pts_diff'] = pdiff(d)
    d['pts_home'] = d[score_keys[0]].diff()
    d['pts_away'] = d[score_keys[1]].diff()

    dscs = d[[time_key, 'pts_diff', 'pts_home', 'pts_away']]
    dscs = dscs.set_index([time_key], verify_integrity=True)
    dscs = dscs.reindex(xrange(SECS_PER_GAME), fill_value=0)
    return dscs

Rpf = lambda df, delta: df.rolling(window=delta, min_periods=delta, win_type='boxcar')

def hist2d(df, score_keys):
    vmx = int(df[score_keys].max().max())
    dfc = df[df[score_keys[0]].notnull() & df[score_keys[1]].notnull()]
    H, xedges, yedges = np.histogram2d(dfc['pts_home'].values, dfc['pts_away'].values, bins=(xrange(vmx), xrange(vmx)))
    return H, vmx

def load(infile, score_keys=['Score1', 'Score2'], nmins=5):
    d = pd.read_csv(infile, delimiter='\t')
    d['TotalSecsLeft'] = SECS_PER_GAME - (60*d['MinutesRemaining'] + d['SecondsRemaining'])
    # GameID	Year	Month	Day	Team1	Team2	MinutesRemaining	SecondsRemaining	TimeRemaining	Score1	Score2
    dfs = []
    for (game_id, dfc) in d.groupby('GameID'):
        # print game_id
        dfg = load_game(dfc, score_keys=score_keys, time_key='TotalSecsLeft')

        Rp = Rpf(dfg, 60*nmins).sum()
        ix = np.abs(dfg['pts_diff']) > 0 & Rp['pts_home'].notnull()
        Rp['GameID'] = game_id
        Rp['Team1'] = dfc['Team1'].values[0]
        Rp['Team2'] = dfc['Team2'].values[0]
        dfs.append(Rp[ix])

    df = pd.concat(dfs)
    # fnm = os.path.join('data', 'output', 'out_{0}.csv'.format(nmins))
    # df.to_csv(fnm)

    # (H, vmx) = hist2d(df, ['pts_home', 'pts_away'])
    # fnm = os.path.join('data', 'output', 'out_{0}_{1}.mat'.format(nmins, vmx))
    # savemat(fnm, {'H': H})

    vs = (df['pts_home'] - df['pts_away'])
    print (vs.mean(), vs.median(), vs.var())
    print (np.abs(vs).mean(), np.abs(vs).median(), np.abs(vs).var())

if __name__ == '__main__':
    # load(sys.argv[1], nmins=5)

    for nmins in [2, 4, 6, 8, 10]:
        print '-------'
        print nmins
        print '-------'
        load(sys.argv[1], nmins=nmins)
