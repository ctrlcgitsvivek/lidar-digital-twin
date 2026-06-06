import numpy as np
from config import *

# ==========================================
# ROTATING LIDAR SCAN
# ==========================================

def generate_lidar_rays():

    rays = []

    # FULL ROTATION

    yaw_angles = np.arange(

        0,

        360,

        ANGULAR_RESOLUTION

    )

    # VERTICAL CHANNELS

    pitch_angles = np.linspace(

        -FOV_VERTICAL / 2,

        FOV_VERTICAL / 2,

        32

    )

    # ==========================================
    # ROTATING SCAN
    # ==========================================

    for yaw in yaw_angles:

        for pitch in pitch_angles:

            yaw_rad = np.radians(yaw)

            pitch_rad = np.radians(pitch)

            # DIRECTION VECTOR

            direction = np.array([

                np.cos(pitch_rad)
                * np.cos(yaw_rad),

                np.cos(pitch_rad)
                * np.sin(yaw_rad),

                np.sin(pitch_rad)

            ])

            direction = (
                direction /
                np.linalg.norm(direction)
            )

            # ==========================================
            # BEAM DIVERGENCE
            # ==========================================

            divergence = np.random.normal(

                0,

                BEAM_DIVERGENCE * 0.001,

                3

            )

            direction += divergence

            direction = (
                direction /
                np.linalg.norm(direction)
            )

            rays.append(direction)

    return np.array(rays)

# ==========================================
# MEMS OSCILLATION PATTERN
# ==========================================

def generate_mems_pattern(num_points=5000):

    rays = []

    t = np.linspace(0, 20, num_points)

    for k in t:

        yaw = 60 * np.sin(2 * k)

        pitch = 20 * np.sin(3 * k)

        yaw_rad = np.radians(yaw)

        pitch_rad = np.radians(pitch)

        direction = np.array([

            np.cos(pitch_rad)
            * np.cos(yaw_rad),

            np.cos(pitch_rad)
            * np.sin(yaw_rad),

            np.sin(pitch_rad)

        ])

        direction = (
            direction /
            np.linalg.norm(direction)
        )

        rays.append(direction)

    return np.array(rays)