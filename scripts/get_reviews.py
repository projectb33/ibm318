import time
import os
import sys
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

CITY = sys.argv[1]

with open("../dataset/{}/hotels.txt".format(CITY)) as FileHandle:
    hotel_names = FileHandle.readlines()

for hotel_name in hotel_names:
    BASE_URL='https://www.tripadvisor.in{}'.format(hotel_name[:-1])
    
    response = get(BASE_URL)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    total_reviews = html_soup.find_all('span', class_ = 'hotels-community-content-common-TabAboveHeader__tabCount--26Tct')[0].text

    urls=[]

    _iter = 0
    for counter, ch in enumerate(BASE_URL):
        if ch == "-":
            if _iter == 3:
                se_loc = counter
                break
            _iter+=1
    bus = [BASE_URL[:se_loc]+"-or",BASE_URL[se_loc:]] #base url splits
    print("-------------------------")
    print("Collecting review for",BASE_URL[se_loc+1:-5])
    print("-------------------------")
    for i in range(0,int(total_reviews),5):
        if i == 0:
            urls.append(BASE_URL)
        else:
            urls.append(bus[0]+str(i)+bus[1])
    
    contents = []
    names = []
    ids = []
    ratings = []
    log = []
    islocal = []
    for url in urls:
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        reviews = html_soup.find_all('div', class_ = 'hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H')
    
        for review in reviews:
            try:
                contents.append(review.find('div', class_="cPQsENeY").span.text)
                names.append(review.find('div', class_="social-member-event-MemberEventOnObjectBlock__event_type--3njyv").a.text)
                ids.append(review.find('div', class_="social-member-event-MemberEventOnObjectBlock__event_type--3njyv").a['href'])
                ratings.append(review.find('div', class_="location-review-review-list-parts-RatingLine__bubbles--GcJvM").span['class'][1].split("_")[1])
                try:
                    islocal.append(review.find('span', class_="social-member-common-MemberHometown__hometown--3kM9S").text)
                except:
                    islocal.append("")
            except:
                continue
    city = [CITY]*(len(contents))
    df=pd.DataFrame({"location":city,"review":contents,"name":names,"user_profile":ids,"userloc":islocal,"rating":ratings})
    df.to_csv("../dataset/{}/{}.csv".format(CITY,BASE_URL[se_loc+1:-5]), index=False)
# logs=pd.DataFrame(log)
# logs.to_csv("logs/logs{}.csv".format(CITY), index=False)

  