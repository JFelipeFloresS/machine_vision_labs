from controller.lab1_controller import display_latest_image
from controller.lab1_controller import generate_image
from controller.lab1_controller import capture_video
from view.abstract_menu import AbstractMenu


class Lab1Menu(AbstractMenu):
    def __init__(self):
        main_menu_options = \
            {1: "Capture Video",
             2: "Generate Image from Video",
             3: "View Latest Image",
             9: "Back to Main Menu",
             99: "Exit"}
        super().__init__("Lab 1 Menu", main_menu_options)

    def execute_choice(self, choice):
        if choice == 1:
            capture_video()
        elif choice == 2:
            generate_image()
        elif choice == 3:
            display_latest_image()
        elif choice == 9:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True
