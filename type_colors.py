import json
import colorsys
import numpy as np
from colorama import Fore, Back, Style, init
init(autoreset=True)

# Load the Pokémon data
with open('pokemon_data.json', 'r') as file:
    pokemon_data = json.load(file)

# Create a dictionary to store the average color and count for each type combination
type_colors = {}

# Loop over each Pokémon
for pokemon in pokemon_data:
    # Get the types and average color of the Pokémon
    types = tuple(sorted(pokemon['types']))
    dominant_color = pokemon['dominant_color']

    # Convert RGB to HSL
    hsl_color = colorsys.rgb_to_hls(*[x/255. for x in dominant_color])

    # Adjust colors to make them more vibrant
    hsl_color = (hsl_color[0], 0.5, 1)

    # Add the average color to the corresponding entry in the dictionary
    if types in type_colors:
        type_colors[types]['colors'].append(hsl_color)
        type_colors[types]['count'] += 1
    else:
        type_colors[types] = {'colors': [hsl_color], 'count': 1}

# Calculate the average color for each type combination
for types, data in type_colors.items():
    # Calculate the average HSL values
    avg_hsl = np.mean(data['colors'], axis=0)

    # Convert the average HSL values back to RGB
    avg_rgb = colorsys.hls_to_rgb(*avg_hsl)

    # Round the RGB values and convert to int
    avg_rgb_rounded = tuple(map(lambda x: round(x*255), avg_rgb))

    type_colors[types]['dominant_color'] = avg_rgb_rounded

# Print the results
for types, data in type_colors.items():
    r, g, b = data['dominant_color']
    # Convert RGB to console color (0-255 to 0-7)
    console_color = (r // 32, g // 32, b // 32)
    # Create ANSI escape code for this color
    color_code = f'\033[38;2;{console_color[0]*36};{console_color[1]*36};{console_color[2]*36}m'
    print(f'{color_code}{", ".join(types)}: {data["dominant_color"]}, count: {data["count"]}')