from PIL import Image
import numpy as np
import colorsys
import json
from collections import Counter

# Load the Pokémon data
with open('pokemon_data.json', 'r') as file:
    pokemon_data = json.load(file)

# Loop over each Pokémon
for pokemon in pokemon_data:
    # Open the image file
    with Image.open(f'pokemon_images/{pokemon["src"]}') as img:
        # Convert the image to RGBA
        rgba_img = img.convert('RGBA')

    # Flatten the image into a list of RGBA values
    rgba_values = list(rgba_img.getdata())

    # Filter out transparent pixels and keep only the RGB values
    rgb_values = [rgba[:3] for rgba in rgba_values if rgba[3] > 0]

    # Calculate the mode RGB values
    mode_rgb = Counter(rgb_values).most_common(1)[0][0]

    # Add the mode color to the Pokémon's data
    pokemon['dominant_color'] = mode_rgb

    # Write the updated data back to the JSON file
    with open('pokemon_data.json', 'w') as file:
        json.dump(pokemon_data, file)