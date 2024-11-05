import requests # type: ignore
from bs4 import BeautifulSoup
import pandas as pd # type: ignore


# URL to the Pokedex
pokedexurl = 'https://pokemondb.net/pokedex/all'
pokedexresponse = requests.get(pokedexurl)
pokedexsoup = BeautifulSoup(pokedexresponse.text, 'html.parser')

# Locate Pokedex Table
nationaldex = pokedexsoup.find('table', {'id': 'pokedex'})

# Extract Pokedex Data
pokedata = []
rows = nationaldex.find('tbody').find_all('tr')

for row in rows:
    p = {}
    columns = row.find_all('td')

    p['Number'] = int(columns[0].text.strip())
    p['Name'] = columns[1].find('a').text.strip()
    small_tag = columns[1].find('small')  # Try to find the <small> tag to see if it is an alternate form
    if small_tag:  # Check if the small tag exists
        p['Name'] = small_tag.text.strip()  # Extract the text if found
    p['Type'] = ', '.join([type_.text.strip() for type_ in columns[2].find_all('a')])
    p['Total'] = columns[3].text.strip()
    p['Hp'] = columns[4].text.strip()
    p['Attack'] = columns[5].text.strip()
    p['Defense'] = columns[6].text.strip()
    p['Sp_atk'] = columns[7].text.strip()
    p['Sp_def'] = columns[8].text.strip()
    p['Speed'] = columns[9].text.strip()

    pokedata.append(p)

# Function to assign region based on corresponding pokemon number
def assign_generation(number):
    if 1 <= number <= 151:
        return 1
    elif 152 <= number <= 251:
        return 2
    elif 252 <= number <= 386:
        return 3
    elif 387 <= number <= 493:
        return 4
    elif 494 <= number <= 649:
        return 5
    elif 650 <= number <= 721:
        return 6
    elif 722 <= number <= 809:
        return 7
    elif 810 <= number <= 898:
        return 8
    else:
        return 9  # Adjust for any new generations (Current assign_generation version is as of 10/24)

# ----------------------Adding region and generation to pokedata---------------------------------------------------------------------------------------------
for pokemon in pokedata:
    pokemon['Generation'] = assign_generation(pokemon['Number'])

# Legendary and Mythical Numbers
legendary_pokemon_numbers = [
    144, 145, 146, 150, 243, 244, 245, 249, 250, 377, 378, 379, 
    380, 381, 382, 383, 384, 480, 481, 482, 483, 484, 485, 487, 
    488, 638, 639, 640, 641, 642, 643, 644, 716, 717, 718, 785, 
    786, 787, 788, 789, 790, 791, 792, 888, 889, 890
] # As of 10/24

mythical_pokemon_numbers = [
    151, 251, 385, 386, 489, 490, 492, 493, 494, 
    647, 648, 649, 719, 720, 721, 801, 802, 807, 
    893, 894, 895, 896, 897, 898
] # As of 10/24

#Function to assign Legendary or Mythical Status
def assign_legendary_mythical(number):
    if number in legendary_pokemon_numbers:
        is_legendary = "Legendary"
    else:
        is_legendary = "No"
    if number in mythical_pokemon_numbers:
        is_mythical = "Mythical"
    else:
        is_mythical = "No"
    return is_legendary, is_mythical

#Adding Legendary and Mythical to pokedata
for pokemon in pokedata:
    pokemon['Legendary'], pokemon['Mythical'] = assign_legendary_mythical(pokemon['Number'])

#---------------Scraping pokemon that appeared in a generation-----------------------------------------------------------------------------------------------

#Making PokedexScraper Class
class PokedexScraper:
    def __init__ (self, url, region, table_index=1):
        self.url = url
        self.region = region
        self.table_index = table_index
        self.dex_names = []

    def fetch_page(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.content

    def parse_pokemon_names(self):
        content = self.fetch_page()
        soup = BeautifulSoup(content, 'html.parser')

        #Finding correct table
        tables = soup.find_all('table', {'class' : 'tab'})
        dex_table = tables[self.table_index]

        #Parsing rows, ignoring first two header rows
        rows = dex_table.find_all('tr')[2:]
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 3:
                pokemon_name = columns[3].text.strip()
                pokemon_name = remove_japanese_text(pokemon_name)
                self.dex_names.append(pokemon_name)

    def update_pokedex(self, pokedata):
        for pokemon in pokedata:
            if pokemon['Name'] in self.dex_names:
                pokemon[f'{self.region}?'] = True

    
#function to remove additional japanese text from pokemon name
def remove_japanese_text(pokemon_name):
    return ''.join(char for char in pokemon_name if char.isascii())
     

#Scraping Kanto - Excluding Let's Go data
kanto_scraper = PokedexScraper('https://www.serebii.net/fireredleafgreen/kantopokedex.shtml', 'Kanto')
kanto_scraper.parse_pokemon_names()
kanto_scraper.update_pokedex(pokedata)


#Scraping Johto (Had to generate manually given different html structure)
johtourl = 'https://www.serebii.net/heartgoldsoulsilver/johtodex.shtml'
johtoresponse = requests.get(johtourl)
johtosoup = BeautifulSoup(johtoresponse.text, 'html.parser')

#Find johtodex table
johtodex = johtosoup.find('table', {'class' : 'dextable'})

#Parsing pokemon names from the table
johtodex_names = []
rows = johtodex.find_all('tr')[1:]
for row in rows:
    columns = row.find_all('td')
    if len(columns) > 1 :
        pokemon_name = columns[2].text.strip()
        johtodex_names.append(pokemon_name)

#Add if pokemon found in johto to pokedata
for pokemon in pokedata:
    if pokemon['Name'] in johtodex_names:
        pokemon['Johto?'] = True

#Scraping Hoenn
hoenn_scraper = PokedexScraper('https://www.serebii.net/rubysapphire/hoennpokedex.shtml', 'Hoenn')
hoenn_scraper.parse_pokemon_names()
hoenn_scraper.update_pokedex(pokedata)


#Scraping Sinnoh
sinnoh_scraper = PokedexScraper('https://serebii.net/platinum/sinnohdex.shtml', 'Sinnoh', 0)
sinnoh_scraper.parse_pokemon_names()
sinnoh_scraper.update_pokedex(pokedata)


#Scraping Unova (B&W
unovabw_scraper = PokedexScraper('https://www.serebii.net/blackwhite/unovadex.shtml', 'Unova (B/W)', 0)
unovabw_scraper.parse_pokemon_names()
unovabw_scraper.update_pokedex(pokedata)


#Scraping Unova (B2&W2
unovab2w2_scraper = PokedexScraper('https://www.serebii.net/black2white2/unovadex.shtml', 'Unova (B2/W2)', 0)
unovab2w2_scraper.parse_pokemon_names()
unovab2w2_scraper.update_pokedex(pokedata)


#Scraping Kalos Central
kalos1_scraper = PokedexScraper('https://www.serebii.net/xy/centralpokedex.shtml', 'Kalos')
kalos1_scraper.parse_pokemon_names()
kalos1_scraper.update_pokedex(pokedata)


#Scraping Kalos Coastal
kalos2_scraper = PokedexScraper('https://www.serebii.net/xy/coastalpokedex.shtml', 'Kalos')
kalos2_scraper.parse_pokemon_names()
kalos2_scraper.update_pokedex(pokedata)


#Scraping Kalos Mountain
kalos3_scraper = PokedexScraper('https://www.serebii.net/xy/mountainpokedex.shtml', 'Kalos')
kalos3_scraper.parse_pokemon_names()
kalos3_scraper.update_pokedex(pokedata)


#Scraping Alola (US/UM
alolaUSUM_scraper = PokedexScraper('https://www.serebii.net/ultrasunultramoon/alolapokedex.shtml', 'Alola (US/UM)')
alolaUSUM_scraper.parse_pokemon_names()
alolaUSUM_scraper.update_pokedex(pokedata)


#Scraping Alola (S/M
alolaSM_scraper = PokedexScraper('https://www.serebii.net/sunmoon/alolapokedex.shtml', 'Alola (S/M)')
alolaSM_scraper.parse_pokemon_names()
alolaSM_scraper.update_pokedex(pokedata)


#Scraping Galar
galar_scraper = PokedexScraper('https://www.serebii.net/swordshield/galarpokedex.shtml', 'Galar')
galar_scraper.parse_pokemon_names()
galar_scraper.update_pokedex(pokedata)


#Scraping Galar (The Crown Tundra
galartct_scraper = PokedexScraper('https://www.serebii.net/swordshield/thecrowntundradex.shtml', 'Galar (TCT)')
galartct_scraper.parse_pokemon_names()
galartct_scraper.update_pokedex(pokedata)


#Scraping Paldea
paldea_scraper = PokedexScraper('https://www.serebii.net/scarletviolet/paldeapokedex.shtml', 'Paldea')
paldea_scraper.parse_pokemon_names()
paldea_scraper.update_pokedex(pokedata)


#-----------------------Setting up dataframe-------------------------------------------------------------------------------------------------------------------

# Convert pokedata to DataFrame draft
draftpokedatadf = pd.DataFrame(pokedata)

#Name Normalization Function for draftpokedatadf
def normalize_draft_name(name):
    name = name.replace('Alolan', 'Alola').replace('Forme', '').replace('Male','M').replace('Female','F')
    name.strip()
    if ' ' in name: 
        parts = name.split()
        if len(parts) == 3:
            return f"{parts[1]}-{parts[0]}-{parts[2]}"
        else:
            return f"{parts[-1]}-{parts[0]}"
    name = name.replace(' ','-')
    return name
    
#Applying normalization to 'Name' column in the draftpokedatadf
draftpokedatadf['Name'] = draftpokedatadf['Name'].apply(normalize_draft_name)

#Additional data extraction from pokemon-data.csv
altpokedata_file_path = r'pokemon-data.csv'
altpokedatadf = pd.read_csv(altpokedata_file_path, encoding = 'utf-8', sep=';')
additional_stats = altpokedatadf[['Name', 'Abilities', 'Tier', 'Next Evolution(s)', 'Moves']]

# Merging the 2 DataFrames based on their shared 'Name' columns
pokedatadf = pd.merge(draftpokedatadf, additional_stats, on='Name', how='left')

# Save to CSV
pokedatadf.to_csv('Pokedex_Data_Project.csv', index=False)
print("Pokedex_Data_Project.csv succesfully saved to device")