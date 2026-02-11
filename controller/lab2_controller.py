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


def filter_image_with_mask(image_path):
    """
    Create Sobel filter mask to detect edges in x- and in y-direction. Filter the input image with these masks and display the results.
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

    # Define Sobel filter masks for x and y direction
    sobel_x = np.array([[10, 0, -10]], dtype=np.float32)

    sobel_y = np.array([[10],
                        [0],
                        [-10]], dtype=np.float32)

    # Apply the Sobel filters to the grayscale image
    filtered_x = cv2.filter2D(gray_image, -1, sobel_x)
    filtered_y = cv2.filter2D(gray_image, -1, sobel_y)

    # Display the original image
    cv2.imshow("Original Image", original_image)

    # Display the filtered images
    cv2.imshow("Sobel Filtered Image (X direction)", filtered_x)
    cv2.imshow("Sobel Filtered Image (Y direction)", filtered_y)

    # Wait for q key press to close the windows
    print("Press 'q' to close the image windows.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Force OpenCV to process window events and close


def create_filter_mask(image_path):
    """
    Create filter masks for the two derivatives of the Gaussian function using 𝜎 = 5 and 𝜎 = 10. Apply those filters to the image and display the results.
    :param image_path:  Path to the input image.
    :return: None
    """
    # Load the original image
    original_image = cv2.imread(image_path)
    if original_image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Define Gaussian derivative filter masks for sigma = 5 and sigma = 10
    sigma_values = [5, 10]
    filtered_images = []

    for sigma in sigma_values:
        ksize = int(6 * sigma + 1)  # Kernel size
        if ksize % 2 == 0:
            ksize += 1  # Ensure kernel size is odd
        ksize = min(ksize, 31)  # Limit maximum kernel size to 31

        # Create Gaussian derivative filters
        gauss_deriv_x = cv2.getDerivKernels(1, 0, ksize, normalize=True)[0]
        gauss_deriv_y = cv2.getDerivKernels(0, 1, ksize, normalize=True)[0]

        # Apply the filters to the grayscale image
        filtered_x = cv2.filter2D(gray_image, -1, gauss_deriv_x)
        filtered_y = cv2.filter2D(gray_image, -1, gauss_deriv_y)

        filtered_images.append((filtered_x, filtered_y, sigma))

    # Display the original image
    cv2.imshow("Original Image", original_image)

    # Display the filtered images
    for filtered_x, filtered_y, sigma in filtered_images:
        cv2.imshow(f"Gaussian Derivative Filtered Image (X direction, σ={sigma})", filtered_x)
        cv2.imshow(f"Gaussian Derivative Filtered Image (Y direction, σ={sigma})", filtered_y)

    # Wait for q key press to close the windows
    print("Press 'q' to close the image windows.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Force OpenCV to process window events and close


def calculate_fourier_transform(image_path):
    """
    Calculate the Fourier transform of the input image and display the absolute values of the spectrum as image.
    Now transform the Fourier spectrum of the image back to the spatial domain and display the resulting image (it should be the same as the input image).
    :param image_path: Path to the input image.
    :return: None
    """
    # Load the original image
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original_image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    sigma = 50
    h, w = original_image.shape
    x, y = np.meshgrid(np.arange(0, w), np.arange(0, h))
    kernel = np.exp(-((x - w / 2) ** 2 + (y - h / 2) ** 2) / (2 * sigma ** 2)) / (2 * np.pi * sigma ** 2)

    # Calculate the 2D Fourier Transform
    ft_img = np.fft.fft2(original_image)
    ft_kernel = np.fft.fft2(np.fft.fftshift(kernel))

    result = abs(np.fft.ifft2(ft_img * ft_kernel)) / 255

    magnitude_spectrum = 20 * np.log(abs(result))
    # Reconstruct the image back to spatial domain
    img_back = np.fft.ifft2(ft_img).real

    # result = cv2.filter2D(img, -1, kernel)
    cv2.imshow("result", result)

    # Display the original image
    cv2.imshow("Original Image", original_image)

    # Display the magnitude spectrum
    cv2.imshow("Magnitude Spectrum", magnitude_spectrum.astype(np.uint8))

    # Display the reconstructed image
    cv2.imshow("Reconstructed Image", img_back.astype(np.uint8))

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
