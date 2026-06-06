import streamlit as st
import subprocess
import os

st.set_page_config(
    page_title="Physics-Based LiDAR Digital Twin",
    layout="wide"
)

st.title(
    "Physics-Based LiDAR Digital Twin"
)

st.write(
    "Terrain Mapping and Environmental Simulation"
)

if st.button("Run Simulation"):

    with st.spinner("Running LiDAR Simulation..."):

        subprocess.run(
            ["python3", "main.py"]
        )

    st.success(
        "Point Cloud Generated Successfully"
    )

    if os.path.exists(
        "final_complete_lidar_scan.pcd"
    ):

        with open(
            "final_complete_lidar_scan.pcd",
            "rb"
        ) as f:

            st.download_button(
                "Download Point Cloud",
                f,
                file_name="final_complete_lidar_scan.pcd"
            )

    if os.path.exists(
        "slam_ready_map.pcd"
    ):

        with open(
            "slam_ready_map.pcd",
            "rb"
        ) as f:

            st.download_button(
                "Download SLAM Map",
                f,
                file_name="slam_ready_map.pcd"
            )

    if os.path.exists(
        "surface_fitted_cloud.pcd"
    ):

        with open(
            "surface_fitted_cloud.pcd",
            "rb"
        ) as f:

            st.download_button(
                "Download Surface Fitted Cloud",
                f,
                file_name="surface_fitted_cloud.pcd"
            )

st.header("Project Details")

st.write("""
### Features

- Terrain Generation from Heightmap
- Time-of-Flight (ToF) LiDAR Simulation
- Atmospheric Attenuation
- Fog Simulation
- Rain Simulation
- Dust Simulation
- Sunlight Interference
- Sensor Noise Injection
- Phantom Returns
- Multipath Reflections
- Surface Normal Estimation
- SLAM Ready Map Generation
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Output Files",
        "3"
    )

with col2:
    st.metric(
        "Environment",
        "Terrain + Forest"
    )

with col3:
    st.metric(
        "Sensor",
        "LiDAR"
    )
