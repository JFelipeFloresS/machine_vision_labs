from controller.lab2_controller import gray_scale, apply_filter_2d, filter_image_with_mask, create_filter_mask, \
    calculate_fourier_transform
from utils.file_utils import LAB2_CAT_IMAGE_PATH
from view.abstract_menu import AbstractMenu


class Lab2Menu(AbstractMenu):
    def __init__(self):
        main_menu_options = \
            {1: "Gray Scale Conversion",
             2: "Filter Image With Mask",
             3: "Create Filter Masks",
             4: "Calculate Fourier Transform",
             5: "Apply Filter 2D",
             9: "Back to Main Menu",
             99: "Exit"}
        super().__init__("Lab 2 Menu", main_menu_options)

    def execute_choice(self, choice):
        if choice == 1:
            gray_scale(LAB2_CAT_IMAGE_PATH)
        elif choice == 2:
            filter_image_with_mask(LAB2_CAT_IMAGE_PATH)
        elif choice == 3:
            create_filter_mask(LAB2_CAT_IMAGE_PATH)
        elif choice == 4:
            calculate_fourier_transform(LAB2_CAT_IMAGE_PATH)
        elif choice == 5:
            apply_filter_2d(LAB2_CAT_IMAGE_PATH)
        elif choice == 9:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True
