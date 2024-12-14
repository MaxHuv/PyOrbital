# test_complete.py
import pytest
import math
import sys
sys.path.insert(1, "./src")

from pyorbital import main
from calculation import (
    orbital_velocity,
    orbital_period,
    escape_velocity,
    specific_orbital_energy,
    hohmann_transfer_delta_v,
    eccentricity,
    swath_width,
    plane_change_delta_v
)
from data import PLANETARY_MU, PLANETARY_RADII
from unittest.mock import patch

# Constants for testing
MU_EARTH = 398600.4418  # Gravitational parameter for Earth (km^3/s^2)
R_EARTH = 6371.0  # Radius of Earth (km)

# Test cases for calculation.py
@pytest.mark.parametrize("mu, r, expected", [
    (MU_EARTH, R_EARTH + 500, 7.612),  # Low Earth Orbit (500 km altitude)
    (MU_EARTH, R_EARTH + 20000, 3.879)  # Medium Earth Orbit (20,000 km altitude)
])
def test_orbital_velocity(mu, r, expected):
    assert math.isclose(orbital_velocity(mu, r), expected, rel_tol=1e-2)

@pytest.mark.parametrize("mu, a, expected", [
    (MU_EARTH, R_EARTH + 500, 5668),  # Low Earth Orbit
    (MU_EARTH, R_EARTH + 20000, 42618)  # Medium Earth Orbit
])
def test_orbital_period(mu, a, expected):
    assert math.isclose(orbital_period(mu, a), expected, rel_tol=1e+1)

@pytest.mark.parametrize("mu, r, expected", [
    (MU_EARTH, R_EARTH, 11.186),  # Surface of Earth
    (MU_EARTH, R_EARTH + 500, 10.764)  # Low Earth Orbit
])
def test_escape_velocity(mu, r, expected):
    assert math.isclose(escape_velocity(mu, r), expected, rel_tol=1e-1)

@pytest.mark.parametrize("mu, r, v, expected", [
    (MU_EARTH, R_EARTH + 500, 7.612, -29.0),  # Low Earth Orbit
    (MU_EARTH, R_EARTH + 20000, 3.879, -7.56)  # Medium Earth Orbit
])
def test_specific_orbital_energy(mu, r, v, expected):
    assert math.isclose(specific_orbital_energy(mu, r, v), expected, rel_tol=1e-1)

@pytest.mark.parametrize("mu, r1, r2, expected1, expected2", [
    (MU_EARTH, R_EARTH + 500, R_EARTH + 35786, 2.37, 1.440),  # LEO to GEO
    (MU_EARTH, R_EARTH + 20000, R_EARTH + 35786, 0.425, 0.377)  # MEO to GEO
])
def test_hohmann_transfer_delta_v(mu, r1, r2, expected1, expected2):
    delta_v1, delta_v2 = hohmann_transfer_delta_v(mu, r1, r2)
    assert math.isclose(delta_v1, expected1, rel_tol=1e-1)
    assert math.isclose(delta_v2, expected2, rel_tol=1e-1)

@pytest.mark.parametrize("periapsis, apoapsis, expected", [
    (R_EARTH + 500, R_EARTH + 35786, 0.72),  # Earth rotation period
    (R_EARTH + 1000, R_EARTH + 40000, 0.72)  # 5 days
])
def test_eccentricity(periapsis, apoapsis, expected):
    assert math.isclose(eccentricity(periapsis, apoapsis), expected, rel_tol=1e-2)

@pytest.mark.parametrize("altitude, fov, expected", [
    (500, 30, 267.95),  # LEO with 30-degree FOV
    (20000, 10, 3500)  # MEO with 10-degree FOV
])
def test_swath_width(altitude, fov, expected):
    assert math.isclose(swath_width(altitude, fov), expected, rel_tol=1e-2)

@pytest.mark.parametrize("v, delta_i, expected", [
    (7.612, 30, 3.94),  # LEO, 30-degree inclination change
    (3.879, 10, 0.677)  # MEO, 10-degree inclination change
])
def test_plane_change_delta_v(v, delta_i, expected):
    assert math.isclose(plane_change_delta_v(v, delta_i), expected, rel_tol=1e-2)

# Test cases for data.py
def test_data_integrity():
    assert PLANETARY_MU["Earth"] == 398600.4418
    assert PLANETARY_RADII["Earth"] == 6371.0
    assert "Mars" in PLANETARY_MU
    assert "Jupiter" in PLANETARY_RADII


# Mocking a valid selection for Earth (index 1) and an altitude of 500 km
@patch("builtins.input", side_effect=["1", "1", "500", "yes"])  # Orbital Velocity
@patch("builtins.print")
def test_orbital_velocity(mock_print, mock_input):
    main()
    output = "\n".join(call.args[0] for call in mock_print.call_args_list)
    assert "Orbital velocity" in output
    assert "7.62 km/s" in output  

@patch("builtins.input", side_effect=["2", "1", "500", "yes"])  # Orbital Period
@patch("builtins.print")
def test_orbital_period(mock_print, mock_input):
    main()
    output = "\n".join(call.args[0] for call in mock_print.call_args_list)
    assert "Orbital period" in output
    assert "5668.14 seconds" in output  

@patch("builtins.input", side_effect=["3", "1", "6371", "no"])  # Escape Velocity
@patch("builtins.print")
def test_escape_velocity(mock_print, mock_input):
    main()
    output = "\n".join(call.args[0] for call in mock_print.call_args_list)
    assert "Escape velocity" in output
    assert "11.19 km/s" in output  

@patch("builtins.input", side_effect=["4", "1", "500", "yes", "7.8"])  # Specific Orbital Energy
@patch("builtins.print")
def test_specific_orbital_energy(mock_print, mock_input):
    main()
    output = "\n".join(call.args[0] for call in mock_print.call_args_list)
    assert "Specific orbital energy: -27.59 km^2/s^2" in output

@patch("builtins.input", side_effect=["5", "1", "500", "yes", "35786", "yes"])  # Hohmann Transfer Delta V
@patch("builtins.print")
def test_hohmann_transfer(mock_print, mock_input):
    main()
    output = "\n".join(call.args[0] for call in mock_print.call_args_list)
    assert "Hohmann transfer delta-v1: 2.37 km/s" in output
    assert "Hohmann transfer delta-v2: 1.45 km/s" in output

@patch("builtins.input", side_effect=["7", "500", "30"])  # Swath Width
@patch("builtins.print")
def test_swath_width(mock_print, mock_input):
    main()
    output = "\n".join(call.args[0] for call in mock_print.call_args_list)
    assert "Swath width: 267.95 km" in output
    
if __name__ == "__main__":
    pytest.main()
