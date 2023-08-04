import pandas as pd
import pandas

from imdb_stats_method import (
    chi_square_test, u_test, test_normality, anova, linear_regression , tukey_hsd,regression_rating_runtime,regression_rating_year)



def literal_eval(x):
    return x.strip("[]").replace("'","").split(", ")

def main():      
    imdb_df = pd.read_csv(
        'movies90.csv',
        index_col=0,
        converters={'genres': lambda x: literal_eval(x), 'directors': lambda x: literal_eval(x)} # https://stackoverflow.com/a/53742380
    )
    
    genres_explode_df = imdb_df.explode('genres')
    directors_explode_df = genres_explode_df.explode('directors')
    
    "Performing Normality test to see which data is normally distributed"
    test_normality(genres_explode_df)
    
    "Found that only averageRating score is normally distributed, proceed with Anova "
    anova(genres_explode_df)
    
    "Anova found significant in average Rating, proceed with Tukey's HSD to compare each pair"
    tukey_hsd(genres_explode_df)

    """   
    "Performing regression between averageRating and Startyear
    to determine whether the average rating of movies tends to increase or decrease over time, 
    and whether the year of release can predict the average rating of a movie.
    """
    
    regression_rating_runtime(genres_explode_df)
    regression_rating_year(genres_explode_df)
    
    """
    Perfomring non parametric U test and Chi square test on data that is not proven to be normally distributed
    """
    u_test(genres_explode_df)
    chi_square_test(directors_explode_df)
    
    "Perform linear regression on year of release and the average rating to see their relationship"
    linear_regression(genres_explode_df)
    



if __name__ == '__main__':
    main()