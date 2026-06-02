from __future__ import annotations

from dataclasses import dataclass


AU_KM = 149_597_870.7
EARTH_RADIUS_KM = 6_371.0084
SUN_MASS_KG = 1.9885e30
J2000_JD = 2_451_545.0


@dataclass(frozen=True)
class OrbitalElements:
    a: float
    a_rate: float
    e: float
    e_rate: float
    inclination: float
    inclination_rate: float
    mean_longitude: float
    mean_longitude_rate: float
    longitude_perihelion: float
    longitude_perihelion_rate: float
    longitude_node: float
    longitude_node_rate: float
    b: float = 0.0
    c: float = 0.0
    s: float = 0.0
    f: float = 0.0


@dataclass(frozen=True)
class SimpleOrbit:
    semi_major_axis_au: float
    eccentricity: float
    inclination_degrees: float
    orbital_period_days: float
    phase_degrees: float = 0.0


@dataclass(frozen=True)
class RingSpec:
    inner_radius_multiple: float
    outer_radius_multiple: float
    rgba: tuple[int, int, int, int]


@dataclass(frozen=True)
class BodySpec:
    key: str
    name: str
    kind: str
    radius_km: float
    mass_kg: float
    rotation_period_days: float
    color_rgb: tuple[int, int, int]
    axis_tilt_degrees: float = 0.0
    orbital_elements: OrbitalElements | None = None
    simple_orbit: SimpleOrbit | None = None
    ring: RingSpec | None = None
    atmosphere_rgba: tuple[int, int, int, int] | None = None


@dataclass(frozen=True)
class MoonSpec:
    key: str
    name: str
    parent_key: str
    radius_km: float
    mass_kg: float
    orbit_radius_km: float
    orbital_period_days: float
    color_rgb: tuple[int, int, int]
    phase_degrees: float = 0.0
    inclination_degrees: float = 0.0


SUN = BodySpec(
    key="sun",
    name="Sun",
    kind="star",
    radius_km=695_700.0,
    mass_kg=SUN_MASS_KG,
    rotation_period_days=25.38,
    color_rgb=(255, 213, 91),
    axis_tilt_degrees=7.25,
)


PLANETS: tuple[BodySpec, ...] = (
    BodySpec(
        key="mercury",
        name="Mercury",
        kind="planet",
        radius_km=2_439.4,
        mass_kg=0.330103e24,
        rotation_period_days=58.6462,
        color_rgb=(153, 143, 132),
        axis_tilt_degrees=0.034,
        orbital_elements=OrbitalElements(
            0.38709927,
            0.00000037,
            0.20563593,
            0.00001906,
            7.00497902,
            -0.00594749,
            252.25032350,
            149472.67411175,
            77.45779628,
            0.16047689,
            48.33076593,
            -0.12534081,
        ),
    ),
    BodySpec(
        key="venus",
        name="Venus",
        kind="planet",
        radius_km=6_051.8,
        mass_kg=4.86731e24,
        rotation_period_days=-243.018,
        color_rgb=(222, 181, 105),
        axis_tilt_degrees=177.4,
        atmosphere_rgba=(255, 210, 126, 42),
        orbital_elements=OrbitalElements(
            0.72333566,
            0.00000390,
            0.00677672,
            -0.00004107,
            3.39467605,
            -0.00078890,
            181.97909950,
            58517.81538729,
            131.60246718,
            0.00268329,
            76.67984255,
            -0.27769418,
        ),
    ),
    BodySpec(
        key="earth",
        name="Earth",
        kind="planet",
        radius_km=6_371.0084,
        mass_kg=5.97217e24,
        rotation_period_days=0.99726968,
        color_rgb=(68, 126, 205),
        axis_tilt_degrees=23.44,
        atmosphere_rgba=(92, 170, 255, 48),
        orbital_elements=OrbitalElements(
            1.00000261,
            0.00000562,
            0.01671123,
            -0.00004392,
            -0.00001531,
            -0.01294668,
            100.46457166,
            35999.37244981,
            102.93768193,
            0.32327364,
            0.0,
            0.0,
        ),
    ),
    BodySpec(
        key="mars",
        name="Mars",
        kind="planet",
        radius_km=3_389.50,
        mass_kg=0.641691e24,
        rotation_period_days=1.02595676,
        color_rgb=(196, 92, 57),
        axis_tilt_degrees=25.19,
        atmosphere_rgba=(210, 105, 75, 24),
        orbital_elements=OrbitalElements(
            1.52371034,
            0.00001847,
            0.09339410,
            0.00007882,
            1.84969142,
            -0.00813131,
            -4.55343205,
            19140.30268499,
            -23.94362959,
            0.44441088,
            49.55953891,
            -0.29257343,
        ),
    ),
    BodySpec(
        key="jupiter",
        name="Jupiter",
        kind="planet",
        radius_km=69_911.0,
        mass_kg=1_898.125e24,
        rotation_period_days=0.41354,
        color_rgb=(214, 171, 126),
        axis_tilt_degrees=3.13,
        atmosphere_rgba=(232, 201, 166, 22),
        orbital_elements=OrbitalElements(
            5.20288700,
            -0.00011607,
            0.04838624,
            -0.00013253,
            1.30439695,
            -0.00183714,
            34.39644051,
            3034.74612775,
            14.72847983,
            0.21252668,
            100.47390909,
            0.20469106,
        ),
    ),
    BodySpec(
        key="saturn",
        name="Saturn",
        kind="planet",
        radius_km=58_232.0,
        mass_kg=568.317e24,
        rotation_period_days=0.44401,
        color_rgb=(224, 197, 139),
        axis_tilt_degrees=26.73,
        ring=RingSpec(1.35, 2.35, (214, 191, 142, 138)),
        atmosphere_rgba=(241, 219, 170, 18),
        orbital_elements=OrbitalElements(
            9.53667594,
            -0.00125060,
            0.05386179,
            -0.00050991,
            2.48599187,
            0.00193609,
            49.95424423,
            1222.49362201,
            92.59887831,
            -0.41897216,
            113.66242448,
            -0.28867794,
        ),
    ),
    BodySpec(
        key="uranus",
        name="Uranus",
        kind="planet",
        radius_km=25_362.0,
        mass_kg=86.8099e24,
        rotation_period_days=-0.71833,
        color_rgb=(131, 210, 213),
        axis_tilt_degrees=97.77,
        ring=RingSpec(1.55, 1.95, (155, 211, 214, 58)),
        atmosphere_rgba=(150, 232, 235, 26),
        orbital_elements=OrbitalElements(
            19.18916464,
            -0.00196176,
            0.04725744,
            -0.00004397,
            0.77263783,
            -0.00242939,
            313.23810451,
            428.48202785,
            170.95427630,
            0.40805281,
            74.01692503,
            0.04240589,
        ),
    ),
    BodySpec(
        key="neptune",
        name="Neptune",
        kind="planet",
        radius_km=24_622.0,
        mass_kg=102.4092e24,
        rotation_period_days=0.67125,
        color_rgb=(74, 111, 214),
        axis_tilt_degrees=28.32,
        atmosphere_rgba=(76, 124, 255, 28),
        orbital_elements=OrbitalElements(
            30.06992276,
            0.00026291,
            0.00859048,
            0.00005105,
            1.77004347,
            0.00035372,
            -55.12002969,
            218.45945325,
            44.96476227,
            -0.32241464,
            131.78422574,
            -0.00508664,
        ),
    ),
)


DWARF_BODIES: tuple[BodySpec, ...] = (
    BodySpec(
        key="ceres",
        name="Ceres",
        kind="dwarf",
        radius_km=469.7,
        mass_kg=9.38416e20,
        rotation_period_days=0.37809042,
        color_rgb=(124, 116, 105),
        axis_tilt_degrees=4.0,
        simple_orbit=SimpleOrbit(2.7675, 0.0758, 10.59, 1681.63, 35.0),
    ),
    BodySpec(
        key="pluto",
        name="Pluto",
        kind="dwarf",
        radius_km=1_188.3,
        mass_kg=1.30246e22,
        rotation_period_days=-6.3872,
        color_rgb=(181, 156, 132),
        axis_tilt_degrees=119.6,
        simple_orbit=SimpleOrbit(39.482, 0.2488, 17.16, 90_560.0, 238.0),
    ),
)


ASTEROID_BODIES: tuple[BodySpec, ...] = (
    BodySpec(
        key="vesta",
        name="4 Vesta",
        kind="asteroid",
        radius_km=261.385,
        mass_kg=0.0,
        rotation_period_days=0.2225886513,
        color_rgb=(165, 158, 145),
        axis_tilt_degrees=0.0,
        orbital_elements=OrbitalElements(
            2.361541280085,
            0.0,
            0.090167645047,
            0.0,
            7.144060599544,
            0.0,
            -2285.952307101792,
            9919.755919109353,
            255.239446921594,
            0.0,
            103.702298034214,
            0.0,
        ),
    ),
    BodySpec(
        key="ida",
        name="243 Ida",
        kind="asteroid",
        radius_km=16.0,
        mass_kg=0.0,
        rotation_period_days=0.1930833333,
        color_rgb=(134, 120, 103),
        axis_tilt_degrees=0.0,
        orbital_elements=OrbitalElements(
            2.862543414664,
            0.0,
            0.045548263774,
            0.0,
            1.130114887920,
            0.0,
            -1478.423544995568,
            7433.034958301208,
            437.336837642060,
            0.0,
            323.548316065356,
            0.0,
        ),
    ),
    BodySpec(
        key="mathilde",
        name="253 Mathilde",
        kind="asteroid",
        radius_km=26.4,
        mass_kg=0.0,
        rotation_period_days=17.4041666667,
        color_rgb=(92, 88, 84),
        axis_tilt_degrees=0.0,
        orbital_elements=OrbitalElements(
            2.646519093622,
            0.0,
            0.264370003489,
            0.0,
            6.740899232137,
            0.0,
            -1599.789084906811,
            8361.452964738417,
            337.092324880359,
            0.0,
            179.496020026610,
            0.0,
        ),
    ),
    BodySpec(
        key="eros",
        name="433 Eros",
        kind="asteroid",
        radius_km=8.42,
        mass_kg=0.0,
        rotation_period_days=0.2195833333,
        color_rgb=(154, 137, 115),
        axis_tilt_degrees=0.0,
        orbital_elements=OrbitalElements(
            1.458120998475,
            0.0,
            0.222835940707,
            0.0,
            10.828466513998,
            0.0,
            -4499.201117210529,
            20445.792647267102,
            483.199856249747,
            0.0,
            304.270102575332,
            0.0,
        ),
    ),
    BodySpec(
        key="gaspra",
        name="951 Gaspra",
        kind="asteroid",
        radius_km=6.1,
        mass_kg=0.0,
        rotation_period_days=0.2934166667,
        color_rgb=(148, 132, 111),
        axis_tilt_degrees=0.0,
        orbital_elements=OrbitalElements(
            2.210232960638,
            0.0,
            0.173420289601,
            0.0,
            4.105754340169,
            0.0,
            -2400.203362156037,
            10955.626599608888,
            383.024836437961,
            0.0,
            252.987864841208,
            0.0,
        ),
    ),
    BodySpec(
        key="bennu",
        name="101955 Bennu",
        kind="asteroid",
        radius_km=0.24222,
        mass_kg=0.0,
        rotation_period_days=0.1790025417,
        color_rgb=(116, 108, 98),
        axis_tilt_degrees=0.0,
        orbital_elements=OrbitalElements(
            1.126391025895,
            0.0,
            0.203745076242,
            0.0,
            6.034943770248,
            0.0,
            -3142.285595919938,
            30113.450820877431,
            68.283927036539,
            0.0,
            2.060866195696,
            0.0,
        ),
    ),
)


MOONS: tuple[MoonSpec, ...] = (
    MoonSpec("moon", "Moon", "earth", 1_737.4, 7.342e22, 384_400.0, 27.321661, (190, 190, 185), 12.0, 5.14),
    MoonSpec("phobos", "Phobos", "mars", 11.3, 1.0659e16, 9_376.0, 0.31891, (142, 128, 112), 45.0, 1.1),
    MoonSpec("deimos", "Deimos", "mars", 6.2, 1.4762e15, 23_463.0, 1.26244, (128, 119, 106), 160.0, 1.8),
    MoonSpec("io", "Io", "jupiter", 1_821.6, 8.9319e22, 421_700.0, 1.769, (236, 209, 92), 0.0, 0.04),
    MoonSpec("europa", "Europa", "jupiter", 1_560.8, 4.7998e22, 671_100.0, 3.551, (205, 194, 174), 70.0, 0.47),
    MoonSpec("ganymede", "Ganymede", "jupiter", 2_634.1, 1.4819e23, 1_070_400.0, 7.155, (164, 143, 119), 150.0, 0.2),
    MoonSpec("callisto", "Callisto", "jupiter", 2_410.3, 1.0759e23, 1_882_700.0, 16.689, (126, 118, 103), 230.0, 0.2),
    MoonSpec("enceladus", "Enceladus", "saturn", 252.1, 1.0802e20, 238_020.0, 1.370, (215, 222, 226), 20.0, 0.0),
    MoonSpec("rhea", "Rhea", "saturn", 763.8, 2.3065e21, 527_108.0, 4.518, (184, 178, 168), 92.0, 0.35),
    MoonSpec("titan", "Titan", "saturn", 2_574.7, 1.3452e23, 1_221_870.0, 15.945, (212, 148, 74), 180.0, 0.33),
    MoonSpec("iapetus", "Iapetus", "saturn", 734.5, 1.8056e21, 3_560_850.0, 79.3215, (133, 127, 121), 260.0, 15.47),
    MoonSpec("miranda", "Miranda", "uranus", 235.8, 6.59e19, 129_900.0, 1.413, (170, 176, 172), 40.0, 4.2),
    MoonSpec("titania", "Titania", "uranus", 788.9, 3.527e21, 435_910.0, 8.706, (165, 162, 155), 130.0, 0.1),
    MoonSpec("oberon", "Oberon", "uranus", 761.4, 3.014e21, 583_520.0, 13.463, (140, 136, 131), 240.0, 0.1),
    MoonSpec("triton", "Triton", "neptune", 1_353.4, 2.139e22, 354_759.0, -5.877, (187, 184, 176), 85.0, 156.9),
)


SOLAR_BODIES: tuple[BodySpec, ...] = (SUN, *PLANETS, *DWARF_BODIES, *ASTEROID_BODIES)
BODIES_BY_KEY = {body.key: body for body in SOLAR_BODIES}
MOONS_BY_PARENT: dict[str, tuple[MoonSpec, ...]] = {}
for moon in MOONS:
    MOONS_BY_PARENT.setdefault(moon.parent_key, ())
    MOONS_BY_PARENT[moon.parent_key] = (*MOONS_BY_PARENT[moon.parent_key], moon)
