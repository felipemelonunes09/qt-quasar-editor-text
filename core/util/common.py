import math

def distance(pointA: tuple, pointB: tuple) -> int:
    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pointA, pointB)))
    return int(dist)