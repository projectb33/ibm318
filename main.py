import time

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

CITY = "haridwar"
hotel_names = pd.read_csv('./report/hotels/hotel_namesharidwar.csv')['hotel_name'].values

contents = []
names = []
ids = []
ratings = []
log = []

start = time.time()
for hotel_name in hotel_names:
  
  BASE_URL='https://www.tripadvisor.in{}'.format(hotel_name)

  response = get(BASE_URL)
  html_soup = BeautifulSoup(response.text, 'html.parser')
  total_reviews = html_soup.find_all('span', class_ = 'hotels-community-content-common-TabAboveHeader__tabCount--26Tct')[0].text

  urls=[]
  prefix = hotel_name[0:40]
  suffix = hotel_name[40:]
  
  for i in range(0,int(total_reviews),5):
    if i == 0:
      urls.append(BASE_URL)
    else:
      urls.append("https://tripadvisor.com{}or{}-{}".format(prefix,i,suffix))


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
df.to_csv("report/reviews_{}.csv".format(CITY), index=False)

logs=pd.DataFrame(log)
logs.to_csv("logs/logs{}.csv".format(CITY), index=False)

print((end - start)/60 , "min")
  