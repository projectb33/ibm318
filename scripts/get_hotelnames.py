import time
import os
import sys
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

BASE_URL= sys.argv[2] #example: 'https://www.tripadvisor.in/Hotels-g616028-Haridwar_Haridwar_District_Uttarakhand-Hotels.html'
TRAIL_NUM = 2
CITY_NAME = sys.argv[1] #example: haridwar
FOLDER_LOC = "../dataset/{}".format(CITY_NAME)
FILE_LOC = "{}/{}".format(FOLDER_LOC,"hotels.txt")
#/hotels.csv
#Check folder status
if not os.path.exists(FOLDER_LOC):
    os.makedirs(FOLDER_LOC)

response = get(BASE_URL)
html_soup = BeautifulSoup(response.text, 'html.parser')
total_hotels = html_soup.find_all('span', class_ = 'hotels-sort-filter-header-sort-filter-header__highlight--14Kyo')[0].text
try:
    total_hotels = int(total_hotels.split(" ")[2])
except:
    total_hotels = int(total_hotels.split(" ")[0])
			

#create a url format string
_iter = 0
for counter, ch in enumerate(BASE_URL):
    if ch == "-":
        if _iter == 1:
            se_loc = counter
            break
        _iter+=1
bus = [BASE_URL[:se_loc]+"-oa",BASE_URL[se_loc:]] #base url splits

urls = []
for i in range(0,total_hotels,30): #30 is a pagination value
    if i == 0:
        urls.append(BASE_URL)
    else:
        urls.append(bus[0]+str(i)+bus[1])


start = time.time()

hotels = []

for counter,url in enumerate(urls):
    print("{} hotel stored".format(counter*30))
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    all_hotels = html_soup.find_all('a', class_ = 'property_title')
    for hotel in all_hotels:
          hotels.append(hotel['href'])

end = time.time()

with open(FILE_LOC,"w") as FileHandler:
    FileHandler.write("\n".join(hotels))

print((end - start)/60 , "min")
  