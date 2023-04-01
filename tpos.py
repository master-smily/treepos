import csv
import random
import locale
import math
from typing import NamedTuple

class Tree(NamedTuple):
    id: int
    diameter_m: float
    diameter: float
    ca: float
    x: int
    y: int
    b: float
    b_ca: float

class Point(NamedTuple):
    x: int
    y: int

def read_tree_file():
    locale.setlocale(locale.LC_NUMERIC, 'sv_SE')
    forest = []
    with open('Tree position.csv', newline='') as csvfile:
        r = csv.reader(csvfile, dialect='excel', delimiter=';')
        next(r)
        for line in r:
            if line[0] == '':
                break
            forest.append(Tree(
                locale.atoi(line[0]),
                locale.atof(line[1]),
                locale.atof(line[2]),
                locale.atof(line[3]),
                locale.atoi(line[4]),
                locale.atoi(line[5]),
                locale.atof(line[6]),
                locale.atof(line[7])
            ))
    locale.setlocale(locale.LC_NUMERIC, '')
    return forest

def generate_points(n, forest, radius):
    min_x = min(forest, key=lambda t: t.x).x + radius
    max_x = max(forest, key=lambda t: t.x).x - radius
    min_y = min(forest, key=lambda t: t.y).y + radius
    max_y = max(forest, key=lambda t: t.y).y - radius
    points = []
    for _ in range(n):
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        points.append(Point(x, y))
    return points

def check_tree_near_sample(points, forest, radius):
    matches = [[] for _ in points]
    for t in forest:
        for p, match in zip(points, matches):
            x_diff = abs(t.x - p.x)
            y_diff = abs(t.y - p.y)
            d = math.hypot(x_diff, y_diff)
            if d <= radius:
                match.append(t)
    return matches

def print_results(points, matches):
    for i, (p, ms) in enumerate(zip(points, matches)):
        if len(ms) != 0:
            print()

        print(f"Sample point {i} at x: {p.x:n}, y: {p.y:n}")
        for m in ms:
            print(f"   {m.id} at ({m.x:n}, {m.y:n})")

def main():
    forest = read_tree_file()
    print("How many sample points?", end=' ')
    sample_n = int(input())

    print("What radius?", end=' ')
    radius = int(input())
    print()

    points = generate_points(sample_n, forest, radius)
    matches = check_tree_near_sample(points, forest, radius)

    print_results(points, matches)

if __name__ == "__main__":
    main()
