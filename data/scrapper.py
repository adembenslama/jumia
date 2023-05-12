from bs4 import BeautifulSoup
import requests
import json

data_file = open('data/phone.json', 'w', encoding='utf8')
marque_file = open('data/brand.json', 'w', encoding='utf8')


data_file.write('[\n')
marque_file.write('[\n')

brands = set()

for page in range(1, 14):
    print('---', page, '---')
    url = 'https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page=' + \
        str(page)+'#catalog-listing'
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all('article', {'class': 'prd _fb col c-prd'})

    for item in articles:
        name = item.find('h3', {'class': 'name'}).text
        brand = name.split()[0]
        if brand not in brands:

            brands.add(brand)
            brand_data = {'marque': brand}
            json_data = json.dumps(brand_data, ensure_ascii=False)
            marque_file.write(json_data)
            marque_file.write(",\n")

        data = {
            'name': name,
            'marque': brand,
            'price': item.find('div', {'class': 'prc'}).text,
            'image': item.find('div', {'class': 'img-c'}).find('img')['data-src'],
            'link': 'https://www.jumia.com.tn'+item.find('a', {'class': 'core'})['href']
        }
        json_data = json.dumps(data, ensure_ascii=False)
        data_file.write(json_data)
        data_file.write(",\n")

data_file.write("\n]")
marque_file.write("\n]")

data_file.close()
marque_file.close()
