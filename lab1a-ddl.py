"""
EXPERIMENT 1a
Implementation of DDA (Digital Differential Analyzer) Line Drawing Algorithm using OpenGL
"""

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# ---------- Window setup ----------
WIDTH, HEIGHT = 600, 600

if not glfw.init():
    raise Exception("GLFW could not be initialized")

# No version hints -> gives a compatibility profile so glBegin/glVertex work
window = glfw.create_window(WIDTH, HEIGHT, "Experiment 1a - DDA Line Drawing", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window could not be created")

glfw.make_context_current(window)

# Set up a simple coordinate system: origin at center, range -300 to 300
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(-WIDTH / 2, WIDTH / 2, -HEIGHT / 2, HEIGHT / 2)
glMatrixMode(GL_MODELVIEW)

glClearColor(1.0, 1.0, 1.0, 1.0)  # white background
glPointSize(3.0)


def dda_line(x0, y0, x1, y1):
    """Compute pixel points for a line from (x0,y0) to (x1,y1) using DDA algorithm."""
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return [(x0, y0)]

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x0, y0
    points = []
    for _ in range(int(steps) + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    return points


def draw_points(points, color=(0.0, 0.0, 0.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for (x, y) in points:
        glVertex2i(x, y)
    glEnd()


# ---------- INPUT: define your line endpoints here ----------
x0, y0 = -200, -100
x1, y1 = 200, 150

line_points = dda_line(x0, y0, x1, y1)

print("DDA generated points:")
for p in line_points:
    print(p)

# ---------- Render loop ----------
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)

    draw_points(line_points, color=(0.0, 0.0, 1.0))  # blue line

    glfw.swap_buffers(window)

glfw.terminate()