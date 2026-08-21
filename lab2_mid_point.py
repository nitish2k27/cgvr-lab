"""
EXPERIMENT 2
Implementation of Midpoint Circle Drawing Algorithm using OpenGL
(uses eight-way symmetry of a circle)
"""

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# ---------- Window setup ----------
WIDTH, HEIGHT = 600, 600

if not glfw.init():
    raise Exception("GLFW could not be initialized")

window = glfw.create_window(WIDTH, HEIGHT, "Experiment 2 - Midpoint Circle Drawing", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window could not be created")

glfw.make_context_current(window)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(-WIDTH / 2, WIDTH / 2, -HEIGHT / 2, HEIGHT / 2)
glMatrixMode(GL_MODELVIEW)

glClearColor(1.0, 1.0, 1.0, 1.0)  # white background
glPointSize(3.0)


def plot_symmetric_points(xc, yc, x, y):
    """Given one computed point (x, y) relative to center, return all 8 symmetric points."""
    return [
        (xc + x, yc + y),
        (xc - x, yc + y),
        (xc + x, yc - y),
        (xc - x, yc - y),
        (xc + y, yc + x),
        (xc - y, yc + x),
        (xc + y, yc - x),
        (xc - y, yc - x),
    ]


def midpoint_circle(xc, yc, radius):
    """Compute pixel points for a circle using the Midpoint Circle Drawing Algorithm."""
    points = []

    x = 0
    y = radius
    p = 1 - radius  # initial decision parameter

    points.extend(plot_symmetric_points(xc, yc, x, y))

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

        points.extend(plot_symmetric_points(xc, yc, x, y))

    return points


def draw_points(points, color=(0.0, 0.0, 0.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for (x, y) in points:
        glVertex2i(x, y)
    glEnd()


# ---------- INPUT: define center and radius here ----------
xc, yc = 0, 0
radius = 8

circle_points = midpoint_circle(xc, yc, radius)

print(f"Midpoint Circle generated {len(circle_points)} points:")
for p in circle_points:
    print(p)

# ---------- Render loop ----------
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)

    draw_points(circle_points, color=(0.0, 0.5, 0.0))  # green circle

    glfw.swap_buffers(window)

glfw.terminate()