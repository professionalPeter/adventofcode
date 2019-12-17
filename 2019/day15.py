"""Solutions for Day 15 of Advent of Code 2019

https://adventofcode.com/2019/day/15
"""
from intcode import IntCodeProcessor, ExecutionError, ExecutionCode

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
OPEN = 1
SUCCESS = 2

DELTAS = {NORTH: (0,1), SOUTH: (0,-1), WEST: (-1,0), EAST: (1,0)}
OPPOSITE_DIRECTION = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}

def part1(inputs = None):
    """Output the answer to part 1 - Minimum number of movement commands to move to the oxygen system"""
    cpu = IntCodeProcessor(path='day15input.txt')
    path = {(0, 0): True}
    grid = {(0, 0): OPEN}

    successful_paths = find_paths(0,0,None, grid, path, cpu)

    # remove the "unmarked" locations from the paths
    marked_paths = [[loc for loc, marked in path.items() if marked] for path in successful_paths] 
    shortest_path = min(marked_paths, key=len)

    # subtract 1 because we want the number of movement commands, so we need to
    # subtract out the initial location
    num_movement_commands = len(shortest_path) - 1
    print(f'Part 1 answer: {num_movement_commands}')

def part2(inputs = None):
    """Output the answer to part 2 - """
    cpu = IntCodeProcessor(path='day15input.txt')
    path = {(0, 0): True}
    grid = {(0, 0): OPEN}
    find_paths(0, 0, None, grid, path, cpu)

    newly_filled_locs = [loc for loc, status in grid.items() if status == SUCCESS]

    steps = -1 # start at -1, because we go through the loop 1 extra time to determine that there are no more spaces to fill
    while len(newly_filled_locs) > 0:
        newly_filled_locs = fill_adjacent(newly_filled_locs, grid)
        steps += 1
    print(f'Part 2 answer: {steps}')



def find_paths(x, y, direction, grid, path, robot):
    ran_robot = False # track if we ran the robot so we can backtrack
    try:
        successful_paths = []

        # Test taking a step in the specified direction
        if direction is None:
            new_x = x
            new_y = y
        else:
            new_x = x + DELTAS[direction][0]
            new_y = y + DELTAS[direction][1]

            path_status = path.get((new_x, new_y))
            grid_status = grid.get((new_x, new_y))

            # if we don't know what's at the location, run the robot to find out
            if grid_status is None:
                grid_status = run_robot(robot, direction)
                ran_robot = True
                grid[new_x,new_y] = grid_status

            # Base of the recursion - if we found the goal, then record the successful path and start unwinding
            if grid_status == SUCCESS:
                successful_paths = [path.copy()]
                successful_paths[0][new_x, new_y] = True
                print(f'SUCCESS: {(new_x, new_y)}')
                return successful_paths
            
            # Base of the recursion - if we couldn't take the step (either because we hit a wall or already traversed the location),
            # then record the successful path and start unwinding
            if grid_status == WALL or path_status:
                # we shouldn't need to worry about backtracking here in path_status == true case
                # because if path_status == True, then we shouldn't have needed to run the robot
                return successful_paths

        # record that we've already traversed this location
        path[new_x,new_y] = True

        # find the set of successful paths in each direction
        for next_direction in [NORTH, EAST, SOUTH, WEST]:
            successful_paths += find_paths(new_x,new_y, next_direction, grid, path, robot)

        # unmark that we've traversed this location, so that the callers are free to traverse it again if desired
        path[new_x,new_y] = False
        return successful_paths
    finally:
        # if the robot ran and actually changed the location, then we need to backtrack, so that
        # we return to the location the robot was in when this function was entered
        if ran_robot and (grid_status == OPEN or grid_status == SUCCESS):
            backtrack_result = run_robot(robot, OPPOSITE_DIRECTION[direction])
            assert(backtrack_result == OPEN)
    
def run_robot(robot, direction):
    try:
        robot.execute_program(direction, reset=False)
    except ExecutionError as err:
        assert err.reason == ExecutionCode.NEED_INPUT
    status = robot.outputs.pop()
    assert len(robot.outputs) == 0
    return status

def locations_adjacent_to(loc):
    return [(loc[0] + DELTAS[direction][0], loc[1] + DELTAS[direction][1]) for direction in [NORTH,SOUTH,WEST,EAST]]

def fill_adjacent(locations, grid):
    newly_filled = []
    for loc in locations:
        for adjacent in locations_adjacent_to(loc):
            if grid.get(adjacent) == OPEN:
                grid[adjacent] = SUCCESS
                newly_filled += [adjacent]
    return newly_filled

if __name__ == '__main__':
    part1()
    part2()


"""
Make directions an enum?
"""
