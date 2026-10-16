import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# REGION CODES (OUTCODES)
# ==========================================================
INSIDE = 0   # 0000
LEFT   = 1   # 0001
RIGHT  = 2   # 0010
BOTTOM = 4   # 0100
TOP    = 8   # 1000


def compute_outcode(x, y, xmin, ymin, xmax, ymax):
    """Compute the 4-bit region code for a point relative to the clip window."""
    code = INSIDE

    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT

    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP

    return code


def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    """
    Clips the line (x1,y1)-(x2,y2) against the rectangular window
    defined by (xmin,ymin) - (xmax,ymax).
    Returns (accepted, x1, y1, x2, y2)
    accepted = False means the line is completely outside (rejected).
    """

    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    outcode2 = compute_outcode(x2, y2, xmin, ymin, xmax, ymax)
    accepted = False

    while True:

        # -------- Trivial accept: both points inside --------
        if outcode1 == 0 and outcode2 == 0:
            accepted = True
            break

        # -------- Trivial reject: both share an outside region --------
        elif (outcode1 & outcode2) != 0:
            accepted = False
            break

        # -------- Otherwise, clip against whichever point is outside --------
        else:
            x, y = 0.0, 0.0

            # Pick the point that is outside the window
            outcode_out = outcode1 if outcode1 != 0 else outcode2

            # Find intersection point using the line's slope
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax

            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin

            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax

            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Replace the outside point with the intersection point
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

    return accepted, x1, y1, x2, y2


# ==========================================================
# DISPLAY
# ==========================================================

def display(xmin, ymin, xmax, ymax, orig_line, clipped_line, accepted):
    ox1, oy1, ox2, oy2 = orig_line

    plt.figure(figsize=(7, 7))

    # Draw clip window
    window_x = [xmin, xmax, xmax, xmin, xmin]
    window_y = [ymin, ymin, ymax, ymax, ymin]
    plt.plot(window_x, window_y, 'k-', linewidth=2, label="Clip Window")

    # Draw original line (dashed)
    plt.plot([ox1, ox2], [oy1, oy2], 'b--', label="Original Line")

    # Draw clipped line (solid, only if accepted)
    if accepted:
        cx1, cy1, cx2, cy2 = clipped_line
        plt.plot([cx1, cx2], [cy1, cy2], 'r-', linewidth=3, label="Clipped Line")
    else:
        plt.text(0.5, 0.5, "Line completely REJECTED (outside window)",
                  transform=plt.gca().transAxes, ha='center', color='red')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Cohen-Sutherland Line Clipping")
    plt.grid(True)
    plt.legend()
    plt.axis("equal")
    plt.show()


# ==========================================================
# MAIN PROGRAM
# ==========================================================

print("=" * 60)
print("        EXPERIMENT 5")
print("  COHEN-SUTHERLAND LINE CLIPPING ALGORITHM")
print("=" * 60)

print("\n--- Enter Clipping Window ---")
xmin = float(input("Enter Xmin: "))
ymin = float(input("Enter Ymin: "))
xmax = float(input("Enter Xmax: "))
ymax = float(input("Enter Ymax: "))

print("\n--- Enter Line Endpoints ---")
x1 = float(input("Enter x1: "))
y1 = float(input("Enter y1: "))
x2 = float(input("Enter x2: "))
y2 = float(input("Enter y2: "))

accepted, cx1, cy1, cx2, cy2 = cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax)

print("\nOriginal Line: ({:.2f}, {:.2f}) -> ({:.2f}, {:.2f})".format(x1, y1, x2, y2))
print("Clip Window: Xmin={}, Ymin={}, Xmax={}, Ymax={}".format(xmin, ymin, xmax, ymax))

if accepted:
    print("\nLine ACCEPTED (partially or fully inside).")
    print("Clipped Line: ({:.2f}, {:.2f}) -> ({:.2f}, {:.2f})".format(cx1, cy1, cx2, cy2))
else:
    print("\nLine REJECTED (completely outside the clip window).")

display(xmin, ymin, xmax, ymax, (x1, y1, x2, y2), (cx1, cy1, cx2, cy2), accepted)

print("\nExperiment completed successfully!")