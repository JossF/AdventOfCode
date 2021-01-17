import pandas

opposites = dict(l='r', r='l', t='b', b='t')


def get_top(df):
    return df.iloc[0, :].tolist()


def get_left(df):
    return list(reversed(df.iloc[:, 0].tolist()))


def get_bottom(df):
    full_size = df.shape[0] - 1
    return list(reversed(df.iloc[full_size, :].tolist()))


def get_right(df):
    full_size = df.shape[0] - 1
    return df.iloc[:, full_size].tolist()


def flip_lr(df):
    return df.reindex(columns=list(reversed(df.columns)))


def flip_tb(df):
    return df.reindex(index=list(reversed(df.index.tolist())))


def rotate_r(df):
    return flip_lr(df.transpose())


def rotate_flip(top_orient, orient, df):
    """
    Assuming we are attaching to "b"

    :param top_orient: the side attached to bottom of last tile
    :param orient: whether the edges is reversed or not
    :param df: tile
    :return: tile, correctly orientated
    """
    if top_orient == 't':
        if orient == -1:
            return df
        return flip_lr(df)
    if top_orient == 'l':
        if orient == -1:
            return rotate_r(df)
        return flip_lr(rotate_r(df))
    if top_orient == 'b':
        if orient == -1:
            return rotate_r(rotate_r(df))
        return flip_tb(df)
    if top_orient == 'r':
        if orient == -1:
            return rotate_r(rotate_r(rotate_r(df)))
        return flip_lr(rotate_r(rotate_r(rotate_r(df))))


def test_utils():
    test_df = pandas.DataFrame({'A': [1, 2], 'B': [3, 4]})
    assert get_right(test_df) == [3, 4]
    assert get_left(test_df) == [2, 1]
    assert get_top(test_df) == [1, 3]
    assert get_bottom(test_df) == [4, 2]
    assert pandas.DataFrame({'B': [3, 4], 'A': [1, 2]}).equals(flip_lr(test_df))
    assert pandas.DataFrame({'A': [2, 1], 'B': [4, 3]}).reset_index(drop=True).equals(
        flip_tb(test_df).reset_index(drop=True))
    print(test_df)
    for spin in opposites.keys():
        for rev in [1, -1]:
            print(f"Matching side: {spin}, mirror: {rev} : {rotate_flip(spin, rev, test_df)}")


def load_inputs(location):
    raw = pandas.read_csv(location, header=None)
    tile_dict = {}
    for tile_line in raw[0].tolist():
        id, vals = tile_line.split(":;")
        split_vals = [[j for j in v] for v in vals.split(";")]
        tile_dict[id] = pandas.DataFrame(split_vals)
    return tile_dict


def edge_list(starting_tile_id, starting_orient, match_dict, orient_dict, tile_dict):
    """
    Starting orient = 'b' Only works for 'b' at the moment

    :param starting_tile_id:
    :param starting_orient:
    :param match_dict:
    :param orient_dict:
    :param tile_dict:
    :return:
    """
    if starting_orient != 'b':
        raise (NotImplemented("Do work for starting orient not b"))
    current_tile_id = starting_tile_id
    next_tile_id, matching_loc = match_dict.get((starting_tile_id, starting_orient), False)
    orient = 1
    tile_list = [current_tile_id]
    oriented_tiles = [tile_dict.get(starting_tile_id)]
    print(f"{1}: {starting_orient} & {orient}")
    while next_tile_id:
        tile_orient = orient_dict.get((current_tile_id, next_tile_id), orient_dict.get((next_tile_id, current_tile_id)))
        tile = tile_dict.get(next_tile_id)
        flipped_tile = rotate_flip(matching_loc, tile_orient*orient, tile)
        tile_list.append(next_tile_id)
        oriented_tiles.append(flipped_tile)
        assert oriented_tiles[-2].iloc[9, :].tolist() == oriented_tiles[-1].iloc[0, :].tolist()
        print(f"{len(oriented_tiles)}: {matching_loc} & {orient} ({tile_orient})")
        # next tile
        orient = orient*tile_orient*-1
        matching_loc = opposites[matching_loc]
        current_tile_id = next_tile_id
        next_tile_id, matching_loc = match_dict.get((current_tile_id, matching_loc), (False, False))
    return tile_list, oriented_tiles


def find_corners(tile_dictionary):
    tile_edge_locations = {}
    edge_owners = {}
    unmmatched_edges = []
    tile_match_pairs = {}
    match_orientations = {}
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
                match_orientations[(t_id, matching_id)] = 1 if matching_edge == tuple(edge) else -1
            else:
                edge_owners[tuple(edge)] = t_id
        unmmatched_edges.extend(new_edges)
    final_counts = {}
    inverse_matches = dict(zip(tile_match_pairs.values(), tile_match_pairs.keys()))
    full_matches = dict(inverse_matches)
    full_matches.update(tile_match_pairs)
    for t_id, t_tile in tile_dictionary.items():
        final_counts[t_id] = sum([1 for loc in ['t', 'r', 'b', 'l'] if
                                  (t_id, loc) in list(full_matches.keys())])

    corners = [t_id_f for t_id_f, c in final_counts.items() if c == 2]
    tl_corner = corners[0]
    tl_matched = [k[1] for k in full_matches.keys() if k[0] == tl_corner]
    for edge_along in sorted(tl_matched):
        edge_list(tl_corner, edge_along, full_matches, orient_dict=match_orientations, tile_dict=tile_dictionary)
    print(corners)


if __name__ == '__main__':
    test_utils()
    tile_d = load_inputs(r'C:\Users\Joss\PycharmProjects\pythonProject\advent_of_code\2020\day_20_input.csv')
    find_corners(tile_d)
