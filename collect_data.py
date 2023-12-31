import sys
import pandas as pd
import os


def convert():
    did_convert = False
    file_names = ['title.basics', 'title.ratings', 'title.crew']

    #  Check if CSV file exists; if not, produce
    for name in file_names:
        if not os.path.isfile('raw-csv-data/' + name + '.csv.gz'):
            if not did_convert:
                did_convert = True
                print(' <some data not found>')

            print(' <' + name + '> not found: converting')
            (pd.read_csv('raw-tsv-data/' + name + '.tsv.gz', sep='\t', low_memory=False)).to_csv(
                'raw-csv-data/' + name + '.csv.gz', index=False, compression='gzip')
            print(' ~converted <' + name + '> to csv')

    if not did_convert:
        print(' <all data found>')
    return


def collect():
    # Read basic data & only have movie data
    titleBasics = pd.read_csv('raw-csv-data/title.basics.csv.gz', index_col=0, low_memory=False, compression='gzip')
    titleBasics = titleBasics[titleBasics['titleType'] == 'movie']

    # Remove movies with unknown release year, runtime, and genre
    titleBasics = titleBasics[titleBasics['startYear'] != '\\N']
    titleBasics = titleBasics[titleBasics['runtimeMinutes'] != '\\N']
    titleBasics = titleBasics[titleBasics['genres'] != '\\N']

    # Cast release year & runtime as integers
    titleBasics['startYear'] = titleBasics['startYear'].astype('int')
    titleBasics['runtimeMinutes'] = titleBasics['runtimeMinutes'].astype('int')

    # Only include movies released since 1995
    titleBasics = titleBasics[(titleBasics['startYear']) > 1994]

    # Remove excess data
    titleBasics = titleBasics.drop(['titleType', 'originalTitle', 'isAdult', 'endYear'], axis=1)

    # Import and join ratings data
    titleRatings = pd.read_csv('raw-csv-data/title.ratings.csv.gz', index_col=0, compression='gzip')
    titleRatings = titleRatings[titleRatings['numVotes'] > 49]
    movies = titleBasics.join(titleRatings)

    # Import and join director data
    titleCrew = pd.read_csv('raw-csv-data/title.crew.csv.gz', index_col=0, compression='gzip')
    titleCrew = titleCrew.drop(['writers'], axis=1)
    movies = movies.join(titleCrew)
    movies = movies[movies['directors'] != '\\N']

    # Drop movies with no rating and/or directors
    movies = movies.dropna()

    # Convert genre and directors to lists
    movies['genres'] = movies['genres'].str.split(',')
    movies['directors'] = movies['directors'].str.split(',')

    # Split into 90/10 subsets
    movies90 = movies.sample(frac=0.9, random_state=1)
    movies10 = movies.drop(movies90.index)

    movies90.to_csv('movies90.csv')
    movies10.to_csv('movies10.csv')
    return


def main():
    # Detect if additional argument is given
    if len(sys.argv) > 1:
        produce = sys.argv[1]
    else:
        produce = 'NA'

    print('<Checking if tsv files need to be converted>')
    convert()

    # If additional argument is given, produce data again
    # Else, only produce if data is missing
    if produce == 'produce':
        print('<forcing production of filtered 90/10 subsets>')
        collect()
    else:
        print('<Checking if filtered & 90/10 split data exists>')
        if not os.path.isfile('movies90.csv') or not os.path.isfile('movies10.csv'):
            print(' <collecting data into 90/10 subsets>')
            collect()
        else:
            print(' <data found>')


if __name__ == '__main__':
    main()
