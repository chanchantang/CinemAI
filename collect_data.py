import pandas
import pandas as pd
import string
from statsmodels.nonparametric.smoothers_lowess import lowess


def replace_directors(directors):
    nameBasics = pd.read_csv('name.basics.csv.gz', index_col=0, compression='gzip')
    nameBasics = nameBasics.drop(['birthYear', 'deathYear', 'primaryProfession', 'knownForTitles'], axis=1)
    nameDict = nameBasics.to_dict()
    for each in directors:
        each = nameDict[each]


def collect():
    # Read basic data & only have movie data
    titleBasics = pd.read_csv('title.basics.csv.gz', index_col=0, low_memory=False, compression='gzip')
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
    titleRatings = pd.read_csv('title.ratings.csv.gz', index_col=0, compression='gzip')
    titleRatings = titleRatings[titleRatings['numVotes'] > 49]
    movies = titleBasics.join(titleRatings)

    # Import and join director data
    titleCrew = pd.read_csv('title.crew.csv.gz', index_col=0, compression='gzip')
    titleCrew = titleCrew.drop(['writers'], axis=1)
    movies = movies.join(titleCrew)
    movies = movies[movies['directors'] != '\\N']

    # Drop movies with no rating and/or directors
    movies = movies.dropna()

    # Convert genre and directors to lists
    movies['genres'] = movies['genres'].str.split(',')
    movies['directors'] = movies['directors'].str.split(',')

    # Loess filtered additional set
    measurements = movies['averageRating'].values.tolist()
    input_range = movies['startYear'].values.tolist()
    filtered = lowess(measurements, input_range, frac=0.1)
    filter_df = pandas.DataFrame(filtered).set_index(0)

    # Split into 90/10 subsets
    movies90 = movies.sample(frac=0.9, random_state=1)
    movies10 = movies.drop(movies90.index)

    movies90.to_csv('movies90.csv.gz', compression='gzip')
    movies10.to_csv('movies10.csv.gz', compression='gzip')
    filter_df.to_csv('loess_year_by_rating.csv.gz', compression='gzip', header=None)
    return movies90, movies10, filter_df
