import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool

"""
The script gets cryptocurrencies data from coinmarketcap.com and saves csv.
"""

URL = 'https://coinmarketcap.com/all/views/all/'
all_links = []

# Reading html code of given page.
def get_html(url):
    r = requests.get(url)
    return r.text

# Get urls of each page of cryptocurrency and add to the all_links list.
def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('table').find_all("td", class_='currency-name')
    for link in links:
        a = 'https://coinmarketcap.com' + link.find('a', class_='currency-name-container')['href']
        all_links.append(a)

# Reads html of given page, gets currency attributes and returns them within dictionary
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h1').img['alt']
    price = soup.find('span', id='quote_price').text
    data = {'name': name, 'price': price}
    return data

# Put currency data to the csv file and saves it.
def save_csv(data):
    with open('currencies.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['price']))

# Performs all the operations: gets an html code, extracts data and saves it.
def make_all(url):
    data = get_page_data(get_html(url))
    save_csv(data)
    print(data['name'], 'parsed')


get_all_links(get_html(URL))

# Starts 10 threads performing  the operations.
with Pool(10) as p:
    p.map(make_all, all_links)


