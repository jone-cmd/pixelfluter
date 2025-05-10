from PIL import Image
import sys
import numpy as np
import random

commands = []

with Image.open(sys.argv[1]) as image:
    array = np.asarray(image)
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
        command = f"PX {j} {i} {hex_color}"
        commands.append(command)
random.shuffle(commands)
for command in commands:
    print(command)
