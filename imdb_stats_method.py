import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas
import statsmodels.api as sm


from scipy.stats import mannwhitneyu
from scipy.stats import chi2_contingency
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy import stats

def test_normality(movies):
    # define the columns to test
    columns = ['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']

    # create a copy of the DataFrame
    movies_transformed = movies.copy()


    # apply square root transformation in attempt to form a normal distribution
    for column in columns:
        movies_transformed[column] = np.log(movies_transformed[column])
        plt.hist(movies_transformed[column],bins = 30)
        plt.title(f'Histogram of {column}')
        plt.show()
        
def anova(movies):
    # split the data into groups based on genre
    groups = []
    for genre in movies['genres'].unique():
        group = movies[movies['genres'] == genre]['averageRating']
        groups.append(group)

    # perform one-way ANOVA
    f_value, p_value = stats.f_oneway(*groups)

    # check if the differences between groups are statistically significant
    print("ANOVA p_value :",p_value)
    if p_value < 0.05:
        print('Some genres tend to have higher or lower average ratings than others. Proceed to Post Hoc Analysis')
    else:
        print('The average rating of movies does not appear to depend on their genre.')        
        
def tukey_hsd(movies):
    # define the data and groups
    data = movies['averageRating']
    groups = movies['genres']

    result = pairwise_tukeyhsd(data, groups)
    print(result)

def regression_rating_year(movies):
    # define the response and predictor variables
    y = movies['averageRating']
    x = movies['startYear']

    # create a DataFrame containing the data
    data = pd.DataFrame({'y': y, 'x': x, 'one': 1})

    # fit the model
    results = sm.OLS(data['y'], data[['x', 'one']]).fit()

    # print the results
    print(results.summary())

def regression_rating_runtime(movies):
    # define the response and predictor variables
    y = movies['averageRating']
    x = movies['runtimeMinutes']

    # create a DataFrame containing the data
    data = pd.DataFrame({'y': y, 'x': x, 'one': 1})

    # fit the model
    results = sm.OLS(data['y'], data[['x', 'one']]).fit()

    # print the results
    print(results.summary())    

def chi_square_test(movies):
    # create a contingency table
    contingency_table = pd.crosstab(movies['directors'], movies['genres'])

    # perform the Chi-Square test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    alpha = 0.05
    print("Chi Square test p_value :",p_value)
    if p_value < alpha:
        print('Certain directors may be more likely to work on movies of certain genres.')
    else:
        print('Certain directors are not likely to work on movies of certain genres.')
        
        
def u_test(movies):
    # define the groups to compare
    group1 = movies[movies['genres'] == 'Adventure']['averageRating']
    group2 = movies[movies['genres'] == 'Action']['averageRating']

    # perform the Mann-Whitney U test
    u, p_value = mannwhitneyu(group1, group2)

    print("U test p_value :",p_value)

    alpha = 0.05
    if p_value < alpha:
        print('The average rating of Adventure movies is more diverse than Action Movie')
    else:
        print('The average rating of Adventure movies is not diverse as Action movie')

   

def linear_regression(movies):
    # extract the data
    "Linear regression does not require the independent variable startYear to be normally distributed"

    x = movies['startYear']
    y = movies['averageRating']

    # perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    print("Linear regression p_value :" , p_value)

    if p_value < 0.05:
        print('movies released in later years tend to have higher average ratings than movies released in earlier years')
    else:
        print('movies released in later years does not tend to have higher average ratings than movies released in earlier years')