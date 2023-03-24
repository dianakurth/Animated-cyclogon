import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys


def check_triangle(side_a, side_b, side_c):
    if side_a + side_b > side_c and side_a + side_c > side_b and side_b + side_c > side_a:
        return True
    else:
        return False


radius = 3
step = 0.1
length = 50
x = np.arange(0, length, step)
le_y = int(length / step)
y = np.zeros(le_y)

a = int(input("First side: "))
b = int(input("Second side: "))
c = int(input("Third side: "))

if check_triangle(a, b, c) is False:
    print("This triangle does not exist")
    sys.exit()

# triangle's angles in radians
alfa = np.arccos(((a ** 2) + (c ** 2) - (b ** 2)) / (2 * a * c))
beta = np.arccos(((c ** 2) + (b ** 2) - (a ** 2)) / (2 * c * b))
gamma = np.arccos(((b ** 2) + (a ** 2) - (c ** 2)) / (2 * a * b))

# angles in degrees
alfaD = alfa * (180 / np.pi)
betaD = beta * (180 / np.pi)
gammaD = gamma * (180 / np.pi)

# initial coordinates of triangle
xa = 0
ya = 0

xb = a
yb = 0

yc = np.sin(alfa) * c
xc = np.cos(alfa) * c

# centre of triangle
cen_x = (xa + xb + xc) / 3
cen_y = (ya + yb + yc) / 3

# distances from vertices to centre
centre_to_a = np.sqrt((cen_x - xa) ** 2 + (cen_y - ya) ** 2)
centre_to_b = np.sqrt((cen_x - xb) ** 2 + (cen_y - yb) ** 2)
centre_to_c = np.sqrt((cen_x - xc) ** 2 + (cen_y - yc) ** 2)

if (b < a < c) or (c < a < b):
    medium = a
elif (a < b < c) or (c < b < a):
    medium = b
elif (a < c < b) or (b < c < a):
    medium = c
elif a == b == c:
    medium = b
elif a == b or a == c:
    medium = a
elif b == a or b == c:
    medium = a
else:
    medium = a

divider = (centre_to_a + centre_to_b + centre_to_c) / 3 - medium / 10

# inside angles of the triangle (between lines from centre to vertices)
alfa_inside = np.arccos(((centre_to_a ** 2) + (centre_to_b ** 2) - (a ** 2)) / (2 * centre_to_a * centre_to_b))
beta_inside = np.arccos(((centre_to_b ** 2) + (centre_to_c ** 2) - (b ** 2)) / (2 * centre_to_b * centre_to_c))
gamma_inside = np.arccos(((centre_to_c ** 2) + (centre_to_a ** 2) - (c ** 2)) / (2 * centre_to_c * centre_to_a))

fig, ax = plt.subplots()
plt.axis('equal')

line, = ax.plot(x, y, color='blue')
centre, = ax.plot(0, 0, marker='.', color='green')
cyclogon, = ax.plot(0, 0, color='blue')
triangle, = ax.plot(0, 0, color='green')
radius, = ax.plot(0, 0, color='green')

cyclogon_x = []
cyclogon_y = []


def animate(i):
    xi = x[i]
    yi = y[i]

    aa = xi / divider
    addx_a = centre_to_a * np.sin(aa)
    addy_a = centre_to_a * np.cos(aa)

    bb = xi / divider + alfa_inside
    addx_b = centre_to_b * np.sin(bb)
    addy_b = centre_to_b * np.cos(bb)

    cc = xi / divider + alfa_inside + beta_inside
    addx_c = centre_to_c * np.sin(cc)
    addy_c = centre_to_c * np.cos(cc)

    v1x = addx_a + xi
    v1y = addy_a + yi

    v2x = addx_b + xi
    v2y = addy_b + yi

    v3x = addx_c + xi
    v3y = addy_c + yi

    # moving the triangle so it stays above the line
    if v1y < v2y and v1y < v3y:
        moved = abs(v1y)
    elif v2y < v1y and v2y < v3y:
        moved = abs(v2y)
    elif v3y < v2y and v3y < v1y:
        moved = abs(v3y)
    else:
        moved = abs(v1y)

    coord_cen_x = (v1x + v2x + v3x) / 3
    coord_cen_y = (v1y + v2y + v3y) / 3

    centre.set_xdata(coord_cen_x)
    centre.set_ydata(coord_cen_y + moved)

    if medium == b:
        vx = v1x
        vy = v1y
    elif medium == a:
        vx = v3x
        vy = v3y
    elif medium == c:
        vx = v2x
        vy = v2y
    else:
        vx = v1x
        vy = v1y

    cyclogon_x.append(vx)
    cyclogon_y.append(vy + moved)
    cyclogon.set_xdata(cyclogon_x)
    cyclogon.set_ydata(cyclogon_y)

    triangle.set_data([v1x, v2x, v3x, v1x], [v1y + moved, v2y + moved, v3y + moved, v1y + moved])

    radius.set_data([coord_cen_x, vx], [coord_cen_y + moved, vy + moved])

    return triangle, radius, cyclogon, centre


animation = FuncAnimation(fig, func=animate, frames=le_y, interval=1, repeat=False)

plt.show()
