from itertools import product

def manhattan_distance(point):
    return sum([abs(x) for x in point])

def convert_to_vector(vector_description):
    direction = vector_description[0]
    magnitude = int(vector_description[1:])

    if direction == 'R':
        return [magnitude, 0]
    elif direction == 'L':
        return [-magnitude, 0]
    elif direction == 'U':
        return [0, magnitude]
    elif direction == 'D':
        return [0, -magnitude]
    else:
        raise ValueError(f'Invalid direction: {direction}')

def sum_vectors(vectors):
    return [sum(t) for t in zip(cursor,vector)]

def intersection_point_of(segment0, segment1):
    left = max(min(segment0[0][0], segment0[1][0]), min(segment1[0][0], segment1[1][0]))
    right = min(max(segment0[0][0], segment0[1][0]), max(segment1[0][0], segment1[1][0]))
    bottom = max(min(segment0[0][1], segment0[1][1]), min(segment1[0][1], segment1[1][1]))
    top = min(max(segment0[0][1], segment0[1][1]), max(segment1[0][1], segment1[1][1]))

    if left != right or top != bottom:
        return None

    return [left, top]

#test_data = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
#paths = [path.split(',') for path in test_data.splitlines()]

with open('day3input.txt') as file:
    paths = [path.split(',') for path in file.read().splitlines()]

# Map vectors to line segments
for index, path in enumerate(paths):
    cursor = [0,0]
    segments = []
    for vector_description in path:
        vector = convert_to_vector(vector_description)
        new_segment = [cursor]
        cursor = sum_vectors([cursor, vector])
        new_segment.append(cursor)
        segments.append(new_segment)
    paths[index] = segments
        
# Find intersecting line segments
intersections = []
for segment0, segment1 in product(paths[0], paths[1]):
    intersection = intersection_point_of(segment0, segment1)
    if intersection is not None and intersection != [0,0]:
        intersections.append(intersection)

# Find closest intersection
print('Part 1 answer: ', min([abs(point[0]) + abs(point[1]) for point in intersections]))
def distance_on_path_to_point(path, point):
    distance = 0
    for segment in path:
        if intersection_point_of(segment, [point, point]) is None:
            distance += manhattan_distance([segment[1][0] - segment[0][0], segment[1][1] - segment[0][1]])
        else:
            distance += manhattan_distance([point[0] - segment[0][0], point[1] - segment[0][1]])
            return distance
    return None

distances = [distance_on_path_to_point(paths[0], intersection) + distance_on_path_to_point(paths[1], intersection) for intersection in intersections]

print('Part 2 answer: ', min(distances))
