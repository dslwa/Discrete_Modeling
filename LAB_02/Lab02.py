import numpy as np
from PIL import Image


def binarize(image, threshold=127):
    gray_image = image.convert('L')
    image_data = np.array(gray_image)
    binary_data = (image_data > threshold) * 255
    binary_data = binary_data.astype(np.uint8)

    binary_image = Image.fromarray(binary_data, 'L')
    binary_image.save("Images/Output/binarize.jpg")
    return binary_image


def border_handling(image_matrix, x, y, nx, ny):
    ix = x + nx
    iy = y + ny

    rows = image_matrix.shape[0]
    cols = image_matrix.shape[1]

    if ix >= rows or ix < 0 or iy < 0 or iy >= cols:
        return -1, 0
    else:
        return ix, iy


def dilate(image, radius=1):
    if image.mode != 'L':
        image = image.convert('L')

    img_matrix = np.array(image) / 255.0
    rows, cols = img_matrix.shape

    output_matrix = np.zeros((rows, cols))
    initial_val = 1

    for x in range(rows):
        for y in range(cols):
            result_value = initial_val

            for nx in range(-radius, radius + 1):
                for ny in range(-radius, radius + 1):

                    tx, ty = border_handling(img_matrix, x, y, nx, ny)

                    if tx == -1:
                        neighbour_value = ty
                    else:
                        neighbour_value = img_matrix[tx, ty]

                    result_value = min(result_value, neighbour_value)

            output_matrix[x, y] = result_value

    output_matrix = (output_matrix * 255).astype(np.uint8)

    output_image = Image.fromarray(output_matrix, 'L')
    output_image.save("Images/Output/dilate.jpg")

    return output_image


def erode(image, radius=1):
    if image.mode != 'L':
        image = image.convert('L')

    img_matrix = np.array(image) / 255.0
    rows, cols = img_matrix.shape

    output_matrix = np.zeros((rows, cols))

    initial_val = 0

    for x in range(rows):
        for y in range(cols):
            result_value = initial_val

            for nx in range(-radius, radius + 1):
                for ny in range(-radius, radius + 1):

                    tx, ty = border_handling(img_matrix, x, y, nx, ny)

                    if tx == -1:
                        neighbour_value = ty
                    else:
                        neighbour_value = img_matrix[tx, ty]

                    result_value = max(result_value, neighbour_value)

            output_matrix[x, y] = result_value

    output_matrix = (output_matrix * 255).astype(np.uint8)

    output_image = Image.fromarray(output_matrix, 'L')
    output_image.save("Images/Output/erode.jpg")

    return output_image


def opening(image, radius=1):
    eroded_image = erode(image, radius)
    opened_image = dilate(eroded_image, radius=3)
    opened_image.save("Images/Output/opened.jpg")
    return opened_image


def closing(image, radius=1):
    dilated_image = dilate(image, radius)
    closed_image = erode(dilated_image, radius=3)
    closed_image.save("Images/Output/closed.jpg")
    return closed_image


def apply_convulsion(image, mask):
    img_matrix = np.array(image, dtype=np.float32)

    if len(img_matrix.shape) == 2:
        img_matrix = img_matrix[:, :, np.newaxis]

    rows, cols, channels = img_matrix.shape
    mask_size = mask.shape[0]
    pad_size = mask_size // 2

    mask_sum = np.sum(mask)
    if mask_sum == 0:
        mask_sum = 1

    output_matrix = np.zeros((rows, cols, channels), dtype=np.float32)

    for x in range(rows):
        for y in range(cols):
            pixel_values = [0] * channels
            for lx in range(-pad_size, pad_size + 1):
                for ly in range(-pad_size, pad_size + 1):
                    tx, ty = border_handling(img_matrix[:, :, 0], x, y, lx, ly)
                    if tx != -1:
                        for i in range(channels):
                            pixel_values[i] += img_matrix[tx, ty, i] * mask[lx + pad_size, ly + pad_size]

            for i in range(channels):
                output_matrix[x, y, i] = pixel_values[i] / mask_sum

    org_max = np.max(img_matrix)
    org_min = np.min(img_matrix)
    out_max = np.max(output_matrix)
    out_min = np.min(output_matrix)

    if out_max - out_min > 0:
        output_matrix = (output_matrix - out_min) / (out_max - out_min) * (org_max - org_min) + org_min
    else:
        output_matrix = np.clip(output_matrix, org_min, org_max)

    output_matrix = np.clip(output_matrix, 0, 255)

    output_matrix = np.array(output_matrix, dtype=np.uint8)
    output_image = Image.fromarray(output_matrix.squeeze())

    return output_image
