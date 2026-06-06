import numpy as np

# SPEED OF LIGHT

C = 3e8

# ==========================================
# TIME OF FLIGHT
# ==========================================

def calculate_tof(distance):

    tof = (
        2 * distance
    ) / C

    return tof

# ==========================================
# MATERIAL REFLECTIVITY
# ==========================================

def material_reflectivity(z):

    # HIGHLY REFLECTIVE

    if z > 9:

        return 0.95

    # NORMAL TERRAIN

    elif z > 4:

        return 0.65

    # ABSORBING MATERIAL

    else:

        return 0.25

# ==========================================
# RETURN INTENSITY
# ==========================================

def calculate_intensity(

    distance,
    reflectivity

):

    intensity = (

        reflectivity /

        (distance ** 2 + 1)

    )

    return intensity

# ==========================================
# ATMOSPHERIC ATTENUATION
# ==========================================

def atmospheric_attenuation(

    intensity,
    alpha=0.01,
    distance=1

):

    attenuated = (

        intensity *

        np.exp(-alpha * distance)

    )

    return attenuated

# ==========================================
# PHANTOM RETURNS
# ==========================================

def generate_phantom_point(point):

    phantom = point.copy()

    phantom += np.random.normal(

        0,

        0.5,

        3

    )

    phantom[2] += np.random.uniform(

        0.5,

        2.0

    )

    return phantom

# ==========================================
# MULTIPATH REFLECTION
# ==========================================

def multipath_reflection(point):

    reflected = point.copy()

    reflected[0] += np.random.uniform(-1, 1)

    reflected[1] += np.random.uniform(-1, 1)

    reflected[2] *= 0.8

    return reflected