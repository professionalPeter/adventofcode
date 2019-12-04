'''Day 4 - This could stand to be cleaned up, but for now we're onto day 5'''

def passes_criteria(candidate):
    chars = str(candidate)
    current_run = 1
    runs = set()
    for l, r in zip(chars, chars[1:]):
        if l == r:
            current_run +=1
        elif r < l:
            return (False, False)
        else:
            runs.add(current_run)
            current_run = 1
    runs.add(current_run)
    return (max(runs) > 1, 2 in runs)

results = [passes_criteria(candidate) for candidate in range(153517, 630395)]
print('Part 1 answer: ', sum([1 if result[0] else 0 for result in results]))
print('Part 2 answer: ', sum([1 if result[1] else 0 for result in results]))
