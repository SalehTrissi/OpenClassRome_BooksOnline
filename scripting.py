import os
from pprint import pprint

import constants
from utils import html_parser, get_data_from_one_book, save_books_data_in_csv, check_category, \
    get_all_noms_and_urls_categorys, save_book_data_in_csv, extract_images, get_pages_urls


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
    # get_data_books_from_one_category(category_url)
    print(category)
    save_books_data_in_csv(category_url, category)


def extracting_data_for_all_books_in_site():
    for link in get_all_noms_and_urls_categorys()[0]:
        response = html_parser(link)
        category = response.find('div', {'class': 'page-header action'}).find('h1').text
        # get_data_books_from_one_category(link)
        # print(get_data_books_from_one_category(link))
        print(category)
        save_books_data_in_csv(link, category)


def extracting_images_from_category():
    nams_categorys = get_all_noms_and_urls_categorys()[1]
    urls_categorys = get_all_noms_and_urls_categorys()[0]
    category = check_category()
    index = [link_text for link_text in nams_categorys].index(category)
    category_url = urls_categorys[index]
    try:
        os.mkdir(os.getcwd() + f"/images/")
        os.mkdir(os.getcwd()+f"/images/{category}")
    except:
        pass
    os.chdir(os.getcwd()+f"/images/{category}")
    for page_url in get_pages_urls(category_url):
        extract_images(page_url)


def extracting_all_images_from_the_site():
    try:
        os.mkdir(os.getcwd()+"/all-images")
    except:
        pass
    os.chdir(os.getcwd()+"/all-images")
    links = get_all_noms_and_urls_categorys()[0]
    for link in links:
        for page_url in get_pages_urls(link):
            extract_images(page_url)


# pprint(extracting_data_for_all_books_in_category())
# extracting_data_for_all_books_in_site()
# extracting_images_from_category()
# extracting_all_images_from_the_site()
