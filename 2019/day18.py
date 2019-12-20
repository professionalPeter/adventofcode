"""Solutions for Day 18 of Advent of Code 2019

https://adventofcode.com/2019/day/18
"""
from itertools import permutations
from string import ascii_lowercase
from copy import deepcopy
import logging

logging.basicConfig(level=logging.WARN)

def part1(inputs = None):
    """Output the answer to part 1 - """
    print(f'Part 1 answer: {None}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    print(f'Part 2 answer: {None}')

def puzzle_input():
    """Returns the official input for the puzzle"""
    with open('day18input.txt') as file:
        return file.read()

def test_input0():
    """Returns the test data set from the description of part 1"""
    return """
#########
#b.A.@.a#
#########"""[1:]

def test_input1():
    """Returns the test data set from the description of part 2"""
    return """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""[1:]

def test_input2():
    """Returns the test data set from the description of part 2"""
    return """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""[1:]

def test_input3():
    return """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""[1:]

def test_input4():
    return """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""[1:]

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = '#'
OPEN = '.'
START = '@'
KEYS = set(ascii_lowercase)
DELTAS = {NORTH: (0,1), SOUTH: (0,-1), WEST: (-1,0), EAST: (1,0)}
OPPOSITE_DIRECTION = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}

def grid_element_at(grid, x, y):
    try:
        return grid[y][x]
    except IndexError:
        return None

def can_enter_location(grid_status, goal, state):
    return grid_status == OPEN or grid_status in state['owned_keys'] or grid_status in state['unlocked_doors'] or grid_status == goal or grid_status == START

depth = 0

def find_paths(x, y, grid, goal, state = None, path = None):
    global depth
    depth += 1
    path = path or {}
    successful_paths = []

    path_status = path.get((x, y))
    grid_status = grid_element_at(grid, x, y)
    logging.debug(f'{" " * depth}{(x, y)}: grid_status: {grid_status} path_status: {path_status}')

    # Base of the recursion - if we couldn't take the step (either because we hit a wall or already traversed the location),
    # then record the successful path and start unwinding
    if not can_enter_location(grid_status, goal, state) or path_status:
        depth -= 1
        return successful_paths

    # record that we've already traversed this location
    # store the grid_status, because why not <shrug>? We just need something other than None to exist there
    path[x,y] = grid_status

    # Base of the recursion - if we found the goal, then record the successful path and start unwinding
    if grid_status == goal:
        successful_paths = [path.copy()]
    else:
        # find the set of successful paths in each direction
        for next_direction in [NORTH, EAST, SOUTH, WEST]:
            new_x = x + DELTAS[next_direction][0]
            new_y = y + DELTAS[next_direction][1]
            successful_paths += find_paths(new_x,new_y, grid, goal, state, path)

    # unmark that we've traversed this location, so that the callers are free to traverse it again if desired
    # del rather than set it to False so that if the same location was somehow inserted later, it would be properly ordered
    del path[x,y]
    depth -= 1
    return successful_paths

find_key_call_count = 0
def find_key(key, starting_point, grid, state):
    logging.debug(f'Finding key: {key}')
    global find_key_call_count
    find_key_call_count += 1

    paths = find_paths(starting_point[0], starting_point[1], grid, key, state)
    if not paths:
        return None, state
    best_path = min(paths, key=len)
    logging.debug(f'Found key: {key} - {best_path}')
    return best_path, state

def find_path_sequence(keys, starting_point, grid, state, owned=[]):
    # Base case - only one key to find
    if len(keys) == 1:
        for key in keys:
            logging.info(f'T: {owned + [key]}')
            new_state = deepcopy(state)
            key_path, new_state = find_key(key, starting_point, grid, new_state)
            return [list(key_path.keys())]

    successful_paths = []
    for next_key in keys:
        owned.append(next_key)
        try:
            logging.info(f'T: {owned}')
            new_state = deepcopy(state)
            key_path, new_state = find_key(next_key, starting_point, grid, new_state)
            if not key_path:
                continue
            #TODO: Does this incorrectly persist state for callers without the deepcopy above.
            # Think about successive iterations of the loop
            new_state['unlocked_doors'].add(next_key.upper())
            new_state['owned_keys'].add(next_key)
            key_path = list(key_path.keys())
            rest_starting_point = key_path.pop()
            rest_keys = keys - set([next_key])
            rest_paths = find_path_sequence(rest_keys, rest_starting_point, grid, new_state, owned)
            if not rest_paths:
                continue
            successful_paths += [key_path + path for path in rest_paths]
        finally:
            owned.pop()
    return successful_paths

if __name__ == '__main__':
    part1()
    part2()

    data = test_input2()
    grid = data.splitlines()
    keys = [k for row in grid for k in row if k in ascii_lowercase]
    home_point = [(x,y) for y, row in enumerate(grid) for x, element in enumerate(row) if element == START][0]
    print('Starting at', home_point)


    results = find_path_sequence(set(keys), home_point, grid, {'owned_keys': set(), 'unlocked_doors': set()})
    lens = [len(l)-1 for l in results]
    print(lens, min(lens))

    """
    # create the list of possible paths by determining the possible key order combinations
    print(f'Generating candidate paths for {keys}')
    candidate_paths = list(permutations(keys))
    print(f'Searching {len(candidate_paths)} candidate paths')

    successful_paths = []
    for index, candidate_path in enumerate(candidate_paths):
        description = "".join(candidate_path)
        full_path = []
        state = {'unlocked_doors': set()}
        starting_point = home_point
        logging.debug(f'Searching keys in path: {description}')
        for key in candidate_path:
            key_path, state = find_key(key, starting_point, grid, state)
            if not key_path:
                logging.debug(f'Failed to find key: {key}')
                break
            full_path += key_path.keys() 
            state['unlocked_doors'].add(key.upper())
            # drop the first element, because the starting point of this path matches the 
            # end point of the last path
            starting_point = full_path.pop()
        else:
            successful_paths.append(full_path)
            logging.info(f'Found full path {description} - length: {len(full_path)}')
        if index % 10000 == 0: print(f'Searched {index} paths')
    print(len(successful_paths))
    if successful_paths:
        print('Best path:', len(min(successful_paths, key = len)))
    else:
        print('No path found :(')
        """

"""
Optimization: select the direction in the direction of the key first and the direction away from the key last
TODO: Handle case where we found a key we weren't looking for
Do we even need to get grid_status in find_paths? We could just pass x,y to all the functions
Where should the knowledge of the 'unlocked_doors' really live? Creation?
make depth a part of find_paths instead of a global (use try finally)
Does state need to be returned from everything?
THe name keys is confusing when it occurs alongside dict.keys()
Make find_key no longer return state
Can I somehow enforce that find_key, find_path, etc don't modify the state?
x - Fail the path if you hit a key that you don't own. This will cut down the search space, since that path is necessarily covered in another permutation
Get rid of the deep copy?
Preprocess keys to find inaccessible keys without pathfinding
"""
