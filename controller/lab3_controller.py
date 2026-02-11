import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

from utils.file_utils import IMAGE_DIR

# Determine thresholds for removing the green background (these values may need to be adjusted)
lower_thresholds = [59]  # Lower bound for green hue
upper_thresholds = [75]  # Upper bound for green hue
display_threshold_values = False

def task1(input_image_path: str, target_image_path: str) -> None:
    """
    Load and display the input image and the target image. Convert the input image into HSV colour
    representation and extract the Hue channel. Also display the Hue channel image.
    :param input_image_path: Path to the input image.
    :param target_image_path: Path to the target image.
    :return: None
    """
    # Load the input and target images
    input_image = cv2.imread(input_image_path)
    target_image = cv2.imread(target_image_path)

    if input_image is None:
        print(f"Error: Unable to load input image at {input_image_path}")
        return

    if target_image is None:
        print(f"Error: Unable to load target image at {target_image_path}")
        return

    # Convert the input image to HSV color space
    hsv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    # Extract the Hue channel
    hue_channel = hsv_image[:, :, 0]

    # Display the input image, target image, and hue channel
    cv2.imshow("Input Image", input_image)
    cv2.imshow("Target Image", target_image)
    cv2.imshow("Hue Channel", hue_channel)

    # Wait for q key press to close the windows
    print("Press 'q' to close the image windows.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Force OpenCV to process window events and close

def task2(input_image_path: str, display_histogram: bool = True) -> None:
    """
    Calculate and display the histogram of the Hue channel image to determine the thresholds for
    removing the green background. Apply the thresholds to the Hue channel image to calculate a
    binary mask of the foreground. Display the foreground mask.
    :param input_image_path: Path to the input image.
    :param display_histogram: Whether to display the histogram of the Hue channel.
    :return: None
    """
    # Load the input image
    input_image = cv2.imread(input_image_path)

    if input_image is None:
        print(f"Error: Unable to load input image at {input_image_path}")
        return

    # Invert the mask to get the foreground
    foreground_mask = get_foreground_mask(input_image_path, display_histogram)

    # Display the foreground mask
    cv2.imshow("Foreground Mask", foreground_mask)

    # save the foreground mask for debugging purposes
    generated_file_name = f"{IMAGE_DIR}/lab3/foreground_mask_{lower_thresholds}x{upper_thresholds}_{display_threshold_values}.png"

    does_file_exist = os.path.isfile(generated_file_name)
    if not does_file_exist:
        cv2.imwrite(generated_file_name, foreground_mask)

    # Wait for q key press to close the windows
    print("Press 'q' to close the image windows.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Force OpenCV to process window events and close

def task3(input_image_path: str, target_image_path: str) -> None:
    """
    Cut out the foreground from the input image and resize the cut-out to 300x200 pixels. Replace the
    pixels of the target image with the cut-out, so that the foreground appears at the bottom in the
    middle of the target image. The background of the cut-out should be transparent.
    :param input_image_path: Path to the input image.
    :param target_image_path: Path to the target image.
    :return: None
    """
    # Load the input and target images
    input_image = cv2.imread(input_image_path)
    target_image = cv2.imread(target_image_path)
    target_expected_width = 300
    target_expected_height = 400

    if input_image is None:
        print(f"Error: Unable to load input image at {input_image_path}")
        return

    if target_image is None:
        print(f"Error: Unable to load target image at {target_image_path}")
        return

    # Create a binary mask where the green background is removed
    foreground_mask = get_foreground_mask(input_image_path)

    # Invert the mask to get the foreground
    foreground_mask = cv2.bitwise_not(foreground_mask)

    # Cut out the foreground from the input image using the mask
    foreground = cv2.bitwise_and(input_image, input_image, mask=foreground_mask)

    # Resize the cut-out foreground and mask
    resized_foreground = cv2.resize(foreground, (target_expected_width, target_expected_height))
    resized_mask = cv2.resize(foreground_mask, (target_expected_width, target_expected_height), interpolation=cv2.INTER_NEAREST)

    # Add alpha channel to the resized foreground
    b, g, r = cv2.split(resized_foreground)
    alpha = resized_mask
    rgba = cv2.merge((b, g, r, alpha))

    # Prepare the target image for overlay (convert to BGRA if needed)
    if target_image.shape[2] == 3:
        target_bgra = cv2.cvtColor(target_image, cv2.COLOR_BGR2BGRA)
    else:
        target_bgra = target_image.copy()

    target_height, target_width = target_bgra.shape[:2]
    x_offset = (target_width - target_expected_width) // 2
    y_offset = target_height - target_expected_height

    # Overlay the RGBA foreground onto the target image using alpha blending
    roi = target_bgra[y_offset:y_offset+target_expected_height, x_offset:x_offset+target_expected_width]
    alpha_fg = rgba[:, :, 3] / 255.0
    alpha_bg = 1.0 - alpha_fg
    for c in range(3):
        roi[:, :, c] = (alpha_fg * rgba[:, :, c] + alpha_bg * roi[:, :, c]).astype('uint8')
    roi[:, :, 3] = np.maximum(roi[:, :, 3], rgba[:, :, 3])
    target_bgra[y_offset:y_offset+target_expected_height, x_offset:x_offset+target_expected_width] = roi

    # Display the result (convert to BGR for OpenCV display)
    display_img = cv2.cvtColor(target_bgra, cv2.COLOR_BGRA2BGR)
    cv2.imshow("Result Image (Foreground Transparent)", display_img)

    # Wait for q key press to close the windows
    print("Press 'q' to close the image windows.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Force OpenCV to process window events and close

def get_foreground_mask(input_image_path: str, display_histogram: bool = False) -> np.ndarray:
    """
    Helper function to get the foreground mask for the input image.
    :param input_image_path: Path to the input image.
    :param display_histogram: Whether to display the histogram of the Hue channel.
    :return: Foreground mask as a binary image.
    """
    # Load the input image
    input_image = cv2.imread(input_image_path)

    if input_image is None:
        print(f"Error: Unable to load input image at {input_image_path}")
        # Return a zero mask of default size (1x1) to avoid NoneType issues
        return np.zeros((1, 1), dtype=np.uint8)

    # Convert the input image to HSV color space
    hsv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    # Extract the Hue channel
    hue_channel = hsv_image[:, :, 0]

    # Initialize the mask to zeros
    background_mask = np.zeros_like(hue_channel, dtype=np.uint8)

    # Create a binary mask where the green background is detected using arrays of thresholds
    for index in range(len(lower_thresholds)):
        low = lower_thresholds[index]
        high = upper_thresholds[index]
        mask = cv2.inRange(hue_channel, low, high)
        background_mask = mask if index == 0 else cv2.bitwise_or(background_mask, mask)

    # Invert the background mask to get the foreground mask
    if display_threshold_values:
        foreground_mask = cv2.bitwise_not(background_mask)
    else:
        foreground_mask = background_mask

    # Calculate the histogram of the Hue channel
    hist = cv2.calcHist([hue_channel], [0], None, [180], [0, 180])

    # Display the histogram of the Hue channel if requested
    if display_histogram:
        plt.figure(figsize=(15, 5))  # Set the plot width to 12 inches and height to 5 inches
        plt.plot(hist)
        plt.title("Hue Channel Histogram")
        plt.xlabel("Hue Value")
        plt.ylabel("Frequency")
        plt.xlim([0, 180])
        # make the hue value markers to display every 5 hue values
        plt.xticks(np.arange(0, 181, 5))
        plt.yticks(np.arange(0, 150000, 10000))
        plt.show()

    return foreground_mask