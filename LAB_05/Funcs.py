import numpy as np
import random

STATES = {
    "green_area": 0,
    "burned_area": 1,
    "water": 2,
    "fire": 3
}


def water_based_binarize(image, blue_threshold=150):
    rgb_array = np.array(image)
    blue_channel = rgb_array[:, :, 2]
    binary_blue_image = (blue_channel > blue_threshold).astype(np.uint8)

    state_image = np.zeros_like(binary_blue_image, dtype=np.uint8)
    state_image[binary_blue_image == 0] = STATES["green_area"]
    state_image[binary_blue_image == 1] = STATES["water"]
    return state_image


def initialize_fire(state_image, fire_count=1, fire_radius=1):
    fire_positions = []
    rows, cols = state_image.shape

    for _ in range(fire_count):
        while True:
            x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if state_image[x, y] == STATES["green_area"]:
                fire_positions.append((x, y))
                for dx in range(-fire_radius, fire_radius):
                    for dy in range(-fire_radius, fire_radius):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols:
                            if state_image[nx, ny] == STATES["green_area"]:
                                state_image[nx, ny] = STATES["fire"]
                break

    return state_image, fire_positions


def automaton_step(state_image, fire_duration, wind=None, wind_strength=1):
    new_state = state_image.copy()
    rows, cols = state_image.shape

    wind_directions = {
        "N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1),
        "NE": (-1, 1), "NW": (-1, -1), "SE": (1, 1), "SW": (1, -1)
    }
    reverse_directions = {
        "N": (1, 0), "S": (-1, 0), "E": (0, -1), "W": (0, 1),
        "NE": (1, -1), "NW": (1, 1), "SE": (-1, -1), "SW": (-1, 1)
    }

    wind_dx, wind_dy = wind_directions.get(wind, (0, 0))
    reverse_dx, reverse_dy = reverse_directions.get(wind, (0, 0))

    for x in range(rows):
        for y in range(cols):
            if state_image[x, y] == STATES["fire"]:
                fire_duration[x, y] += 1

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    if random.random() < 0.4:
                        nx = (x + dx) % rows
                        ny = (y + dy) % cols

                        if wind and (dx == wind_dx and dy == wind_dy):
                            nx = (nx + wind_dx * wind_strength) % rows
                            ny = (ny + wind_dy * wind_strength) % cols

                        if state_image[nx, ny] == STATES["green_area"]:
                            new_state[nx, ny] = STATES["fire"]

                if wind:
                    if random.random() < 0.4:
                        opposite_x = (x + reverse_dx) % rows
                        opposite_y = (y + reverse_dy) % cols
                        if state_image[opposite_x, opposite_y] == STATES["green_area"]:
                            new_state[opposite_x, opposite_y] = STATES["fire"]

                if fire_duration[x, y] >= 30:
                    new_state[x, y] = STATES["burned_area"]

            elif state_image[x, y] == STATES["water"]:
                continue

            elif state_image[x, y] == STATES["burned_area"]:
                continue

    return new_state, fire_duration
