import math
import os

import requests
from bs4 import BeautifulSoup
import csv

import constants


def html_parser(url: str):
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
    response = html_parser(url)
    product_page_url = url
    title = response.find('title').text.strip()
    review_rating = response.find('p', {'class': 'star-rating'})['class'][1]
    div_product_description = response.find('div', {'id': 'product_description'})

    try:
        product_description = div_product_description.find_next_sibling().text
    except TypeError:
        product_description = ''

    table_product_information = response.find('table', {'class': 'table table-striped'}).find_all('td')
    universal_product_code = table_product_information[0].text
    price_including_tax = table_product_information[3].text.replace('Â', '')
    price_excluding_tax = table_product_information[2].text.replace('Â', '')
    number_available = table_product_information[5].text
    category = response.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()
    image_url = f"{constants.url}" + response.find('img')['src'].strip('./')

    return product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,\
        product_description, category, review_rating, image_url


def get_url_book_from_category(category_url: str):
    """Recuperation toutes les livres dans un category"""
    urls_books = []
    for page_url in get_pages_urls(category_url):
        response = html_parser(page_url)
        link_book = response.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
        for links in link_book:
            urls_books.append(f"{constants.url}catalogue/" + links.find('a')['href'].strip('./'))
    return urls_books


def get_data_books_from_one_category(category_url: str):
    books_data = []
    for book_url in get_url_book_from_category(category_url):
        books_data.append(get_data_from_one_book(book_url))
        print(get_data_from_one_book(book_url))
    return books_data


def get_number_of_pages_category(category_url: str):
    response = html_parser(category_url)
    numbers_results = response.find('div', {'class': 'col-sm-8 col-md-9'}).find('strong').text
    numbers_of_pages = math.ceil(int(numbers_results) / 20)
    return numbers_of_pages


def get_pages_urls(category_url: str):
    """
    Recuperation toutes les urls des pages de chaque categories
    :param category_url:
    :return:
    """
    number_of_pages = get_number_of_pages_category(category_url)
    pages_urls = []
    if number_of_pages == 1:
        return [category_url]
    else:
        for i in range(number_of_pages):
            page_url = category_url.replace("index", f"page-{i+1}")
            pages_urls.append(page_url)
    return pages_urls


def get_all_noms_and_urls_categorys():
    """
    Récupère tous les liens et les nomes de toutes les catégories
    :return: all_noms_categorys, all_noms_categorys
    """
    response = html_parser(constants.url)
    all_urls_categorys = []
    all_noms_categorys = []
    list_books = response.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')
    for list_book in list_books:
        all_urls_categorys.append(f"{constants.url}" + list_book.a['href'])
        all_noms_categorys.append(list_book.text.strip())
    return all_urls_categorys, all_noms_categorys


def check_category():
    """
    Vérifier si le nom de catégorie entré figure dans notre liste de catégories.
    :return: Category
    """
    print(f"Noms des catégories: {get_all_noms_and_urls_categorys()[1]}")
    category = input("Choisissez une catégorie (ou tapez exit à quitter) ? ")
    while category not in get_all_noms_and_urls_categorys()[1]:
        if category == "exit":
            print("You choose to exit program. Good bye !")
            exit()
        print("Erreur: Catégorie non disponible dans les catégories")
        print(f"Veuillez choisir dans cette liste: {get_all_noms_and_urls_categorys()[1]}")
        category = input("Quelle catégorie choisir ? ")
    print(f"Vous avez choisi {category}")
    return category


def extract_images(link):
    print(link)
    response = html_parser(link)
    images = response.find_all('img')
    for image in images:
        name_image = image['alt'].replace(":", " ").replace("/", " ").replace("\"", " ").replace("*", " ")\
            .replace("?", " ").lstrip()
        link_image = f'{constants.url}/' + image['src'].lstrip('./')
        with open(name_image + '.jpg', 'wb') as file:
            img = requests.get(link_image)
            file.write(img.content)
            print('Writing: ', name_image)
            print(link_image)


def save_book_data_in_csv(category_url: str, category):
    """
    Enregistrer les informations d'un livre dans un fichier csv
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
        write.writerows([get_data_from_one_book(category_url)])


def save_books_data_in_csv(category_url: str, category):
    """
    Enregistrer les informations des livres dans un fichier csv
    :return:
    """
    try:
        os.mkdir(os.getcwd() + "/csv")
    except:
        pass
    with open(f"csv/{category}.csv", "w", newline="", encoding='utf-8') as file:
        write = csv.writer(file, delimiter=';')
        write.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax",
                        "price_excluding_tax", "number_available", "product_description", "category",
                        "review_rating", "image_url"])
        write.writerows(get_data_books_from_one_category(category_url))


# print(get_data_from_one_book(constants.url_book_set_me_free))
# save_book_data_in_csv(constants.url_book_set_me_free, 'Young Adult')
# pprint(get_number_of_pages_category('https://books.toscrape.com/catalogue/category/books/default_15/index.html'))
# pprint(get_pages_urls('https://books.toscrape.com/catalogue/category/books/default_15/index.html'))
# pprint(get_url_book_from_category('https://books.toscrape.com/catalogue/category/books/default_15/index.html'))
# pprint(get_all_noms_and_urls_categorys())
# pprint(check_category())
# pprint(get_all_data_books_from_one_category('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html'))
# save_books_data_in_csv('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html', 'Mystery')
# pprint(get_data_from_one_book('https://books.toscrape.com/catalogue/in-a-dark-dark-wood_963/index.html'))
# save_books_data_in_csv('https://books.toscrape.com/catalogue/category/books/classics_6/index.html', 'Classics')