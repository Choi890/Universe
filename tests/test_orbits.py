from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from universe.orbits import heliocentric_position_au, julian_day, moon_position_km
from universe.main import (
    DISTANCE_UNITS_PER_AU,
    EYES_ASTEROID_ALBEDO_TEXTURES,
    SolarSystemScene,
    geographic_light_dot,
    geographic_surface_vector,
    greenwich_mean_sidereal_time_degrees,
    rotation_y_for_solar_alignment,
    subsolar_point_degrees,
)
from universe.solar_data import ASTEROID_BODIES, PLANETS


class DistanceVector:
    def __init__(self, length: float):
        self._length = length

    def __sub__(self, other: object) -> "DistanceVector":
        return self

    def length(self) -> float:
        return self._length


class OrbitTests(unittest.TestCase):
    def test_julian_day_j2000(self) -> None:
        jd = julian_day(datetime(2000, 1, 1, 12, tzinfo=timezone.utc))
        self.assertAlmostEqual(jd, 2_451_545.0, places=6)

    def test_planet_positions_are_finite(self) -> None:
        jd = julian_day(datetime(2026, 5, 26, tzinfo=timezone.utc))
        for planet in PLANETS:
            with self.subTest(planet=planet.name):
                position = heliocentric_position_au(planet.orbital_elements, jd)
                self.assertTrue(np.isfinite(position).all())
                self.assertGreater(np.linalg.norm(position), 0.2)

    def test_real_asteroid_positions_are_finite(self) -> None:
        jd = julian_day(datetime(2026, 5, 27, tzinfo=timezone.utc))
        expected_keys = {"vesta", "ida", "mathilde", "eros", "gaspra", "bennu"}
        self.assertEqual({asteroid.key for asteroid in ASTEROID_BODIES}, expected_keys)
        for asteroid in ASTEROID_BODIES:
            with self.subTest(asteroid=asteroid.name):
                self.assertEqual(asteroid.kind, "asteroid")
                self.assertIsNotNone(asteroid.orbital_elements)
                position = heliocentric_position_au(asteroid.orbital_elements, jd)
                self.assertTrue(np.isfinite(position).all())
                self.assertGreater(np.linalg.norm(position), 0.3)

    def test_real_asteroid_textures_exist(self) -> None:
        texture_dir = ROOT / "assets" / "textures"
        model_dir = ROOT / "assets" / "models" / "asteroids"
        model_manifest = json.loads((model_dir / "eyes_asteroid_models.json").read_text(encoding="utf-8"))
        for asteroid in ASTEROID_BODIES:
            with self.subTest(asteroid=asteroid.name):
                self.assertTrue((texture_dir / f"{asteroid.key}.jpg").exists())
                self.assertTrue((texture_dir / f"{asteroid.key}_source.jpg").exists())
                self.assertIn(asteroid.key, model_manifest)
                self.assertTrue((ROOT / model_manifest[asteroid.key]["local"]).exists())
                self.assertIn(asteroid.key, EYES_ASTEROID_ALBEDO_TEXTURES)
                self.assertTrue(
                    (model_dir / asteroid.key / EYES_ASTEROID_ALBEDO_TEXTURES[asteroid.key]).exists()
                )

    def test_asteroid_rock_mesh_is_closed_volumetric_shape(self) -> None:
        scene = SolarSystemScene.__new__(SolarSystemScene)
        scene.Vec3 = lambda x, y, z: (x, y, z)
        scene.Mesh = lambda **kwargs: kwargs

        mesh = SolarSystemScene.create_asteroid_rock_mesh(scene, "eros", 0.2, segments=24, rings=12)
        vertices = mesh["vertices"]
        xs = [vertex[0] for vertex in vertices]
        ys = [vertex[1] for vertex in vertices]
        zs = [vertex[2] for vertex in vertices]

        self.assertGreater(max(xs) - min(xs), max(ys) - min(ys))
        self.assertGreater(max(zs) - min(zs), 0.12)
        self.assertGreater(max(ys) - min(ys), 0.12)
        self.assertGreater(len(mesh["triangles"]), 8)

    def test_earth_stays_near_one_au(self) -> None:
        earth = next(planet for planet in PLANETS if planet.key == "earth")
        jd = julian_day(datetime(2026, 5, 26, tzinfo=timezone.utc))
        distance = float(np.linalg.norm(heliocentric_position_au(earth.orbital_elements, jd)))
        self.assertGreater(distance, 0.97)
        self.assertLess(distance, 1.03)

    def test_moon_orbit_radius(self) -> None:
        position = moon_position_km(384_400.0, 27.321661, 3.0, 12.0, 5.14)
        self.assertAlmostEqual(float(np.linalg.norm(position)), 384_400.0, delta=1e-6)

    def test_solar_irradiance_falls_off_with_distance(self) -> None:
        scene = SolarSystemScene.__new__(SolarSystemScene)
        sun = object()

        mercury = SolarSystemScene.solar_irradiance_for_position(
            scene,
            DistanceVector(0.387 * DISTANCE_UNITS_PER_AU),
            sun,
        )
        earth = SolarSystemScene.solar_irradiance_for_position(
            scene,
            DistanceVector(1.0 * DISTANCE_UNITS_PER_AU),
            sun,
        )
        neptune = SolarSystemScene.solar_irradiance_for_position(
            scene,
            DistanceVector(30.1 * DISTANCE_UNITS_PER_AU),
            sun,
        )

        self.assertGreater(mercury, earth)
        self.assertGreater(earth, neptune)

    def test_sphere_uvs_preserve_texture_horizontal_orientation(self) -> None:
        scene = SolarSystemScene.__new__(SolarSystemScene)
        scene.Vec3 = lambda x, y, z: (x, y, z)
        scene.Mesh = lambda **kwargs: kwargs

        mesh = SolarSystemScene.create_uv_sphere_mesh(scene, segments=4, rings=2)
        first_row_uvs = mesh["uvs"][:5]

        self.assertEqual(first_row_uvs[0][0], 0.0)
        self.assertEqual(first_row_uvs[-1][0], 1.0)

    def test_korea_is_daytime_near_kst_noon(self) -> None:
        jd = julian_day(datetime(2026, 5, 27, 3, tzinfo=timezone.utc))
        subsolar_longitude, subsolar_latitude = subsolar_point_degrees(jd)
        seoul_daylight = geographic_light_dot(
            37.5665,
            126.9780,
            subsolar_latitude,
            subsolar_longitude,
        )

        self.assertGreater(seoul_daylight, 0.82)

    def test_greenwich_sidereal_time_is_normalized(self) -> None:
        jd = julian_day(datetime(2026, 5, 27, 3, tzinfo=timezone.utc))
        gmst = greenwich_mean_sidereal_time_degrees(jd)

        self.assertGreaterEqual(gmst, 0.0)
        self.assertLess(gmst, 360.0)

    def test_earth_rotation_aligns_korea_with_real_sun_at_kst_noon(self) -> None:
        jd = julian_day(datetime(2026, 5, 27, 3, tzinfo=timezone.utc))
        earth = next(planet for planet in PLANETS if planet.key == "earth")
        earth_position = heliocentric_position_au(earth.orbital_elements, jd)
        scene_light = np.array([-earth_position[0], -earth_position[2], -earth_position[1]], dtype=float)
        scene_light /= np.linalg.norm(scene_light)
        subsolar_longitude, subsolar_latitude = subsolar_point_degrees(jd)
        rotation_y = rotation_y_for_solar_alignment(
            geographic_surface_vector(subsolar_latitude, subsolar_longitude),
            (float(scene_light[0]), float(scene_light[1]), float(scene_light[2])),
            earth.axis_tilt_degrees,
        )

        seoul = geographic_surface_vector(37.5665, 126.9780)
        tilt = np.radians(earth.axis_tilt_degrees)
        yaw = np.radians(rotation_y)
        after_tilt = np.array(
            [
                seoul[0],
                seoul[1] * np.cos(tilt) - seoul[2] * np.sin(tilt),
                seoul[1] * np.sin(tilt) + seoul[2] * np.cos(tilt),
            ],
            dtype=float,
        )
        world = np.array(
            [
                after_tilt[0] * np.cos(yaw) + after_tilt[2] * np.sin(yaw),
                after_tilt[1],
                -after_tilt[0] * np.sin(yaw) + after_tilt[2] * np.cos(yaw),
            ],
            dtype=float,
        )

        self.assertGreater(float(np.dot(world, scene_light)), 0.45)


if __name__ == "__main__":
    unittest.main()
