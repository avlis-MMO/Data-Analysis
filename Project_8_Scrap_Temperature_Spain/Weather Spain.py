from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import os

# This script will scrap the temperatures from the badajoz weather station and save it to a csv.
# I had to use selenium because the web site had DOM

# Get the driver to be able to acess the html
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

dict = {}
directory_of_python_script = os.path.dirname(os.path.abspath(__file__))

# Iterate through the 12 months
if __name__ == '__main__':
    for i in range(1,13):
        driver.get('https://www.wunderground.com/history/monthly/es/badajoz/LEBZ/date/2021-'+str(i))
        driver.implicitly_wait(10)
        time.sleep(5)
        
        # Get page source
        page_source = driver.page_source

        # Parse the html to get the temperatures
        soup = bs(page_source, 'lxml')
        table = soup.find('table', class_ = 'days ng-star-inserted')
        rows = table.find('tbody').find_all('table')[1].find_all('tr')
        temp = []
        j = 1

        # Get the rows with the temp and skip the one without temp
        for row in rows:
            if not re.search(r'\d', row.find_all('td')[0].text):
                continue
            temp.append(row.find_all('td')[0].text.strip())
            temp.append(row.find_all('td')[1].text.strip())
            temp.append(row.find_all('td')[2].text.strip())

            # Save the day and the corresponding temps in a dict
            dict[str(j)+'/'+str(i)+'/2021'] = temp
            temp=[]
            j = j + 1
    driver.quit()

    # Save everything to a dataframe
    df = pd.DataFrame.from_dict(dict, orient='index', columns=['Max','Avg','Min'])
    df.to_csv(os.path.join(directory_of_python_script, 'LEBZ_2021.csv'))
