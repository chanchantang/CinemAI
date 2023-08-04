# CMPT 353 Final Project
Danny (301449063)<br>
Matthew (301430325)<br>
Chanson (301429611)<br>

## IMDb Data
The dataset is too large to be stored on github. The original data is in a TSV format, but we reformat it to CSV for convenience. The converion runtime can be long.

To download the original TSV (which would make the data collection convert it to CSV) [use this link](https://drive.google.com/file/d/1JoKgJM8xrNt--sZ9zWDbRpJMHgE_C01k/view?usp=sharing).

Else, to download the converted CSV data, [use this link](https://drive.google.com/file/d/1qbzchb2LG0dwYFOtvLQ5te8jl3sZU8qH/view?usp=sharing).

**Both datasets are required to be in a folder directory of the same ZIP file name**<br>
(either raw-tsv-data/ or raw-csv-data/)

## Data Analysis
1. Run collect_data.py to clean and collect the data<br>
>The data produced by this already exists for convenience & will not reproduce the files again unless it is missing. However, you can force it to reproduce the files through providing an additional argument:

```
python collect_data.py produce
```
2. Run the imdb.ipynb notebook to gain access to the general analysis of IMDb's data
3. Run the imdb_stats_tests.py to see the detailed statistical analysis of IMDb's data.

## TMDb Data
Acquired from https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

1. Run the tmdb_stats_tests.py to see more statistical tests on the tmdb data in lieu of imdb data.
2. Run the tmdb.ipnb notebook for our movie success machine learning model.
