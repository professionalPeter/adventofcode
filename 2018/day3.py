import re
from collections import namedtuple

Point = namedtuple("Point", "x y")

class Claim:
    def __init__(self, claim_id, x, y, width, height):
        self.claim_id = claim_id
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

    def __str__(self):
        return f'#{self.claim_id} ({self.x},{self.y}) {self.width}x{self.height}'

    @property
    def diagonal(self):
        return Point(self.x + self.width, self.y + self.height)
            
        
def parse_claim(claim_str):
    match = re.search('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', claim_str)
    return Claim(match.group(1), match.group(2), match.group(3), match.group(4), match.group(5))

