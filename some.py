import cv2
import numpy as np
from sklearn.cluster import KMeans
from skimage import measure
import svgwrite

# Load the image with transparency (RGBA)
image = cv2.imread('shirt.png', cv2.IMREAD_UNCHANGED)

# Convert the image to RGB and remove alpha channel (since it's a transparent PNG)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)

# Reshape the image to a list of pixels
pixels = image_rgb.reshape((-1, 3))

# Apply K-means clustering to reduce the number of colors (e.g., 10 colors)
num_colors = 10
kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(pixels)

# Get the RGB values of the cluster centers (dominant colors)
dominant_colors = kmeans.cluster_centers_.astype(int)

# Recreate the image using the clustered colors
quantized_image = kmeans.cluster_centers_[kmeans.labels_].reshape(image_rgb.shape).astype(np.uint8)

# Convert the quantized image to grayscale and threshold for segmentation
gray_image = cv2.cvtColor(quantized_image, cv2.COLOR_RGB2GRAY)
_, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)

# Find connected components (regions) in the segmented image
regions = measure.label(binary_image)

# Show segmented regions (just for visualization, optional)
import matplotlib.pyplot as plt
plt.imshow(regions)
plt.show()
