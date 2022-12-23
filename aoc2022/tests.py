from utils import merge_segments
import pytest


# segments = [(1,4), (6,7), (4,6)]
# print(merge_segments(segments))  # should print [(1, 7)]


@pytest.mark.parametrize("inp,exp", [([(1,4), (6,7), (4,6)], [(1,7)])])
def test_merge_segments(inp, exp):
    assert merge_segments(inp) == exp
