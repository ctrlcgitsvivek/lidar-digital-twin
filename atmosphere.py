import numpy as np

# ==========================================
# FOG EFFECT
# ==========================================

def apply_fog(

    intensity,
    distance,
    fog_density=0.02

):

    attenuation = np.exp(

        -fog_density * distance

    )

    return intensity * attenuation

# ==========================================
# RAIN EFFECT
# ==========================================

def apply_rain(

    intensity,
    distance,
    rain_density=0.01

):

    attenuation = np.exp(

        -rain_density * distance

    )

    return intensity * attenuation

# ==========================================
# DUST INTERFERENCE
# ==========================================

def apply_dust(

    intensity,
    distance,
    dust_density=0.015

):

    attenuation = np.exp(

        -dust_density * distance

    )

    random_scatter = np.random.uniform(

        0.85,
        1.0

    )

    return intensity * attenuation * random_scatter

# ==========================================
# SUNLIGHT INTERFERENCE
# ==========================================

def apply_sunlight(

    intensity,
    sunlight_strength=0.1

):

    noise = np.random.normal(

        0,

        sunlight_strength

    )

    return max(

        intensity - noise,

        0

    )

# ==========================================
# SENSOR NOISE
# ==========================================

def add_noise(

    point,
    sigma=0.03

):

    noise = np.random.normal(

        0,

        sigma,

        3

    )

    return point + noise

# ==========================================
# VISIBILITY CHECK
# ==========================================

def visibility_check(

    intensity,
    threshold=0.001

):

    return intensity > threshold