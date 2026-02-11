import os

curr_dir = os.path.dirname(__file__)
curr_dir = os.path.join(curr_dir, "../")
output_dir = os.path.abspath(os.path.join(curr_dir, 'output'))
IMAGE_DIR = os.path.join(output_dir, 'images')
VIDEO_DIR = os.path.join(output_dir, 'videos')

# lab2 directory in assets/lab2/cat.png
LAB2_DIR = os.path.abspath(os.path.join(curr_dir, 'assets/lab2'))
LAB2_CAT_IMAGE_PATH = os.path.join(LAB2_DIR, 'cat.png')

# lab3 directory in assets/lab3
LAB3_DIR = os.path.abspath(os.path.join(curr_dir, 'assets/lab3'))
LAB3_INPUT_IMAGE_PATH = os.path.join(LAB3_DIR, 'Girl_in_front_of_a_green_background.jpg')
LAB3_TARGET_IMAGE_PATH = os.path.join(LAB3_DIR, 'Tour_Eiffel.jpg')