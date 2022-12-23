from collections import deque
from utils import read_input, get_extreme, timeit, get_distance, merge_segments
import time
import re


def find_coverage_at_y_segments(sensor_positions, beacon_positions, at_y=10):

    segments = []
    for (sx, sy), (bx, by) in zip(sensor_positions, beacon_positions):
        d = get_distance(sx, sy, bx, by)
        dy = abs(sy - at_y)
        if dy <= d:
            xmin = sx - abs(d - dy)
            xmax = sx + abs(d - dy)
            segments.append((xmin, xmax))
    segments = merge_segments(segments)
    return segments


def find_coverage_at_y(sensor_positions, beacon_positions, at_y=10):

    coverage_x = set()
    for (sx, sy), (bx, by) in zip(sensor_positions, beacon_positions):
        d = get_distance(sx, sy, bx, by)
        dy = abs(sy - at_y)
        if dy <= d:
            xmin = sx - abs(d - dy)
            xmax = sx + abs(d - dy)
            for x in range(xmin, xmax + 1):
                coverage_x.add(x)

    for x,y in beacon_positions:
        if y==at_y and x in coverage_x:
            coverage_x.remove(x)
    return coverage_x


def count_coverage_at_y(sensor_positions, beacon_positions, at_y=10):

    coverage_x = find_coverage_at_y(sensor_positions, beacon_positions, at_y=at_y)
    return len(coverage_x)


def parse_input(lines):
    sensor_positions=[]
    beacon_positions=[]
    for line in lines:
        matches=re.match(
            r'Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)', line)
        sensor_positions.append((int(matches.group(1)), int(matches.group(2))))
        beacon_positions.append((int(matches.group(3)), int(matches.group(4))))
    return sensor_positions, beacon_positions


if __name__ == '__main__':
    # Read the input
    lines=read_input()

    sensor_positions, beacon_positions=parse_input(lines)

    # Level 1
    count=count_coverage_at_y(sensor_positions, beacon_positions, at_y=10)
    print(count)


    # Level 2
    times = []
    y_max = 4_000_002
    mod = y_max if y_max < 10 else y_max // 10
    for i, y in enumerate(range(0, y_max)):
        with timeit(return_val=True) as t:
            segments=find_coverage_at_y_segments(sensor_positions, beacon_positions, at_y=y)
            if len(segments) > 1:
                for seg, next_seg in zip(segments, segments[1:]):
                    if seg[1] < next_seg[0] - 1:
                        print(f"Beacon at: ({seg[1]+1},{y})")
        times.append(t())
        if i % mod == 0:
            print(f"Step {i:_}: {times[-1]:.6f} sec")
