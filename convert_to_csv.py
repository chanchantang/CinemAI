import pandas as pd
import os

file_names = ['title.basics', 'title.ratings', 'title.crew', 'name.basics']


def convert():
    did_convert = False
    for name in file_names:
        if not os.path.isfile('movie-data/' + name + '.csv.gz'):
            if not did_convert:
                did_convert = True
                print(' <some data not found>')

            print(' <' + name + '> not found: converting')
            (pd.read_csv('data/' + name + '.tsv.gz', sep='\t', low_memory=False)).to_csv('movie-data/' + name + '.csv.gz', index=False, compression='gzip')
            print(' ~converted <' + name + '> to csv')

    if not did_convert:
        print(' <all data found>')
