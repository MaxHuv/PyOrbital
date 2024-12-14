# test_complete.py
import pytest
import math
from unittest.mock import patch
from src.pyorbital.pyorbital import main
from src.pyorbital.calculation import (
    orbital_velocity,
    orbital_period,
    escape_velocity,
    specific_orbital_energy,
    hohmann_transfer_delta_v,
    revisit_time,
    swath_width,
    plane_change_delta_v
)
from src.pyorbital.data import PLANETARY_MU, PLANETARY_RADII

# Constants for testing
MU_EARTH = 398600.4418  # Gravitational parameter for Earth (km^3/s^2)
R_EARTH = 6371.0  # Radius of Earth (km)

# Test cases for calculation.py
@pytest.mark.parametrize("mu, r, expected", [
    (MU_EARTH, R_EARTH + 500, 7.612),  # Low Earth Orbit (500 km altitude)
    (MU_EARTH, R_EARTH + 20000, 3.879)  # Medium Earth Orbit (20,000 km altitude)
])
def test_orbital_velocity(mu, r, expected):
    assert math.isclose(orbital_velocity(mu, r), expected, rel_tol=1e-3)

@pytest.mark.parametrize("mu, a, expected", [
    (MU_EARTH, R_EARTH + 500, 5828),  # Low Earth Orbit
    (MU_EARTH, R_EARTH + 20000, 43081)  # Medium Earth Orbit
])
def test_orbital_period(mu, a, expected):
    assert math.isclose(orbital_period(mu, a), expected, rel_tol=1e-2)

@pytest.mark.parametrize("mu, r, expected", [
    (MU_EARTH, R_EARTH, 11.186),  # Surface of Earth
    (MU_EARTH, R_EARTH + 500, 10.764)  # Low Earth Orbit
])
def test_escape_velocity(mu, r, expected):
    assert math.isclose(escape_velocity(mu, r), expected, rel_tol=1e-3)

@pytest.mark.parametrize("mu, r, v, expected", [
    (MU_EARTH, R_EARTH + 500, 7.612, -29.3),  # Low Earth Orbit
    (MU_EARTH, R_EARTH + 20000, 3.879, -19.9)  # Medium Earth Orbit
])
def test_specific_orbital_energy(mu, r, v, expected):
    assert math.isclose(specific_orbital_energy(mu, r, v), expected, rel_tol=1e-1)

@pytest.mark.parametrize("mu, r1, r2, expected1, expected2", [
    (MU_EARTH, R_EARTH + 500, R_EARTH + 35786, 3.927, 1.630),  # LEO to GEO
    (MU_EARTH, R_EARTH + 20000, R_EARTH + 35786, 0.735, 1.022)  # MEO to GEO
])
def test_hohmann_transfer_delta_v(mu, r1, r2, expected1, expected2):
    delta_v1, delta_v2 = hohmann_transfer_delta_v(mu, r1, r2)
    assert math.isclose(delta_v1, expected1, rel_tol=1e-3)
    assert math.isclose(delta_v2, expected2, rel_tol=1e-3)

@pytest.mark.parametrize("period, omega, expected", [
    (5828, 7.2921e-5, 86400),  # Earth rotation period
    (43081, 7.2921e-5, 432000)  # 5 days
])
def test_revisit_time(period, omega, expected):
    assert math.isclose(revisit_time(period, omega), expected, rel_tol=1e-2)

@pytest.mark.parametrize("altitude, fov, expected", [
    (500, 30, 267.95),  # LEO with 30-degree FOV
    (20000, 10, 698.13)  # MEO with 10-degree FOV
])
def test_swath_width(altitude, fov, expected):
    assert math.isclose(swath_width(altitude, fov), expected, rel_tol=1e-2)

@pytest.mark.parametrize("v, delta_i, expected", [
    (7.612, 30, 3.946),  # LEO, 30-degree inclination change
    (3.879, 10, 1.349)  # MEO, 10-degree inclination change
])
def test_plane_change_delta_v(v, delta_i, expected):
    assert math.isclose(plane_change_delta_v(v, delta_i), expected, rel_tol=1e-3)

# Test cases for data.py
def test_data_integrity():
    assert PLANETARY_MU["Earth"] == 398600.4418
    assert PLANETARY_RADII["Earth"] == 6371.0
    assert "Mars" in PLANETARY_MU
    assert "Jupiter" in PLANETARY_RADII

# Test cases for pyorbital.py (integration test)
@patch("builtins.input", side_effect=["Earth", "altitude", "500"])
def test_pyorbital_integration(mock_input):
    with patch("builtins.print") as mock_print:
        main()
        assert mock_print.called
        output = "\n".join(call.args[0] for call in mock_print.call_args_list)
        assert "Orbital velocity" in output
        assert "Orbital period" in output
        assert "Escape velocity" in output

if __name__ == "__main__":
    pytest.main()
