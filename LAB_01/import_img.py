from PIL import Image
import numpy as np


with open('grayscale_image.txt', 'r') as file:

    data = [[int(num) for num in line.split()] for line in file]

image_data = np.array(data, dtype=np.uint8)

image = Image.fromarray(image_data, 'L')
