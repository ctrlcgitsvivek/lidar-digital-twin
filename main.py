import open3d as o3d
import numpy as np

from terrain import generate_terrain

from lidar_sensor import (
    generate_lidar_rays,
    generate_mems_pattern
)

from tof_model import (

    calculate_tof,
    calculate_intensity,
    atmospheric_attenuation,
    material_reflectivity,
    generate_phantom_point,
    multipath_reflection

)

from atmosphere import (

    apply_fog,
    apply_rain,
    apply_dust,
    apply_sunlight,
    add_noise,
    visibility_check

)

from config import *

# ==========================================
# LOAD TERRAIN
# ==========================================

print("Loading terrain...")

terrain_points, terrain_colors, height_data, rows, cols = generate_terrain()

# ==========================================
# GENERATE SENSOR PATTERNS
# ==========================================

print("Generating LiDAR scan patterns...")

rays = generate_lidar_rays()
mems_rays = generate_mems_pattern()

# ==========================================
# STORAGE
# ==========================================

final_points = []
final_colors = []

# ==========================================
# MAIN SIMULATION
# ==========================================

print("Running physics-based LiDAR simulation...")

# ==========================================
# FINAL REALISTIC SCAN SETTINGS
# ==========================================

sample_step = 3

for idx, point in enumerate(terrain_points):

    x, y, z = point

    # ==========================================
    # REALISTIC SCANLINE STRUCTURE
    # ==========================================

    scan_band = int(y * 2)

    if scan_band % 2 != 0:
        continue

    # ==========================================
    # SPARSE BEAM SAMPLING
    # ==========================================

    if idx % sample_step != 0:
        continue

    # ==========================================
    # DISTANCE
    # ==========================================

    distance = np.linalg.norm(point)

    # ==========================================
    # SENSOR RANGE LIMIT
    # ==========================================

    if distance > MAX_RANGE:
        continue

    # ==========================================
    # DROPPED RETURNS
    # ==========================================

    drop_probability = 0.05

    distance_factor = min(

        distance / MAX_RANGE,

        1.0

    )

    drop_probability += distance_factor * 0.15

    if np.random.rand() < drop_probability:
        continue

    # ==========================================
    # TIME OF FLIGHT
    # ==========================================

    tof = calculate_tof(distance)

    # ==========================================
    # MATERIAL REFLECTIVITY
    # ==========================================

    reflectivity = material_reflectivity(z)

    # ==========================================
    # LASER RETURN INTENSITY
    # ==========================================

    intensity = calculate_intensity(

        distance,

        reflectivity

    )

    # ==========================================
    # ATMOSPHERIC ATTENUATION
    # ==========================================

    intensity = atmospheric_attenuation(

        intensity,

        alpha=0.01,

        distance=distance

    )

    # ==========================================
    # FOG EFFECT
    # ==========================================

    intensity = apply_fog(

        intensity,

        distance,

        fog_density=0.035

    )

    # ==========================================
    # RAIN EFFECT
    # ==========================================

    intensity = apply_rain(

        intensity,

        distance,

        rain_density=0.01

    )

    # ==========================================
    # DUST EFFECT
    # ==========================================

    intensity = apply_dust(

        intensity,

        distance,

        dust_density=0.025

    )

    # ==========================================
    # SUNLIGHT INTERFERENCE
    # ==========================================

    intensity = apply_sunlight(

        intensity,

        sunlight_strength=0.03

    )

    # ==========================================
    # DETECTION THRESHOLD
    # ==========================================

    visible = visibility_check(

        intensity,

        threshold=DETECTION_THRESHOLD

    )

    if not visible:
        continue

    # ==========================================
    # SENSOR NOISE / CLOCK JITTER
    # ==========================================

    noisy_point = add_noise(

        point,

        sigma=0.03

    )

    final_points.append(noisy_point)

    # ==========================================
    # PHANTOM RETURNS
    # ==========================================

    if np.random.rand() < 0.008:

        phantom = generate_phantom_point(

            noisy_point

        )

        final_points.append(phantom)

        final_colors.append([1, 1, 0])

    # ==========================================
    # MULTIPATH REFLECTIONS
    # ==========================================

    if np.random.rand() < 0.008:

        reflected = multipath_reflection(

            noisy_point

        )

        final_points.append(reflected)

        final_colors.append([1, 0, 1])

    # ==========================================
    # SAFE ZONE DETECTION
    # ==========================================

    safe_zone = False

    ix = int(x / GRID_SCALE)
    iy = int(y / GRID_SCALE)

    if (

        ix > 2 and
        iy > 2 and
        ix < rows - 2 and
        iy < cols - 2

    ):

        local_patch = height_data[
            ix-2:ix+2,
            iy-2:iy+2
        ]

        variation = np.std(local_patch)

        if variation < 0.015:

            safe_zone = True

    # ==========================================
    # OBSTACLE DETECTION
    # ==========================================

    obstacle = False

    if z > TERRAIN_HEIGHT * 0.6:
        obstacle = True

    # ==========================================
    # FINAL COLORING
    # ==========================================

    if obstacle:

        color = [1, 0, 0]

    elif safe_zone:

        color = [0, 0.4, 1]

    else:

        color = [0, 0.7, 0]

    final_colors.append(color)

# ==========================================
# CONVERT ARRAYS
# ==========================================

final_points = np.array(final_points)
final_colors = np.array(final_colors)

# ==========================================
# CREATE POINT CLOUD
# ==========================================

pcd = o3d.geometry.PointCloud()

pcd.points = o3d.utility.Vector3dVector(
    final_points
)

pcd.colors = o3d.utility.Vector3dVector(
    final_colors
)

# ==========================================
# SAVE OUTPUT
# ==========================================

o3d.io.write_point_cloud(
    "final_complete_lidar_scan.pcd",
    pcd
)

print("Main point cloud saved")

# ==========================================
# SURFACE NORMAL ESTIMATION
# ==========================================

print("Estimating surface normals...")

pcd.estimate_normals(

    search_param=o3d.geometry.KDTreeSearchParamHybrid(

        radius=1.0,
        max_nn=30

    )

)

pcd.normalize_normals()

# ==========================================
# SAVE SURFACE FITTED CLOUD
# ==========================================

o3d.io.write_point_cloud(
    "surface_fitted_cloud.pcd",
    pcd
)

print("Surface fitting completed")

# ==========================================
# SLAM READY MAP
# ==========================================

slam_downsampled = pcd.voxel_down_sample(
    voxel_size=0.3
)

o3d.io.write_point_cloud(
    "slam_ready_map.pcd",
    slam_downsampled
)

print("SLAM-ready map exported")

# ==========================================
# METRICS
# ==========================================

print("\n========== SIMULATION METRICS ==========\n")

print(f"Total Final Points : {len(final_points)}")

print("\n========================================\n")

# ==========================================
# VISUALIZATION
# ==========================================

o3d.visualization.draw_geometries(

    [pcd],

    window_name="Physics-Based 3D LiDAR Digital Twin"

)