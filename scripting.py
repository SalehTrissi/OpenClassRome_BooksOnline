from pprint import pprint

import constants
from utils import get_data_from_one_book, save_book_data_in_csv


def extracting_data_from_a_book():
    """Extraire des données d'un livre"""
    return pprint(get_data_from_one_book(constants.url_book_set_me_free)),\
        save_book_data_in_csv(constants.url_book_set_me_free, "")
