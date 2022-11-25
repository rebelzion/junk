"""
The goal is to generate random convex polygons.
There are different methods:
1. https://cglab.ca/~sander/misc/ConvexGeneration/convex.html mentioned here it's fast and random.
"""

import turtle
from typing import List, Tuple, Optional
import random
import numpy as np
import numpy.linalg as linalg

Point2D = Tuple[float, float]
Vector2D = Tuple[float, float]

def polar2cart(radius: float, theta: float) -> Point2D:
    """
    Convert from Polar coordiantes to Cartesian coordinates.
    radius: magnitude from origin
    theta: angle magnitude between X-axis in radians.
    Returns:
        (x,y)
    """
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return x,y


def get_ang(a: np.ndarray, b: np.ndarray, in_deg: bool = False) -> float:
    ang_rad = np.arccos(a @ b / (linalg.norm(a) * linalg.norm(b)))
    return np.degrees(ang_rad) if in_deg else ang_rad


def get_perpendicular(v: Vector2D) -> Vector2D:
    y = random.randint(0, 100)
    x = - (v[1] * y) / v[0]
    return (x,y)


def draw_vector(t: turtle.Turtle, x: int, y:int) -> None:

    t.penup()
    t.setposition(0,0)
    t.pendown()
    t.goto(x,y)
    t.penup()


def fill_polygon(t: turtle.Turtle, xs: List[int], ys: List[int], color: str = 'red') -> None:
    if not xs:
        return

    t.fillcolor(color)
    t.begin_fill()

    t.penup()
    t.setposition(xs[0], ys[0])
    t.pendown()
    for x,y in zip(xs[1:], ys[1:]):
        t.goto(x,y)
    t.goto(xs[0], ys[0])
    t.end_fill()


def generate_random_convex_polygon_on_circle(radius: float, n: int) -> Tuple[List[float], List[float]]:


    degs = [np.random.randint(0, 360) for _ in range(n)]
    degs = sorted(degs)

    xs = []
    ys = []

    for deg in degs:

        x,y = polar2cart(radius=radius, theta=np.radians(deg))
        xs.append(x)
        ys.append(y)
    return xs, ys



def write_text_at(turtle: turtle.Turtle, x: float, y: float, text: str):


    px, py = turtle.position()
    turtle.penup()
    turtle.setposition(x, y)
    turtle.write(text, move=False, font=('Arial', 16, 'bold'))

    turtle.setposition(px, py)


def generate_random_convex_polygon(
    npoints: int,
    sx: Optional[int] = None,
    sy: Optional[int] = None,
    seed: Optional[int] = None,
    xlim: Tuple[int, int] = (0, 300),
    ylim: Tuple[int, int] = (0, 300)
) -> Tuple[List[int], List[int]]:

    random.seed(seed)

    if not sx and not sy:
        sx, sy = random.randint(*xlim), random.randint(*ylim)


    # go along a line and for the next point you always have to be on the left of the line

    xs = [sx, np.random.randint(*xlim)]
    ys = [sy, np.random.randint(*ylim)]
    """
    # TODO @vronin: Debug this
    for i in range(npoints-2):

        v = np.array([xs[-1] - xs[-2], ys[-1] - ys[-2]])
        ang_xy_v = get_ang(a=np.array([0,1]), b=v, in_deg=True)
        print(f'{ang_xy_v=}')
        pv = np.array(get_perpendicular((v[0], v[1])))
        w = np.array([xs[0] - xs[-1], ys[0] - ys[-1]])
        print('w = ', w)
        deg_min = 90
        deg_max = get_ang(a=w, b=-pv, in_deg=True)

        print(deg_min, deg_max, random.randint(deg_min, deg_max))

        rad = np.radians(random.randint(deg_min, deg_max))
        mag = random.randint(100, 300)

        x,y = polar2cart(radius = mag, theta = rad)

        xs.append(x)
        ys.append(y)
    """

    return xs,ys

# xs, ys = generate_random_convex_polygon(10)

n = 4
radius = 200
write_text_at(turtle, -400, 500, f"Random Convex Polygon of {n} Points on a Circle of Radius={radius}")
xs, ys = generate_random_convex_polygon_on_circle(radius = radius, n = n)


t = turtle.Turtle()

fill_polygon(t, xs = xs, ys = ys, color = 'green')
turtle.mainloop()
