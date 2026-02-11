from view.abstract_menu import AbstractMenu

from view.lab1_menu import Lab1Menu
from view.lab2_menu import Lab2Menu
from view.lab3_menu import Lab3Menu


class MainMenu(AbstractMenu):
    def __init__(self):
        main_menu_options = \
            {1: "Lab 1",
             2: "Lab 2",
             3: "Lab 3",
             99: "Exit"}
        super().__init__("Main Menu", main_menu_options)

    def execute_choice(self, choice):
        if choice == 1:
            Lab1Menu().run()
        elif choice == 2:
            Lab2Menu().run()
        elif choice == 3:
            Lab3Menu().run()
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True
