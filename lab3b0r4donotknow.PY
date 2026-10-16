import numpy as np
import matplotlib.pyplot as plt
import math


# ==========================================================
# TRANSFORMATION MATRICES (from notes)
# ==========================================================

def translation(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=float)


def rotation_origin(angle_deg):
    """Rotation about the origin (CCW positive, as per notes)."""
    theta = math.radians(angle_deg)
    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta),  math.cos(theta), 0],
        [0, 0, 1]
    ], dtype=float)


def rotation_pivot(angle_deg, px, py):
    """
    Rotation about an arbitrary pivot (px, py).
    Built exactly as in the notes:
        1. Translate pivot to origin  -> T(-px, -py)
        2. Rotate about origin        -> R(theta)
        3. Translate back             -> T(px, py)
    Composite = T2 . R . T1
    """
    T1 = translation(-px, -py)
    R = rotation_origin(angle_deg)
    T2 = translation(px, py)
    return T2 @ R @ T1


def scaling_origin(sx, sy):
    """Scaling relative to the origin (as per notes)."""
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype=float)


def scaling_pivot(sx, sy, px, py):
    """Scaling relative to an arbitrary reference point (px, py)."""
    T1 = translation(-px, -py)
    S = scaling_origin(sx, sy)
    T2 = translation(px, py)
    return T2 @ S @ T1


def reflection_x():
    return np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ], dtype=float)


def reflection_y():
    return np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ], dtype=float)


def reflection_y_equals_x():
    return np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ], dtype=float)


def shearing(shx, shy):
    return np.array([
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ], dtype=float)


# ==========================================================
# APPLY MATRIX
# ==========================================================

def apply_transformation(points, matrix):
    homogeneous = np.hstack((points, np.ones((len(points), 1))))
    result = (matrix @ homogeneous.T).T
    return result[:, :2]


# ==========================================================
# INPUT POINTS
# ==========================================================

def get_points():
    n = int(input("\nEnter number of vertices: "))
    points = []
    for i in range(n):
        print(f"\nVertex {i + 1}")
        x = float(input("Enter X coordinate: "))
        y = float(input("Enter Y coordinate: "))
        points.append([x, y])
    return np.array(points, dtype=float)


# ==========================================================
# BUILD ONE TRANSFORMATION MATRIX FROM MENU CHOICE
# ==========================================================

def build_matrix(step_no):
    print(f"\n--- Transformation {step_no} ---")
    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    print("4. Reflection")
    print("5. Shearing")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        tx = float(input("Enter Tx: "))
        ty = float(input("Enter Ty: "))
        return translation(tx, ty), f"Translation(tx={tx}, ty={ty})"

    elif choice == 2:
        angle = float(input("Enter rotation angle (degrees): "))
        print("1. Rotation about Origin")
        print("2. Rotation about Arbitrary Pivot")
        rchoice = int(input("Enter your choice: "))

        if rchoice == 1:
            return rotation_origin(angle), f"Rotation(angle={angle} about origin)"
        else:
            px = float(input("Enter pivot X: "))
            py = float(input("Enter pivot Y: "))
            return rotation_pivot(angle, px, py), f"Rotation(angle={angle} about pivot ({px},{py}))"

    elif choice == 3:
        sx = float(input("Enter Sx: "))
        sy = float(input("Enter Sy: "))
        print("1. Scaling relative to Origin")
        print("2. Scaling relative to Arbitrary Point")
        schoice = int(input("Enter your choice: "))

        if schoice == 1:
            return scaling_origin(sx, sy), f"Scaling(sx={sx}, sy={sy} about origin)"
        else:
            px = float(input("Enter reference point X: "))
            py = float(input("Enter reference point Y: "))
            return scaling_pivot(sx, sy, px, py), f"Scaling(sx={sx}, sy={sy} about ({px},{py}))"

    elif choice == 4:
        print("1. Reflection about X-axis")
        print("2. Reflection about Y-axis")
        print("3. Reflection about y = x")
        rchoice = int(input("Enter your choice: "))

        if rchoice == 1:
            return reflection_x(), "Reflection(X-axis)"
        elif rchoice == 2:
            return reflection_y(), "Reflection(Y-axis)"
        else:
            return reflection_y_equals_x(), "Reflection(y = x)"

    elif choice == 5:
        shx = float(input("Enter Shx: "))
        shy = float(input("Enter Shy: "))
        return shearing(shx, shy), f"Shearing(shx={shx}, shy={shy})"

    else:
        print("Invalid choice, skipping this step.")
        return np.eye(3), "Identity (invalid choice)"


def show_point_multiplication(matrix, point, transformed_point):
    x, y = point
    xp, yp = transformed_point

    m = matrix

    print(f"\n[ x' ]   [ {m[0,0]:>6.3f}  {m[0,1]:>6.3f}  {m[0,2]:>6.3f} ]   [ {x:>6.2f} ]")
    print(f"[ y' ] = [ {m[1,0]:>6.3f}  {m[1,1]:>6.3f}  {m[1,2]:>6.3f} ] . [ {y:>6.2f} ]")
    print(f"[ 1  ]   [ {m[2,0]:>6.3f}  {m[2,1]:>6.3f}  {m[2,2]:>6.3f} ]   [ {1:>6.2f} ]")

    print(f"\nx' = ({m[0,0]:.3f})({x:.2f}) + ({m[0,1]:.3f})({y:.2f}) + ({m[0,2]:.3f})(1) = {xp:.3f}")
    print(f"y' = ({m[1,0]:.3f})({x:.2f}) + ({m[1,1]:.3f})({y:.2f}) + ({m[1,2]:.3f})(1) = {yp:.3f}")


# ==========================================================
# DISPLAY GRAPH
# ==========================================================

def display(original, transformed, title):
    original_closed = np.vstack([original, original[0]])
    transformed_closed = np.vstack([transformed, transformed[0]])

    plt.figure(figsize=(8, 6))
    plt.plot(original_closed[:, 0], original_closed[:, 1], 'b-o', label="Original")
    plt.plot(transformed_closed[:, 0], transformed_closed[:, 1], 'r-o', label="Final Transformed")

    plt.axhline(0)
    plt.axvline(0)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.axis("equal")
    plt.show()


# ==========================================================
# MAIN PROGRAM
# ==========================================================

print("=" * 60)
print("        EXPERIMENT 4")
print("  COMPOSITE 2D TRANSFORMATIONS")
print("     USING MATRIX REPRESENTATION")
print("=" * 60)

points = get_points()

n_steps = int(input("\nHow many transformations to compose (in order applied)? "))

composite_matrix = np.eye(3)
step_labels = []

for i in range(1, n_steps + 1):
    matrix, label = build_matrix(i)
    step_labels.append(label)
    # Compose so that the FIRST chosen transform is applied FIRST:
    # overall = T_n @ ... @ T2 @ T1
    composite_matrix = matrix @ composite_matrix

transformed = apply_transformation(points, composite_matrix)

# ---------- Output ----------
print("\nOrder of composition applied:")
for i, label in enumerate(step_labels, start=1):
    print(f"  Step {i}: {label}")

print("\nFinal Composite Transformation Matrix:")
print(np.round(composite_matrix, decimals=10))

print("\nOriginal Coordinates:")
for i, point in enumerate(points):
    print(f"Vertex {i + 1}: ({point[0]:.2f}, {point[1]:.2f})")

print("\nFinal Transformed Coordinates:")
for i, point in enumerate(transformed):
    print(f"Vertex {i + 1}: ({point[0]:.2f}, {point[1]:.2f})")

print("\n" + "=" * 60)
print("MATRIX MULTIPLICATION FOR EACH POINT")
print("=" * 60)
for i in range(len(points)):
    print(f"\n--- Vertex {i + 1} ---")
    show_point_multiplication(composite_matrix, points[i], transformed[i])

display(points, transformed, "Composite 2D Transformation")

print("\nExperiment completed successfully!")