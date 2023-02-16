import constants
from scripting import extracting_data_from_a_book, extracting_data_for_all_books_in_category, \
    extracting_data_for_all_books_in_site


def main_menu():
    """
    Affiche le menu principale
    """
    print(constants.MENU)
    choice = input('Votre choix : ')
    selection_available = ["1", "2", "3", "4"]
    
    while choice in selection_available:
        if choice == "1":
            extracting_data_from_a_book()
            exit()
        elif choice == "2":
            extracting_data_for_all_books_in_category()
            exit()
        elif choice == "3":
            extracting_data_for_all_books_in_site()
            exit()
        elif choice == "4":
            print("Au revoir")
            exit()

    while choice not in selection_available:
        print("Vous devez saisir le bon number")
        main_menu()


main_menu()
