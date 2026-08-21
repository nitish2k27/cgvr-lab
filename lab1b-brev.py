"""
EXPERIMENT 1b
Implementation of Bresenham's Line Drawing Algorithm using OpenGL
"""

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# ---------- Window setup ----------
WIDTH, HEIGHT = 600, 600

if not glfw.init():
    raise Exception("GLFW could not be initialized")

window = glfw.create_window(WIDTH, HEIGHT, "Experiment 1b - Bresenham Line Drawing", None, None)
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


def bresenham_line(x0, y0, x1, y1):
    """Compute pixel points for a line from (x0,y0) to (x1,y1) using Bresenham's algorithm.
    Handles all slope cases (any octant)."""
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x1 >= x0 else -1
    sy = 1 if y1 >= y0 else -1

    x, y = x0, y0

    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx + 1):
            points.append((x, y))
            if p >= 0:
                y += sy
                p -= 2 * dx
            x += sx
            p += 2 * dy
    else:
        p = 2 * dx - dy
        for _ in range(dy + 1):
            points.append((x, y))
            if p >= 0:
                x += sx
                p -= 2 * dy
            y += sy
            p += 2 * dx

    return points


def draw_points(points, color=(0.0, 0.0, 0.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for (x, y) in points:
        glVertex2i(x, y)
    glEnd()


# ---------- INPUT: define your line endpoints here ----------
x0, y0 = 20, 10
x1, y1 = 30,18 

line_points = bresenham_line(x0, y0, x1, y1)

print("Bresenham generated points:")
for p in line_points:
    print(p)

# ---------- Render loop ----------
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)

    draw_points(line_points, color=(1.0, 0.0, 0.0))  # red line

    glfw.swap_buffers(window)

glfw.terminate()