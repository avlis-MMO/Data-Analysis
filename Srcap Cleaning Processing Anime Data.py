from unittest import skip
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd
import os
import numpy as np

anime_rank = []
anime_menbers = []

anime_genre = []
arr_year = np.arange(2000, 2021, 1)
seasons = []
dic = {}

# This script was  made to get information about anime from Myanimelist to try to use to predcit the score of animes to be aired
# but after some training and analyses of that data i came to the conclusion that it is impossible to predict the score
# with enough accuracy, beacause the score isnt dependent on the number of members or genre or number of genres
# but the quality of the anime it self and people opinion

# Code to extract data to use on the alghoritmo
def Get_Data():
    for year in arr_year:
        for season in ['fall','winter', 'spring','summer']:
            url = 'https://myanimelist.net/anime/season/'+str(year)+'/'+str(season)
            
            web_site = requests.get(url)
            soup = bs(web_site.text, 'html.parser')
            Season_anime = soup.find("div",{"class":"seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1"})
            list_anime = Season_anime.find_all("div",{"class":"js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-1"})

            
            # Extract the genres and members of the anime
            for anime in list_anime:
                temp = []
                for t in anime.find("div",{"class":"genres-inner js-genre-inner"}):
                    genre = t.text.replace('\n','').replace(' ','').replace('-','')
                    if len(genre) > 1:
                        temp.append(genre)

                # Making sure it has genre cause it wil affect the data
                if len(temp) < 1:
                    continue
                else:
                    anime_genre.append(temp) 

                if anime.find("div",{"class":"information"}).find("div",{"title":"Score"}).text.replace('\n','').replace(' ','') == 'N/A':
                    anime_rank.append(None)
                else:
                    anime_rank.append(anime.find("div",{"class":"information"}).find("div",{"title":"Score"}).text.replace('\n','').replace(' ',''))
                
                # Transform the number os members to a integer
                if 'K' in anime.find("div",{"class":"information"}).find("div",{"title":"Members"}).text.replace('\n','').replace(' ',''):
                    anime_menbers.append(float(anime.find("div",{"class":"information"}).find("div",{"title":"Members"}).text.replace('\n','').replace(' ','')[:-1])*1000)
                elif 'M'in anime.find("div",{"class":"information"}).find("div",{"title":"Members"}).text.replace('\n','').replace(' ',''):
                    anime_menbers.append(float(anime.find("div",{"class":"information"}).find("div",{"title":"Members"}).text.replace('\n','').replace(' ','')[:-1])*1000000)
                else:
                    anime_menbers.append(float(anime.find("div",{"class":"information"}).find("div",{"title":"Members"}).text.replace('\n','').replace(' ','')))
                
    # Create a dataframe to store all the information, this dataframe is not properly organized
    Anime_df = pd.DataFrame({'Anime Genres': anime_genre, 'Anime Members':anime_menbers, 'Anime Score': anime_rank})

    # Eliminate all the anime with null score since they wont help us with creating the alghoritmo
    Anime_df = Anime_df[Anime_df['Anime Score'].notnull()].reset_index()
    Anime_df = Anime_df.sort_values(by='Anime Members', ascending=False)

    # Create dataframe with the data used to train the alghoritmo
    All_genres = sorted(set([x for xs in Anime_df['Anime Genres'].to_list() for x in xs]))
    All_genres.append('N_genres')
    X_data = pd.DataFrame(Anime_df['Anime Members'])
    X_data.rename(columns = {'Anime Members':'Members'}, inplace = True)
    X_data[All_genres]=np.zeros((Anime_df.shape[0], len(All_genres)))

    # Count how many genres an anime has
    for i,genres in enumerate(Anime_df['Anime Genres']):
        for genre in genres:
            X_data.loc[(X_data.index == i) & (X_data[genre] == 0), genre] = 1
            X_data.loc[(X_data.index == i) & (X_data['N_genres'] == 0), 'N_genres'] = len(genres)

    # Create a dataframe with the labels
    Y_data = pd.DataFrame(Anime_df['Anime Score'])

    # Safe the information to be used later
    directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
    X_data.to_csv(os.path.join(directory_of_python_script,'X_data.csv', index=False))
    Y_data.to_csv(os.path.join(directory_of_python_script,'Y_data.csv', index=False))
    Anime_df.to_csv(os.path.join(directory_of_python_script,'Anime_df.csv', index=False))
    
if __name__ == "__main__":

    Get_Data()
