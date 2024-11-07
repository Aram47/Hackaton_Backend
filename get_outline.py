import os
import cv2
import numpy as np
import svgwrite
from PIL import Image

def convert_png_to_black(input_path, output_path):
    # Open the PNG image
    image = Image.open(input_path).convert("RGBA")

    # Make the image black
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a > 0:  # If not transparent
                pixels[x, y] = (0, 0, 0, a)  # Convert to black

    # Save the modified image
    image.save(output_path)

def png_to_svg_with_outline(png_path, svg_path, contour_thickness=5):
    # Read the image using OpenCV
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)

    # Extract the alpha channel (transparency)
    alpha_channel = img[:, :, 3]

    # Invert alpha channel to make the non-transparent areas white
    _, binary_img = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the image
    img_with_contours = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(img_with_contours, contours, -1, (0, 0, 255), contour_thickness)

    # # Display the image with contours
    # cv2.imshow("Contours", img_with_contours)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Create an SVG drawing with the same dimensions as the input image
    height, width = img.shape[:2]
    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(width, height))

    # Combine all contours into a single path string
    path_data = ""
    for contour in contours:
        if len(contour) > 0:
            path_data += "M" + " L".join([f"{point[0][0]},{point[0][1]}" for point in contour]) + " Z "

    # Add the combined path to the SVG with thicker stroke width
    dwg.add(dwg.path(d=path_data, fill='none', stroke='black', stroke_width=contour_thickness))

    # Save the SVG
    dwg.save()

    print(f"Converted {png_path} to {svg_path}")

def convert_and_get_outline(input_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = "result"
    input_path = os.path.join(input_dir, filename + ".png")
    temp_black_path = os.path.join(output_dir, "temp_black_image.png")
    output_svg_path = os.path.join(output_dir, filename + ".svg")

    # Convert PNG to a fully black image
    convert_png_to_black(input_path, temp_black_path)

    # Extract outline contour and convert to SVG with a thicker outline
    png_to_svg_with_outline(temp_black_path, output_svg_path, contour_thickness=5)

    # Optionally, remove the temporary black image file
    os.remove(temp_black_path)

# Example usage
input_directory = "./imgs"  # Replace with your input directory path
output_directory = "./svg_output"  # Replace with your desired output directory path

convert_and_get_outline(input_directory, output_directory)
