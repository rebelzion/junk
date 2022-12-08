"""
Given a list of N elements and a window of size K,
start sliding the window from the start of the list and retrieve
the maximum at every step.

Result: List of N-K elements `output`, with the meaning:
    output[i] = maximum value from the input list in the window i..i+k

Solution:
    1. can be solved in O(N * K) with brute-force by finding the maximum at every step
    through linear iteration in the k sized window.

    2. can be solved in O(N * log(K)) with using a heap to maintain the k elements and
    retrieve the maximum in O(1)

    3. can be solved in O(N) by maintaining a deque with the following assumption:
        while deque[-1] < A[i]: deque.pop(), meaning in the deque we will always
        maintain the highest values in decreasing order starting from deque[0].
        The maximum at every step will be at deque[0].
"""


from collections import deque
import pytest
from typing import List


def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    d = deque()
    res = []
    max_elem = 0
    def clean_deque(i):

        if d and d[0] <= i - k:
            d.popleft()

        while d and nums[i] > nums[d[-1]]:
            d.pop()

    for i in range(k):
        clean_deque(i)
        d.append(i)
        if nums[i] > nums[max_elem]:
            max_elem = i
    res.append(nums[max_elem])

    for i in range(k, len(nums)):
        clean_deque(i)
        d.append(i)
        res.append(nums[d[0]])

    return res

def generate_tests():

    tests = [
        (([3], 1), [3]),                        # one element
        (([1,2,3], 1), [1,2,3]),                # increasing sequence k = 1
        (([3,2,1], 1), [3,2,1]),                # decreasing sequence k = 1
        (([3,1,2,4,6,3,7],3),[3,4,6,6,7]),      # k > 1
    ]
    return tests


@pytest.mark.parametrize("inp,expected", generate_tests())
def test_maxSlidingWindow(inp, expected):
    assert(maxSlidingWindow(nums=inp[0], k=inp[1]) == expected)
