# Sort shopping list

import pandas as pd
import numpy as np
import spacy
import os

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
        doc = nlp(item.lower())
        lemma_item = " ".join([token.lemma_ for token in doc])
        cleaned_items.append(lemma_item)
    return cleaned_items


if __name__ == '__main__':
    locations = get_locations()
    products = get_products()

    print(clean_items(products))
    print(clean_items(locations["Product"]))
