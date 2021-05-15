
# Helper functions for shopping sorter
import pandas as pd
import spacy
import re


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
    match_products = items.set_index('CleanProduct').join(locations.set_index('CleanProduct')[['Aisle', 'Position']])
    match_products.fillna({'Aisle': 'Unknown', 'Position': 0}, inplace=True)
    return match_products


def item_sorter(match_products):
    sort_products = match_products.sort_values(by=['Aisle', 'Position'])

    outlist = []
    for aisle in sort_products['Aisle'].unique():
        outlist.append('---- Aisle: {} ----'.format(aisle))
        for product in sort_products.loc[sort_products['Aisle'] == aisle]['Product']:
            outlist.append(product)

    stringout = '\n'.join(outlist)
    return stringout



if __name__ == '__main__':

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