import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials


url = 'https://www.bigbasket.com/'


category_urls = [
    'fruits-vegetables/',
    'foodgrains-oil-masala/',
    'bakery-cakes-dairy/',
    'beverages/',
    'snacks-branded-foods/'
]


num_products = 10


scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Big Basket Sample Data').sheet1


for category_url in category_urls:
    
    page = requests.get(url + category_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    
    subcategories = soup.find_all('a', class_='ng-binding')

    
    for subcategory in subcategories:
        
        subcategory_url = url + subcategory['href']
        subcategory_page = requests.get(subcategory_url)
        subcategory_soup = BeautifulSoup(subcategory_page.content, 'html.parser')

        
        products = subcategory_soup.find_all('div', class_='col-sm-12 col-xs-7 prod-name')

       
        for i in range(num_products):
            try:
                product_name = products[i].find('a', class_='ng-binding')['title']
                product_price = products[i].find('span', class_='discnt-price').text.strip()
            except:
                continue

            sheet.append_row([category_url[:-1], subcategory.text.strip(), product_name, product_price])

print('Data has been scraped and saved to the Google Sheet.')
