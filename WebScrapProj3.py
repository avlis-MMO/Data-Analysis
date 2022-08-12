from curses.ascii import isalnum, isdigit
from bs4 import BeautifulSoup as bs
import requests
from datetime import date
import pandas as pd
import re
import os

# In this code i am going to search the top 500 actors on IDMb and get their names, when they were born, where they were born and how many movies they made
# using beautiful soup to scrap all the information and then in another script present this information

links = []
names = []
birth = []
death = []
age = []
places = []
gender = []
movies = []


# Function to get the age of the actors
def get_age(born,death=date.today()):

    return death.year - born.year - ((death.month, death.day) < (born.month, born.day))

# Get the links to acess the pages where the information of the actors is
def get_links():
    
    for i in range(1,501,50):
        url1 = 'https://www.imdb.com/search/name/?match_all=true&start='+str(i)+'&ref_=rlm'

        web_site = requests.get(url1)
        soup = bs(web_site.text, 'html.parser')
        humans = soup.find_all("div",{"class":"lister-item mode-detail"})
        for human in humans:
            links.append(human.div.a['href'])

# Get all the info to build the dataframe
def get_info():

    # Use the links to acess the pafe with the info of each actor using beautiful soup
    for link in links:
        jobs = []
        url2 = 'https://www.imdb.com'+link

        web_site = requests.get(url2)
        soup = bs(web_site.text, 'html.parser')
        
        table = soup.find("table")
        
        # Get the jobs of the person as made to find it is a female or male
        for x in table.find("div",{"class":"infobar"}).find_all("span",{"class":"itemprop"}):
            jobs.append(x.text.replace('\n','').replace('',''))

        # If in the list of jobs there is actor we assume its a male and save as M if there is actress we assume its a female and we save F
        if 'Actor' in jobs:
            gen = 'Actor'
            gender.append('M')

        elif 'Actress' in jobs:
            gen = 'Actress'
            gender.append('F')

        # In case it isnt an actor or acatress dont add it to the dataframe
        else:
            continue

        # Save the names
        names.append(table.find("span",{"class":"itemprop"}).text)

        # Check if the page as information about where and when they were born if not add none
        if table.find("div",{"id":"name-born-info"}):

            # Check if the page as information about when they were born if not add none
            if table.find("time"):
                time = table.find("time").attrs["datetime"].split("-")

                # In case the info doesnt provide the specific day of birth assume it is one to calculate aprox age
                # Present the day of birth as day/month/year
                if time[2] == '0':
                    birth.append('__/'+time[1]+'/'+time[0])
                    time[2] = '1'
                else:
                    birth.append(time[2]+'/'+time[1]+'/'+time[0])

                # Check if the page has information about the person death, if yes had if not says it is alive
                # Present the day of death as day/month/year
                if table.find("div",{"id":"name-death-info"}):
                    time_d = table.find("div",{"id":"name-death-info"}).find("time").attrs["datetime"].split("-")
                    death.append(time_d[2]+'/'+time_d[1]+'/'+time_d[0])
                    age.append(get_age(date(int(time[0]),int(time[1]),int(time[2])),date(int(time_d[0]),int(time_d[1]),int(time_d[2]))))
                else:
                    death.append('Alive')
                    age.append(get_age(date(int(time[0]),int(time[1]),int(time[2]))))
                    
            else:
                birth.append(None)
                death.append(None)
                age.append(None)
            places.append(table.find("div",{"id":"name-born-info"}).find_all("a")[-1].text)

        else:
            birth.append(None)
            death.append(None)
            age.append(None)
            places.append(None)
        
        # Get the information of how many movies/series they took part to acess this information it must be known if it an actress or actor
        movies.append(int(re.findall(r'\d+', soup.find("div",{"id":"filmography"}).find("div",{"id":"filmo-head-"+gen.lower()}).text.replace('\n','').replace('(',''))[0]))
    
    # Create dict with all the information, transform it to a data frame and save it
    dict = {'Name': names, 'Gender': gender, 'Born in': places, 'Birth': birth, 'Death': death, 'Age': age, 'Movies/Series': movies}
    df = pd.DataFrame(dict)
    directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
    df.to_csv(os.path.join(directory_of_python_script, 'IDMB.csv'))
    
if __name__ == "__main__":
    get_links()
    get_info()