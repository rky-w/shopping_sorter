
from flask import Flask, Response, make_response
from flask_restful import Resource, Api, reqparse
from helpers import get_locations, get_products, clean_items, item_matcher, item_sorter
import pandas as pd
from io import StringIO
import csv
import json


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
            headers={"Content-disposition":
                         "attachment; filename=locations.csv"})


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


api.add_resource(ListSort, '/listsort')  # '/users' is our entry point for Users


if __name__ == '__main__':
    app.run()  # run our Flask app
