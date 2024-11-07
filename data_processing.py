# Process data
from PIL import Image
import os

def crop_to_square(image_path, output_path=None):
    """
    Crop an image to a square around the center.

    Args:
    image_path (str): The path to the input image.
    output_path (str): The path where the cropped image will be saved. If None, overwrite the input image.

    Returns:
    None
    """
    with Image.open(image_path) as img:
        # Get dimensions
        width, height = img.size
        print(width)
        print(height)
        # Determine the size of the square and the top left coordinates
        new_size = min(width, height)
        left = (width - new_size) // 2
        right = (width + new_size) // 2
        top = height - new_size
        bottom = height

        # Crop the image
        img_cropped = img.crop((left, top, right, bottom))

        # Save the cropped image
        if output_path is None:
            output_path = image_path
        img_cropped.save(output_path)
        print(f"Image saved to {output_path}")

def resize_image(image_path, output_path=None, new_size=(1080, 1080)):
    """
    Resize an image to new dimensions.

    Args:
    image_path (str): The path to the input image.
    output_path (str): The path where the resized image will be saved. If None, overwrite the input image.
    new_size (tuple): The new size as a tuple, default is (1080, 1080).

    Returns:
    None
    """
    with Image.open(image_path) as img:
        # Check if the image is square
        if img.width != img.height:
            raise ValueError("Image is not square. Please provide a square image.")

        # Resize the image
        img_resized = img.resize(new_size, Image.LANCZOS)

        # Save the resized image
        if output_path is None:
            output_path = image_path
        img_resized.save(output_path)
        print(f"Resized image saved to {output_path}")

# Compile dataset

# Host on huggingface


if __name__ == "__main__":
    #image_path = "test_image.jpg"  # Replace with the path to your image
    #crop_to_square(image_path, "test_image_result.jpg")
    image_path = "test_image_result.jpg"  # Replace with the path to your image
    resize_image(image_path=image_path, output_path="test_resize_result.jpg")


