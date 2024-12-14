# pyorbital.py
""" Main file containing the main function"""
import calculation as cc
from data import PLANETARY_MU, PLANETARY_RADII


def get_body_parameters():
    """Retrieve selected body data
    Args:1

    Returns:
        float: Gravitational parameter (km^3/s^2).
        float: Body Radius (km).
    """
    print("Select a planetary body:")
    for i, body in enumerate(PLANETARY_MU.keys(), start=1):
        print(f"{i}. {body}")
    choice = int(input("Enter the number corresponding to the body: "))
    body_name = list(PLANETARY_MU.keys())[choice - 1]
    return PLANETARY_MU[body_name], PLANETARY_RADII[body_name]


def main():
    print("__________Orbital Mechanics Calculator__________")
    print("Choose a calculation:")
    print("1. Orbital Velocity")
    print("2. Orbital Period")
    print("3. Escape Velocity")
    print("4. Specific Orbital Energy")
    print("5. Hohmann Transfer Delta-V")
    print("6. Eccentricity")
    print("7. Swath Width")
    print("8. Plane Change Delta-V")
    print("________________________________________________")

    choice = int(input("Enter the number of your choice: "))

    if choice == 1:
        mu, radius = get_body_parameters()
        r = float(
            input(
                "Enter the orbital radius from the center of the body [km] \
                (or altitude above surface [km]): "
            )
        )
        use_altitude = (
            input("Did you enter an altitude? (yes/no): ").strip().lower() == "yes"
        )
        if use_altitude:
            r += radius
        velocity = cc.orbital_velocity(mu, r)
        print(f"Orbital velocity: {velocity:.2f} km/s")

    elif choice == 2:
        mu, radius = get_body_parameters()
        a = float(
            input("Enter the semi-major axis [km] (or altitude above surface [km]): ")
        )
        use_altitude = (
            input("Did you enter an altitude? (yes/no): ").strip().lower() == "yes"
        )
        if use_altitude:
            a += radius
        period = cc.orbital_period(mu, a)
        print(f"Orbital period: {period:.2f} seconds")

    elif choice == 3:
        mu, radius = get_body_parameters()
        r = float(
            input(
                "Enter the distance from the center of the body [km]\
                  (or altitude above surface [km]): "
            )
        )
        use_altitude = (
            input("Did you enter an altitude? (yes/no): ").strip().lower() == "yes"
        )
        if use_altitude:
            r += radius
        velocity = cc.escape_velocity(mu, r)
        print(f"Escape velocity: {velocity:.2f} km/s")

    elif choice == 4:
        mu, radius = get_body_parameters()
        r = float(
            input("Enter the orbital radius [km] (or altitude above surface [km]): ")
        )
        use_altitude = (
            input("Did you enter an altitude? (yes/no): ").strip().lower() == "yes"
        )
        if use_altitude:
            r += radius
        v = float(input("Enter the orbital velocity [km/s]: "))
        energy = cc.specific_orbital_energy(mu, r, v)
        print(f"Specific orbital energy: {energy:.2f} km^2/s^2")

    elif choice == 5:
        mu, radius = get_body_parameters()
        r1 = float(
            input(
                "Enter the radius of the initial orbit [km] (or altitude above surface [km]): "
            )
        )
        use_altitude1 = (
            input("Did you enter an altitude for the initial orbit? (yes/no): ")
            .strip()
            .lower()
            == "yes"
        )
        if use_altitude1:
            r1 += radius
        r2 = float(
            input(
                "Enter the radius of the final orbit [km] (or altitude above surface [km]): "
            )
        )
        use_altitude2 = (
            input("Did you enter an altitude for the final orbit? (yes/no): ")
            .strip()
            .lower()
            == "yes"
        )
        if use_altitude2:
            r2 += radius
        delta_v1, delta_v2 = cc.hohmann_transfer_delta_v(mu, r1, r2)
        print(f"Hohmann transfer delta-v1: {delta_v1:.2f} km/s")
        print(f"Hohmann transfer delta-v2: {delta_v2:.2f} km/s")

    elif choice == 6:
        mu, radius = get_body_parameters()
        r1 = float(
            input(
                "Enter the radius of the periapsis [km] (or altitude above surface at periapsis [km]): "
            )
        )
        use_altitude1 = (
            input("Did you enter an altitude ? (yes/no): ").strip().lower() == "yes"
        )
        if use_altitude1:
            r1 += radius
        r2 = float(
            input(
                "Enter the radius of the apoapsis [km] (or altitude above surface at apoapsis [km]): "
            )
        )
        use_altitude2 = (
            input("Did you enter an altitude ? (yes/no): ").strip().lower() == "yes"
        )
        if use_altitude2:
            r2 += radius
        ecc = cc.eccentricity(r1, r2)
        print(f"Eccentricity: {ecc:.2f}")

    elif choice == 7:
        altitude = float(input("Enter the satellite altitude [km]: "))
        fov = float(input("Enter the field of view [degrees]: "))
        swath = cc.swath_width(altitude, fov)
        print(f"Swath width: {swath:.2f} km")

    elif choice == 8:
        v = float(input("Enter the orbital velocity [km/s]: "))
        delta_i = float(input("Enter the inclination change [degrees]: "))
        delta_v = cc.plane_change_delta_v(v, delta_i)
        print(f"Delta-V for plane change: {delta_v:.2f} km/s")

    else:
        print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
