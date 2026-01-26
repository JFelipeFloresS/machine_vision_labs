import cv2
import numpy as np

def gray_scale(image_path):
    """
    Load the input image and convert it into grayscale. Display both the original and the grayscale image.
    :param image_path: Path to the input image.
    :return: None
    """
    # Load the original image
    original_image = cv2.imread(image_path)
    if original_image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Display the original image
    cv2.imshow("Original Image", original_image)

    # Display the grayscale image
    cv2.imshow("Grayscale Image", gray_image)

    # Wait for q key press to close the windows
    print("Press 'q' to close the image windows.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Force OpenCV to process window events and close

def apply_filter_2d(image_path):
    """
    Load the input image and apply a 2D filter (blurring effect). Display both the original and the filtered image.
    :param image_path: Path to the input image.
    :return: None
    """
    # Load the original image
    original_image = cv2.imread(image_path)
    if original_image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    # Define a 5x5 averaging filter kernel
    kernel = np.ones((5, 5), np.float32) / 25

    # Apply the filter to the image
    filtered_image = cv2.filter2D(original_image, -1, kernel)

    # Display the original image
    cv2.imshow("Original Image", original_image)

    # Display the filtered image
    cv2.imshow("Filtered Image", filtered_image)

    # Wait for q key press to close the windows
    print("Press 'q' to close the image windows.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Force OpenCV to process window events and close