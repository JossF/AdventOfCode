import pandas


def get_top(df):
    return df.loc[0, :].tolist()


def get_left(df):
    return df.loc[:, 0].tolist()


def get_bottom(df):
    full_size = df.shape[0] - 1
    return df.loc[full_size, :].tolist()


def get_right(df):
    full_size = df.shape[0] - 1
    return df.loc[:, full_size].tolist()


def load_inputs(location):
    raw = pandas.read_csv(location, header=None)
    tile_dict = {}
    for tile_line in raw[0].tolist():
        id, vals = tile_line.split(":;")
        split_vals = [[j for j in v] for v in vals.split(";")]
        tile_dict[id] = pandas.DataFrame(split_vals)
    return tile_dict


def find_corners(tile_dictionary):
    tile_edge_locations = {}
    edge_owners = {}
    unmmatched_edges = []
    tile_match_pairs = {}
    for t_id, tile in tile_dictionary.items():
        assert (tile.shape[0] == tile.shape[1])
        new_edges = []
        edges = [get_top(tile), get_right(tile), get_bottom(tile), get_left(tile)]
        loc_dict = dict(zip([tuple(e) for e in edges], ['t', 'r', 'b', 'l']))
        tile_edge_locations[t_id] = loc_dict
        for edge in edges:
            rev_edge = list(reversed(edge))
            matching_id = False
            matching_edge = ()
            for e in [edge, rev_edge]:
                matching_id = edge_owners.get(tuple(e), matching_id)
                matching_edge = tuple(e) if edge_owners.get(tuple(e), False) else matching_edge
            if matching_id:
                resp_loc = tile_edge_locations[matching_id][matching_edge]
                tile_match_pairs[(t_id, loc_dict[tuple(edge)])] = (matching_id, resp_loc)
            else:
                edge_owners[tuple(edge)] = t_id
        unmmatched_edges.extend(new_edges)
    final_counts = {}
    for t_id, t_tile in tile_dictionary.items():
        final_counts[t_id] = sum([1 for loc in ['t', 'r', 'b', 'l'] if
                                  (t_id, loc) in list(tile_match_pairs.keys()) + list(tile_match_pairs.values())])
    print([t_id_f for t_id_f, c in final_counts.items() if c == 2])


if __name__ == '__main__':
    tile_d = load_inputs(r'C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_20_input.csv')
    find_corners(tile_d)
