import sys
import glob
import os.path
from basketball import aggregate_on_minutes

def convert(infile, outfile=None):
    if outfile is None:
        outfile = infile.replace('.txt', '.tsv')
    aggregate_on_minutes(fin=infile, fout=outfile)

def convert_all(indir):
    for infile in glob.glob(os.path.join(indir, '*.txt')):
        convert(infile)

if __name__ == '__main__':
    convert_all(sys.argv[1])
