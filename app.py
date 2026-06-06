import streamlit as st
import subprocess
import os

st.title("Physics-Based LiDAR Digital Twin")

st.write(
    "Terrain Mapping and Environmental Simulation"
)

if st.button("Run Simulation"):

    result = subprocess.run(
        ["python", "main.py"],
        capture_output=True,
        text=True
    )

    st.text(result.stdout)

    if os.path.exists(
        "final_complete_lidar_scan.pcd"
    ):
        st.success(
            "Point Cloud Generated Successfully"
        )