from pprint import pprint

import requests
from bs4 import BeautifulSoup

import constants


def html_parsel(url: str):
    """
    Return le contenu de la page html
    :param url:https://books.toscrape.com/
    :return: soup
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_data_from_one_book(url: str):
    """
    Obtenir des données d’un livre à partir de sin url
    :param url: https://books.toscrape.com/catalogue/set-me-free_988/index.html
    :return: toutes les données pour un livre
    """
    response = html_parsel(url)

    product_page_url = url
    title = response.find('title').text.strip()
    review_rating = response.find('p', {'class': 'star-rating'})['class'][1]
    div_product_description = response.find('div', {'id': 'product_description'})
    try:
        product_description = div_product_description.find_next_sibling().text
    except:
        product_description = ''

    table_product_information = response.find('table', {'class': 'table table-striped'}).find_all('td')
    universal_product_code = table_product_information[0].text
    price_including_tax = table_product_information[3].text
    price_excluding_tax = table_product_information[2].text
    number_available = table_product_information[5].text
    category = response.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()
    image_url = f"{constants.url}" + response.find('img')['src'].strip('./')

    return product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,\
        product_description, category, review_rating, image_url


# pprint(get_data_from_one_book('https://books.toscrape.com/catalogue/set-me-free_988/index.html'))
