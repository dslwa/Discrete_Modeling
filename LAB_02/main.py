from Lab02 import *
import os
img = Image.open("Images/Input/image.jpg")
img.convert('L')


def load_mask(filename, delimiter=","):
    if not os.path.exists(filename):
        print(f"Plik {filename} nie istnieje. Sprawdź ścieżkę.")
        return None
    with open(filename, 'r') as file:
        matrix = [[float(num) for num in line.split(delimiter)] for line in file]
        return np.array(matrix, dtype=np.float32)


image = binarize(img)
image2 = dilate(image)
image3 = erode(image, 2)

image4 = opening(image)
image5 = closing(image)

mask3x3 = load_mask("Images/Masks/Maska3x3")
mask5x5 = load_mask("Images/Masks/Maska5x5")

if mask5x5 is not None:
    img4 = apply_convulsion(image, mask5x5)
    img4.save("Images/Output/splot5x5.jpg")
else:
    print("Wrong file path")

if mask3x3 is not None:
    img5 = apply_convulsion(image, mask3x3)
    img5.save("Images/Output/splot3x3.jpg")
else:
    print("Nie udało się załadować maski 3x3. Sprawdź ścieżkę do pliku.")