import random
import sys
from typing import Iterable

import numpy as np
from PIL import Image


def all_chars_same(interable: Iterable) -> bool:
    """
    Check if all items in the interable are the same.
    For example, '000000' or 'ffffff' returns True, but '123456' returns False.
    """
    return len(set(interable)) == 1


def convert_subimage(pixels: list[tuple[int, int, tuple[int, int, int]]]) -> list[str]:
    commands = []
    for x, y, color in pixels:
        try:
            if color[3] == 0:
                continue
        except IndexError:
            pass
        hex_color = "%02x%02x%02x" % tuple(
            color[:3]
        )  # https://stackoverflow.com/a/3380739
        if all_chars_same(hex_color):
            hex_color = hex_color[0] * 2
        command = f"PX {x} {y} {hex_color}"
        commands.append(command)
    random.shuffle(commands)
    return commands


def convert_image(image_path):
    with Image.open(image_path) as image:
        array = np.asarray(image)
    commands = []
    commands += convert_subimage([(x, y, tuple(array[y][x])) for y in range(
        0, array.shape[0], 2) for x in range(0, array.shape[1], 2)])
    commands += convert_subimage([(x, y, tuple(array[y][x])) for y in range(
        1, array.shape[0], 2) for x in range(0, array.shape[1], 2)])
    commands += convert_subimage([(x, y, tuple(array[y][x])) for y in range(
        0, array.shape[0], 2) for x in range(1, array.shape[1], 2)])
    commands += convert_subimage([(x, y, tuple(array[y][x])) for y in range(
        1, array.shape[0], 2) for x in range(1, array.shape[1], 2)])
    for command in commands:
        print(command)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python pixelflut-converter.py <image_path> [<image_path> ...] > actions.txt")
        sys.exit(1)

    for image_path in sys.argv[1:]:
        convert_image(image_path)


if __name__ == "__main__":
    main()
