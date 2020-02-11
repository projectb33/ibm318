import time

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

BASE_URL='https://www.tripadvisor.in/Hotel_Review-g297689-d1149675-Reviews-Sterling_Mussoorie-Mussoorie_Dehradun_District_Uttarakhand.html'
BASE_URL_INC='https://www.tripadvisor.in/Hotel_Review-g297689-d1149675-Reviews-or5-Sterling_Mussoorie-Mussoorie_Dehradun_District_Uttarakhand.html'
TRAIL_NUM = 2
HOTEL_NAME = "Sterling_Mussoorie-Mussoorie_Dehradun_District_Uttarakhand"

urls=[]

for i in range(0,1920,5):
  if i == 0:
    urls.append("https://www.tripadvisor.in/Hotel_Review-g297689-d1149675-Reviews-or5-Sterling_Mussoorie-Mussoorie_Dehradun_District_Uttarakhand.html")
  else:
    urls.append("https://www.tripadvisor.in/Hotel_Review-g297689-d1149675-Reviews-or{}-Sterling_Mussoorie-Mussoorie_Dehradun_District_Uttarakhand.html".format(i))

contents = []
names = []
ids = []
ratings = []
log = []

start = time.time()
for url in urls:
  response = get(url)
  html_soup = BeautifulSoup(response.text, 'html.parser')
  reviews = html_soup.find_all('div', class_ = 'hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H')

  for counter, review in enumerate(reviews):
    try:
      contents.append(review.find('div', class_="cPQsENeY").span.text)
      names.append(review.find('div', class_="social-member-event-MemberEventOnObjectBlock__event_type--3njyv").a.text)
      ids.append(review.find('div', class_="social-member-event-MemberEventOnObjectBlock__event_type--3njyv").a['href'])
      ratings.append(review.find('div', class_="location-review-review-list-parts-RatingLine__bubbles--GcJvM").span['class'][1].split("_")[1])
    except:
      log.append([counter, review])

end = time.time()

df=pd.DataFrame({"review":contents,"name":names,"user_profile":ids,"rating":ratings})
df.to_csv("report/reviews{}.csv".format(HOTEL_NAME), index=False)

logs=pd.DataFrame(log)
logs.to_csv("logs/logs{}.csv".format(HOTEL_NAME), index=False)

print((start - end)/60 , "min")
  