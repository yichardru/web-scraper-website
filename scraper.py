import requests
from bs4 import BeautifulSoup
import pandas as pd

k = "nvidia 4090"

#Extract Data
def get_data(keyword: str):
    keyword = keyword.replace(' ', '+')
    keyword = keyword.lower()
    r = requests.get('https://www.ebay.com/sch/i.html?_from=R40&_nkw=%27'+keyword+'%27&_sacat=0')
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

#Parse
def parse(soup):
    res = []
    results = soup.find_all('div', {'class' : 's-item__info clearfix'})
    for item in results:
        title = item.find('span', {'role' : 'heading'}).text
        price = float(item.find('span', {'class' : 's-item__price'}).text.replace('$', '').replace(',','').strip())
        link = item.find('a', {'class' : 's-item__link'})['href']
        res.append([title, price, link])
    return res

#Output
def export(plist, keyword):
    product_data_frame = pd.DataFrame(plist, columns=['title', 'price', 'link'])
    product_data_frame.to_csv(keyword + ' output.csv', sep="\t", index=False)
    print("Saved")
    return

soup = get_data(k)
productlist = parse(soup)
export(productlist, k)