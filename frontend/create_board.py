from PIL import Image

WIDTH = 8
HEIGHT = 8

COLOR_1 = (118, 150, 86)
COLOR_2 = (238, 238, 210)

# Create new image of the board
img = Image.new('RGB', (WIDTH, HEIGHT))
pixels = img.load()

# Color the pixels
for i in range(WIDTH):
    for j in range(HEIGHT):
        if (i + j) % 2 == 1: # Odd pixels
            pixels[i, j] = COLOR_1
        else: # Even pixels
            pixels[i, j] = COLOR_2

# Resize the image to 1200 x 1200 pixels
SIZE = (1200, 1200)
img = img.resize(SIZE, Image.NEAREST)
img.save(f'src/assets/boards/{WIDTH}x/board_{WIDTH}x{HEIGHT}.png')
