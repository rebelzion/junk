import pytest

class MedianFinder:

    def __init__(self):
        self.nums = []

    def addNum(self, num: int) -> None:
        i = 0
        N = len(self.nums)
        while i < N and num > self.nums[i]:
            i += 1

        if i >= N:
            self.nums.append(num)
        else:
            self.nums = self.nums[:i] + [num] + self.nums[i:]


    def findMedian(self) -> float:
        N = len(self.nums)
        if N % 2 == 0:
            return (self.nums[N // 2] + self.nums[(N-1) // 2]) / 2
        else:
            return self.nums[N // 2]




def generate_tests():
    tests = [
        ((["addNum", "addNum", "findMedian", "addNum", "findMedian"], [[1], [2],[],[3],[]]), [None, None, 1.5, None, 2]),
        ((["addNum", "findMedian"],[[1], []]), [None, 1])
    ]

    return tests


@pytest.mark.parametrize("inp,expected", generate_tests())
def test_median_finder_insertion_sort(inp,expected):

    mf = MedianFinder()
    fnames, params = inp
    for fname, param, exp in zip(fnames, params, expected):
        func = getattr(mf, fname)
        out = func(*param)

        assert out == exp




