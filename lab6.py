"""
EXPERIMENT 6
Z-BUFFER (DEPTH BUFFER) ALGORITHM FOR HIDDEN SURFACE REMOVAL

Convention used: smaller z = nearer to the viewer.

Algorithm:
  1. Frame buffer  <- background color
  2. Z-buffer      <- infinity (farthest possible depth)
  3. For every polygon (triangle), for every pixel (x, y) it covers:
        compute depth z at that pixel (interpolated from the vertices)
        if z < zbuffer[y][x]:
              zbuffer[y][x] = z
              framebuffer[y][x] = polygon color
"""

import numpy as np
import matplotlib.pyplot as plt

COLORS = {
    "red":     (1.0, 0.0, 0.0),
    "green":   (0.0, 0.7, 0.0),
    "blue":    (0.0, 0.0, 1.0),
    "yellow":  (1.0, 1.0, 0.0),
    "cyan":    (0.0, 1.0, 1.0),
    "magenta": (1.0, 0.0, 1.0),
    "orange":  (1.0, 0.5, 0.0),
}


# ==========================================================
# INPUT
# ==========================================================

def get_input():
    print("\n--- Frame buffer size ---")
    width = int(input("Enter width  (pixels, e.g. 100): "))
    height = int(input("Enter height (pixels, e.g. 100): "))

    n = int(input("\nEnter number of triangles: "))
    triangles = []

    for i in range(n):
        print(f"\n--- Triangle {i + 1} ---")
        verts = []
        for j in range(3):
            x = float(input(f"  Vertex {j + 1} X: "))
            y = float(input(f"  Vertex {j + 1} Y: "))
            z = float(input(f"  Vertex {j + 1} Z (depth, smaller = nearer): "))
            verts.append((x, y, z))

        print("  Colors:", ", ".join(COLORS.keys()))
        cname = input("  Enter color name: ").strip().lower()
        if cname not in COLORS:
            print("  Unknown color, using red.")
            cname = "red"

        triangles.append((verts, cname))

    return width, height, triangles


# ==========================================================
# RASTERIZATION HELPERS
# ==========================================================

def barycentric(px, py, v0, v1, v2):
    """Return barycentric weights (w0, w1, w2) of pixel (px, py), or None if degenerate."""
    x0, y0, _ = v0
    x1, y1, _ = v1
    x2, y2, _ = v2

    denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if denom == 0:
        return None

    w0 = ((y1 - y2) * (px - x2) + (x2 - x1) * (py - y2)) / denom
    w1 = ((y2 - y0) * (px - x2) + (x0 - x2) * (py - y2)) / denom
    w2 = 1 - w0 - w1
    return w0, w1, w2


def render(width, height, triangles, use_zbuffer=True):
    """Draw all triangles. With use_zbuffer=False, later triangles simply overwrite earlier ones."""
    framebuffer = np.ones((height, width, 3))          # white background
    zbuffer = np.full((height, width), np.inf)         # initialise to infinity

    for verts, cname in triangles:
        color = COLORS[cname]
        v0, v1, v2 = verts

        xs = [v[0] for v in verts]
        ys = [v[1] for v in verts]
        x_min = max(int(np.floor(min(xs))), 0)
        x_max = min(int(np.ceil(max(xs))), width - 1)
        y_min = max(int(np.floor(min(ys))), 0)
        y_max = min(int(np.ceil(max(ys))), height - 1)

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                w = barycentric(x, y, v0, v1, v2)
                if w is None:
                    continue
                w0, w1, w2 = w

                # pixel is inside the triangle
                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    z = w0 * v0[2] + w1 * v1[2] + w2 * v2[2]   # interpolated depth

                    if not use_zbuffer:
                        framebuffer[y, x] = color
                    elif z < zbuffer[y, x]:                    # nearer than stored?
                        zbuffer[y, x] = z
                        framebuffer[y, x] = color

    return framebuffer, zbuffer


# ==========================================================
# MAIN
# ==========================================================

print("=" * 60)
print("        EXPERIMENT 6")
print("  Z-BUFFER ALGORITHM FOR HIDDEN SURFACE REMOVAL")
print("=" * 60)

width, height, triangles = get_input()

fb_no_z, _ = render(width, height, triangles, use_zbuffer=False)
fb_z, zbuf = render(width, height, triangles, use_zbuffer=True)

# Depth map for display (background = blank)
depth_display = np.where(np.isinf(zbuf), np.nan, zbuf)

print("\nDepth range stored in Z-buffer:")
if np.all(np.isnan(depth_display)):
    print("  No pixels were drawn.")
else:
    print(f"  Nearest  z = {np.nanmin(depth_display):.3f}")
    print(f"  Farthest z = {np.nanmax(depth_display):.3f}")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(fb_no_z, origin="lower")
axes[0].set_title("Without Z-buffer\n(last drawn overwrites)")

axes[1].imshow(fb_z, origin="lower")
axes[1].set_title("With Z-buffer\n(hidden surfaces removed)")

im = axes[2].imshow(depth_display, origin="lower", cmap="viridis")
axes[2].set_title("Z-buffer contents\n(darker = nearer)")
fig.colorbar(im, ax=axes[2], fraction=0.046)

for ax in axes:
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

plt.tight_layout()
plt.show()

print("\nExperiment completed successfully!")