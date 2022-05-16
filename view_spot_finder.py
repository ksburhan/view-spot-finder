import json
import sys
import time


def sort_by_key(values):
    return values["value"]


if __name__ == '__main__':
    # set variables and load data
    start = time.time()
    arguments = sys.argv
    mesh_file = arguments[1]
    number_view_spots = int(arguments[2])
    view_spots = []
    view_spots_found = 0
    f = open(mesh_file)
    mesh = json.load(f)
    f.close()
    visited_nodes = []

    # sort height values in descending order
    sorted_values = sorted(mesh["values"], key=sort_by_key, reverse=True)

    # for each height value of target elements check if not already visited (known as not maximum)
    for target_value in sorted_values:
        target_element_id = target_value["element_id"]
        target_nodes = mesh["elements"][target_element_id]["nodes"]
        neighbours = []
        if target_element_id in visited_nodes:
            continue

        # find all neighbours to target element (atleast one vertex shared)
        for element in mesh["elements"]:
            if element["id"] is target_element_id or \
                    not any(n in element["nodes"] for n in target_nodes):
                continue
            else:
                neighbours.append(element["id"])

        # check if any of the neighbours have higher value
        # if yes -> current element is not maximum
        # if no -> current element is maximum
        # every neighbour that has smaller height value cannot be maximum -> is added to the visited nodes
        is_maxima = True
        own_height = target_value["value"]
        for neighbour in neighbours:
            neighbour_height = mesh["values"][neighbour]["value"]
            if own_height < neighbour_height:
                is_maxima = False
                break
            else:
                visited_nodes.append(neighbour)

        # if all neighbours have smaller height value, current element is a maximum and added to the list
        if is_maxima:
            view_spots.append(mesh["values"][target_element_id])
            view_spots_found = view_spots_found + 1
        else:
            visited_nodes.append(target_element_id)

        if view_spots_found == number_view_spots:
            break

    print(json.dumps(view_spots, indent=2, separators=(',', ': ')))
