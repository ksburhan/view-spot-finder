import json
import sys


def sort_by_key(values):
    return values["value"]


if __name__ == '__main__':
    arguments = sys.argv

    mesh_file = arguments[1]
    number_view_spots = arguments[2]
    view_spots_found = 0

    f = open(mesh_file)
    mesh = json.load(f)
    f.close()
    sorted_values = sorted(mesh["values"], key=sort_by_key, reverse=True)
    for value in sorted_values:
        element_id = value["element_id"]
        nodes = mesh["elements"][element_id]["nodes"]
        neighbours = []
        for element in mesh["elements"]:
            if element["id"] is element_id or not any(n in element["nodes"] for n in nodes):
                continue
            else:
                neighbours.append(element["id"])

