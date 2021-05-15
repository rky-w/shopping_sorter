# Sort shopping list

import pandas as pd

from helpers import get_locations, get_products, clean_items, item_matcher, item_sorter

# os.system('python -m spacy download en_core_web_sm')

# Get location data
locations = get_locations()
locations["CleanProduct"] = clean_items(locations["Product"])

# Get shopping list products
original_products = get_products()
clean_products = clean_items(original_products)
products = pd.DataFrame({'Product': original_products, 'CleanProduct': clean_products})

# Match list items to location reference data
match_products = item_matcher(products, locations)

# Sort and return output list
output_string = item_sorter(match_products)

print(output_string)