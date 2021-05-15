
from flask import Flask, Response, make_response
from flask_restful import Resource, Api, reqparse
from helpers import get_locations, clean_items, item_matcher, item_sorter
import pandas as pd


app = Flask(__name__)
api = Api(app)


class ListSort(Resource):
    def get(self):
        # Get location data
        locations = get_locations()
        locations["CleanProduct"] = clean_items(locations["Product"])

        return Response(
            locations.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=locations.csv"})


    def post(self):
        # Get shopping list products
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('list', required=True)  # add arguments
        args = parser.parse_args()  # parse arguments to dictionary

        raw_string = args['list']
        original_products = raw_string.splitlines()
        clean_products = clean_items(original_products)
        products = pd.DataFrame({'Product': original_products, 'CleanProduct': clean_products})

        # Get location data
        locations = get_locations()
        locations["CleanProduct"] = clean_items(locations["Product"])

        # Match list items to location reference data
        match_products = item_matcher(products, locations)

        # Sort and return output list
        output_string = item_sorter(match_products)

        resp = make_response(output_string, 200)
        resp.mimetype = "text/plain"

        return resp

    def put(self):
        # Get item to add
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('store', required=True, type=str)  # add arguments
        parser.add_argument('identifier', required=True, type=str)  # add arguments
        parser.add_argument('product', required=True, type=str)  # add arguments
        parser.add_argument('aisle', required=True, type=str)  # add arguments
        parser.add_argument('position', required=True, type=int)  # add arguments
        args = parser.parse_args()  # parse arguments to dictionary

        # All location details
        all_locations = pd.read_csv("./resources/product_locations.csv")

        # New locations to add
        new_location = pd.DataFrame([args])
        new_location.columns = all_locations.columns

        # Full outer join to add or update values
        merge_locations = pd.merge(all_locations, new_location,
                 how='outer',
                 left_on=["Store", "Identifier", "Product"],
                 right_on=["Store", "Identifier", "Product"],
                 suffixes=['_old','_new'])

        # Coalesce columns
        merge_locations["Aisle"] = merge_locations["Aisle_new"].combine_first(merge_locations["Aisle_old"])
        merge_locations["Position"] = merge_locations["Position_new"].combine_first(merge_locations["Position_old"])
        merge_locations.drop(["Aisle_new", "Aisle_old", "Position_new", "Position_old"], axis=1, inplace=True)

        # Reorder
        merge_locations.sort_values(["Store", "Identifier", "Aisle", "Position"], inplace=True)

        # Write back to CSV
        resp = merge_locations.to_csv("./resources/product_locations.csv", index=False)

        return resp



api.add_resource(ListSort, '/listsort')  # '/listsort' is our entry point for Users


if __name__ == '__main__':
    app.run()  # run our Flask app
