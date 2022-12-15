import pytest
from typing import List, Tuple, Dict


def generate_tests():
    return [
        ([("a", "<", "b")], True),
        ([("a", ">", "b")], True),
        ([("a", ">", "b"), ("a", "<", "b")], False),
        ([("a", ">", "b"), ("a", ">", "c"), ("c", ">", "b")], True),
    ]


def parse_input(inequalities: List[Tuple[str,str,str]]) -> Dict[str, List[str]]:

    graph = {}
    for x,sign,y in inequalities:
        if sign == ">":
            if x not in graph:
                graph[x] = []
            graph[x].append(y)
        else:
            if y not in graph:
                graph[y] = []
            graph[y].append(x)
    return graph


def check_inequalities(inequalities: List[Tuple[str, str, str]]) -> bool:

    graph = parse_input(inequalities)
    visited = {}
    for node, neighbours in graph.items():
        visited[node] = 0
        for n in neighbours:
            visited[n] = 0

    def has_loop(v: str, graph: Dict[str, List[str]]) -> bool:

        visited[v] = 1
        for u in graph.get(v, []):
            if visited[u] == 1:
                return True
            elif visited[u] == 0:
                res = has_loop(u, graph)
                if res:
                    return True

        visited[v] = 2
        return False

    for node, status in visited.items():
        if status == 0:
            is_loop = has_loop(node, graph)
            if is_loop:
                return False

    return True



@pytest.mark.parametrize("inp,expected", [([("a", ">", "b")], {"a": ["b"]}), ([("a", "<", "b")], {"b": ["a"]})])
def test_parse_input(inp, expected):

    assert parse_input(inp) == expected


@pytest.mark.parametrize("inp,expected", generate_tests())
def test_check_inequalities(inp, expected):

    assert check_inequalities(inp) == expected



