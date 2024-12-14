# calculation.py
""" Module providing functions to make the calculations"""
import math


def orbital_velocity(mu, r):
    """Calculate the orbital velocity.
    Args:
        mu (float): Gravitational parameter (km^3/s^2).
        r (float): Orbital radius (km).
    Returns:
        float: Orbital velocity (km/s).
    """
    return math.sqrt(mu / r)


def orbital_period(mu, a):
    """Calculate the orbital period.
    Args:
        mu (float): Gravitational parameter (km^3/s^2).
        a (float): Semi-major axis (km).
    Returns:
        float: Orbital period (s).
    """
    return 2 * math.pi * math.sqrt(a**3 / mu)


def escape_velocity(mu, r):
    """Calculate the escape velocity.
    Args:
        mu (float): Gravitational parameter (km^3/s^2).
        r (float): Distance from the center of the body (km).
    Returns:
        float: Escape velocity (km/s).
    """
    return math.sqrt(2 * mu / r)


def specific_orbital_energy(mu, r, v):
    """Calculate the specific orbital energy.
    Args:
        mu (float): Gravitational parameter (km^3/s^2).
        r (float): Orbital radius (km).
        v (float): Orbital velocity (km/s).
    Returns:
        float: Specific orbital energy (km^2/s^2).
    """
    return (v**2 / 2) - (mu / r)


def hohmann_transfer_delta_v(mu, r1, r2):
    """Calculate the delta-V for a Hohmann transfer.
    Args:
        mu (float): Gravitational parameter (km^3/s^2).
        r1 (float): Radius of the initial orbit (km).
        r2 (float): Radius of the final orbit (km).
    Returns:
        tuple: Delta-V for the first and second burns (km/s).
    """
    a_transfer = (r1 + r2) / 2
    v1 = math.sqrt(mu / r1)
    v2 = math.sqrt(mu / r2)
    v_transfer1 = math.sqrt(2 * mu / r1 - mu / a_transfer)
    v_transfer2 = math.sqrt(2 * mu / r2 - mu / a_transfer)
    delta_v1 = v_transfer1 - v1
    delta_v2 = v2 - v_transfer2
    return delta_v1, delta_v2


def revisit_time(period, omega):
    """Calculate the revisit time.
    Args:
        period (float): Orbital period (s).
        omega (float): Angular velocity of the planet's rotation (rad/s).
    Returns:
        float: Revisit time (s).
    """
    return 2 * math.pi / abs(2 * math.pi / period - omega)


def swath_width(altitude, fov):
    """Calculate the swath width.
    Args:
        altitude (float): Satellite altitude (km).
        fov (float): Field of view (degrees).
    Returns:
        float: Swath width (km).
    """
    return 2 * altitude * math.tan(math.radians(fov / 2))


def plane_change_delta_v(v, delta_i):
    """Calculate the delta-V for a plane change.
    Args:
        v (float): Orbital velocity (km/s).
        delta_i (float): Inclination change (degrees).
    Returns:
        float: Delta-V required for the plane change (km/s).
    """
    return 2 * v * math.sin(math.radians(delta_i / 2))
