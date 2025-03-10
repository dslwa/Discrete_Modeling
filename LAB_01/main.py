from Lab_01 import *
from histogam import *

darken = darken_image(image, 20)

brighten = brighten_image(image, 20)

darken.save('results/darken.bmp')

brighten.save('results/brighten.bmp')

image.save('results/basic.bmp')

brighten_serially(image, 7, 3)

brighten_serially2(image, 5, 3)

img = binarize(image, 127)

while True:

    try:

        threshold = int(input("Give threshold (0-255, or 300 to exit): "))

        if threshold == 300:

            print("Exiting the program.")

            break

        if 0 <= threshold <= 255:

            binary_image = binarize(image, threshold)

            binary_image.show()

        else:

            print("Threshold out of scope. Please enter a value between 0 and 255 or 300 to exit.")

    except ValueError:

        print("Give integer value.")

    plt.show()
