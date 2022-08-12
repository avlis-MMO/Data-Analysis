from bs4 import BeautifulSoup as bs
import requests
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# This code will extract information about the animes in the year given by the user from the webssite my anime list and show the genres
# of the anime that year and create a dataframe with all the information about them
anime_J_name = []
anime_rank = []
anime_members = []
anime_link = []
anime_genre = []
years = []
seasons = []

def Get_Info(year):
    dic = {}
    # Each year has four seasons so we have to extract info from all of them
    for season in ['fall','winter', 'spring','summer']:
        url = 'https://myanimelist.net/anime/season/'+year+'/'+season
        
        # Use beautiful soup to extract the information
        web_site = requests.get(url)
        soup = bs(web_site.text, 'html.parser')

        # Select the section with the new animes each season
        Season_anime = soup.find("div",{"class":"seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1"})
        list_anime = Season_anime.find_all("div",{"class":"js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-1"})

        # Run through each anime and get the information
        for anime in list_anime:

            seasons.append(season)
            temp = []
            anime_J_name.append(anime.find("h2",{"class":"h2_anime_title"}).text)
            anime_link.append(anime.h2.a['href'])

            # If the anime still hasnt a score given to it atribute none
            if anime.find("div",{"class":"information"}).find("div",{"title":"Score"}).text.replace('\n','').replace(' ','') == 'N/A':
                anime_rank.append(None)
            else:
                anime_rank.append(anime.find("div",{"class":"information"}).find("div",{"title":"Score"}).text.replace('\n','').replace(' ',''))
            
            anime_members.append(anime.find("div",{"class":"information"}).find("div",{"title":"Members"}).text.replace('\n','').replace(' ',''))
            
            # Get all the genres and append to a list
            for t in anime.find("div",{"class":"genres-inner js-genre-inner"}):
                temp.append(t.text.replace('\n','').replace(' ',''))
            anime_genre.append(' '.join(temp).replace(' ',', '))
            
    # Create the dataframe with lists with all the information
    Anime_df = pd.DataFrame({'Season':seasons,'Anime Name':anime_J_name, 'Anime Score':anime_rank, 'Anime Members':anime_members, 'Anime Genres': anime_genre, 'More Info':anime_link})

    # Assign a rank to the anime based on the members and score
    # Create a dict with the nae of the anime as key and the rank as value
    for anime, members, score in zip(Anime_df['Anime Name'], Anime_df['Anime Members'], Anime_df['Anime Score']):
        if 'K' in members and score != None:
            dic[anime] = round(0.40 * float(score) *100 + 0.6 * float(members[:-1]))
        elif score == None:
            dic[anime] = 0
        else:
            dic[anime] = round(float(score) * 100 * 0.4 + 0.6 * float(members[:-1])/1000)

    # Order the key based on the rank
    dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
    Anime_df['Rank'] = Anime_df['Anime Score']

    # Add the rank to the dataframe
    for i, key in enumerate(dic.keys()):
        Anime_df.loc[Anime_df['Anime Name'] == key, 'Rank'] = (i+1)
    Anime_df = Anime_df.sort_values(['Rank'], na_position='last').reset_index()
    del Anime_df['index']

    # Save file to folder
    directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
    Anime_df.to_csv(os.path.join(directory_of_python_script, year+'_Anime.csv'))

    return Anime_df

if __name__ == "__main__":
    
    # Get year from user
    year = sys.argv[1]
    if int(year) == date.today().year+2:
        print("max year searchable: {0}".format(date.today().year+1))
        exit()
    Anime_df = Get_Info(year)

    # Create histogram with the genres and their number
    data1=[]
    l = Anime_df['Anime Genres'].tolist()
    for i in l:
        data1.append(i.split(','))
    flat_list = [x.replace(' ','') for xs in data1 for x in xs if len(x) > 1]

    ax = sns.countplot(flat_list)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    plt.tight_layout()
    plt.show()