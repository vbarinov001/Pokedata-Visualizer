# Pokedata Visualizer Project

## 📚 About Data

Web scraped pokemon data from Pokemondb.net and Serebii.net that includes Pokemon Name, Stats, Type, Generation, Region, and Mythical/Legendary status. Aqcuired additional Pokemon data for Abilities, Tier, Next Evo(s), and Moves from the pokemon-data and moves-data datasets on Kaggle by Nicholas Vadivelu (https://www.kaggle.com/n2cholas/datasets). 

## 💡 Highlights

- Generation stat creep most noticable amongst fighting type pokemon
- Generation 3 (including alternate forms) contributed the weakest pokemon given the average stat / amount added ratio. Generation 5 (including alternate forms) is a close runner up
- Generation 6 (including alternate forms) contributed the strongest pokemon given the average stat / amount added ratio
- NU competitve tier pokemon had the most noticable stat creep

## ✏️ Data Wrangling

Conducted web scraping using the BeautifulSoup Python library
Created pokedata data table using Pandas library
Conducted simple data wrangling and data cleaning:
- Removed rows with missing values
- Created function to remove additional japanese characters from scraped pokemon names
- Created normalization function to scraped pokemon names to make them compatible with the pokemon-data kaggle dataset
- Unpivoted pokemon stats data to make usable in Power BI dashboard

## 📊 Visualization

Produced a 2-pager dashboard using Power BI.

[View the PDF](Pokedex_Data_Project.pdf)

(Dashboard available to download in respective repository)
