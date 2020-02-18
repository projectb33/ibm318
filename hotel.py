import time

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

BASE_URL='https://www.tripadvisor.in/Hotels-g616028-Haridwar_Haridwar_District_Uttarakhand-Hotels.html'
TRAIL_NUM = 2
CITY_NAME = "haridwar"

urls = []
for i in range(0,580,30):
  if i == 0:
    urls.append(BASE_URL)
  else:
    urls.append("https://www.tripadvisor.in/Hotels-g616028-oa{}-Haridwar_Haridwar_District_Uttarakhand-Hotels.html".format(i))

start = time.time()

hotels = []

for url in urls:
  response = get(url)
  html_soup = BeautifulSoup(response.text, 'html.parser')
  all_hotels = html_soup.find_all('a', class_ = 'property_title')
  for hotel in all_hotels:
    hotels.append(hotel['href'])

end = time.time()

df=pd.DataFrame({"hotel_name":hotels})
df.to_csv("report/hotels/hotel_{}.csv".format(CITY_NAME), index=False)

print((end - start)/60 , "min")
  