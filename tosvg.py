import os
from PIL import Image, ImageOps, ImageFilter
import vtracer

def convert_png_to_svg(input_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prompt for the PNG file name
    filename = input("Input png file name: ")
    input_path = os.path.join(input_dir, filename + ".png")

    # Open the PNG image
    image = Image.open(input_path).convert("RGBA")

    # Step 1: Make the image black (keep alpha transparent, convert colors to black)
    image = make_image_black(image)

    # Step 2: Convert to grayscale to simplify edge detection
    grayscale_image = image.convert("L")  # Convert to grayscale

    # Step 3: Apply a threshold to turn the image into pure black and white
    thresholded_image = grayscale_image.point(lambda p: p > 128 and 255)  # Any value > 128 becomes white, else black

    # Step 4: Apply edge detection (e.g., using a filter)
    edge_image = thresholded_image.filter(ImageFilter.FIND_EDGES)

    # Step 5: Invert the image so the edges become black
    edge_image = ImageOps.invert(edge_image)

    # Step 6: Remove the background (make white areas transparent)
    edge_image = make_background_transparent(edge_image)

    # Save the edge-detected image temporarily
    temp_path = os.path.join(output_dir, "temp_edges.png")
    edge_image.save(temp_path)

    # Step 7: Convert the image with the outline (transparent background) to SVG using vtracer
    output_path = os.path.splitext(input_path)[0] + "_outline.svg"
    vtracer.convert_image_to_svg_py(temp_path, output_path, colormode='color')

    print(f"Converted {input_path} to {output_path}")

    # Optionally, remove the temporary edge image file
    os.remove(temp_path)

def make_image_black(image):
    """
    Converts the image to black (RGB: 0, 0, 0) where non-transparent pixels are,
    keeping the alpha channel unchanged.
    """
    image = image.convert("RGBA")
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a > 0:  # If not transparent
                pixels[x, y] = (0, 0, 0, a)  # Convert to black (retain alpha)

    return image

def make_background_transparent(image):
    """
    Converts all white pixels in the image to transparent.
    This is useful to remove the white background and keep only the black outlines.
    """
    image = image.convert("RGBA")
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if r == 255 and g == 255 and b == 255:  # Check for white pixels
                pixels[x, y] = (0, 0, 0, 0)  # Make it fully transparent

    return image

# Example usage
input_directory = "."  # Replace with your input directory path
output_directory = "./svg_output"  # Replace with your desired output directory path
convert_png_to_svg(input_directory, output_directory)
