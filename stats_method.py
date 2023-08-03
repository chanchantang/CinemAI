import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas


from convert_to_csv import convert
from collect_data import collect

from scipy import stats
from scipy.stats import mannwhitneyu
from scipy.stats import chi2_contingency

def chi_squared_test(movies):
    # create a contingency table
    contingency_table = pd.crosstab(movies['genres'], movies['directors'])

    # perform the chi-squared test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    # check if the differences between groups are statistically significant
    if p_value < 0.05:
        print('There is a significant association between genres and directors.')
    else:
        print('There is no significant association between genres and directors.')
        
        
def u_test(movies):
  
    
    column='averageRating'
    alpha=0.05
    # create a new DataFrame that only includes rows where the genres column contains a single value
    single_genre_movies = movies[movies['genres'].apply(lambda x: len(x) == 1)]

    # get the unique genres
    genres = single_genre_movies['genres'].unique()

    # compare each genre with all other genres
    for i, genre1 in enumerate(genres):
        for genre2 in genres[i+1:]:
            # define the groups to compare
            group1 = single_genre_movies[single_genre_movies['genres'] == genre1][column]
            group2 = single_genre_movies[single_genre_movies['genres'] == genre2][column]

            # perform the Mann-Whitney U test
            u, p_value = mannwhitneyu(group1, group2)

            # check if the differences between groups are statistically significant
            if p_value < alpha:
                print(f'{genre1} vs {genre2}: The {column} values are significantly different.')
            else:
                print(f'{genre1} vs {genre2}: The {column} values are not significantly different.')

def test_normality(movies):
    # define the columns to test
    columns = ['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']

    # set the significance level
    alpha = 0.05

    # create a copy of the DataFrame
    movies_transformed = movies.copy()


    # apply the square root transformation
    for column in columns:
        movies_transformed[column] = np.log(movies_transformed[column])

   

def anova(movies):
    # split the data into groups based on genre
    groups = []
    for genre in movies['genres'].unique():
        group = movies[movies['genres'] == genre]['averageRating']
        groups.append(group)

    # perform one-way ANOVA
    f_value, p_value = stats.f_oneway(*groups)

    # check if the differences between groups are statistically significant
    if p_value < 0.05:
        print('Some genres tend to have higher or lower average ratings than others.')
    else:
        print('The average rating of movies does not appear to depend on their genre.')
        
        
        

def linear_regression(movies):
    # extract the data
    x = movies['startYear']
    y = movies['averageRating']

    # perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    if p_value < 0.05:
        print('the average rating appear to consistently increase or decrease as the year of release changes.')
    else:
        print('the average rating does not appear to consistently increase or decrease as the year of release changes')