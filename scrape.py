from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm

# Directory to save images
save_dir = 'pokemon_images'
os.makedirs(save_dir, exist_ok=True)

# Base URL of the Bulbapedia
base_url = 'https://bulbapedia.bulbagarden.net'

# URL of the National Pokédex page
pokedex_url = f'{base_url}/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'

# Fetch the National Pokédex page
response = requests.get(pokedex_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all tables with class "roundy"
pokedex_tables = soup.find_all('table', class_='roundy')

# Initialize a list to store all Pokémon rows
pokemon_rows = []

# Loop through each table
for table in pokedex_tables:
    # Find all Pokémon rows in the current table and add them to the list
    pokemon_rows += table.select('tr')

print(f"Found {len(pokemon_rows)} Pokémon forms.")

# Initialize the progress bar
pbar = tqdm(total=len(pokemon_rows), ncols=70, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {postfix}')

# Loop through each Pokémon row
for i, pokemon_row in enumerate(pokemon_rows):
    # Find the Pokémon name and image URL
    pokemon_link = pokemon_row.find('a')
    if pokemon_link:
        pokemon_name = pokemon_link.get('title')
        pokemon_image = pokemon_link.find('img')
        if pokemon_image:
            image_url = pokemon_image.get('src')

            # Check if the image URL is relative
            if image_url.startswith('/'):
                # Convert the relative URL to an absolute URL
                image_url = f'{base_url}{image_url}'

            # Send a GET request to the image URL
            response = requests.get(image_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Save the image
                with open(os.path.join(save_dir, f"{pokemon_name}_{i}.png"), 'wb') as file:
                    file.write(response.content)
                pbar.set_postfix_str(f"Downloading {pokemon_name}")
            else:
                pbar.set_postfix_str(f"Failed to download {pokemon_name}")

    # Update the progress bar
    pbar.update()

pbar.close()
print("All images downloaded.")