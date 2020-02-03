from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

BASE_URL='https://www.tripadvisor.in/Hotel_Review-g297689-d1149675-Reviews-Sterling_Mussoorie-Mussoorie_Dehradun_District_Uttarakhand.html'
TRAIL_NUM = 1

response = get(BASE_URL)
html_soup = BeautifulSoup(response.text, 'html.parser')
reviews = html_soup.find_all('div', class_ = 'hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H')

contents = []
names = []
ids = []
ratings = []
log = []

for counter, review in enumerate(reviews):
  try:
    contents.append(review.find('div', class_="cPQsENeY").span.text)
    names.append(review.find('div', class_="social-member-event-MemberEventOnObjectBlock__event_type--3njyv").a.text)
    ids.append(review.find('div', class_="social-member-event-MemberEventOnObjectBlock__event_type--3njyv").a['href'])
    ratings.append(review.find('div', class_="location-review-review-list-parts-RatingLine__bubbles--GcJvM").span['class'][1].split("_")[1])
  except:
    log.append([counter, review])


df=pd.DataFrame({"review":contents,"name":names,"user_profile":ids,"rating":ratings})
df.to_csv("report/reviews{}.csv".format(TRAIL_NUM), index=False)

logs=pd.DataFrame(log)
logs.to_csv("logs/logs{}.csv".format(TRAIL_NUM), index=False)

  