# Sort shopping list

import pandas as pd
import numpy as np
import spacy
import os
import re

os.system('python -m spacy download en_core_web_sm')


def get_locations(store='Aldi', identifier='Muller'):
    all_locations = pd.read_csv("./resources/product_locations.csv")
    locations = all_locations[(all_locations["Store"] == store) & (all_locations["Identifier"] == identifier)]
    return locations


def get_products():
    products = [line.rstrip() for line in open('./resources/test_list.txt')]
    return products


def clean_items(items):
    cleaned_items = []
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    for item in items:
        strip_item = re.sub(r"[^a-z]", " ", item.lower())
        doc = nlp(strip_item)
        lemma_item = " ".join([token.lemma_ for token in doc])
        cleaned_items.append(lemma_item)
    return cleaned_items


def item_matcher(items, locations):
    items_df = pd.DataFrame(items, columns=['Product'])
    match_products = items_df.set_index('Product').join(locations.set_index('CleanProduct')[['Aisle', 'Position']])
    return match_products


if __name__ == '__main__':

    # Get location data
    locations = get_locations()
    locations["CleanProduct"] = clean_items(locations["Product"])

    # Get shopping list products
    products = get_products()
    products = clean_items(products)

    match_products = item_matcher(products, locations)

    match_products.sort_values(by=['Aisle', 'Position'])

print(match_products)