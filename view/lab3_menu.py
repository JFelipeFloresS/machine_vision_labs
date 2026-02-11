from controller.lab3_controller import task1, task2, task3
from utils.file_utils import LAB3_INPUT_IMAGE_PATH, LAB3_TARGET_IMAGE_PATH
from utils.user_input_handler import get_user_input
from view.abstract_menu import AbstractMenu


class Lab3Menu(AbstractMenu):
    def __init__(self):
        main_menu_options = \
            {1: "Task 1: Load and Display Input and Target images. Convert the input image into HSV colour and extract the hue channel. Also display the hue channel image.",
             2: "Task 2: Calculate the histogram of the hue channel to determine the thresholds for removing the bg. Apply the thresholds to the Hue channel to create a binary mask. Display the foreground mask.",
             3: "Task 3: Cut the foreground from the input image using the binary mask and paste it onto the target image. Display the result.",
             9: "Back to Main Menu",
             99: "Exit"}
        super().__init__("Lab 3 Menu", main_menu_options)

    def execute_choice(self, choice):
        if choice == 1:
            task1(LAB3_INPUT_IMAGE_PATH, LAB3_TARGET_IMAGE_PATH)
        elif choice == 2:
            display_histogram = get_user_input("Do you want to display the histogram of the Hue channel? (y/n): ", available_options=['y', 'n'], default_value="n") == 'y'
            task2(LAB3_INPUT_IMAGE_PATH, display_histogram)
        elif choice == 3:
            task3(LAB3_INPUT_IMAGE_PATH, LAB3_TARGET_IMAGE_PATH)
        elif choice == 9:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True