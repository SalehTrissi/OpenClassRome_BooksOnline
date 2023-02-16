import os

import requests
from bs4 import BeautifulSoup
import csv

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


def save_books_data_in_csv(category_url: str, category):
    """
    Enregistrer les informations des livres dans un fichier csv
    :return:
    """
    try:
        os.mkdir(os.getcwd() + "/csv")
    except:
        pass
    os.chdir(os.getcwd() + "/csv")
    with open(category + '.csv', "w", newline="") as file:
        write = csv.writer(file, delimiter=';')
        write.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax",
                        "price_excluding_tax", "number_available", "product_description", "category",
                        "review_rating", "image_url"])
        write.writerow(get_data_from_one_book(category_url))

# print(get_data_from_one_book(constants.url_book_set_me_free))
# save_book_data_in_csv(constants.url_book_set_me_free, 'Young Adult')
