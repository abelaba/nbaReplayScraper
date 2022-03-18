from bs4 import BeautifulSoup
import requests
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["BasketBall"]
mycollection = mydb["videos"]

URL = f'https://nbareplay.net/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')

links = soup.find_all(class_="entry-thumbnail thumbnail-landscape")


for link in links:
    data = {}
    second_URL = link.a['href']

    data["title"] = link.a['title']
    data['url'] = second_URL

    second_link = requests.get(second_URL)
    second_link_soup = BeautifulSoup(second_link.content, 'lxml')
    quarters = second_link_soup.find_all(
        class_="su-button su-button-style-default")[:4]

    data["quarters"] = []

    for quarter in quarters:
        third_link = requests.get(quarter['href'])
        third_link_soup = BeautifulSoup(third_link.content, 'lxml')
        data["quarters"].append(third_link_soup.iframe['src'])

    try:
        mycollection.insert_one(data)
        print(data["title"])
        print()
    except Exception as e:
        print(e)
        pass
