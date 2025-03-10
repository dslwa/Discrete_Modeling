import numpy as np
from PIL import Image


def darken_image(image, percent):

    if not (1 <= percent <= 99):
        raise ValueError("Percent out of scope")

    image_data = np.array(image, dtype=np.float32)

    factor = (100 - percent) / 100.0

    darken_data = image_data * factor

    darken_data = np.clip(darken_data, 0, 255).astype(np.uint8)

    darken_image_result = Image.fromarray(darken_data, 'L')

    return darken_image_result


def brighten_image(image, percent):

    if not (1 <= percent <= 99):
        raise ValueError("Percent out of scope")

    image_data = np.array(image, dtype=np.float32)

    factor = 1 + (percent / 100.0)

    brighten_data = image_data * factor

    brighten_data = np.clip(brighten_data, 0, 255).astype(np.uint8)

    brighten_data_result = Image.fromarray(brighten_data, 'L')

    return brighten_data_result


def brighten_serially(image, step_percent, num_images):

    for i in range(num_images):

        percent = step_percent * (i + 1)

        brightened_image = brighten_image(image, percent)

        brightened_image.save(f'results/brightened_image_{percent}.png')


def brighten_serially2(image, step_percent, num_images):
    current_image = image

    for i in range(num_images):

        percent = step_percent

        current_image = brighten_image(current_image, percent)

        current_image.save(f'results/brightened_image_2nd{ i }.png')


def binarize(image, threshold):

    image_data = np.array(image)

    binary_data = (image_data > threshold) * 255

    binary_image = Image.fromarray(binary_data.astype(np.uint8), 'L')

    binary_image.save(f'results/binary_image_{threshold}.png')

    return binary_image
