import pprint 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

import scipy as sp
from scipy.stats import ttest_ind

# Requests sends and recieves HTTP requests.
import requests

# Beautiful Soup parses HTML documents in python.
from bs4 import BeautifulSoup
import copy



def scrape():
    #This is for when we concatenate the url for the button
    web = 'https://fbref.com'
    #This is the website we want to scrape
    url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #This is a list to grab the last 25 years of EPL data
    lst = list(range(1996,2021))
    lst = lst[::-1]
    #We are going to loop the scraping process
    for year in lst:
        #This is the button to scrape the previous years data
        button = soup.select_one('#meta > div:nth-child(2) > div > a.button2.prev').get('href')
        #Here we are concatenating the URL and the button
        webbutton = web + button
        r = requests.get(webbutton)
        soup = BeautifulSoup(r.text, 'html.parser')
        #Grabing all the tables on the website
        tables = soup.find_all('table')
        #Grabing the the table we want
        indices = tables[0].find_all('th') 
        rows = tables[0].find_all('tr')
        #Getting the data ready to put into pandas DF
        columns = {}
        for index in indices: 
            columns[index.text] = None
        all_data = []
        keys = list(columns.keys())
        for i,row in enumerate(rows):
            if i > 0:
                new_row = copy.copy(columns)
                entries = row.find_all('td')
                for j,entry in enumerate(entries):
                    new_row[keys[j+1]]= entry.text
                all_data.append(new_row)
        #Adjusting my data
        for dic in range(20): 
            all_data[dic]['Rk'] = (dic+1)
        #Making a pandas df 
        df = pd.DataFrame(all_data) 
        #deleting last columns that are not needed
        dlst = list(range(len(columns)-24,len(columns))) 
        df.drop(df.columns[dlst], axis = 1, inplace = True)
        #Saving data into a csv
        df.to_csv(f'data/{year}.csv', sep='!', index=False)

