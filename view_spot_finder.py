import json
import sys
import time


def sort_by_key(values):
    return values["value"]


if __name__ == '__main__':
    start = time.time()
    arguments = sys.argv

    mesh_file = arguments[1]
    number_view_spots = int(arguments[2])
    view_spots = []
    view_spots_found = 0

    f = open(mesh_file)
    mesh = json.load(f)
    f.close()
    sorted_values = sorted(mesh["values"], key=sort_by_key, reverse=True)
    elements_with_neighbours = []
    for value in sorted_values:
        if view_spots_found == number_view_spots:
            break
        element_id = value["element_id"]
        nodes = mesh["elements"][element_id]["nodes"]
        neighbours = []
        for element in mesh["elements"]:
            if element["id"] is element_id or not any(n in element["nodes"] for n in nodes):
                continue
            else:
                neighbours.append(element["id"])
        is_maxima = True
        own_height = value["value"]
        for neighbour in neighbours:
            neighbour_height = mesh["values"][neighbour]["value"]
            if own_height < neighbour_height:
                is_maxima = False
                break
        if not is_maxima:
            continue
        else:
            view_spots.append(mesh["values"][element_id])
            view_spots_found = view_spots_found + 1
        elements_with_neighbours.append((element_id, neighbours))

    print(view_spots)
    end = time.time()
    print(end - start)
