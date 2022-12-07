"""
Implementation of naive multiplication and spare multiplication
for sparse matrices multiplication
"""
import numpy as np
import time

from typing import List, Tuple, Optional, Union, Dict

Matrix = List[List[Union[float, int]]]


def naive_matmul(A: Matrix, B: Matrix) -> Matrix:

    M, K = len(A), len(A[0])
    K, N = len(B), len(B[0])

    res = [[0] * N for _ in range(M)]

    for i in range(M):
        for j in range(N):
            for k in range(K):
                res[i][j] += A[i][k] * B[k][j]
    return res


def convert_sparse_to_list(mat: Matrix) -> Dict[int, List[Tuple[int, int]]]:
    """
    >>> convert_sparse_to_list([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    {0: [(0, 1)], 1: [(1, 2)], 2: [(2, 3)]}
    """
    sparse_mat = {}
    for i, row in enumerate(mat):
        for j, val in enumerate(row):
            if val != 0:
                if i not in sparse_mat:
                    sparse_mat[i] = []
                sparse_mat[i].append((j, val))
    return sparse_mat


def sparse_matmul(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    M, K = len(A), len(A[0])
    K, N = len(B), len(B[0])

    res = [[0] * N for _ in range(M)]

    # convert to list of tuples
    sparse_A = convert_sparse_to_list(A)
    sparse_B = convert_sparse_to_list(B)

    # perform sparse multiplication on lists
    for row, cols in sparse_A.items():
        for col, val in cols:
            if col in sparse_B:
                for col2, val2 in sparse_B[col]:
                    res[row][col2] += val * val2

    # convert back to matrix
    return res


def test_wrapper(func):
    def wrapper(*args, **kwargs):
        *inputs, output = func(*args, **kwargs)
        return {
            "input": inputs,
            "output": output,
        }

    return wrapper


@test_wrapper
def create_large_test(
    m: int, k: int, n: int, num_non_zero: Optional[int] = None
) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:

    if num_non_zero:
        mats = [np.zeros((m, k)), np.zeros((k, n))]
        for mat in mats:
            row_indices = np.random.randint(0, mat.shape[0], num_non_zero)
            col_indices = np.random.randint(0, mat.shape[1], num_non_zero)
            mat[row_indices, col_indices] = 1
        a, b = mats
    else:
        a = np.random.randint(1, 100, (m, k))
        b = np.random.randint(1, 100, (k, n))

    expected_output = np.matmul(a, b)
    return a.tolist(), b.tolist(), expected_output.tolist()


tests = {
    "one_element": {
        "input": ([[1]], [[1]]),
        "output": [[1]],
    },
    "2x2": {
        "input": ([[1, 0], [-1, 0]], [[0, 1], [1, 0]]),
        "output": [[0, 1], [0, -1]],
    },
    "large": create_large_test(m=300, k=200, n=100),
    "large_sparse": create_large_test(m=300, k=200, n=100, num_non_zero=50),
}

if __name__ == "__main__":
    import doctest

    doctest.testmod()

    np.random.seed(0)

    for op in [naive_matmul, sparse_matmul]:
        print(f"Testing {op.__name__}\n========")
        stats = {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "failed_tests": [],
        }
        for tname, test in tests.items():
            print(f"Running test: {tname}")
            try:
                start = time.perf_counter()
                res = op(*test["input"])
                end = time.perf_counter()
                print(f"\tTime: {(end - start):.5f} sec")

                if res == test["output"]:
                    stats["passed"] += 1
                else:
                    stats["failed"] += 1
                    stats["failed_tests"].append((tname, res))
            except Exception as e:
                stats["failed"] += 1
                stats["failed_tests"].append((tname, e))
            finally:
                stats["total"] += 1

        print(f"Total: {stats['total']}")
        print(f"Passed: {stats['passed']}")
        print(f"Failed: {stats['failed']}")
        if stats["failed"] == 0:
            print("All tests passed!\N{winking face}")
        else:
            print("Failed tests!\N{crying face}")
            for tname, res in stats["failed_tests"]:
                print(f"\tTest: {tname}")
                # print(f"Result: {res} -- Expected: {tests[tname]['output']}")
