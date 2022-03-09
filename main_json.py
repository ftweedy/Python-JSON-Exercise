import sys
import os
import json

class GeoJsonFeatureCollection:
    def __init__(self, input_file):
        self.input_file = input_file
        self.read_data()

    def read_data(self):
        with open(self.input_file, "r") as input:
            data = input.read()
            self.data = json.loads(data)

    def get_feature(self, input_feature_id: str):
        feature = ""
        for x in self.data["features"]:
            if x["properties"]["id"] == input_feature_id:
                feature = x
        return feature

    def get_parent_feature(self, feature):
        parent = feature["properties"]["parent"]
        if parent:
            for x in self.data["features"]:
                if x["properties"]["id"] == parent:
                    return x
                    break

    def get_children_feature(self, feature):
        output = []
        child = feature["properties"]["id"]
        for x in self.data["features"]:
            if x["properties"]["parent"] == child:
                output.append(x)
        return output

    def get_all_shelves(self):
        output = []
        for x in self.data["features"]:
            if x["geometry"]["type"] == "Polygon":
                output.append(x)
        return output

    def get_all_facings(self):
        output = []
        for x in self.data["features"]:
            if x["geometry"]["type"] == "LineString":
                output.append(x)
        return output

    def get_facing_compound_label(self, feature):
        parent = feature["properties"]["parent"]
        output = ""
        if parent:
            for x in self.data["features"]:
                if x["properties"]["id"] == parent:
                    output = x["properties"]["label"]
                    output = output + "_" + feature["properties"]["label"]
                    break
        return output


def main():
    json_collection = GeoJsonFeatureCollection(sys.argv[1])
    print(json_collection.get_facing_compound_label({
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [[0, 10], [10, 10]]
      },
      "properties": {
        "id": "01_N",
        "type": "facing",
        "parent": "01",
        "label": "N"
      }
    }))

    # print(json_collection.get_all_facings())
    # print(json_collection.get_all_shelves())

    # print(json_collection.get_feature("01"))

    # print(json_collection.get_parent_feature({
    #   "type": "Feature",
    #   "geometry": {
    #     "type": "LineString",
    #     "coordinates": [[0, 10], [10, 10]]
    #   },
    #   "properties": {
    #     "id": "01_N",
    #     "type": "facing",
    #     "parent": "01",
    #     "label": "N"
    #   }
    # }))

    # print(json_collection.get_children_feature({
    #   "type": "Feature",
    #   "geometry": {
    #     "type": "Polygon",
    #     "coordinates": [
    #       [[0, 10], [10, 10], [10, 0], [0, 0], [0, 10]]
    #     ]
    #   },
    #   "properties": {
    #     "id": "01",
    #     "angle": 0.0,
    #     "label": "shelf_01",
    #     "type": "shelf",
    #     "parent": None
    #   }
    # }))

if __name__ == "__main__":
    main()