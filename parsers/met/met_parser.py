import json
import os
import re

import requests

from models import session, Item

regex = r"\(([0-9\.]+)\s×\s([0-9\.]+)\scm\)"


def get_height_width_from_dimensions(dimensions):
    matches = re.findall(regex, dimensions)
    if len(matches) > 0:
        return [float(i) * 10 for i in matches[0]]
    return None
URL_ROOT = 'https://collectionapi.metmuseum.org/public/collection/v1'
OBJECTS_JSON_FILE = 'objects.json'


class METParser:
    def __init__(self):
        self.items_ids = []
        self.new_items = []

    def start(self):
        self.get_index()
        self.dedublicate_items()
        self.download_items()
        self.remove_objects()

    def download_items(self):
        for item_id in self.new_items:
            self.get_item(item_id)

    def dedublicate_items(self):
        self.new_items = self.items_ids

    def remove_objects(self):
        os.remove(OBJECTS_JSON_FILE)

    def get_index(self):
        if os.path.isfile(OBJECTS_JSON_FILE):
            print("File exist")
            with open(OBJECTS_JSON_FILE) as json_file:
                self.items_ids = json.load(json_file)
                return

        response = requests.get(f"{URL_ROOT}/objects")
        objects_response = json.loads(response.content)
        self.items_ids = objects_response['objectIDs']
        print(f'Got {len(self.items_ids)} items')

        with open(OBJECTS_JSON_FILE, 'w') as outfile:
            json.dump(self.items_ids, outfile)

    def get_item(self, item_id: str):
        print(f'Parsing: {item_id} item')
        if not Item.exists_with_source_id(item_id):

            response = requests.get(f"{URL_ROOT}/objects/{item_id}")
            obj = json.loads(response.content)

            item = Item()
            item.item_title = obj['title']
            item.item_type = obj['classification']
            item.item_medium = obj['medium']
            item.item_creator_name = obj['artistDisplayName']
            item.item_creator_artist_codename = obj['artistAlphaSort']
            item.item_created = obj['objectDate']

            if obj['dimensions']:
                dimensions = get_height_width_from_dimensions(obj['dimensions'])
                if dimensions:
                    height, width = dimensions
                    item.height = height
                    item.item_width = width
            if obj['primaryImageSmall']:
                item.item_image_preview_url = obj['primaryImageSmall']

            if obj['primaryImage']:
                item.item_image_large_url = obj['primaryImage']
            item.item_api_source_id = obj['objectID']
            item.item_api_source = 'met'
            item.item_source_url = obj['objectURL']

            session.add(item)
            session.commit()



