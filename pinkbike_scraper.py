import requests
import re
from bs4 import BeautifulSoup
import itertools
from datetime import datetime
import time
import csv
import pandas
from pathlib import Path
from forex_python.converter import CurrencyRates
from tqdm import tqdm

i=0
bikes = []
YEAR_PATTERN = re.compile("^(19|20)\d{2}$")
FOREX = CurrencyRates()
numRetry = 0
df_brands = pandas.read_csv("brands.csv")
masterBrands = df_brands.loc[:,'Brand']
masterSpellings = df_brands.loc[:,'Spelling']

# iterate over every page
for page in tqdm(range(1,1280)):
    time.sleep(.1)
    # Create URL and request html for the page
    URL = 'https://www.pinkbike.com/buysell/list/?region=3&page='+ str(page) + '&category=75,102,2,1,74&itemcondition=2,3,4,5,6'
    try:
        req = requests.get(URL, timeout=1)
        req.raise_for_status()
    except Exception as err: #need to do a better error handling here
        print("Issue with the network")
        print(err.args[0])
        numRetry = numRetry + 1
        if numRetry < 12:
            continue
        else:
            #page = page - 1
            time.sleep(10)
            break

    # Parsing the HTML
    soup = BeautifulSoup(req.content, 'html.parser')

    # finiding the containers that have relevant information
    items = soup.find_all('div', class_='bsitem-title')
    prices = soup.find_all('td', class_='bsitem-price')
    details = soup.find_all('table', class_='bsitem-details')

    # iterating over each bike found in search
    for (item, price, detail) in zip(items, prices, details):
        bike = {}

        # get year, title and category from <a>
        title = item.find('a').string
        category = item.find('br').next_element.strip()
        year = ''

        # split year from title
        if YEAR_PATTERN.match(title.split(" ", 1)[0]):
            year = title.split(" ", 1)[0]
            item["Year"] = year

        # parsing brand from title text
        for (masterBrand, masterSpelling) in zip(masterBrands, masterSpellings):
            if masterSpelling.upper() in title.upper():
                bike['Brand'] = masterBrand
                break

        # put year, title and category into bike dictionary
        bike['Year'] = year
        bike["Title"] = title
        bike['Category'] = category

        # put price and currency into bike dictionary
        price = price.find('b').string
        ammount = price.split(" ", 1)[0]
        currency = price.split(" ", 1)[1].strip()
        bike["Price"] = ammount
        bike["Currency"] = currency

        ammount = int(ammount.lstrip("$"))
        if currency == 'CAD':
            bike["Price in USD"] = ammount * .74
        elif currency == 'EUR':
            bike["Price in USD"] = ammount * 1.04
        elif currency == 'GBP':
            bike["Price in USD"] = ammount * 1.25
        elif currency == 'zl':
            bike["Price in USD"] = ammount * .24
        elif currency == 'USD':
            bike["Price in USD"] = ammount

        #convert everything to USD and format
        # usdPrice = FOREX.convert(currency, "USD", int(ammount.lstrip("$")))
        # bike["Price in USD"] = '$'+'{:.2f}'.format(usdPrice)

        # put link and ID into bike dictionary
        link = item.find('a').get('href')
        bike["Link"] = link
        bike["ID"] = link.split("/", 5)[4]

        # get location sold from
        location = detail.find('img').next_element.strip()
        try:
            bike["City"] = location.split(',')[0].strip()
            bike["State"] = location.split(',')[1].strip()
            bike["Country"] = location.split(',')[2].strip()
        except:
            bike['Country'] = bike['State']
            bike['State'] = ''

        # Get item specs from itemdetail class
        itemSpecs = item.find_all('div', class_='itemdetail')

        # iterate over each spec
        for itemSpec in itemSpecs:
            # Get category and description from itemSpec
            specCat = itemSpec.b.string
            specDes = specCat.next_element

            if specCat == "Condition : ":
                bike['Condition'] = specDes
            elif specCat == "Frame Size : ":
                bike['Frame Size'] = specDes
            elif specCat == "Wheel Size : ":
                bike['Wheel Size'] = specDes
            elif specCat == "Material : ":
                bike['Material'] = specDes
            elif specCat == "Front Travel : ":
                bike['Front Travel'] = specDes
            elif specCat == "Rear Travel : ":
                bike['Rear Travel'] = specDes
        # add bike to bikes list
        bikes.append(bike)
        i = i + 1

# put bikes list into csv
df = pandas.DataFrame(bikes)
df.to_csv("~/pinkbike-scrape-willy/North_American_Bikes.csv", index=False)
print('Data Stored in North_American_Bikes.csv')
