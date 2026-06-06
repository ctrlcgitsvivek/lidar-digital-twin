import numpy as np
from PIL import Image
from config import *

# ==========================================
# LOAD TERRAIN
# ==========================================

def generate_terrain():

    img = Image.open(
        "heightmap.png"
    ).convert("L")

    height_data = np.array(
        img
    ).astype(np.float32)

    # NORMALIZE

    height_data = (
        height_data - height_data.min()
    ) / (
        height_data.max() - height_data.min()
    )

    # SMOOTH TERRAIN

    for _ in range(8):

        height_data = (

            np.roll(height_data, 1, axis=0) +

            np.roll(height_data, -1, axis=0) +

            np.roll(height_data, 1, axis=1) +

            np.roll(height_data, -1, axis=1) +

            height_data

        ) / 5.0

    # REDUCE RESOLUTION

    height_data = height_data[::2, ::2]

    rows, cols = height_data.shape

    terrain_points = []

    terrain_colors = []

    # GENERATE POINTS

    for i in range(rows):

        for j in range(cols):

            x = i * GRID_SCALE

            y = j * GRID_SCALE

            z = (
                height_data[i, j]
                * TERRAIN_HEIGHT
            )

            terrain_points.append([
                x,
                y,
                z
            ])

            terrain_colors.append([
                0,
                0.7,
                0
            ])

    return (

        np.array(terrain_points),

        np.array(terrain_colors),

        height_data,

        rows,

        cols

    )