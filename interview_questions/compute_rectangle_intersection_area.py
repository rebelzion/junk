"""
Compute area of intersection between two axis aligned rectangles.
This operation is used a lot in Object Detection and Tracking.
It's implemented in many well known libraries, but it's a good exercise to implement it yourself.
"""

import doctest
from dataclasses import dataclass
import cv2 as cv

@dataclass
class Rectangle:
    x: int
    y: int
    w: int
    h: int

def compute_intersection_area(r1: Rectangle, r2: Rectangle) -> int:
    """
    >>> compute_intersection_area(Rectangle(0,0,1,2), Rectangle(3,3,2,2))
    0
    >>> compute_intersection_area(Rectangle(0,0,3,3), Rectangle(1, 0, 2, 2))
    4
    >>> compute_intersection_area(Rectangle(0,2,3,3), Rectangle(1,1,2,1))
    0
    >>> compute_intersection_area(Rectangle(0,0,3,3), Rectangle(1,1,2,1))
    2
    """
    xli = max(r1.x, r2.x)
    xri = min(r1.x + r1.w, r2.x + r2.w)

    yui = max(r1.y, r2.y)
    ydi = min(r1.y + r1.h, r2.y + r2.h)


    return max(0, xri - xli) * max(0, ydi - yui)



if __name__ == '__main__':
    doctest.testmod()
