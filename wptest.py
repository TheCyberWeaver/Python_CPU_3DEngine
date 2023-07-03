# Import warp and numpy
import warp as wp
from PIL import Image
import numpy as np

# Initialize warp
wp.init()

# Define the coordinates of the two points
x1 = 100 # x-coordinate of the first point
y1 = 200 # y-coordinate of the first point
x2 = 500 # x-coordinate of the second point
y2 = 400 # y-coordinate of the second point

# Define the color of the line (red, green, blue)
color = (255, 0, 0)

# Define a kernel function that draws a line on the screen
@wp.kernel
def draw_line(screen: wp.array(dtype=wp.vec3), x1: int, y1: int, x2: int, y2: int, color: wp.vec3):
    # Get the thread index
    tid = wp.tid()
    # Get the screen width and height
    width = screen.shape[0]
    height = screen.shape[1]
    # Get the x and y coordinates of the current pixel
    x = tid % width
    y = tid // width
    # Check if the pixel is on the line using Bresenham's algorithm
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    e2 = 0
    while True:
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
        if x == x2 and y == y2:
            break
    # If the pixel is on the line, set its color to the given color
    if x == tid % width and y == tid // width:
        screen[tid] = color

# Create a screen of size 800x600 as a warp array of vec3 values
screen = wp.zeros((800, 600), dtype=wp.vec3)

# Launch the kernel function with the screen and the line parameters as inputs
wp.launch(kernel=draw_line, dim=screen.size, inputs=[screen, x1, y1, x2, y2, color])

# Convert the screen array to a numpy array of uint8 values
screen_np = np.array(screen, dtype=np.uint8)

# Save the screen array as an image file using PIL or any other library

img = Image.fromarray(screen_np, mode="RGB")
img.save("line.png")