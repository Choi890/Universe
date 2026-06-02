from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import random
from typing import Any

import numpy as np

from .orbits import (
    heliocentric_position_au,
    julian_day,
    moon_position_km,
    orbital_path_au,
    simple_orbit_path_au,
    simple_orbit_position_au,
)
from .solar_data import AU_KM, EARTH_RADIUS_KM, J2000_JD, MOONS, SOLAR_BODIES, BodySpec, MoonSpec


SECONDS_PER_DAY = 86_400.0
REALTIME_DAYS_PER_SECOND = 1.0 / SECONDS_PER_DAY
MIN_TIME_MULTIPLIER = 1.0 / 1024.0
MAX_TIME_MULTIPLIER = 4096.0
DISTANCE_UNITS_PER_AU = 95.0
MOON_DISTANCE_BOOST = 95.0
STAR_COUNT = 14000
ASTEROID_COUNT = 0
MINOR_ORBIT_COUNT = 92
PICK_MIN_SCREEN_RADIUS = 0.045
PICK_MAX_SCREEN_RADIUS = 0.18
MIN_DISPLAY_SOLAR_IRRADIANCE = 0.00085
MAX_DISPLAY_SOLAR_IRRADIANCE = 7.0
TARGET_FPS = 120
NEPTUNE_ORBIT_AU = 30.1
SYSTEM_VIEW_DISTANCE = 4700.0
MAX_VIEW_DISTANCE = 9200.0
TEXTURE_DIR = Path(__file__).resolve().parents[2] / "assets" / "textures"
MODEL_DIR = Path(__file__).resolve().parents[2] / "assets" / "models"
EYES_ASTEROID_MODEL_FILE = MODEL_DIR / "asteroids" / "eyes_asteroid_models.json"
KST = timezone(timedelta(hours=9), "KST")
KOREAN_FONT_CANDIDATES = (
    Path("C:/Windows/Fonts/malgun.ttf"),
    Path("C:/Windows/Fonts/malgunbd.ttf"),
    Path("C:/Windows/Fonts/NotoSansKR-VF.ttf"),
)

NASA_REFERENCE_TEXTURES = {
    "sun": "sun_source",
    "mercury": "mercury",
    "venus": "venus_source",
    "mars": "mars",
    "jupiter": "jupiter_source",
    "saturn": "saturn_source",
    "uranus": "uranus_source",
    "neptune": "neptune_source",
}

PLANET_MATERIALS = {
    "mercury": {"atmosphere": (0, 0, 0), "atmosphere_strength": 0.0, "ambient": 0.025, "terminator": 0.045, "saturation": 0.92},
    "venus": {"atmosphere": (255, 214, 140), "atmosphere_strength": 0.56, "ambient": 0.080, "terminator": 0.125, "saturation": 0.82},
    "mars": {"atmosphere": (224, 118, 82), "atmosphere_strength": 0.16, "ambient": 0.035, "terminator": 0.060, "saturation": 1.08},
    "jupiter": {"atmosphere": (240, 211, 176), "atmosphere_strength": 0.25, "ambient": 0.040, "terminator": 0.090, "saturation": 1.06},
    "saturn": {"atmosphere": (244, 220, 170), "atmosphere_strength": 0.26, "ambient": 0.050, "terminator": 0.105, "saturation": 0.90},
    "uranus": {"atmosphere": (168, 232, 228), "atmosphere_strength": 0.48, "ambient": 0.060, "terminator": 0.145, "saturation": 0.72},
    "neptune": {"atmosphere": (112, 168, 218), "atmosphere_strength": 0.42, "ambient": 0.055, "terminator": 0.130, "saturation": 0.88},
    "pluto": {"atmosphere": (190, 210, 255), "atmosphere_strength": 0.08, "ambient": 0.025, "terminator": 0.050, "saturation": 0.95},
    "ceres": {"atmosphere": (0, 0, 0), "atmosphere_strength": 0.0, "ambient": 0.025, "terminator": 0.045, "saturation": 0.90},
    "asteroid": {"atmosphere": (0, 0, 0), "atmosphere_strength": 0.0, "ambient": 0.070, "terminator": 0.095, "saturation": 0.92},
}

DISPLAY_NAMES_KO = {
    "sun": "태양",
    "mercury": "수성",
    "venus": "금성",
    "earth": "지구",
    "mars": "화성",
    "jupiter": "목성",
    "saturn": "토성",
    "uranus": "천왕성",
    "neptune": "해왕성",
    "ceres": "세레스",
    "pluto": "명왕성",
}

ORBIT_LINE_COLORS = {
    "mercury": (178, 181, 186, 116),
    "venus": (228, 201, 132, 118),
    "earth": (122, 176, 238, 128),
    "mars": (224, 129, 88, 116),
    "jupiter": (225, 198, 142, 126),
    "saturn": (230, 212, 153, 128),
    "uranus": (142, 220, 225, 116),
    "neptune": (118, 154, 230, 118),
    "ceres": (166, 160, 150, 82),
    "pluto": (154, 165, 188, 78),
}

MINOR_ORBIT_LABELS = (
    "2018 VG18",
    "2014 NW65",
    "1995 SN55",
    "1P/Halley",
    "2P/Encke",
    "2060 Chiron",
)

MINOR_ORBIT_PRESETS = {
    "2018 VG18": (78.0, 0.71, 24.0, 18.0, 284.0),
    "2014 NW65": (36.0, 0.46, 18.5, 116.0, 42.0),
    "1995 SN55": (24.0, 0.48, 5.0, 205.0, 118.0),
    "1P/Halley": (17.8, 0.967, 162.3, 58.4, 111.3),
    "2P/Encke": (2.22, 0.85, 11.8, 334.6, 186.5),
    "2060 Chiron": (13.7, 0.38, 6.9, 209.3, 339.0),
}

ASTEROID_SHAPE_PROFILES = {
    "vesta": {"axes": (1.04, 0.86, 0.92), "roughness": 0.055, "ridge": 0.02, "seed": 4.1},
    "ida": {"axes": (1.58, 0.48, 0.42), "roughness": 0.105, "ridge": 0.00, "seed": 8.7},
    "mathilde": {"axes": (1.12, 0.78, 0.64), "roughness": 0.125, "ridge": 0.00, "seed": 12.4},
    "eros": {"axes": (1.52, 0.54, 0.46), "roughness": 0.115, "ridge": 0.00, "seed": 18.2},
    "gaspra": {"axes": (1.28, 0.64, 0.54), "roughness": 0.110, "ridge": 0.00, "seed": 23.6},
    "bennu": {"axes": (0.92, 0.78, 0.90), "roughness": 0.065, "ridge": 0.18, "seed": 31.3},
}

EYES_ASTEROID_ALBEDO_TEXTURES = {
    "bennu": "bennu_whole.jpg",
    "vesta": "vesta_04.png",
    "eros": "eros_diff.jpg",
    "gaspra": "gaspra_albedo.jpg",
    "ida": "asteroid_02_diff.jpg",
    "mathilde": "asteroid_03_diff.jpg",
}


@dataclass
class BodyRuntime:
    spec: BodySpec
    entity: Any
    label: Any
    visual_radius: float
    position_au: np.ndarray
    ring_entities: list[Any] | None = None
    atmosphere_entity: Any | None = None
    cloud_entity: Any | None = None
    glow_entity: Any | None = None


@dataclass
class MoonRuntime:
    spec: MoonSpec
    entity: Any
    visual_radius: float


@dataclass
class AsteroidRuntime:
    entity: Any
    orbit_radius_au: float
    angle: float
    inclination: float
    period_days: float
    spin: tuple[float, float, float]


@dataclass
class MinorOrbitLabel:
    entity: Any
    base_scale: float
    world_position: Any


def _load_ursina() -> dict[str, Any]:
    # Delay importing Ursina until launch so tests can import math helpers without a graphics runtime.
    try:
        from ursina import (
            AmbientLight,
            DirectionalLight,
            Entity,
            Mesh,
            PointLight,
            Shader,
            Sky,
            Text,
            Ursina,
            Vec3,
            camera,
            color,
            held_keys,
            lerp,
            load_model,
            load_texture,
            mouse,
            scene,
            time,
            window,
        )
        from ursina.shaders import unlit_shader
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Ursina is not installed. Run: python -m pip install -r requirements.txt"
        ) from exc

    return {
        "AmbientLight": AmbientLight,
        "DirectionalLight": DirectionalLight,
        "Entity": Entity,
        "Mesh": Mesh,
        "PointLight": PointLight,
        "Shader": Shader,
        "Sky": Sky,
        "Text": Text,
        "Ursina": Ursina,
        "Vec3": Vec3,
        "camera": camera,
        "color": color,
        "held_keys": held_keys,
        "lerp": lerp,
        "load_model": load_model,
        "load_texture": load_texture,
        "mouse": mouse,
        "scene": scene,
        "time": time,
        "unlit_shader": unlit_shader,
        "window": window,
    }


def visual_radius_for_body(body: BodySpec) -> float:
    if body.kind == "star":
        return 3.35
    if body.kind == "asteroid":
        return max(0.075, min(0.20, (body.radius_km / EARTH_RADIUS_KM) ** 0.35 * 0.46))
    if body.kind == "dwarf":
        return max(0.13, (body.radius_km / EARTH_RADIUS_KM) ** 0.50 * 0.36)
    return max(0.34, (body.radius_km / EARTH_RADIUS_KM) ** 0.55 * 0.72)


def visual_radius_for_moon(moon: MoonSpec) -> float:
    return max(0.045, (moon.radius_km / EARTH_RADIUS_KM) ** 0.52 * 0.20)


def key_value(held_keys: Any, key: str) -> float:
    try:
        return float(held_keys[key])
    except Exception:
        return 0.0


def vec_length(vec: Any) -> float:
    return math.sqrt(vec.x * vec.x + vec.y * vec.y + vec.z * vec.z)


def vec_normalized(vec: Any, vec3_factory: Any) -> Any:
    length = vec_length(vec)
    if length <= 1e-8:
        return vec3_factory(0, 0, 0)
    return vec / length


def normalize_degrees(value: float) -> float:
    return value % 360.0


def signed_degrees(value: float) -> float:
    return (value + 180.0) % 360.0 - 180.0


def greenwich_mean_sidereal_time_degrees(jd: float) -> float:
    centuries = (jd - J2000_JD) / 36_525.0
    return normalize_degrees(
        280.46061837
        + 360.98564736629 * (jd - J2000_JD)
        + 0.000387933 * centuries * centuries
        - centuries * centuries * centuries / 38_710_000.0
    )


def subsolar_point_degrees(jd: float) -> tuple[float, float]:
    days = jd - J2000_JD
    mean_longitude = normalize_degrees(280.460 + 0.9856474 * days)
    mean_anomaly = math.radians(normalize_degrees(357.528 + 0.9856003 * days))
    ecliptic_longitude = math.radians(
        normalize_degrees(
            mean_longitude
            + 1.915 * math.sin(mean_anomaly)
            + 0.020 * math.sin(2.0 * mean_anomaly)
        )
    )
    obliquity = math.radians(23.439 - 0.0000004 * days)

    right_ascension = normalize_degrees(
        math.degrees(math.atan2(math.cos(obliquity) * math.sin(ecliptic_longitude), math.cos(ecliptic_longitude)))
    )
    declination = math.degrees(math.asin(math.sin(obliquity) * math.sin(ecliptic_longitude)))
    longitude = signed_degrees(right_ascension - greenwich_mean_sidereal_time_degrees(jd))
    return longitude, declination


def geographic_light_dot(
    latitude_degrees: float,
    longitude_degrees: float,
    subsolar_latitude_degrees: float,
    subsolar_longitude_degrees: float,
) -> float:
    latitude = math.radians(latitude_degrees)
    longitude = math.radians(longitude_degrees)
    subsolar_latitude = math.radians(subsolar_latitude_degrees)
    subsolar_longitude = math.radians(subsolar_longitude_degrees)
    return (
        math.sin(latitude) * math.sin(subsolar_latitude)
        + math.cos(latitude)
        * math.cos(subsolar_latitude)
        * math.cos(longitude - subsolar_longitude)
    )


def geographic_surface_vector(latitude_degrees: float, longitude_degrees: float) -> tuple[float, float, float]:
    latitude = math.radians(latitude_degrees)
    longitude = math.radians(longitude_degrees)
    cos_latitude = math.cos(latitude)
    return (
        -cos_latitude * math.cos(longitude),
        math.sin(latitude),
        -cos_latitude * math.sin(longitude),
    )


def rotation_y_for_solar_alignment(
    surface_vector: tuple[float, float, float],
    target_light_vector: tuple[float, float, float],
    axis_tilt_degrees: float,
) -> float:
    tilt = math.radians(axis_tilt_degrees)
    local_x, local_y, local_z = surface_vector
    tilted_x = local_x
    tilted_z = local_y * math.sin(tilt) + local_z * math.cos(tilt)
    target_x, _, target_z = target_light_vector
    return normalize_degrees(
        math.degrees(math.atan2(target_x, target_z) - math.atan2(tilted_x, tilted_z))
    )


def configure_panda_runtime_options() -> None:
    try:
        from panda3d.core import loadPrcFileData

        loadPrcFileData("", "sync-video false")
        loadPrcFileData("", f"clock-mode limited\nclock-frame-rate {TARGET_FPS}")
    except Exception:
        pass


class SolarSystemScene:
    def __init__(self, api: dict[str, Any]):
        # The scene controller keeps all runtime entities, simulation time, and camera state together.
        self.api = api
        self.Entity = api["Entity"]
        self.Mesh = api["Mesh"]
        self.Shader = api["Shader"]
        self.Text = api["Text"]
        self.Vec3 = api["Vec3"]
        self.camera = api["camera"]
        self.color = api["color"]
        self.held_keys = api["held_keys"]
        self.lerp = api["lerp"]
        self.mouse = api["mouse"]
        self.scene = api["scene"]
        self.time = api["time"]
        self.unlit_shader = api["unlit_shader"]
        self.window = api["window"]
        self.load_model = api["load_model"]
        self.load_texture = api["load_texture"]
        self.configure_text_font()

        self.start_datetime = datetime.now(timezone.utc)
        self.start_jd = julian_day(self.start_datetime)
        self.sim_days = 0.0
        self.time_scale = REALTIME_DAYS_PER_SECOND
        self.paused = False
        self.show_orbits = True
        self.show_labels = True
        self.show_moons = True
        self.follow_index: int | None = None
        self.camera_mode = "orbit"

        self.view_yaw = 0.0
        self.view_pitch = 56.0
        self.view_distance = SYSTEM_VIEW_DISTANCE
        self.inspect_yaw = 0.0
        self.inspect_pitch = 8.0
        self.inspect_roll = 0.0
        self.focus = self.Vec3(0, 0, 0)
        self.free_yaw = 0.0
        self.free_pitch = 0.0
        self.free_roll = 0.0
        self.free_speed = 180.0
        self.inspect_runtime: BodyRuntime | None = None

        self.body_runtime: dict[str, BodyRuntime] = {}
        self.moon_runtime: list[MoonRuntime] = []
        self.asteroids: list[AsteroidRuntime] = []
        self.orbit_entities: list[Any] = []
        self.ecliptic_entities: list[Any] = []
        self.minor_orbit_labels: list[MinorOrbitLabel] = []
        self.lit_entities: list[Any] = []
        self.sun_light: Any | None = None
        self.textures = self.load_textures()
        self.eyes_asteroid_models = self.load_eyes_asteroid_model_manifest()
        self.sphere_segments = 160
        self.sphere_rings = 80
        self.earth_shader = self.create_earth_shader()
        self.planet_shader = self.create_planet_shader()
        self.sun_shader = self.create_sun_shader()

        self.configure_window()
        self.create_lighting()
        self.create_starfield()
        self.create_ecliptic_reference()
        self.create_minor_orbit_network()
        self.create_bodies()
        self.create_asteroid_belt()
        self.create_ui()
        self.update_body_positions()
        self.update_camera(force=True)
        self.update_physical_effects()
        self.update_labels()
        self.update_ui()

    def rgb(self, r: int, g: int, b: int) -> Any:
        return self.color.rgb32(r, g, b)

    def rgba(self, r: int, g: int, b: int, a: int) -> Any:
        return self.color.rgba32(r, g, b, a)

    def configure_text_font(self) -> None:
        for font_path in KOREAN_FONT_CANDIDATES:
            if not font_path.exists():
                continue
            try:
                from ursina import application

                application.fonts_folder = font_path.parent
                self.Text.default_font = font_path.name
            except Exception:
                pass
            return

    def display_name_for_body(self, body: BodySpec) -> str:
        return DISPLAY_NAMES_KO.get(body.key, body.name)

    def load_textures(self) -> dict[str, Any]:
        textures: dict[str, Any] = {}
        project_root = TEXTURE_DIR.parents[1]
        for path in TEXTURE_DIR.glob("*.*"):
            if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            try:
                texture = self.load_texture(path.relative_to(project_root).as_posix())
            except Exception:
                continue
            if texture:
                textures[path.stem] = texture
        return textures

    def load_eyes_asteroid_model_manifest(self) -> dict[str, Any]:
        if not EYES_ASTEROID_MODEL_FILE.exists():
            return {}
        try:
            data = json.loads(EYES_ASTEROID_MODEL_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return data if isinstance(data, dict) else {}

    def create_uv_sphere_mesh(self, segments: int = 128, rings: int = 64) -> Any:
        vertices = []
        normals = []
        uvs = []
        triangles = []

        for ring in range(rings + 1):
            v = ring / rings
            theta = math.pi * v
            y = math.cos(theta)
            radial = math.sin(theta)
            for segment in range(segments + 1):
                u = segment / segments
                phi = math.tau * u
                x = math.cos(phi) * radial
                z = math.sin(phi) * radial
                point = self.Vec3(x, y, z)
                vertices.append(point)
                normals.append(point)
                # Keep NASA/JPL equirectangular maps in their source east-west orientation.
                uvs.append((u, 1.0 - v))

        row = segments + 1
        for ring in range(rings):
            for segment in range(segments):
                a = ring * row + segment
                b = a + 1
                c = a + row
                d = c + 1
                triangles.append((a, b, c))
                triangles.append((b, d, c))

        return self.Mesh(vertices=vertices, triangles=triangles, normals=normals, uvs=uvs, static=True)

    def new_sphere_model(self) -> Any:
        return self.create_uv_sphere_mesh(self.sphere_segments, self.sphere_rings)

    def load_eyes_asteroid_model(self, key: str) -> Any | None:
        config = self.eyes_asteroid_models.get(key)
        if not config:
            return None
        local_path = config.get("local")
        if not isinstance(local_path, str):
            return None
        model_path = Path(__file__).resolve().parents[2] / local_path
        if not model_path.exists():
            return None
        try:
            return self.load_model(model_path.relative_to(Path(__file__).resolve().parents[2]).as_posix())
        except Exception:
            return None

    def eyes_asteroid_rotation(self, key: str) -> tuple[float, float, float]:
        config = self.eyes_asteroid_models.get(key, {})
        rotation = config.get("rotate", {}) if isinstance(config, dict) else {}
        if not isinstance(rotation, dict):
            return 0.0, 0.0, 0.0
        return (
            float(rotation.get("x", 0.0)),
            float(rotation.get("y", 0.0)),
            float(rotation.get("z", 0.0)),
        )

    def load_eyes_asteroid_albedo_texture(self, key: str) -> Any | None:
        texture_name = EYES_ASTEROID_ALBEDO_TEXTURES.get(key)
        if not texture_name:
            return None
        texture_path = MODEL_DIR / "asteroids" / key / texture_name
        if not texture_path.exists():
            return None
        try:
            return self.load_texture(texture_path.relative_to(Path(__file__).resolve().parents[2]).as_posix())
        except Exception:
            return None

    def apply_texture_to_model_tree(self, entity: Any, texture: Any) -> None:
        try:
            entity.texture = texture
        except Exception:
            pass
        try:
            matches = entity.findAllMatches("**/+GeomNode")
        except Exception:
            matches = []
        for node in matches:
            try:
                node.clearMaterial()
                node.setColor(1, 1, 1, 1)
                node.setTexture(texture, 1)
            except Exception:
                pass

    def normalize_eyes_asteroid_entity(self, entity: Any, key: str, radius: float) -> None:
        try:
            bounds = entity.getTightBounds()
        except Exception:
            bounds = None
        if not bounds:
            return

        minimum, maximum = bounds
        extents = (
            max(1e-8, float(maximum.x - minimum.x)),
            max(1e-8, float(maximum.y - minimum.y)),
            max(1e-8, float(maximum.z - minimum.z)),
        )
        config = self.eyes_asteroid_models.get(key, {})
        eyes_scale = config.get("scale", None) if isinstance(config, dict) else None
        if isinstance(eyes_scale, list) and len(eyes_scale) == 3:
            max_axis = max(abs(float(value)) for value in eyes_scale) or 1.0
            axis_scale = tuple(abs(float(value)) / max_axis for value in eyes_scale)
        else:
            axis_scale = (1.0, 1.0, 1.0)

        adjusted_max_extent = max(extents[index] * axis_scale[index] for index in range(3))
        model_scale = (radius * 2.0) / adjusted_max_extent
        entity.scale = tuple(model_scale * axis_scale[index] for index in range(3))

    def asteroid_surface_multiplier(self, key: str, theta: float, phi: float) -> float:
        profile = ASTEROID_SHAPE_PROFILES.get(key, {})
        roughness = float(profile.get("roughness", 0.08))
        seed = float(profile.get("seed", 1.0))
        ridge = float(profile.get("ridge", 0.0))
        latitude = math.cos(theta)
        equator = math.sin(theta)

        harmonics = (
            0.52 * math.sin(phi * 2.0 + seed) * math.sin(theta * 1.7 + seed * 0.3)
            + 0.34 * math.sin(phi * 5.0 - seed * 0.6) * math.sin(theta * 3.0 + 0.4)
            + 0.24 * math.cos(phi * 9.0 + seed * 1.1) * math.sin(theta * 4.8)
            + 0.16 * math.sin((phi + theta) * 13.0 + seed)
        )
        crater_like_depressions = (
            -0.055 * math.exp(-((signed_degrees(math.degrees(phi) - seed * 13.0) / 34.0) ** 2 + ((latitude - 0.18) / 0.22) ** 2))
            -0.040 * math.exp(-((signed_degrees(math.degrees(phi) + seed * 9.0) / 26.0) ** 2 + ((latitude + 0.34) / 0.18) ** 2))
        )
        equatorial_ridge = ridge * math.exp(-(latitude / 0.22) ** 2) * (0.78 + 0.22 * math.sin(phi * 6.0 + seed))
        return max(0.62, 1.0 + roughness * harmonics + crater_like_depressions + equatorial_ridge * equator)

    def create_asteroid_rock_mesh(self, key: str, radius: float, segments: int = 96, rings: int = 48) -> Any:
        profile = ASTEROID_SHAPE_PROFILES.get(key, {})
        axis_x, axis_y, axis_z = profile.get("axes", (1.0, 0.72, 0.68))
        vertices = []
        normals = []
        uvs = []
        triangles = []

        for ring in range(rings + 1):
            v = ring / rings
            theta = math.pi * v
            y_unit = math.cos(theta)
            radial = math.sin(theta)
            for segment in range(segments + 1):
                u = segment / segments
                phi = math.tau * u
                rough_radius = radius * self.asteroid_surface_multiplier(key, theta, phi)
                x = math.cos(phi) * radial * rough_radius * axis_x
                y = y_unit * rough_radius * axis_y
                z = math.sin(phi) * radial * rough_radius * axis_z
                point = self.Vec3(x, y, z)
                normal_x = x / axis_x
                normal_y = y / axis_y
                normal_z = z / axis_z
                normal_length = max(1e-8, math.sqrt(normal_x * normal_x + normal_y * normal_y + normal_z * normal_z))
                vertices.append(point)
                normals.append(self.Vec3(normal_x / normal_length, normal_y / normal_length, normal_z / normal_length))
                uvs.append((u, 1.0 - v))

        row = segments + 1
        for ring in range(rings):
            for segment in range(segments):
                a = ring * row + segment
                b = a + 1
                c = a + row
                d = c + 1
                triangles.append((a, b, c))
                triangles.append((b, d, c))

        return self.Mesh(vertices=vertices, triangles=triangles, normals=normals, uvs=uvs, static=True)

    def body_texture(self, key: str) -> Any | None:
        return self.textures.get(key)

    def current_sim_datetime(self) -> datetime:
        return self.start_datetime + timedelta(days=self.sim_days)

    def current_sim_datetime_kst(self) -> datetime:
        return self.current_sim_datetime().astimezone(KST)

    def time_multiplier(self) -> float:
        return self.time_scale / REALTIME_DAYS_PER_SECOND

    def set_time_multiplier(self, multiplier: float) -> None:
        multiplier = max(MIN_TIME_MULTIPLIER, min(MAX_TIME_MULTIPLIER, multiplier))
        self.time_scale = multiplier * REALTIME_DAYS_PER_SECOND

    def sync_to_real_time(self) -> None:
        self.start_datetime = datetime.now(timezone.utc)
        self.start_jd = julian_day(self.start_datetime)
        self.sim_days = 0.0
        self.set_time_multiplier(1.0)
        self.paused = False

    def format_time_multiplier(self) -> str:
        multiplier = self.time_multiplier()
        if abs(multiplier - 1.0) < 1e-6:
            return "real time x1"
        if multiplier >= 1.0:
            return f"time x{multiplier:g}"
        return f"time x{multiplier:.4g}"

    def format_radius(self, radius_km: float) -> str:
        if radius_km < 1.0:
            return f"{radius_km * 1000.0:,.0f} m"
        if radius_km < 100.0:
            return f"{radius_km:,.1f} km"
        return f"{radius_km:,.0f} km"

    def create_earth_shader(self) -> Any:
        return self.Shader(
            name="earth_physical_shader",
            language=self.Shader.GLSL,
            vertex="""
#version 140
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

out vec2 texcoord;
out vec3 world_normal;
out vec3 world_position;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoord = p3d_MultiTexCoord0;
    world_normal = normalize(mat3(p3d_ModelMatrix) * p3d_Normal);
    world_position = (p3d_ModelMatrix * p3d_Vertex).xyz;
}
""",
            fragment="""
#version 140
uniform sampler2D p3d_Texture0;
uniform sampler2D night_texture;
uniform sampler2D cloud_texture;
uniform vec4 p3d_ColorScale;
uniform vec3 sun_position;
uniform vec3 camera_position;
uniform float cloud_strength;
uniform float atmosphere_strength;
uniform float cloud_offset;
uniform float solar_irradiance;

in vec2 texcoord;
in vec3 world_normal;
in vec3 world_position;

out vec4 fragColor;

void main() {
    vec3 normal = normalize(world_normal);
    vec3 light_dir = normalize(sun_position - world_position);
    vec3 view_dir = normalize(camera_position - world_position);
    float ndl = dot(normal, light_dir);
    float daylight = smoothstep(-0.055, 0.105, ndl);
    float twilight = smoothstep(-0.34, 0.18, ndl);
    float lambert = max(ndl, 0.0);
    float solar_display = clamp(pow(max(solar_irradiance, 0.00085), 0.31), 0.10, 1.72);

    vec3 day = texture(p3d_Texture0, texcoord).rgb;
    vec3 night = texture(night_texture, texcoord).rgb;
    vec2 cloud_uv = vec2(fract(texcoord.x + cloud_offset), texcoord.y);
    vec4 clouds = texture(cloud_texture, cloud_uv);

    vec3 lit_day = day * (0.040 + solar_display * (0.30 + 0.98 * lambert));
    lit_day = mix(lit_day, vec3(1.0), clouds.a * cloud_strength * solar_display * (0.20 + 0.58 * daylight));

    float ocean = smoothstep(0.18, 0.58, day.b - max(day.r, day.g) * 0.42);
    vec3 half_dir = normalize(light_dir + view_dir);
    float specular = pow(max(dot(normal, half_dir), 0.0), 72.0) * ocean * daylight * 0.34 * solar_display;

    float rim = pow(1.0 - max(dot(normal, view_dir), 0.0), 2.45);
    float sunset = smoothstep(-0.16, 0.12, ndl) * (1.0 - smoothstep(0.10, 0.38, ndl));
    vec3 atmosphere = vec3(0.30, 0.58, 1.0) * rim * atmosphere_strength * sqrt(solar_display) * (0.26 + daylight);
    atmosphere += vec3(1.0, 0.38, 0.13) * rim * sunset * 0.22 * solar_display;

    vec3 night_surface = day * (0.038 + 0.040 * sqrt(solar_display));
    night_surface += clouds.rgb * clouds.a * cloud_strength * (0.018 + 0.034 * twilight);
    vec3 night_lights = night * 1.12 * (1.0 - daylight);
    vec3 dusk_scatter = day * twilight * (1.0 - daylight) * (0.12 + 0.08 * solar_display);
    vec3 color = mix(night_surface + night_lights + dusk_scatter, lit_day, daylight);
    color += vec3(specular);
    color += atmosphere;
    color = vec3(1.0) - exp(-color * 0.94);
    fragColor = vec4(color * p3d_ColorScale.rgb, 1.0);
}
""",
        )

    def create_planet_shader(self) -> Any:
        return self.Shader(
            name="solar_lit_planet_shader",
            language=self.Shader.GLSL,
            vertex="""
#version 140
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform vec2 texture_scale;
uniform vec2 texture_offset;

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

out vec2 texcoord;
out vec3 world_normal;
out vec3 world_position;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoord = (p3d_MultiTexCoord0 * texture_scale) + texture_offset;
    world_normal = normalize(mat3(p3d_ModelMatrix) * p3d_Normal);
    world_position = (p3d_ModelMatrix * p3d_Vertex).xyz;
}
""",
            fragment="""
#version 140
uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
uniform vec3 sun_position;
uniform vec3 camera_position;
uniform vec3 atmosphere_color;
uniform float atmosphere_strength;
uniform float ambient_light;
uniform float terminator_softness;
uniform float specular_strength;
uniform float color_saturation;
uniform float solar_irradiance;

in vec2 texcoord;
in vec3 world_normal;
in vec3 world_position;

out vec4 fragColor;

void main() {
    vec3 normal = normalize(world_normal);
    vec3 light_dir = normalize(sun_position - world_position);
    vec3 view_dir = normalize(camera_position - world_position);
    float ndl = dot(normal, light_dir);
    float lambert = max(ndl, 0.0);
    float physical_softness = clamp(terminator_softness, 0.045, 0.145);
    float daylight = smoothstep(-physical_softness, physical_softness, ndl);
    float twilight = smoothstep(-0.34, 0.12, ndl);
    float solar_display = clamp(pow(max(solar_irradiance, 0.00085), 0.31), 0.07, 1.76);

    vec4 sampled_albedo = texture(p3d_Texture0, texcoord);
    if (sampled_albedo.a < 0.04) {
        discard;
    }
    vec3 albedo = sampled_albedo.rgb;
    float luminance = dot(albedo, vec3(0.299, 0.587, 0.114));
    albedo = mix(vec3(luminance), albedo, color_saturation);

    vec3 day_color = albedo * (0.024 + solar_display * (0.18 + 0.88 * lambert));
    vec3 night_color = albedo * (0.026 + ambient_light * 0.55 + 0.020 * sqrt(solar_display));
    vec3 color = mix(night_color, day_color, daylight);
    color += albedo * twilight * (1.0 - daylight) * 0.10 * sqrt(solar_display);

    vec3 half_dir = normalize(light_dir + view_dir);
    float specular = pow(max(dot(normal, half_dir), 0.0), 96.0) * specular_strength * daylight * solar_display;

    float rim = pow(1.0 - max(dot(normal, view_dir), 0.0), 2.35);
    float limb_light = 0.22 + 0.78 * smoothstep(-0.20, 0.18, ndl);
    vec3 atmosphere = atmosphere_color * rim * atmosphere_strength * limb_light * sqrt(solar_display);

    color += atmosphere + vec3(specular);
    color = vec3(1.0) - exp(-color * 1.04);
    fragColor = vec4(color * p3d_ColorScale.rgb, sampled_albedo.a * p3d_ColorScale.a);
}
""",
        )

    def create_sun_shader(self) -> Any:
        return self.Shader(
            name="sun_photosphere_shader",
            language=self.Shader.GLSL,
            vertex="""
#version 140
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

out vec2 texcoord;
out vec3 world_normal;
out vec3 world_position;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoord = p3d_MultiTexCoord0;
    world_normal = normalize(mat3(p3d_ModelMatrix) * p3d_Normal);
    world_position = (p3d_ModelMatrix * p3d_Vertex).xyz;
}
""",
            fragment="""
#version 140
uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
uniform vec3 camera_position;
uniform float sun_time;

in vec2 texcoord;
in vec3 world_normal;
in vec3 world_position;

out vec4 fragColor;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < 5; i++) {
        value += noise(p) * amplitude;
        p *= 2.03;
        amplitude *= 0.5;
    }
    return value;
}

void main() {
    vec3 normal = normalize(world_normal);
    vec3 view_dir = normalize(camera_position - world_position);
    float limb = max(dot(normal, view_dir), 0.0);

    vec2 flow_uv = vec2(fract(texcoord.x + sun_time * 0.0035), texcoord.y);
    vec3 source = texture(p3d_Texture0, flow_uv).rgb;
    float granules = fbm(texcoord * vec2(110.0, 56.0) + vec2(sun_time * 0.20, -sun_time * 0.05));
    float cells = fbm(texcoord * vec2(28.0, 14.0) - vec2(sun_time * 0.028, sun_time * 0.016));
    float spots = smoothstep(0.72, 0.90, fbm(texcoord * vec2(10.0, 5.0) + vec2(1.7, -0.4)));
    float active_latitude = smoothstep(0.18, 0.46, texcoord.y) * (1.0 - smoothstep(0.54, 0.82, texcoord.y));
    spots *= active_latitude;

    vec3 deep_orange = vec3(1.00, 0.34, 0.04);
    vec3 orange = vec3(1.00, 0.58, 0.10);
    vec3 yellow = vec3(1.00, 0.86, 0.28);
    vec3 white_hot = vec3(1.00, 0.96, 0.68);

    vec3 plasma = mix(deep_orange, yellow, clamp(granules * 0.76 + cells * 0.28, 0.0, 1.0));
    plasma = mix(plasma, white_hot, smoothstep(0.66, 0.96, granules) * 0.26);
    vec3 color = mix(source, plasma, 0.18);
    color *= 1.22 + 0.18 * cells + 0.07 * sin((texcoord.y * 42.0 + sun_time * 0.5));
    color = mix(color, color * vec3(0.28, 0.13, 0.035), spots * 0.36);

    float limb_darkening = 0.50 + 0.50 * pow(limb, 0.42);
    float rim = pow(1.0 - limb, 2.2);
    color *= limb_darkening;
    color += (source * 0.45 + orange * 0.55) * rim * 0.72;
    color += white_hot * pow(max(limb, 0.0), 6.0) * 0.10;

    color = color / (color + vec3(0.82));
    fragColor = vec4(color * 1.42 * p3d_ColorScale.rgb, 1.0);
}
""",
        )

    def configure_earth_material(self, entity: Any) -> None:
        night_texture = self.textures.get("earth_night") or self.textures.get("earth")
        cloud_texture = self.textures.get("earth_clouds") or self.textures.get("earth")
        if night_texture:
            entity.set_shader_input("night_texture", night_texture)
        if cloud_texture:
            entity.set_shader_input("cloud_texture", cloud_texture)
        entity.set_shader_input("cloud_strength", 0.48 if self.textures.get("earth_clouds") else 0.0)
        entity.set_shader_input("atmosphere_strength", 0.92)
        entity.set_shader_input("cloud_offset", 0.0)
        entity.set_shader_input("sun_position", self.Vec3(0, 0, 0))
        entity.set_shader_input("camera_position", self.camera.position)
        entity.set_shader_input("solar_irradiance", 1.0)

    def configure_planet_material(self, entity: Any, key: str) -> None:
        settings = PLANET_MATERIALS.get(
            key,
            {"atmosphere": (185, 198, 220), "atmosphere_strength": 0.03, "ambient": 0.025, "terminator": 0.050, "saturation": 0.92},
        )
        atmosphere = settings["atmosphere"]
        entity.set_shader_input("sun_position", self.Vec3(0, 0, 0))
        entity.set_shader_input("camera_position", self.camera.position)
        entity.set_shader_input("texture_scale", (1.0, 1.0))
        entity.set_shader_input("texture_offset", (0.0, 0.0))
        entity.set_shader_input(
            "atmosphere_color",
            self.Vec3(atmosphere[0] / 255.0, atmosphere[1] / 255.0, atmosphere[2] / 255.0),
        )
        entity.set_shader_input("atmosphere_strength", float(settings["atmosphere_strength"]))
        entity.set_shader_input("ambient_light", float(settings["ambient"]))
        entity.set_shader_input("terminator_softness", float(settings["terminator"]))
        entity.set_shader_input("specular_strength", float(settings.get("specular", 0.0)))
        entity.set_shader_input("color_saturation", float(settings["saturation"]))
        entity.set_shader_input("solar_irradiance", 1.0)
        self.lit_entities.append(entity)

    def configure_sun_material(self, entity: Any) -> None:
        entity.set_shader_input("camera_position", self.camera.position)
        entity.set_shader_input("sun_time", 0.0)

    def body_scale(self, body: BodySpec, radius: float) -> Any:
        diameter = radius * 2.0
        return (diameter, diameter, diameter)

    def set_mouse_locked(self, locked: bool) -> None:
        try:
            self.mouse.locked = locked
        except AttributeError:
            pass

    def mouse_is_locked(self) -> bool:
        try:
            return bool(self.mouse.locked)
        except AttributeError:
            return False

    def configure_window(self) -> None:
        self.window.title = "Universe - Solar System"
        self.window.color = self.rgb(1, 3, 8)
        self.window.fps_counter.enabled = True
        self.window.exit_button.visible = False
        try:
            self.window.vsync = False
        except Exception:
            pass
        try:
            from panda3d.core import ClockObject

            clock = ClockObject.getGlobalClock()
            clock.setMode(ClockObject.MLimited)
            clock.setFrameRate(TARGET_FPS)
        except Exception:
            pass
        self.camera.clip_plane_far = 50000
        self.camera.clip_plane_near = 0.02
        self.camera.fov = 68
        self.set_mouse_locked(False)

    def create_lighting(self) -> None:
        self.api["AmbientLight"](color=self.rgba(3, 4, 7, 255))
        self.api["Sky"](texture=None, color=self.rgb(1, 3, 8))

    def create_starfield(self) -> None:
        rng = np.random.default_rng(2026)
        vertices = []
        for _ in range(STAR_COUNT):
            direction = rng.normal(size=3)
            direction /= np.linalg.norm(direction)
            radius = rng.uniform(9000.0, 15000.0)
            vertices.append(self.Vec3(*(direction * radius)))

        mesh = self.Mesh(vertices=vertices, mode="point", thickness=2)
        self.Entity(
            model=mesh,
            color=self.rgba(222, 234, 255, 232),
            shader=self.unlit_shader,
        )

    def create_ecliptic_reference(self) -> None:
        for radius_au, alpha in ((1.0, 42), (2.8, 26), (5.2, 30), (9.6, 28), (19.2, 24), (30.1, 24)):
            vertices = []
            radius = radius_au * DISTANCE_UNITS_PER_AU
            for index in range(241):
                angle = math.tau * index / 240
                vertices.append(self.Vec3(math.cos(angle) * radius, 0, math.sin(angle) * radius))
            mesh = self.Mesh(vertices=vertices, mode="line", thickness=1)
            self.ecliptic_entities.append(
                self.Entity(
                    model=mesh,
                    color=self.rgba(72, 88, 118, alpha),
                    shader=self.unlit_shader,
                )
            )

    def minor_orbit_point_au(
        self,
        semi_major_axis: float,
        eccentricity: float,
        inclination: float,
        longitude_node: float,
        argument_perihelion: float,
        true_anomaly: float,
    ) -> np.ndarray:
        radius = semi_major_axis * (1.0 - eccentricity * eccentricity) / (
            1.0 + eccentricity * math.cos(true_anomaly)
        )
        x_prime = radius * math.cos(true_anomaly)
        y_prime = radius * math.sin(true_anomaly)

        cos_node = math.cos(longitude_node)
        sin_node = math.sin(longitude_node)
        cos_arg = math.cos(argument_perihelion)
        sin_arg = math.sin(argument_perihelion)
        cos_i = math.cos(inclination)
        sin_i = math.sin(inclination)

        x_ecl = (
            (cos_node * cos_arg - sin_node * sin_arg * cos_i) * x_prime
            + (-cos_node * sin_arg - sin_node * cos_arg * cos_i) * y_prime
        )
        y_ecl = (
            (sin_node * cos_arg + cos_node * sin_arg * cos_i) * x_prime
            + (-sin_node * sin_arg + cos_node * cos_arg * cos_i) * y_prime
        )
        z_ecl = sin_arg * sin_i * x_prime + cos_arg * sin_i * y_prime
        return np.array([x_ecl, y_ecl, z_ecl], dtype=float)

    def minor_orbit_path_au(
        self,
        semi_major_axis: float,
        eccentricity: float,
        inclination: float,
        longitude_node: float,
        argument_perihelion: float,
        samples: int = 360,
    ) -> list[np.ndarray]:
        return [
            self.minor_orbit_point_au(
                semi_major_axis,
                eccentricity,
                inclination,
                longitude_node,
                argument_perihelion,
                math.tau * index / (samples - 1),
            )
            for index in range(samples)
        ]

    def random_minor_orbit(self, rng: random.Random, index: int) -> tuple[float, float, float, float, float]:
        if index < len(MINOR_ORBIT_LABELS):
            preset = MINOR_ORBIT_PRESETS[MINOR_ORBIT_LABELS[index]]
            return (
                preset[0],
                preset[1],
                math.radians(preset[2]),
                math.radians(preset[3]),
                math.radians(preset[4]),
            )

        family = rng.random()
        if family < 0.48:
            semi_major_axis = rng.uniform(1.7, 4.4)
            eccentricity = rng.uniform(0.04, 0.28)
            inclination = math.radians(rng.uniform(-11.0, 11.0))
        elif family < 0.78:
            semi_major_axis = rng.uniform(0.9, 9.0)
            eccentricity = rng.uniform(0.20, 0.72)
            inclination = math.radians(rng.uniform(-28.0, 28.0))
        elif family < 0.93:
            semi_major_axis = rng.uniform(8.5, 33.0)
            eccentricity = rng.uniform(0.10, 0.55)
            inclination = math.radians(rng.uniform(-38.0, 38.0))
        else:
            semi_major_axis = rng.uniform(18.0, 70.0)
            eccentricity = rng.uniform(0.35, 0.78)
            inclination = math.radians(rng.uniform(-64.0, 64.0))

        longitude_node = rng.uniform(0.0, math.tau)
        argument_perihelion = rng.uniform(0.0, math.tau)
        return semi_major_axis, eccentricity, inclination, longitude_node, argument_perihelion

    def create_minor_orbit_network(self) -> None:
        rng = random.Random(7301)
        for index in range(MINOR_ORBIT_COUNT):
            a, e, inclination, node, perihelion = self.random_minor_orbit(rng, index)
            color_roll = rng.random()
            if color_roll < 0.18:
                line_color = self.rgba(202, 219, 246, 74)
            elif color_roll < 0.32:
                line_color = self.rgba(230, 212, 148, 80)
            else:
                line_color = self.rgba(132, 142, 158, 62)

            mesh = self.Mesh(
                vertices=[
                    self.au_to_scene_vec(point)
                    for point in self.minor_orbit_path_au(a, e, inclination, node, perihelion)
                ],
                mode="line",
                thickness=1,
            )
            self.orbit_entities.append(
                self.Entity(
                    model=mesh,
                    color=line_color,
                    shader=self.unlit_shader,
                )
            )

            if index >= len(MINOR_ORBIT_LABELS):
                continue

            label_point = self.minor_orbit_point_au(
                a,
                e,
                inclination,
                node,
                perihelion,
                rng.uniform(0.0, math.tau),
            )
            label_world_position = self.au_to_scene_vec(label_point)
            label = self.Text(
                text=MINOR_ORBIT_LABELS[index],
                parent=self.camera.ui,
                origin=(0, 0),
                position=(0, 0),
                scale=0.24,
                color=self.rgba(205, 214, 226, 182),
                background=True,
                always_on_top=True,
            )
            self.minor_orbit_labels.append(MinorOrbitLabel(label, 0.24, label_world_position))

    def create_bodies(self) -> None:
        for body in SOLAR_BODIES:
            radius = visual_radius_for_body(body)
            eyes_model_loaded = False
            if body.kind == "asteroid":
                model = self.load_eyes_asteroid_model(body.key)
                if model:
                    texture = self.load_eyes_asteroid_albedo_texture(body.key) or self.body_texture(body.key)
                    eyes_model_loaded = True
                else:
                    texture = self.body_texture(body.key)
                    if not texture:
                        continue
                    model = self.create_asteroid_rock_mesh(body.key, radius)
            else:
                texture = self.body_texture(body.key)
                model = self.new_sphere_model()
            scale = 1.0 if body.kind == "asteroid" else self.body_scale(body, radius)
            shader = None
            if body.key == "earth":
                shader = self.earth_shader
            elif body.kind == "star":
                shader = self.sun_shader
            elif texture:
                shader = self.planet_shader

            entity = self.Entity(
                model=model,
                texture=texture,
                color=self.rgba(255, 255, 255, 255) if (texture or eyes_model_loaded) else self.rgb(*body.color_rgb),
                scale=scale,
                shader=shader,
                collider="sphere",
                double_sided=True,
            )
            entity.body_key = body.key
            entity.eyes_model_loaded = eyes_model_loaded
            if eyes_model_loaded:
                self.normalize_eyes_asteroid_entity(entity, body.key, radius)
                if texture:
                    self.apply_texture_to_model_tree(entity, texture)

            label = self.Text(
                text=self.display_name_for_body(body),
                parent=self.camera.ui,
                origin=(0, 0),
                position=(0, 0),
                scale=0.42,
                color=(
                    self.rgba(214, 218, 224, 224)
                    if body.kind == "asteroid"
                    else self.rgba(235, 242, 255, 245)
                    if body.kind == "planet"
                    else self.rgba(220, 232, 255, 230)
                ),
                background=True,
                always_on_top=True,
            )

            runtime = BodyRuntime(body, entity, label, radius, np.zeros(3, dtype=float))
            entity.on_click = self.handle_body_click
            if body.key == "earth":
                self.configure_earth_material(entity)
            elif body.kind == "star":
                self.configure_sun_material(entity)
            elif body.kind != "star" and texture:
                self.configure_planet_material(entity, "asteroid" if body.kind == "asteroid" else body.key)

            if body.kind == "star":
                self.sun_light = self.api["PointLight"](
                    parent=entity,
                    color=self.rgba(255, 244, 214, 255),
                    shadows=False,
                )
                try:
                    self.sun_light._light.setAttenuation((0.25, 0.0, 0.000012))
                except Exception:
                    pass
                glow_texture = self.textures.get("sun_glow")
                if glow_texture:
                    runtime.glow_entity = self.Entity(
                        parent=self.scene,
                        model="quad",
                        texture=glow_texture,
                        position=entity.position,
                        scale=radius * 14.0,
                        color=self.rgba(255, 255, 255, 220),
                        shader=self.unlit_shader,
                        double_sided=True,
                    )
                    runtime.glow_entity.set_billboard_point_world()
            else:
                atmosphere_texture = self.textures.get(f"{body.key}_clouds")
                if atmosphere_texture and body.key not in {"earth", "venus"}:
                    runtime.cloud_entity = self.Entity(
                        parent=entity,
                        model=self.new_sphere_model(),
                        texture=atmosphere_texture,
                        scale=1.028 if body.key == "earth" else 1.045,
                        color=self.rgba(255, 255, 255, 205 if body.key == "venus" else 150),
                        shader=self.unlit_shader,
                        double_sided=True,
                    )

            if body.ring:
                runtime.ring_entities = self.create_ring_entities(body, radius)

            self.body_runtime[body.key] = runtime
            if body.orbital_elements or body.simple_orbit:
                self.create_orbit_path(body)

        for moon in MOONS:
            radius = visual_radius_for_moon(moon)
            moon_texture = self.textures.get(moon.key) or self.textures.get("moon")
            entity = self.Entity(
                model=self.new_sphere_model(),
                texture=moon_texture,
                color=self.rgba(255, 255, 255, 255) if moon_texture else self.rgb(*moon.color_rgb),
                scale=radius * 2.0,
                shader=self.planet_shader if moon_texture else None,
                double_sided=True,
            )
            if moon_texture:
                self.configure_planet_material(entity, moon.key)
            self.moon_runtime.append(MoonRuntime(moon, entity, radius))

    def create_ring_mesh(self, inner_radius: float, outer_radius: float, segments: int) -> Any:
        vertices = []
        triangles = []
        for index in range(segments):
            angle = math.tau * index / segments
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            vertices.append(self.Vec3(cos_a * inner_radius, 0, sin_a * inner_radius))
            vertices.append(self.Vec3(cos_a * outer_radius, 0, sin_a * outer_radius))

        for index in range(segments):
            inner_a = index * 2
            outer_a = inner_a + 1
            inner_b = ((index + 1) % segments) * 2
            outer_b = inner_b + 1
            triangles.append((inner_a, outer_a, outer_b))
            triangles.append((inner_a, outer_b, inner_b))

        return self.Mesh(vertices=vertices, triangles=triangles, mode="triangle")

    def create_ring_entities(self, body: BodySpec, radius: float) -> list[Any]:
        if not body.ring:
            return []

        ring_entities = []
        inner = radius * body.ring.inner_radius_multiple
        outer = radius * body.ring.outer_radius_multiple
        band_count = 64 if body.key == "saturn" else 14
        base_r, base_g, base_b, base_a = body.ring.rgba

        for index in range(band_count):
            start = index / band_count
            end = (index + (0.58 if body.key == "saturn" else 0.72)) / band_count
            band_inner = inner + (outer - inner) * start
            band_outer = inner + (outer - inner) * min(1.0, end)
            if band_outer <= band_inner:
                continue

            midpoint = (start + end) * 0.5
            gap_factor = 1.0
            if body.key == "saturn":
                for gap_center, gap_width, depth in ((0.565, 0.020, 0.10), (0.735, 0.010, 0.26), (0.885, 0.006, 0.34)):
                    if abs(midpoint - gap_center) < gap_width:
                        gap_factor = min(gap_factor, depth)

            band_variation = 0.70 + 0.18 * math.sin(index * 1.7) + 0.12 * math.sin(index * 4.3)
            alpha = int(base_a * gap_factor * band_variation)
            color_shift = 18 * math.sin(index * 0.9) + (22 if body.key == "saturn" and midpoint < 0.30 else 0)
            ring_entities.append(
                self.Entity(
                    model=self.create_ring_mesh(band_inner, band_outer, segments=384),
                    color=self.rgba(
                        max(0, min(255, int(base_r + color_shift))),
                        max(0, min(255, int(base_g + color_shift * 0.6))),
                        max(0, min(255, int(base_b + color_shift * 0.3))),
                        max(5, min(210, alpha)),
                    ),
                    shader=self.unlit_shader,
                    double_sided=True,
                )
            )
        return ring_entities

    def create_orbit_path(self, body: BodySpec) -> None:
        if body.orbital_elements:
            points = orbital_path_au(body.orbital_elements, self.start_jd, 420)
        elif body.simple_orbit:
            points = simple_orbit_path_au(body.simple_orbit, 420)
        else:
            return

        r, g, b, alpha = ORBIT_LINE_COLORS.get(
            body.key,
            (154, 152, 145, 74)
            if body.kind == "asteroid"
            else (118, 137, 168, 76 if body.kind == "planet" else 48),
        )
        mesh = self.Mesh(
            vertices=[self.au_to_scene_vec(point) for point in points],
            mode="line",
            thickness=2 if body.kind == "planet" else 1,
        )
        orbit = self.Entity(
            model=mesh,
            color=self.rgba(r, g, b, alpha),
            shader=self.unlit_shader,
        )
        self.orbit_entities.append(orbit)

    def create_asteroid_belt(self) -> None:
        if ASTEROID_COUNT <= 0:
            return
        rng = random.Random(441)
        asteroid_texture = self.textures.get("asteroid")
        for _ in range(ASTEROID_COUNT):
            orbit_radius_au = rng.uniform(2.08, 3.35)
            angle = rng.uniform(0.0, math.tau)
            inclination = math.radians(rng.uniform(-6.5, 6.5))
            period_days = 365.256 * math.sqrt(orbit_radius_au**3)
            scale = rng.uniform(0.025, 0.080)
            entity = self.Entity(
                model="sphere",
                texture=asteroid_texture,
                color=self.rgb(
                    rng.randint(90, 150),
                    rng.randint(82, 128),
                    rng.randint(70, 105),
                ) if not asteroid_texture else self.rgba(255, 255, 255, 255),
                scale=(scale * rng.uniform(1.4, 2.6), scale * rng.uniform(0.9, 1.7), scale * rng.uniform(1.0, 2.2)),
                rotation=(rng.randrange(360), rng.randrange(360), rng.randrange(360)),
                shader=self.planet_shader if asteroid_texture else None,
                double_sided=True,
            )
            if asteroid_texture:
                self.configure_planet_material(entity, "asteroid")
            self.asteroids.append(
                AsteroidRuntime(
                    entity,
                    orbit_radius_au,
                    angle,
                    inclination,
                    period_days,
                    (
                        rng.uniform(-18.0, 18.0),
                        rng.uniform(-24.0, 24.0),
                        rng.uniform(-16.0, 16.0),
                    ),
                )
            )

    def create_ui(self) -> None:
        self.title_text = self.Text(
            text="태양계",
            parent=self.camera.ui,
            origin=(-0.5, 0.5),
            position=(-0.86, 0.47),
            scale=1.05,
            color=self.rgba(231, 238, 255, 245),
        )
        self.info_text = self.Text(
            text="",
            parent=self.camera.ui,
            origin=(-0.5, 0.5),
            position=(-0.86, 0.405),
            scale=0.66,
            color=self.rgba(177, 205, 246, 225),
        )
        self.controls_text = self.Text(
            text="실시간 궤도 지도  |  좌클릭: 천체 360도 관찰  |  드래그: 회전  |  Z/X: 수평  |  ESC/1: 태양계  |  O/L: 궤도/이름",
            parent=self.camera.ui,
            origin=(0, -0.5),
            position=(0, -0.475),
            scale=0.54,
            color=self.rgba(168, 183, 210, 205),
        )
        self.reference_image = self.Entity(
            parent=self.camera.ui,
            model="quad",
            position=(0.68, 0.235),
            scale=(0.28, 0.28),
            color=self.rgba(255, 255, 255, 245),
            enabled=False,
        )
        self.reference_caption = self.Text(
            text="",
            parent=self.camera.ui,
            origin=(0, 0),
            position=(0.68, 0.065),
            scale=0.47,
            color=self.rgba(220, 232, 255, 230),
            background=True,
            enabled=False,
        )

    def au_to_scene_vec(self, position_au: np.ndarray) -> Any:
        return self.Vec3(
            float(position_au[0] * DISTANCE_UNITS_PER_AU),
            float(position_au[2] * DISTANCE_UNITS_PER_AU),
            float(position_au[1] * DISTANCE_UNITS_PER_AU),
        )

    def earth_rotation_y_for_sun(self, jd: float, earth_position_au: np.ndarray, axis_tilt_degrees: float) -> float:
        subsolar_longitude, subsolar_latitude = subsolar_point_degrees(jd)
        surface_vector = geographic_surface_vector(subsolar_latitude, subsolar_longitude)
        earth_position = self.au_to_scene_vec(earth_position_au)
        light_direction = vec_normalized(self.Vec3(0, 0, 0) - earth_position, self.Vec3)
        return rotation_y_for_solar_alignment(
            surface_vector,
            (light_direction.x, light_direction.y, light_direction.z),
            axis_tilt_degrees,
        )

    def current_selected_body(self) -> BodyRuntime | None:
        if self.camera_mode == "inspect" and self.inspect_runtime:
            return self.inspect_runtime
        if self.follow_index is None:
            return None
        bodies = list(self.body_runtime.values())
        return bodies[self.follow_index % len(bodies)]

    def inspect_distance_for(self, runtime: BodyRuntime) -> float:
        radius = runtime.visual_radius
        if runtime.spec.ring:
            radius *= runtime.spec.ring.outer_radius_multiple
        return max(1.45, radius * 2.85 + 0.65)

    def inspect_min_distance_for(self, runtime: BodyRuntime) -> float:
        radius = runtime.visual_radius
        if runtime.spec.ring:
            radius *= runtime.spec.ring.outer_radius_multiple
        return max(0.8, radius * 1.35)

    def enter_inspect_mode(self, runtime: BodyRuntime) -> None:
        self.inspect_runtime = runtime
        self.follow_index = None
        self.camera_mode = "inspect"
        self.set_mouse_locked(False)
        self.view_distance = self.inspect_distance_for(runtime)
        self.inspect_yaw = 0.0
        self.inspect_pitch = 8.0
        self.inspect_roll = 0.0
        self.show_reference_image(runtime)
        self.apply_scene_visibility()
        self.update_camera(force=True)

    def return_to_system_view(self) -> None:
        self.camera_mode = "orbit"
        self.inspect_runtime = None
        self.follow_index = None
        self.set_mouse_locked(False)
        self.view_distance = SYSTEM_VIEW_DISTANCE
        self.view_pitch = 56.0
        self.hide_reference_image()
        self.apply_scene_visibility()
        self.update_camera(force=True)

    def handle_body_click(self) -> None:
        runtime = self.runtime_from_cursor()
        if not runtime:
            runtime = self.runtime_from_entity(getattr(self.mouse, "hovered_entity", None))
        if not runtime:
            for hit in getattr(self.mouse, "collisions", []) or []:
                runtime = self.runtime_from_entity(getattr(hit, "entity", None))
                if runtime:
                    break
        if runtime:
            self.handle_runtime_click(runtime)

    def handle_runtime_click(self, runtime: BodyRuntime) -> None:
        if self.camera_mode == "inspect":
            return
        self.enter_inspect_mode(runtime)

    def runtime_from_entity(self, entity: Any) -> BodyRuntime | None:
        current = entity
        for _ in range(8):
            if current is None:
                return None
            body_key = getattr(current, "body_key", None)
            if body_key:
                runtime = self.body_runtime.get(body_key)
                if runtime:
                    return runtime
            current = getattr(current, "parent", None)
        return None

    def cursor_lens_position(self) -> tuple[float, float]:
        aspect = max(0.001, float(getattr(self.window, "aspect_ratio", 1.0) or 1.0))
        return (
            float(getattr(self.mouse, "x", 0.0)) * 2.0 / aspect,
            float(getattr(self.mouse, "y", 0.0)) * 2.0,
        )

    def world_to_ui_position(self, world_position: Any) -> tuple[Any, bool]:
        try:
            from panda3d.core import Point2
        except Exception:
            return self.Vec3(0, 0, 0), False

        lens = getattr(self.camera, "lens", None)
        if not lens:
            return self.Vec3(0, 0, 0), False

        screen_point = Point2()
        try:
            camera_point = self.camera.getRelativePoint(self.scene, world_position)
            projected = bool(lens.project(camera_point, screen_point))
        except Exception:
            return self.Vec3(0, 0, 0), False
        if not projected:
            return self.Vec3(0, 0, 0), False

        aspect = max(0.001, float(getattr(self.window, "aspect_ratio", 1.0) or 1.0))
        visible = -1.05 <= float(screen_point.x) <= 1.05 and -1.05 <= float(screen_point.y) <= 1.05
        return self.Vec3(float(screen_point.x) * aspect * 0.5, float(screen_point.y) * 0.5, 0), visible

    def pick_screen_radius_for(self, runtime: BodyRuntime, camera_distance: float) -> float:
        radius = runtime.visual_radius
        if runtime.spec.ring:
            radius *= runtime.spec.ring.outer_radius_multiple
        fov = max(1.0, float(getattr(self.camera, "fov", 68.0) or 68.0))
        projected = radius / max(camera_distance, 0.001) / max(math.tan(math.radians(fov * 0.5)), 0.001)
        return max(PICK_MIN_SCREEN_RADIUS, min(PICK_MAX_SCREEN_RADIUS, projected * 2.4))

    def runtime_from_cursor(self) -> BodyRuntime | None:
        try:
            from panda3d.core import Point2
        except Exception:
            return None

        lens = getattr(self.camera, "lens", None)
        if not lens:
            return None

        cursor_x, cursor_y = self.cursor_lens_position()
        best_runtime: BodyRuntime | None = None
        best_screen_distance = float("inf")

        for runtime in self.body_runtime.values():
            if not getattr(runtime.entity, "enabled", True):
                continue
            screen_point = Point2()
            try:
                camera_point = self.camera.getRelativePoint(self.scene, runtime.entity.position)
                projected = bool(lens.project(camera_point, screen_point))
            except Exception:
                continue
            if not projected:
                continue

            dx = float(screen_point.x) - cursor_x
            dy = float(screen_point.y) - cursor_y
            screen_distance = math.sqrt(dx * dx + dy * dy)
            camera_distance = max(0.001, (runtime.entity.position - self.camera.position).length())
            pick_radius = self.pick_screen_radius_for(runtime, camera_distance)
            if screen_distance <= pick_radius:
                if screen_distance < best_screen_distance:
                    best_screen_distance = screen_distance
                    best_runtime = runtime

        return best_runtime

    def show_reference_image(self, runtime: BodyRuntime) -> None:
        texture_key = NASA_REFERENCE_TEXTURES.get(runtime.spec.key, f"{runtime.spec.key}_source")
        texture = self.textures.get(texture_key) or self.textures.get(runtime.spec.key)
        if not texture:
            self.hide_reference_image()
            return

        self.reference_image.texture = texture
        width = max(1.0, float(getattr(texture, "width", 1) or 1))
        height = max(1.0, float(getattr(texture, "height", 1) or 1))
        aspect = width / height
        max_width = 0.30
        max_height = 0.26
        if aspect >= max_width / max_height:
            self.reference_image.scale = (max_width, max_width / aspect)
        else:
            self.reference_image.scale = (max_height * aspect, max_height)
        self.reference_image.enabled = True
        self.reference_caption.text = f"{self.display_name_for_body(runtime.spec)} NASA/JPL image"
        self.reference_caption.enabled = True

    def hide_reference_image(self) -> None:
        self.reference_image.enabled = False
        self.reference_caption.enabled = False

    def apply_scene_visibility(self) -> None:
        for runtime in self.body_runtime.values():
            runtime.entity.enabled = True
            runtime.label.enabled = self.show_labels
            if runtime.glow_entity:
                runtime.glow_entity.enabled = True
            if runtime.ring_entities:
                for ring_entity in runtime.ring_entities:
                    ring_entity.enabled = True

        for moon in self.moon_runtime:
            moon.entity.enabled = self.show_moons
        for asteroid in self.asteroids:
            asteroid.entity.enabled = True
        for entity in self.orbit_entities + self.ecliptic_entities:
            entity.enabled = self.show_orbits
        for minor_label in getattr(self, "minor_orbit_labels", []):
            minor_label.entity.enabled = self.show_labels and self.show_orbits

    def update(self) -> None:
        # Ursina calls this every frame; advance time, bodies, camera, lighting, and UI together.
        real_dt = max(0.0, self.time.dt)
        dt = min(real_dt, 0.05)
        simulated_days_delta = 0.0
        if not self.paused:
            simulated_days_delta = real_dt * self.time_scale
            self.sim_days += simulated_days_delta

        self.update_body_positions()
        self.update_asteroids(simulated_days_delta)
        if self.camera_mode == "free":
            self.update_free_camera(dt)
        elif self.camera_mode == "inspect":
            self.update_inspect_controls(dt)
            self.update_camera()
        else:
            self.update_view_controls(dt)
            self.update_camera()
        self.update_physical_effects()
        self.update_labels()
        self.update_ui()

    def input(self, key: str) -> None:
        # Keyboard and mouse shortcuts control camera mode, labels, orbits, moons, and time scale.
        if key == "scroll up":
            if self.camera_mode == "free":
                self.free_speed = min(6000.0, self.free_speed * 1.15)
            elif self.camera_mode == "inspect":
                selected = self.current_selected_body()
                minimum = self.inspect_min_distance_for(selected) if selected else 1.0
                self.view_distance = max(minimum, self.view_distance * 0.88)
            else:
                self.view_distance = max(12.0, self.view_distance * 0.88)
        elif key == "scroll down":
            if self.camera_mode == "free":
                self.free_speed = max(2.0, self.free_speed * 0.87)
            elif self.camera_mode == "inspect":
                selected = self.current_selected_body()
                maximum = self.inspect_distance_for(selected) * 2.8 if selected else 120.0
                self.view_distance = min(maximum, self.view_distance * 1.12)
            else:
                self.view_distance = min(MAX_VIEW_DISTANCE, self.view_distance * 1.12)
        elif key == "left mouse down":
            if self.camera_mode != "inspect":
                self.handle_body_click()
        elif key in {"w", "a", "s", "d"} and self.camera_mode == "orbit":
            self.enter_free_camera(lock_mouse=False)
        elif key == "c":
            self.toggle_camera_mode()
        elif key == "escape":
            self.return_to_system_view()
        elif key == "f":
            total = len(self.body_runtime)
            self.inspect_runtime = None
            self.follow_index = 0 if self.follow_index is None else (self.follow_index + 1) % total
            self.camera_mode = "orbit"
            self.set_mouse_locked(False)
            self.hide_reference_image()
            self.apply_scene_visibility()
            selected = self.current_selected_body()
            if selected:
                self.view_distance = max(8.0, min(110.0, selected.visual_radius * 18.0 + 18.0))
        elif key == "1":
            self.return_to_system_view()
        elif key == "o":
            self.show_orbits = not self.show_orbits
            self.apply_scene_visibility()
        elif key == "l":
            self.show_labels = not self.show_labels
            self.apply_scene_visibility()
        elif key == "m":
            self.show_moons = not self.show_moons
            self.apply_scene_visibility()
        elif key == "p":
            self.paused = not self.paused
        elif key == "t":
            self.sync_to_real_time()
        elif key == "[":
            self.set_time_multiplier(self.time_multiplier() * 0.5)
        elif key == "]":
            self.set_time_multiplier(self.time_multiplier() * 2.0)

    def update_view_controls(self, dt: float) -> None:
        yaw_axis = key_value(self.held_keys, "right arrow") - key_value(self.held_keys, "left arrow")
        pitch_axis = key_value(self.held_keys, "up arrow") - key_value(self.held_keys, "down arrow")

        self.view_yaw += yaw_axis * 85.0 * dt
        self.view_pitch += pitch_axis * 70.0 * dt

        if getattr(self.mouse, "right", False) or key_value(self.held_keys, "right mouse"):
            self.view_yaw -= self.mouse.velocity[0] * 220.0
            self.view_pitch -= self.mouse.velocity[1] * 170.0

        self.view_pitch = max(-82.0, min(82.0, self.view_pitch))

    def update_inspect_controls(self, dt: float) -> None:
        yaw_axis = key_value(self.held_keys, "right arrow") - key_value(self.held_keys, "left arrow")
        pitch_axis = key_value(self.held_keys, "up arrow") - key_value(self.held_keys, "down arrow")

        self.inspect_yaw += yaw_axis * 95.0 * dt
        self.inspect_pitch += pitch_axis * 80.0 * dt
        self.inspect_roll += (
            key_value(self.held_keys, "x") - key_value(self.held_keys, "z")
        ) * 95.0 * dt
        if key_value(self.held_keys, "r"):
            self.inspect_roll *= 0.88

        dragging = (
            getattr(self.mouse, "left", False)
            or getattr(self.mouse, "right", False)
            or key_value(self.held_keys, "left mouse")
            or key_value(self.held_keys, "right mouse")
        )
        if dragging:
            self.inspect_yaw -= self.mouse.velocity[0] * 260.0
            self.inspect_pitch -= self.mouse.velocity[1] * 190.0

        self.inspect_pitch = max(-88.0, min(88.0, self.inspect_pitch))

    def toggle_camera_mode(self) -> None:
        if self.camera_mode == "orbit":
            self.enter_free_camera(lock_mouse=True)
        else:
            self.return_to_system_view()

    def enter_free_camera(self, lock_mouse: bool) -> None:
        self.camera_mode = "free"
        self.inspect_runtime = None
        self.follow_index = None
        self.free_yaw = self.camera.rotation_y
        self.free_pitch = self.camera.rotation_x
        self.free_roll = self.camera.rotation_z
        self.set_mouse_locked(lock_mouse)
        self.hide_reference_image()
        self.apply_scene_visibility()

    def update_free_camera(self, dt: float) -> None:
        look_active = self.mouse_is_locked() or getattr(self.mouse, "right", False)
        if look_active:
            self.free_yaw += self.mouse.velocity[0] * 185.0
            self.free_pitch -= self.mouse.velocity[1] * 150.0

        self.free_yaw += (
            key_value(self.held_keys, "right arrow") - key_value(self.held_keys, "left arrow")
        ) * 90.0 * dt
        self.free_pitch += (
            key_value(self.held_keys, "down arrow") - key_value(self.held_keys, "up arrow")
        ) * 80.0 * dt
        self.free_roll += (
            key_value(self.held_keys, "x") - key_value(self.held_keys, "z")
        ) * 95.0 * dt

        if key_value(self.held_keys, "r"):
            self.free_roll *= 0.88

        self.free_pitch = max(-89.0, min(89.0, self.free_pitch))
        self.camera.rotation = (self.free_pitch, self.free_yaw, self.free_roll)

        movement = self.Vec3(0, 0, 0)
        movement += self.camera.forward * (key_value(self.held_keys, "w") - key_value(self.held_keys, "s"))
        movement += self.camera.right * (key_value(self.held_keys, "d") - key_value(self.held_keys, "a"))
        movement += self.camera.up * (key_value(self.held_keys, "e") - key_value(self.held_keys, "q"))
        movement += self.camera.forward * key_value(self.held_keys, "left mouse")
        movement -= self.camera.forward * key_value(self.held_keys, "middle mouse")

        speed = self.free_speed
        if key_value(self.held_keys, "shift"):
            speed *= 4.0
        if key_value(self.held_keys, "control"):
            speed *= 0.22

        if vec_length(movement) > 0.0:
            self.camera.position += vec_normalized(movement, self.Vec3) * speed * dt

    def update_body_positions(self) -> None:
        current_jd = self.start_jd + self.sim_days
        absolute_days = current_jd - J2000_JD

        for runtime in self.body_runtime.values():
            body = runtime.spec
            if body.kind == "star":
                position_au = np.zeros(3, dtype=float)
            elif body.orbital_elements:
                position_au = heliocentric_position_au(body.orbital_elements, current_jd)
            elif body.simple_orbit:
                position_au = simple_orbit_position_au(body.simple_orbit, absolute_days)
            else:
                position_au = np.zeros(3, dtype=float)

            runtime.position_au = position_au
            runtime.entity.position = self.au_to_scene_vec(position_au)
            model_rotation_x, model_rotation_y, model_rotation_z = (
                self.eyes_asteroid_rotation(body.key) if body.kind == "asteroid" else (0.0, 0.0, 0.0)
            )
            runtime.entity.rotation_x = body.axis_tilt_degrees + model_rotation_x
            if body.rotation_period_days:
                if body.key == "earth":
                    runtime.entity.rotation_y = self.earth_rotation_y_for_sun(
                        current_jd,
                        position_au,
                        body.axis_tilt_degrees,
                    )
                elif body.kind == "asteroid":
                    spin_degrees = (absolute_days / body.rotation_period_days * 360.0) % 360.0
                    runtime.entity.rotation_y = model_rotation_y
                    runtime.entity.rotation_z = model_rotation_z + spin_degrees
                else:
                    runtime.entity.rotation_y = (absolute_days / body.rotation_period_days * 360.0) % 360.0
            elif body.kind == "asteroid":
                runtime.entity.rotation_y = model_rotation_y
                runtime.entity.rotation_z = model_rotation_z

            if runtime.ring_entities:
                for ring_entity in runtime.ring_entities:
                    ring_entity.position = runtime.entity.position
                    ring_entity.rotation = (body.axis_tilt_degrees, 0, 0)

            if runtime.cloud_entity:
                runtime.cloud_entity.rotation_y = (
                    runtime.entity.rotation_y * (1.18 if body.key == "earth" else 0.72)
                    + absolute_days * (2.5 if body.key == "earth" else -0.45)
                ) % 360.0

            if runtime.atmosphere_entity:
                runtime.atmosphere_entity.rotation_y = runtime.entity.rotation_y * 0.92

            if runtime.glow_entity:
                runtime.glow_entity.position = runtime.entity.position

        for moon_runtime in self.moon_runtime:
            parent = self.body_runtime.get(moon_runtime.spec.parent_key)
            if not parent:
                continue
            local_km = moon_position_km(
                moon_runtime.spec.orbit_radius_km,
                moon_runtime.spec.orbital_period_days,
                absolute_days,
                moon_runtime.spec.phase_degrees,
                moon_runtime.spec.inclination_degrees,
            )
            local_scene = self.au_to_scene_vec(local_km / AU_KM) * MOON_DISTANCE_BOOST
            moon_runtime.entity.position = parent.entity.position + local_scene

    def solar_irradiance_for_position(self, position: Any, sun_position: Any) -> float:
        distance_au = max(0.05, (position - sun_position).length() / DISTANCE_UNITS_PER_AU)
        irradiance = 1.0 / (distance_au * distance_au)
        return max(MIN_DISPLAY_SOLAR_IRRADIANCE, min(MAX_DISPLAY_SOLAR_IRRADIANCE, irradiance))

    def update_physical_effects(self) -> None:
        earth = self.body_runtime.get("earth")
        sun = self.body_runtime.get("sun")
        if not earth or not sun:
            return

        earth.entity.set_shader_input("sun_position", sun.entity.position)
        earth.entity.set_shader_input("camera_position", self.camera.position)
        earth.entity.set_shader_input("solar_irradiance", self.solar_irradiance_for_position(earth.entity.position, sun.entity.position))
        earth.entity.set_shader_input("cloud_offset", ((self.start_jd + self.sim_days - J2000_JD) * 0.0019) % 1.0)

        sun.entity.set_shader_input("camera_position", self.camera.position)
        sun.entity.set_shader_input("sun_time", float((self.start_jd + self.sim_days - J2000_JD) % 10_000.0))

        for entity in self.lit_entities:
            entity.set_shader_input("sun_position", sun.entity.position)
            entity.set_shader_input("camera_position", self.camera.position)
            entity.set_shader_input("solar_irradiance", self.solar_irradiance_for_position(entity.position, sun.entity.position))

    def update_asteroids(self, simulated_days_delta: float) -> None:
        spin_dt = simulated_days_delta / REALTIME_DAYS_PER_SECOND if simulated_days_delta else 0.0
        for asteroid in self.asteroids:
            if simulated_days_delta:
                asteroid.angle += math.tau * simulated_days_delta / asteroid.period_days
            x = math.cos(asteroid.angle) * asteroid.orbit_radius_au
            z = math.sin(asteroid.angle) * asteroid.orbit_radius_au
            y = z * math.sin(asteroid.inclination)
            z *= math.cos(asteroid.inclination)
            asteroid.entity.position = self.au_to_scene_vec(np.array([x, z, y], dtype=float))
            if spin_dt:
                asteroid.entity.rotation_x += asteroid.spin[0] * spin_dt
                asteroid.entity.rotation_y += asteroid.spin[1] * spin_dt
                asteroid.entity.rotation_z += asteroid.spin[2] * spin_dt

    def update_labels(self) -> None:
        if not self.show_labels:
            for minor_label in getattr(self, "minor_orbit_labels", []):
                minor_label.entity.enabled = False
            return
        for runtime in self.body_runtime.values():
            runtime.label.text = self.display_name_for_body(runtime.spec)
            distance = max(1.0, (runtime.entity.position - self.camera.position).length())
            wide_map = self.camera_mode != "inspect"
            label_offset = runtime.visual_radius + max(1.2, distance * (0.018 if wide_map else 0.010))
            label_position, visible = self.world_to_ui_position(
                runtime.entity.position + self.Vec3(0, label_offset, 0)
            )
            runtime.label.enabled = visible
            runtime.label.position = label_position
            if runtime.spec.kind == "planet":
                runtime.label.scale = 0.42 if wide_map else 0.48
            elif runtime.spec.kind == "star":
                runtime.label.scale = 0.50 if wide_map else 0.58
            else:
                runtime.label.scale = 0.34 if wide_map else 0.42

        for minor_label in getattr(self, "minor_orbit_labels", []):
            label_position, visible = self.world_to_ui_position(minor_label.world_position)
            minor_label.entity.enabled = self.show_orbits and visible
            minor_label.entity.position = label_position
            minor_label.entity.scale = minor_label.base_scale

    def update_camera(self, force: bool = False) -> None:
        selected = self.current_selected_body()
        target_focus = selected.entity.position if selected else self.Vec3(0, 0, 0)
        self.focus = target_focus if force else self.lerp(self.focus, target_focus, min(1.0, self.time.dt * 3.0))

        if self.camera_mode == "inspect" and selected:
            yaw = math.radians(self.inspect_yaw)
            pitch = math.radians(self.inspect_pitch)
        else:
            yaw = math.radians(self.view_yaw)
            pitch = math.radians(self.view_pitch)
        horizontal = math.cos(pitch) * self.view_distance
        offset = self.Vec3(
            math.sin(yaw) * horizontal,
            math.sin(pitch) * self.view_distance,
            -math.cos(yaw) * horizontal,
        )
        if self.camera_mode == "inspect" and selected:
            try:
                offset = selected.entity.getQuat(self.scene).xform(offset)
            except Exception:
                pass
        self.camera.position = self.focus + offset
        if self.camera_mode == "inspect" and selected:
            try:
                self.camera.rotation_z = 0.0
            except Exception:
                pass
        self.camera.look_at(self.focus)
        if self.camera_mode == "inspect" and selected:
            try:
                base_roll = self.camera.rotation_z
                self.camera.rotation_z = base_roll + self.inspect_roll
            except Exception:
                pass

    def update_ui(self) -> None:
        selected = self.current_selected_body()
        sim_utc = self.current_sim_datetime()
        sim_kst = self.current_sim_datetime_kst()
        sim_time_text = f"{sim_utc:%Y-%m-%d %H:%M:%S UTC} / {sim_kst:%Y-%m-%d %H:%M:%S KST}"
        time_rate_text = self.format_time_multiplier()
        if selected:
            body = selected.spec
            self.title_text.text = self.display_name_for_body(body)
            self.info_text.text = (
                f"{body.kind} | 태양으로부터 {np.linalg.norm(selected.position_au):.3f} AU | "
                f"반지름 {self.format_radius(body.radius_km)} | {self.camera_mode} | {sim_time_text} | {time_rate_text}"
            )
        else:
            status = "paused" if self.paused else "running"
            self.title_text.text = "태양계"
            camera_detail = (
                f"free flight {self.free_speed:.0f} u/s"
                if self.camera_mode == "free"
                else "orbit view"
            )
            self.info_text.text = (
                f"태양, 행성, 왜소행성, NASA/JPL 실사 소행성, 주요 위성 | "
                f"{sim_time_text} | {time_rate_text} | {camera_detail} | {status}"
            )


def run() -> None:
    configure_panda_runtime_options()
    api = _load_ursina()
    app = api["Ursina"]()
    scene_controller = SolarSystemScene(api)

    class RuntimeController(api["Entity"]):
        def update(self) -> None:
            scene_controller.update()

        def input(self, key: str) -> None:
            scene_controller.input(key)

    RuntimeController()
    app.run()
