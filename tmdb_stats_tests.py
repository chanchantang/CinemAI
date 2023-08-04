"""
This python class purpose is to make statistcal test on the tmdb ( kaggles) movie dataframe
It has much less movies to compare but still alot (around 5k movies)
We will proceed to see if there's any significant relationship between the genre and the budget,
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def check_normality(data):
    # extract the budget data
    budget = data['budget']

    # create a copy of the budget data
    budget_transformed = budget.copy()

    # add a small positive constant to the budget data
    budget_transformed += 1

    # apply the log transformation
    budget_transformed = np.log(budget_transformed)

    # remove outliers from the data
    lower_bound = 10
    budget_transformed = budget_transformed[budget_transformed > lower_bound]

    # create a histogram of the transformed budget data
    plt.hist(budget_transformed, bins=30)
    plt.title('Histogram of Transformed Budget Data')
    plt.show()


def create_genre_dict(tmdb5000):
    # create an empty dictionary to store the mapping of genre IDs to names
    genre_dict = {}

    # iterate over each row in the tmdb5000 DataFrame
    for index, row in tmdb5000.iterrows():
        # get the genres for this row
        genres = eval(row['genres'])
        
        # iterate over each genre in the list of genres
        for genre in genres:
            # get the genre ID and name
            genre_id = genre['id']
            genre_name = genre['name']
            
            # add the mapping of genre ID to name to the dictionary
            genre_dict[genre_id] = genre_name
    
    return genre_dict

def convert_genres(tmdb, genre_dict):
    # create a copy of the tmdb DataFrame
    tmdb_genres = tmdb.copy()

    # define a function to convert a list of genre IDs into a list of genre names
    def convert_genre_ids(genre_ids):
        # use the genre_dict to convert the genre IDs into genre names
        genre_names = [genre_dict[genre_id] for genre_id in eval(genre_ids)]
        return genre_names

    # apply the convert_genre_ids function to the genres column of the tmdb_genres DataFrame
    tmdb_genres['genres'] = tmdb_genres['genres'].apply(convert_genre_ids)
    
    return tmdb_genres

def drop_columns(tmdb_genres, columns_to_drop):
    # drop the columns from the tmdb_genres DataFrame
    tmdb_genres = tmdb_genres.drop(columns=columns_to_drop)
    tmdb_genres = tmdb_genres.drop(columns=['Unnamed: 0'])
    
    return tmdb_genres

def anova_test(data):
    # create a list to store the budget data for each genre
    budget_data = []
    genres_list = []

    # get the unique genres in the data
    genres = data['genres'].unique()

    # iterate over each genre
    for genre in genres:
        # get the budget data for this genre
        budget = data[data['genres'] == genre]['budget']
        
        # add the budget data to the list
        budget_data.append(budget)
        genres_list.append(genre)

    # perform one-way ANOVA
    f_value, p_value = stats.f_oneway(*budget_data)

    # interpret the results
    alpha = 0.05
    if p_value < alpha:
        print('genre of a movie may have an impact on its budget')
    else:
        print('genre of a movie may not have a significant impact on its budget')
    
    # print mean budget for each genre
    for i in range(len(genres_list)):
        print(f"The mean budget for {genres_list[i]} is {np.mean(budget_data[i])}")



def main():
    # read the tmdb.csv file
    tmdb = pd.read_csv('tmdb.csv')

    # read the tmdb_5000_movies.csv file
    tmdb5000 = pd.read_csv('tmdb_5000_movies.csv')
    
    # create a dictionary that maps genre IDs to names
    genre_dict = create_genre_dict(tmdb5000)
    
    # create a new DataFrame that is a copy of the tmdb.csv file but with the converted genre names
    tmdb_genres = convert_genres(tmdb, genre_dict)
    
    # define the columns to drop
    columns_to_drop = ['keywords','cast','production_companies']
    
    # drop unnecessary columns from the DataFrame
    tmdb_genres = drop_columns(tmdb_genres, columns_to_drop)
    
    genres_explode_df = tmdb_genres.explode('genres')
    
    check_normality(genres_explode_df)
    anova_test(genres_explode_df)
    
  
    

if __name__ == '__main__':
    main()