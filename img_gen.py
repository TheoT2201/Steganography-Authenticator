from PIL import Image
import random

def generate_random_image(width, height):
    # Create a new image with RGB mode
    image = Image.new("RGB", (width, height))
    # Load the pixel map
    pixels = image.load()

    for i in range(width):
        for j in range(height):
            # Assign random RGB values
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            # Set the colour accordingly
            pixels[i, j] = (red, green, blue)

    return image