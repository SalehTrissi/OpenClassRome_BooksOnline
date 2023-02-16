import constants
from scripting import extracting_data_from_a_book


def main_menu():
    """
    Affiche le menu principale
    """
    print(constants.MENU)
    choice = input('Votre choix : ')
    selection_available = ["1", "2"]
    while choice in selection_available:
        if choice == "1":
            extracting_data_from_a_book()
            exit()
        elif choice == "2":
            print("Au revoir")
            exit()


main_menu()
