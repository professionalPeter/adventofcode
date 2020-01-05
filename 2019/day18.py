"""Solutions for Day 18 of Advent of Code 2019

https://adventofcode.com/2019/day/18
"""
from itertools import combinations, permutations
from string import ascii_lowercase, ascii_uppercase
from copy import deepcopy
import logging
import unittest
from pprint import pprint

#logging.basicConfig(level=logging.INFO)

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
#########""".lstrip()

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
DOORS = set(ascii_uppercase)
DELTAS = {NORTH: (0,1), SOUTH: (0,-1), WEST: (-1,0), EAST: (1,0)}
OPPOSITE_DIRECTION = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}

class Maze:
    def __init__(self, ascii_maze):
        self.maze = ascii_maze.lstrip().splitlines()
        self.points_of_interest = {item:(x,y) for y, row in enumerate(self.maze) for x, item in enumerate(row) if item == START or item in KEYS}

    def location_of(self, item):
        return self.points_of_interest.get(item)

    def item_at(self, location):
        try:
            return self.maze[location[1]][location[0]]
        except IndexError:
            return None

    @property
    def keys(self):
        return set(self.points_of_interest) & KEYS

class Path:
    def __init__(self, path):
        self.path = path

    def __len__(self):
        return len(self.path)

    @property
    def doorsPassed(self):
        return [door for door in self.path.values() if door in DOORS]

    @property
    def keysPassed(self):
        return [key for key in self.path.values() if key in KEYS]

depth = 0

def find_paths(x, y, maze, goal, path = None):
    global depth
    depth += 1
    path = path or {}
    successful_paths = []

    path_status = path.get((x, y))
    grid_status = maze.item_at((x, y))
    logging.debug(f'{" " * depth}{(x, y)}: grid_status: {grid_status} path_status: {path_status}')

    # Base of the recursion - if we couldn't take the step (either because we hit a wall or already traversed the location),
    # then record the successful path and start unwinding
    if grid_status == WALL or path_status:
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
            successful_paths += find_paths(new_x,new_y, maze, goal, path)

    # unmark that we've traversed this location, so that the callers are free to traverse it again if desired
    # del rather than set it to False so that if the same location was somehow inserted later, it would be properly ordered
    del path[x,y]
    depth -= 1
    return successful_paths

find_key_call_count = 0
def find_best_path_between(item0, item1, maze):
    logging.debug(f'Finding "{item1}"')
    global find_key_call_count
    find_key_call_count += 1

    starting_point = maze.location_of(item0)
    paths = find_paths(starting_point[0], starting_point[1], maze, item1)
    if not paths:
        return None
    best_path = min(paths, key=len)
    del best_path[starting_point] # drop the starting point, because we want the path to just include the subsequent steps
    path_object = Path(best_path)
    logging.debug(f'Found "{item1}" - {path_object.path} - requires: {path_object.doorsPassed}')

    return path_object

class TestDay18(unittest.TestCase):

    def test_find_key_returns_minimal_path_len(self):
        maze = Maze("""
#########
#.......#
#@.....a#
#.......#
#########""")
        path = find_best_path_between(START, 'a', maze)
        self.assertEqual(len(path), 6)

    def test_find_key_returns_path_through_key(self):
        maze = Maze("""
#########
#@..b..a#
#########""")
        path = find_best_path_between(START, 'a', maze)
        self.assertEqual(len(path), 6)

    def test_find_key_returns_path_through_door(self):
        maze = Maze("""
#########
#@..A..a#
#########""")
        path = find_best_path_between(START, 'a', maze)
        self.assertEqual(len(path), 6)

    def test_find_key_returns_doors_encountered(self):
        maze = Maze("""
#########
#@..A..a#
#########""")
        path = find_best_path_between(START, 'a', maze)
        self.assertEqual(path.doorsPassed, ['A'])

    def test_find_key_returns_other_keys_encountered(self):
        maze = Maze("""
#########
#@..b..a#
#########""")
        path = find_best_path_between(START, 'a', maze)
        self.assertCountEqual(path.keysPassed, ['a', 'b'])
    """
    def test_cost_for_set_with_size(self):
        maze = Maze(
#########
#...b...#
#@.....a#
#....c..#
#########)
        costs = cost_for_set_with_size(1, 'abc', maze)
        self.assertEqual(costs, {make_cache_key('a'): 6, 
                                 make_cache_key('b'): 4,
                                 make_cache_key('c'): 5})
    """

    def test_calc_incremental_costs_adds_next_set_of_keys(self):
        initial_costs_map = {('1', frozenset()):0}

        edge_costs = {frozenset('21'):1,
                      frozenset('31'):15,
                      frozenset('41'):6,
                      frozenset('32'):7,
                      frozenset('42'):3,
                      frozenset('34'):8}
        maze_keys = '234'

        # The resulting dict should contain a key for each maze_key in a tuple with an empty set
        # and the value should be the edge cost from 1 to the maze_key
        result = calc_incremental_costs(maze_keys, initial_costs_map, edge_costs)
        self.assertDictEqual(result, {('2', frozenset('1')):1,
                                      ('3', frozenset('1')):15,
                                      ('4', frozenset('1')):6})

        result = calc_incremental_costs(maze_keys, result, edge_costs)

        # The resulting dict should contain a key for each item from the current_costs_map 
        # combined with each element from maze_keys, with the value set to 
        # value from the current_costs_map plus the value from edge costs from the last key to the next key
        self.assertDictEqual(result, {('3', frozenset('12')):8,
                                      ('4', frozenset('12')):4,
                                      ('2', frozenset('13')):22,
                                      ('4', frozenset('13')):23,
                                      ('2', frozenset('14')):9,
                                      ('3', frozenset('14')):14})

        # The resulting dict should contain a key for each unique set created when combining 
        # the elements of a key from 'result' into a single set (e.g. ('3', frozenset('2')) produces the set('2', '3')
        # then put into a tuple with each item from maze_keys not in the resulting set
        # (e.g. ('4', frozenset('2', '3')))
        # The value for each key should be the minimum value resulting from adding each value from 'result'
        # to the value from edge_costs from the last key to the next key
        result = calc_incremental_costs(maze_keys, result, edge_costs)
        self.assertDictEqual(result, {('4', frozenset('123')):16,
                                      ('3', frozenset('124')):12,
                                      ('2', frozenset('134')):21})


    def test_calc_incremental_costs_excludes_paths_with_locked_doors(self):
        edge_costs = {frozenset('21'):1,
                      frozenset('31'):15,
                      frozenset('41'):6,
                      frozenset('32'):7,
                      frozenset('42'):3,
                      frozenset('34'):8}
        doorsPassed = START

        maze_keys = '234'

        # The resulting dict should contain a key for each maze_key in a tuple with an empty set
        # and the value should be the edge cost from 1 to the maze_key
        result = calc_incremental_costs(maze_keys, initial_costs_map, edge_costs)
        self.assertDictEqual(result, {('2', frozenset('1')):1,
                                      ('3', frozenset('1')):15,
                                      ('4', frozenset('1')):6})

        



def make_cache_key(keys):
    return (frozenset(keys), keys[-1])

cache = {}
def cost_for_set_with_size(size, keys, maze, edge_costs):
    keys = set(keys)
    last_sets = [set(c) for c in combinations(keys, size)]
    for last_set in last_sets:
        next_keys = keys - last_set
        for next_key in next_keys:
            for last_key in last_set:
                last_set_minus_last_key = last_set - set(last_key)
                print(f'g({next_key}, {last_set}) = c({next_key}, {last_key}) + g({last_key}, {last_set_minus_last_key})')
                #cache[next_key, frozenset(last_set)] = adjacency_matrix[last_key, next_key] + cache[last_key, frozenset(last_set_minus_last_key)]
                #find_best_path_between(last_key, next_key, maze)

    return {(frozenset(key), key):len(find_best_path_between(START, key, maze)) for key in keys}

def calc_initial_costs(maze):
    costs = {}
    for key in maze.keys:
        path = find_best_path_between(START, key, maze)
        if path.doorsPassed or (set(path.keysPassed) - set(key)):
            continue
        costs[key, frozenset()] = len(path)
    return costs

def make_adjacency_matrix(maze):
    return {frozenset(pair):find_best_path_between(pair[0], pair[1], maze) for pair in permutations(maze.keys, 2)}

def calc_incremental_costs(all_keys, current_costs_map, edge_costs):
    all_keys = frozenset(all_keys)
    new_costs = {}
    for keys, cost_of_current_keys in current_costs_map.items():
        last_key, rest = keys
        current_keys = frozenset(set(last_key) | rest)
        next_keys = all_keys - current_keys
        for next_key in next_keys:
            #if the new edge does not require keys we don't have
            cost_to_next_maze_key = edge_costs[frozenset([last_key, next_key])] + cost_of_current_keys
            costs_dict_key = (next_key, frozenset(current_keys))
            existing_cost = new_costs.get(costs_dict_key)
            new_costs[costs_dict_key] = cost_to_next_maze_key if existing_cost is None else min(existing_cost, cost_to_next_maze_key)
    return new_costs

if __name__ == '__main__':
    part1()
    part2()

    """
    import time
    maze = Maze(test_input3())
    print('Building adjacency matrix')
    edge_costs = make_adjacency_matrix(maze)
    pprint({k:len(v) for k,v in edge_costs.items()})
    print('Calculating cost to initial keys')
    x = calc_initial_costs(maze)
    pprint(x)
    print('Calculating incrementatal costs')
    x = calc_incremental_costs(maze.keys, x, edge_costs)
    pprint(x)
    print('done')
    """ 
    unittest.main()

    
"""
    data = test_input2()
    grid = data.splitlines()
    keys = [k for row in grid for k in row if k in ascii_lowercase]
    home_point = [(x,y) for y, row in enumerate(grid) for x, element in enumerate(row) if element == START][0]
    print('Starting at', home_point)

    find_adjacency_costs(grid)
    results = find_path_sequence(set(keys), home_point, grid, {'owned_keys': set(), 'unlocked_doors': set()})
    lens = [len(l)-1 for l in results]
    print(f'Path Lens: {lens}', f'Min path len: {min(lens)}', f'find_key_calls: {find_key_call_count}', sep='\n')
    """
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
make owned an ordered set instead of a string
optimization? first find the legal key paths by faking ownership of the keys? find the minimal set of keys needed?
optimization? Can i make it faster by not finding shortest paths initially, but only the required order?
Should be able to get rid of the need for the calc_initial_costs by seeding the current_cost_map with g(START, set())
"""
