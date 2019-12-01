from collections import Counter

def make_letter_frequency_set(word):
    """Create a set containing the frequency counts of letters in the 'word'.
        For example the word "aabbcd", would return {1,2} because though there are
        four letters, each occurs at a frequency of 1 or 2.
    """
    return {occurrences for occurrences in Counter(word).values()}

def part1():
    twos = 0
    threes = 0
    with open('day2input.txt') as fp:
        for line in fp:
            frequency_set = make_letter_frequency_set(line)
            if 2 in frequency_set:
                twos += 1
            if 3 in frequency_set:
                threes += 1

    print('Words with letters that occur twice:', twos)
    print('Words with letters that occur thrice:', threes)
    print('Checksum (product of the above):', twos * threes)

def extract_common_characters(word1, word2):
    """Return string with the characters that differ between the two words removed"""
    return ''.join(char1 for char1, char2 in zip(word1, word2))


def find_ids_differing_by_1(ids):
    """Return the first occurrence of words that only differ at one position"""
    for word1 in ids:
        for word2 in ids:
            if character_diff_count(word1, word2) == 1:
                return (word1, word2)

def character_diff_count(word1, word2):
    """Returns count of the number of characters that differ between the two words"""
    count = 0
    for i in range(len(word1)):
            if word1[i] != word2[i]:
                    count += 1
    return count

def part2(input = None):
    input = input or "day2input.txt"
    with open(input) as idFile:
        ids = idFile.read().splitlines()
        matching_ids = find_ids_differing_by_1(ids)
        #print(f'IDs differing by 1 character: {matching_ids}')
        common_characters = extract_common_characters(matching_ids[0], matching_ids[1])
        print('Matching characters in matching IDs:', common_characters)

part1()
part2()
