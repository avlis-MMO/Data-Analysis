from turtle import color
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# This script will show how the different genres of anime progressed through the years
# It will use beautiful soup to scrap info from the website myanimelist clean it and present line graphics

anime_genre = []
years = []
dic = {}
i = 0
arr_year = np.arange(2000, 2023, 1)
Anime_df = pd.DataFrame(columns=['Year', 'Anime Genres'])

# Run through all the pages based on the year and season 
for year in arr_year:
    for season in ['fall','winter','spring','summer']:
        url = 'https://myanimelist.net/anime/season/'+str(year)+'/'+season
        
        web_site = requests.get(url)
        soup = bs(web_site.text, 'html.parser')

        # Find the html section with the animes of the season
        Season_anime = soup.find("div",{"class":"seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1"})
        list_anime = Season_anime.find_all("div",{"class":"js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-1"})

        # Run through all the animes
        for anime in list_anime:
            
            # Find each genre in the anime
            for t in anime.find("div",{"class":"genres-inner js-genre-inner"}):
                genre = t.text.replace('\n','').replace(' ','').replace('-','')
                if len(genre) > 1:
                    anime_genre.append(genre)
    
    # Append to the empty dataframe the the year and the genre
    Anime_df.loc[i] = pd.Series({'Year': year, 'Anime Genres' :sorted(anime_genre)})
    i = i + 1
    anime_genre = []

# Transform all the genres inside of the dataframe from a list of lists to a single list
flat_list = [x for xs in Anime_df['Anime Genres'].to_list() for x in xs]

# Eliminate all repited genres and get a list with all the genres appearing once
list_genres = sorted(set(flat_list))

# Create new dataframe with a row for each year
Count_Anime_Genres = pd.DataFrame(arr_year, columns=['Year'])

# Add value od zero to all the cells on the dataframe besides the ones from column year
Count_Anime_Genres[list_genres] = np.zeros((len(arr_year),len(list_genres)))

# Iterate through each row of the first dataframe
for i in range(Anime_df.shape[0]):
    # Count the reapeted words for the i year
    df = pd.value_counts(Anime_df['Anime Genres'][i])

    # Add the count value to the corresponding column
    for j in range(df.shape[0]):
        Count_Anime_Genres.loc[Count_Anime_Genres['Year'] == arr_year[i] , df.index[j]] = df.values[j]

# Create plots showing the progression of the genres over the years and save them
directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
for i in list_genres:
    plt.plot('Year', i, data = Count_Anime_Genres, marker = 'o')
    plt.title('Number of '+i+' Animes')
    plt.xlabel('Years')
    plt.ylabel('N.' + i)
    file_name = 'N_'+i+'.png'
    plt.savefig(os.path.join(directory_of_python_script, file_name))
    plt.show()
    

