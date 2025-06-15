from PIL import Image
import sys
import numpy as np
import random

def covert_image(image_path):
    commands = []

    with Image.open(image_path) as image:
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python pixelflut-converter.py <image_path> [<image_path> ...] > actions.txt")
        sys.exit(1)

    for image_path in sys.argv[1:]:
        covert_image(image_path)

if __name__ == "__main__":
    main()
