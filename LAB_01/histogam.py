from import_img import *
import matplotlib.pyplot as plt
import numpy as np

image_data = np.array(image)

unique, counts = np.unique(image_data, return_counts=True)

plt.figure(figsize=(8, 6))


bar_width = 1

plt.bar(unique, counts, width=bar_width, color='blue', alpha=0.7)

plt.title("Pixel Value Distribution", fontsize=16)

plt.xlabel("Pixel Value", fontsize=14)

plt.ylabel("Count", fontsize=14)

plt.grid(True)

plt.xticks([0, 128, 256], fontsize=12)

plt.yticks(np.arange(0, 35001, 10000), fontsize=12)

plt.xlim(-10, 266)

max_index = np.argmax(counts)

most_frequent_pixel = unique[max_index]

frequency = counts[max_index]

print(most_frequent_pixel)
