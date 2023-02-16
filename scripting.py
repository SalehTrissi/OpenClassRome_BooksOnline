from pprint import pprint

import constants
from utils import html_parser, get_data_from_one_book, save_books_data_in_csv, check_category, get_all_noms_and_urls_categorys, \
    get_data_books_from_one_category, save_book_data_in_csv


def extracting_data_from_a_book():
    """Extraire des données d'un livre."""
    return pprint(get_data_from_one_book(constants.url_book_set_me_free)), \
        save_book_data_in_csv(constants.url_book_set_me_free, "Young Adult")


def extracting_data_for_all_books_in_category():
    """Extraction des données de tous les livres appartenant à la catégorie sélectionnée."""
    nams_categorys = get_all_noms_and_urls_categorys()[1]
    urls_categorys = get_all_noms_and_urls_categorys()[0]
    category = check_category()
    index = [link_text for link_text in nams_categorys].index(category)
    category_url = urls_categorys[index]
    get_data_books_from_one_category(category_url)
    save_books_data_in_csv(category_url, category)


def extracting_data_for_all_books_in_site():
    for link in get_all_noms_and_urls_categorys()[0]:
        response = html_parser(link)
        category = response.find('div', {'class': 'page-header action'}).find('h1').text
        print(category)
        get_data_books_from_one_category(link)
        print(get_data_books_from_one_category(link))
        save_books_data_in_csv(link, category)


# pprint(extracting_data_for_all_books_in_category())
# extracting_data_for_all_books_in_site()
