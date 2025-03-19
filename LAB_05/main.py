from Funcs import *
from visualization import *
from PIL import Image

image_path = "Input/map.png"
image = Image.open(image_path)

state_image = water_based_binarize(image, 120)
state_image, fire_positions = initialize_fire(state_image, fire_count=5, fire_radius=6)

steps = 290
fire_duration = np.zeros_like(state_image, dtype=np.uint8)
state_images = [state_image.copy()]

wind_direction = "SE"  # N, S, E, W, NE, NW, SE, SW lub None
wind_strength = 1

for step in range(steps):
    state_image, fire_duration = automaton_step(
        state_image, fire_duration, wind=wind_direction, wind_strength=wind_strength
    )
    state_images.append(state_image.copy())

animate_simulation(state_images, save_as_gif=True, gif_filename="fire_simulation.gif")
