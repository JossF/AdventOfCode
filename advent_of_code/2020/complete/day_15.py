ultimate_sighting = {}

penultimate_sighting = {}


def next_number(prev_number):
    if not penultimate_sighting.get(prev_number):
        return 0
    else:
        return ultimate_sighting.get(prev_number) - penultimate_sighting.get(prev_number)


def update_sightings(prev_number, ind):
    if ultimate_sighting.get(prev_number, None) is not None:
        penultimate_sighting[prev_number] = ultimate_sighting[prev_number]
    ultimate_sighting[prev_number] = ind


def evolve_list(start_inputs, final_index):
    ultimate_sighting.update({x: start_inputs.index(x) + 1 for x in start_inputs})
    ind = len(start_inputs)
    last_number = start_inputs[-1]
    n = last_number
    while ind < final_index:
        n = next_number(n)
        ind += 1
        update_sightings(n, ind)
        print(n, ind)
    return n


if __name__ == '__main__':
    print(evolve_list([0, 3, 6], 2020))
    ultimate_sighting = {}
    penultimate_sighting = {}
    # print(evolve_list([1, 3, 2], 30000000))
    ultimate_sighting = {}
    penultimate_sighting = {}
    print(evolve_list([13, 0, 10, 12, 1, 5, 8], 30000000))
