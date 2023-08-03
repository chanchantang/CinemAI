import pandas as pd
from convert_to_csv import convert
from collect_data import collect
import os


def main():
    print('<Checking if tsv files need to be converted>')
    convert()

    print('<Checking if filtered & 90/10 split data exists>')
    if not os.path.isfile('movies90.csv.gz') or not os.path.isfile('movies10.csv.gz') or not os.path.isfile('loess_year_by_rating.csv.gz'):
            print(' <collecting data into two 90/10 subsets>')
            movies90, movies10, filtered = collect()
    else:
        print(' <data found & now reading>')
        movies90 = pd.read_csv('movies90.csv.gz', index_col=0, compression='gzip')
        movies10 = pd.read_csv('movies10.csv.gz', index_col=0, compression='gzip')
        filtered = pd.read_csv('loess_year_by_rating.csv.gz', index_col=0, compression='gzip', header=None)
    print(movies90)
    print(movies10)
    print(filtered)


if __name__ == '__main__':
    main()
