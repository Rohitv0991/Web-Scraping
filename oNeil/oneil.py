import requests
from bs4 import BeautifulSoup
import pandas as pd


codes = []

with open("Task4.csv") as f:
    fileData = f.readlines()
f.close()

for data in fileData:
    code = (data.split(","))[2]
    codes.append(code)

urls = []
prices = []

for i in range(1, len(codes)):
    params = {
        'access_key': '974c5a990636571be33a1be41364f33d',
        'query': 'site:oneill.com/fr'+ ' "'+str(codes[i])+'"',
    }
    api_result = requests.get('http://api.serpstack.com/search', params)
    api_response = api_result.json()

	if len(api_response['organic_results']) <= 0 :
		urls.append("-")
		prices.append("-")
	else:
		result = ((api_response['organic_results'])[0]) 
		url = (result['url'])   
		urls.append(url)

		r = requests.get(url, headers = {'User-agent': 'Bot'})
		htmlContent = r.content
		soup = BeautifulSoup(htmlContent, 'html.parser')

		price = soup.find('span', class_="sales").text 
		prices.append(price.strip())

df = pd.read_csv("Task4.csv")
df["Product Page URL"] = urls
df["Price(Euros)"] = prices
df.to_csv("Task4.csv", index=False)