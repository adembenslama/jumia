from django.shortcuts import render
from django.http import HttpResponse
import json


def index(request):
    with open('data/phone.json', 'r') as f:
        data = json.load(f)

    with open('data/brand.json', 'r') as f:
        brands = json.load(f)

    selected_brand = request.GET.get('brand', None)
    min_price = request.GET.get('maxPrice', None)
    min_price = request.GET.get('minPrice', None)

    filtered_data = []
    for item in data:
        if selected_brand is not None and item['marque'] != selected_brand:
            continue
        item['price'] = item['price'].split()[0]

        if min_price is not '' and min_price is not None and min_price != 5000 and float(item['price'].replace(',', '')) > float(min_price):
            continue
        if min_price is not '' and min_price is not None and min_price != 5000 and float(item['price'].replace(',', '')) < float(min_price):
            continue

        filtered_data.append(item)

    context = {
        'data': filtered_data,
        'brands': brands,
        'selected_brand': selected_brand,
        'selected_price': min_price,
    }
    return render(request, 'index.html', context)
