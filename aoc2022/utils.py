import matplotlib.pyplot as plt
from typing import Union, Tuple

def plot(points, size: Union[int, Tuple[int, int]] = (10,10), marker='o', **kwargs):

    if size:
        plt.figure(figsize=(size,size) if isinstance(size, int) else size)
    plt.axis("off")

    plt.plot(*zip(*points), marker=marker, **kwargs)
    plt.show()
