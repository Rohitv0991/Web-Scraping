import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# list variables to store result
brands = []
titles = []
prices = []
images = []
links = []

# creates an array containing values from 1 to 85
pages = np.arange(1,86)

for page in pages:
    # base url which will be updated in every iteration using 'str(page)'
    url = "https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page="+str(page)+"&view=180&scale=282"

    # requesting the page
    r = requests.get(url, headers = {'User-agent': 'Chrome'})
    # get html content of the page
    htmlContent = r.content
    # parsing html content using  Beautiful soup
    soup = BeautifulSoup(htmlContent, 'html.parser')
    # get all <a> tags with class "_5ce6f6" each anchor tag contains details of product
    products = soup.find_all('a', class_="_5ce6f6")

    for product in products:
        # get brand name and append in list 'brands'
        brand = product.h3.text
        brands.append(brand)
        # get title and append in list 'titles'
        title = product.p.text
        titles.append(title)
        # get price and append in list 'prices'
        price = product.find('div', class_="_6356bb").text
        prices.append(price)
        # get image url and append in list 'images'
        image = product.meta.attrs['content']
        images.append(image)
        #  get product url and append in list 'links'
        link = product.attrs['href']
        links.append("https://www.farfetch.com"+link)

# using pandas to create a dataframe 'outputData' and stores the result in it
outputData = pd.DataFrame({'Name':titles, 'Brand':brands, 'Price':prices, 'Image URL':images, 'Product URL':links})
# writes 'outputData' to file 'shoesData1.csv'
outputData.to_csv('shoesData1.csv', index=False, encoding='utf-8-sig')