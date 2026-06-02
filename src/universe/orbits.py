from __future__ import annotations

from datetime import datetime, timezone
import math

import numpy as np

from .solar_data import AU_KM, J2000_JD, OrbitalElements, SimpleOrbit


def julian_day(moment: datetime) -> float:
    # 입력 시간이 timezone을 갖고 있지 않으면 UTC로 보고, 모든 계산 기준을 UTC로 맞춘다.
    # Julian day는 행성 위치 계산의 공통 시간 좌표라서 지역 시간 차이를 제거해야 한다.
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    moment = moment.astimezone(timezone.utc)

    year = moment.year
    month = moment.month
    day = moment.day + (
        moment.hour
        + moment.minute / 60.0
        + (moment.second + moment.microsecond / 1_000_000.0) / 3600.0
    ) / 24.0

    if month <= 2:
        year -= 1
        month += 12

    a = year // 100
    b = 2 - a + a // 4
    return (
        math.floor(365.25 * (year + 4716))
        + math.floor(30.6001 * (month + 1))
        + day
        + b
        - 1524.5
    )


def wrap_degrees(value: float) -> float:
    return (value + 180.0) % 360.0 - 180.0


def solve_kepler_radians(mean_anomaly_degrees: float, eccentricity: float, iterations: int = 12) -> float:
    # 평균 근점 이각으로부터 케플러 방정식을 풀어 이심 근점 이각을 구한다.
    # 타원 궤도 위치를 계산하려면 이 값이 필요하므로 Newton 반복으로 빠르게 수렴시킨다.
    mean_anomaly = math.radians(wrap_degrees(mean_anomaly_degrees))
    eccentric_anomaly = mean_anomaly if eccentricity < 0.8 else math.pi

    for _ in range(iterations):
        numerator = eccentric_anomaly - eccentricity * math.sin(eccentric_anomaly) - mean_anomaly
        denominator = 1.0 - eccentricity * math.cos(eccentric_anomaly)
        delta = numerator / denominator
        eccentric_anomaly -= delta
        if abs(delta) <= 1e-12:
            break

    return eccentric_anomaly


def elements_at(elements: OrbitalElements, jd: float) -> dict[str, float]:
    centuries = (jd - J2000_JD) / 36_525.0
    return {
        "a": elements.a + elements.a_rate * centuries,
        "e": elements.e + elements.e_rate * centuries,
        "inclination": elements.inclination + elements.inclination_rate * centuries,
        "mean_longitude": elements.mean_longitude + elements.mean_longitude_rate * centuries,
        "longitude_perihelion": elements.longitude_perihelion
        + elements.longitude_perihelion_rate * centuries,
        "longitude_node": elements.longitude_node + elements.longitude_node_rate * centuries,
        "centuries": centuries,
    }


def _rotate_orbital_plane(
    x_prime: float,
    y_prime: float,
    inclination_degrees: float,
    longitude_perihelion_degrees: float,
    longitude_node_degrees: float,
) -> np.ndarray:
    inclination = math.radians(inclination_degrees)
    longitude_node = math.radians(longitude_node_degrees)
    argument_perihelion = math.radians(longitude_perihelion_degrees - longitude_node_degrees)

    cos_omega = math.cos(argument_perihelion)
    sin_omega = math.sin(argument_perihelion)
    cos_node = math.cos(longitude_node)
    sin_node = math.sin(longitude_node)
    cos_i = math.cos(inclination)
    sin_i = math.sin(inclination)

    x_ecl = (
        (cos_omega * cos_node - sin_omega * sin_node * cos_i) * x_prime
        + (-sin_omega * cos_node - cos_omega * sin_node * cos_i) * y_prime
    )
    y_ecl = (
        (cos_omega * sin_node + sin_omega * cos_node * cos_i) * x_prime
        + (-sin_omega * sin_node + cos_omega * cos_node * cos_i) * y_prime
    )
    z_ecl = sin_omega * sin_i * x_prime + cos_omega * sin_i * y_prime
    return np.array([x_ecl, y_ecl, z_ecl], dtype=float)


def heliocentric_position_au(elements: OrbitalElements, jd: float) -> np.ndarray:
    # 현재 Julian day에 맞춰 공전 요소를 보정한 뒤 태양 중심 좌표를 계산한다.
    # 먼저 궤도면 안의 위치를 구하고, 이후 기울기/노드/근일점 경도를 반영해 3D 좌표로 회전한다.
    current = elements_at(elements, jd)
    centuries = current["centuries"]

    mean_anomaly = (
        current["mean_longitude"]
        - current["longitude_perihelion"]
        + elements.b * centuries * centuries
        + elements.c * math.cos(math.radians(elements.f * centuries))
        + elements.s * math.sin(math.radians(elements.f * centuries))
    )
    eccentric_anomaly = solve_kepler_radians(mean_anomaly, current["e"])
    x_prime = current["a"] * (math.cos(eccentric_anomaly) - current["e"])
    y_prime = current["a"] * math.sqrt(1.0 - current["e"] * current["e"]) * math.sin(eccentric_anomaly)

    return _rotate_orbital_plane(
        x_prime,
        y_prime,
        current["inclination"],
        current["longitude_perihelion"],
        current["longitude_node"],
    )


def orbital_path_au(elements: OrbitalElements, jd: float, samples: int = 256) -> np.ndarray:
    current = elements_at(elements, jd)
    path = []

    for eccentric_anomaly in np.linspace(0.0, math.tau, samples, endpoint=True):
        x_prime = current["a"] * (math.cos(eccentric_anomaly) - current["e"])
        y_prime = current["a"] * math.sqrt(1.0 - current["e"] * current["e"]) * math.sin(
            eccentric_anomaly
        )
        path.append(
            _rotate_orbital_plane(
                x_prime,
                y_prime,
                current["inclination"],
                current["longitude_perihelion"],
                current["longitude_node"],
            )
        )

    return np.array(path, dtype=float)


def simple_orbit_position_au(orbit: SimpleOrbit, elapsed_days: float) -> np.ndarray:
    mean_anomaly = orbit.phase_degrees + 360.0 * elapsed_days / orbit.orbital_period_days
    eccentric_anomaly = solve_kepler_radians(mean_anomaly, orbit.eccentricity)
    x_prime = orbit.semi_major_axis_au * (math.cos(eccentric_anomaly) - orbit.eccentricity)
    y_prime = (
        orbit.semi_major_axis_au
        * math.sqrt(1.0 - orbit.eccentricity * orbit.eccentricity)
        * math.sin(eccentric_anomaly)
    )

    inclination = math.radians(orbit.inclination_degrees)
    return np.array(
        [
            x_prime,
            y_prime * math.cos(inclination),
            y_prime * math.sin(inclination),
        ],
        dtype=float,
    )


def simple_orbit_path_au(orbit: SimpleOrbit, samples: int = 256) -> np.ndarray:
    path = []
    inclination = math.radians(orbit.inclination_degrees)
    for eccentric_anomaly in np.linspace(0.0, math.tau, samples, endpoint=True):
        x_prime = orbit.semi_major_axis_au * (math.cos(eccentric_anomaly) - orbit.eccentricity)
        y_prime = (
            orbit.semi_major_axis_au
            * math.sqrt(1.0 - orbit.eccentricity * orbit.eccentricity)
            * math.sin(eccentric_anomaly)
        )
        path.append([x_prime, y_prime * math.cos(inclination), y_prime * math.sin(inclination)])
    return np.array(path, dtype=float)


def moon_position_km(
    orbit_radius_km: float,
    orbital_period_days: float,
    elapsed_days: float,
    phase_degrees: float = 0.0,
    inclination_degrees: float = 0.0,
) -> np.ndarray:
    direction = -1.0 if orbital_period_days < 0.0 else 1.0
    period = abs(orbital_period_days)
    angle = math.radians(phase_degrees + direction * 360.0 * elapsed_days / period)
    inclination = math.radians(inclination_degrees)
    x = orbit_radius_km * math.cos(angle)
    y = orbit_radius_km * math.sin(angle) * math.cos(inclination)
    z = orbit_radius_km * math.sin(angle) * math.sin(inclination)
    return np.array([x, y, z], dtype=float)


def au_to_km(position_au: np.ndarray) -> np.ndarray:
    return position_au * AU_KM
