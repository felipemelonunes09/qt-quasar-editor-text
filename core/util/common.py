from enum import Enum
import math

def distance(pointA: tuple, pointB: tuple) -> int:
    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pointA, pointB)))
    return int(dist)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    TOP = 3
    BOTTOM = 4
    CENTER = 5
