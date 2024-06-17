from PIL import Image
import numpy as np
import colorsys
import json

# Load the Pokémon data
with open('pokemon_data.json', 'r') as file:
    pokemon_data = json.load(file)

# Loop over each Pokémon
for pokemon in pokemon_data:
    # Open the image file
    with Image.open(f'pokemon_images/{pokemon["src"]}') as img:
        # Convert the image to RGB
        rgb_img = img.convert('RGB')

    # Flatten the image into a list of RGB values
    rgb_values = list(rgb_img.getdata())

    # Convert RGB values to HSL
    hsl_values = [colorsys.rgb_to_hls(r/255., g/255., b/255.) for r, g, b in rgb_values]

    # Calculate the average HSL values
    avg_hsl = np.mean(hsl_values, axis=0)

    # Convert the average HSL values back to RGB
    avg_rgb = colorsys.hls_to_rgb(*avg_hsl)

    # Round the RGB values and convert to int
    avg_rgb_rounded = tuple(map(lambda x: round(x*255), avg_rgb))

    # Add the average color to the Pokémon's data
    pokemon['average_color'] = avg_rgb_rounded

    # Write the updated data back to the JSON file
    with open('pokemon_data.json', 'w') as file:
        json.dump(pokemon_data, file)