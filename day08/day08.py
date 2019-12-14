from typing import Dict, List
from collections import Counter
import copy

Image = List[List[List[int]]]


def parse_image(raw: str, width: int, height: int) -> Image:
    pixels = [int(c) for c in raw]

    num_layers = len(pixels) // width // height

    image = [
        [
            [None for _ in range(width)]
            for _ in range(height)
        ]
        for _ in range(num_layers)
    ]

    layer = i = j = 0

    for pixel in pixels:
        image[layer][i][j] = pixel

        j += 1
        
        if j == width:
            j = 0
            i += 1

        if i == height:
            i = 0
            layer += 1

    return image


RAW = "123456789012"
IMAGE = parse_image(RAW, 3, 2)
assert IMAGE == [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]]


def count_colors(image: Image) -> List[Dict[int, int]]:
    return [
        Counter(pixel for row in layer for pixel in row)
        for layer in image
    ]

def one_times_two(image: Image) -> int:
    color_counts = count_colors(image)
    layer_counts = min(color_counts, key=lambda cc: cc[0])
    return layer_counts[1] * layer_counts[2]


assert one_times_two(IMAGE) == 1

with open('day08.txt') as f:
    raw = f.read().strip()

image = parse_image(raw, width=25, height=6)

# print(one_times_two(image))

def show(image: Image) -> None:
    consolidated = copy.deepcopy(image[0])
    num_layers = len(image)
    height = len(image[0])
    width = len(image[0][0])

    for i in range(height):
        for j in range(width):
            for layer in range(num_layers):
                color = image[layer][i][j]
                if color == 0:
                    consolidated[i][j] = ' '
                    break
                elif color == 1:
                    consolidated[i][j] = '*'
                    break

    for row in consolidated:
        print("".join(row))

RAW2 = "0222112222120000"
IMAGE2 = parse_image(RAW2, 2, 2)

# show(IMAGE2)

show(image)