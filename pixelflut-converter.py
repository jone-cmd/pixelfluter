from PIL import Image
import sys
import numpy as np
import random

commands = []

with Image.open(sys.argv[1]) as image:
    array = np.asarray(image) # Convert image to 3-dimensional numpy array
for i, child in enumerate(array):
    for j, color in enumerate(child):
        try:
            if color[3] == 0:
                continue
        except IndexError:
            pass
        hex_color = "%02x%02x%02x" % tuple(
            color[:3]
        )  # https://stackoverflow.com/a/3380739
        command = f"PX {j} {i} {hex_color}" # Build the command
        commands.append(command) # Save the command
random.shuffle(commands) # Shuffle the commands to avoid sending them from top to bottom
for command in commands:
    print(command) # Print the commands to stdout
