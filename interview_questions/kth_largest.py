import pytest
from typing import List, Optional


def generate_tests():
    tests = [
        (([], 3), None),
        (([1], 3), 1),
        (([3,2,1], 3), 3)
    ]
    return tests


def partition(arr: List[int], l: int, r: int) -> int:

    p = r
    i = l
    j = r-1

    while True:
        while i <= r and arr[i] <= arr[p]:
            i += 1
        while j >= 0 and arr[j] > arr[p]:
            j -= 1

        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            break

    arr[r], arr[j+1] = arr[j+1], arr[r]

    return j+1


@pytest.mark.parametrize("inp,exp", [
    (([3,1,2], 0, 2), 1),
    (([1,2,3,4], 0, 3), 3),
    (([4,2,3,1], 0, 3), 0),
    (([2,1,7,6,8,5,3,4], 0, 7),3),
    (([2,2,1,1,1], 0, 4), 2),
    (([1,1,1,2,2], 0, 4), 4)
])
def test_partition(inp, exp):
    assert partition(arr=inp[0], l=inp[1], r=inp[2]) == exp




def kth_largest_pivot_helper(arr: List[int], k: int, l: int, r: int) -> Optional[int]:
    if l >= r:
        if l >= len(arr):
            l -= 1
        return arr[l]

    p = partition(arr, l, r)
    if p == k:
        return arr[p]
    elif k < p:
        return kth_largest_pivot_helper(arr, k, l, p-1)
    else:
        return kth_largest_pivot_helper(arr, k, p+1, r)



def kth_largest_pivot(arr: List[int], k: int) -> Optional[int]:

    if not arr or k <= 0:
        return None
    if k > len(arr):
        k = len(arr)


    kth_largest = kth_largest_pivot_helper(arr, k, 0, len(arr)-1)
    return kth_largest



def kth_largest_sorting(arr: List[int], k: int) -> Optional[int]:
    """
    Returns `k`-th largest element in `arr` using sorting.
    Time complexity is O(NlogN).
    """
    if not arr or k <= 0:
        return None

    arr = sorted(arr)
    return arr[k-1] if k <= len(arr) else arr[-1]



@pytest.mark.parametrize("inp,expected", generate_tests())
def test_kth_largest_sorting(inp, expected):

    assert kth_largest_sorting(arr=inp[0],k=inp[1]) == expected

@pytest.mark.parametrize("inp,expected", generate_tests())
def test_kth_largest_pivot(inp, expected):

    assert kth_largest_pivot(arr=inp[0],k=inp[1]) == expected


