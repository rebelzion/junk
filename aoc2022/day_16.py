import re
from utils import read_input
from collections import defaultdict
from queue import Queue
from typing import Iterable, Dict
from dataclasses import dataclass
import itertools


@dataclass
class Node:
    id: str
    children: Iterable[str]


@dataclass
class State:
    node_id: str
    steps: int


@dataclass
class Valve(Node):
    flow_rate: int

    def __repr__(self):
        return f"name={self.id}, flow_rate={self.flow_rate}, children={self.children}"


def get_valves_with_flow(valves: Iterable[Valve]) -> Iterable[Valve]:
    return [valve for valve in valves if valve.flow_rate > 0]


def bfs(start_node: Node, graph: Dict[str, Node]) -> Dict[str, int]:

    q = Queue()
    q.put(State(start_node.id, 0))
    visited = set({start_node.id})
    distances = defaultdict(lambda: float('inf'))
    while not q.empty():
        state = q.get()
        node_id = state.node_id
        steps = state.steps
        distances[node_id] = steps

        node = graph[node_id]
        for child_id in node.children:
            if child_id not in visited:
                new_state = State(child_id, steps+1)
                q.put(new_state)
                visited.add(child_id)

    return distances


def get_pairwise_distances(graph, node_ids):

    distances = defaultdict(lambda: defaultdict(lambda: float('inf')))

    for node_id in node_ids:
        distances_from_node = bfs(graph[node_id], graph)
        for other_node_id, dist in distances_from_node.items():
            distances[(node_id, other_node_id)] = dist

    for node_id, other_node_id in itertools.combinations(node_ids, 2):
        assert distances[(node_id, other_node_id)
                         ] == distances[(other_node_id, node_id)]

    sorted_node_ids = sorted(node_ids)
    for node_id in sorted_node_ids:
        for other_node_id in sorted_node_ids:
            print(f"{distances[(node_id, other_node_id)]:2}", end=' ')
        print()

    return distances


def solve(graph: Dict[str, Valve], maxT: int, start_node: str):

    valves_with_flow = [v.id for v in get_valves_with_flow(graph.values())]

    distances = get_pairwise_distances(
        graph, node_ids=valves_with_flow + [start_node])
    # print('distances=')
    # for k, v in distances.items():
    #     print(f"{k} -> {v}")

    print(f"{valves_with_flow=}")

    q = Queue()
    # pressure, node, time_elapsed, open_valves
    q.put((0, start_node, 0, set()))
    max_pressure = -1
    results = []
    while not q.empty():

        state = q.get()
        pressure, node, time_elapsed, open_valves  = state
        # print('node=', node, 'open_valves=', open_valves)

        if time_elapsed > maxT:
            continue

        if time_elapsed == maxT:
            max_pressure = max(pressure, max_pressure)
            results.append((pressure, open_valves))
            continue

        if node not in open_valves and node != start_node:
            pressure_new = pressure + \
                sum(graph[valve].flow_rate for valve in open_valves)
            state_new = (pressure_new, node, time_elapsed +
                         1, open_valves.union({node}))
            q.put(state_new)
        else:
            moved_to_valve = False
            for valve in valves_with_flow:
                if valve not in open_valves:
                    dt = distances[(node, valve)]
                    time_elapsed_new = time_elapsed + dt

                    if time_elapsed_new <= maxT:
                        pressure_new = pressure + dt * \
                            sum(graph[v_].flow_rate for v_ in open_valves)
                        state_new = (
                            pressure_new, valve, time_elapsed_new, open_valves)
                        q.put(state_new)
                        moved_to_valve = True
            if not moved_to_valve:
                time_elapsed_new = time_elapsed + 1
                if time_elapsed_new <= maxT:
                    pressure_new = pressure + \
                        sum(graph[valve].flow_rate for valve in open_valves)
                    state_new = (pressure_new, node, time_elapsed_new, open_valves)
                    q.put(state_new)

    return max_pressure


def parse_input(input: Iterable[str]) -> Iterable[Dict[str, Valve]]:

    graph = {}
    for line in input:
        matches = re.match(
            r"Valve (\w+) has flow rate=(\d+); tunnels* leads* to valves* ((\w+)(, (\w+))*)", line)

        valve = matches[1]
        flow_rate = int(matches[2])
        tunnels_ = matches[3].split(", ")

        new_valve = Valve(id=valve, flow_rate=flow_rate, children=tunnels_)

        graph[valve] = new_valve

    return graph


if __name__ == "__main__":
    input = read_input()

    graph = parse_input(input)

    res = solve(graph=graph, maxT=30, start_node='AA')
    print(f'res={res}')
