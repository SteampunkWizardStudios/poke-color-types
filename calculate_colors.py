import json
from PIL import Image

# Load the Pokémon data
with open('pokemon_data.json', 'r') as file:
    pokemon_data = json.load(file)

# Loop over each Pokémon
for pokemon in pokemon_data:
    # Open the image file
    with Image.open(f'pokemon_images/{pokemon["src"]}') as img:
        # Convert the image to RGB
        rgb_img = img.convert('RGB')

        # Calculate the average color
        r_total, g_total, b_total = 0, 0, 0
        num_pixels = rgb_img.width * rgb_img.height
        for x in range(rgb_img.width):
            for y in range(rgb_img.height):
                r, g, b = rgb_img.getpixel((x, y))
                r_total += r
                g_total += g
                b_total += b
        average_color = (r_total // num_pixels, g_total // num_pixels, b_total // num_pixels)

        # Add the average color to the Pokémon's data
        pokemon['average_color'] = average_color

# Write the updated data back to the JSON file
with open('pokemon_data.json', 'w') as file:
    json.dump(pokemon_data, file)