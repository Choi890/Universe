from pathlib import Path
from types import SimpleNamespace
import sys
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from universe.main import AsteroidRuntime, BodyRuntime, MinorOrbitLabel, MoonRuntime, SolarSystemScene
from universe.solar_data import BodySpec, MoonSpec, RingSpec


class InspectVisibilityTests(unittest.TestCase):
    def make_body(self, key: str, with_ring: bool = False) -> BodyRuntime:
        ring = RingSpec(1.2, 2.1, (210, 190, 150, 120)) if with_ring else None
        return BodyRuntime(
            spec=BodySpec(key, key.title(), "planet", 1.0, 1.0, 1.0, (255, 255, 255), ring=ring),
            entity=SimpleNamespace(enabled=True, body_key=key),
            label=SimpleNamespace(enabled=True),
            visual_radius=1.0,
            position_au=np.zeros(3, dtype=float),
            ring_entities=[SimpleNamespace(enabled=True)] if ring else None,
        )

    def make_scene(self) -> SolarSystemScene:
        scene = SolarSystemScene.__new__(SolarSystemScene)
        scene.show_labels = True
        scene.show_moons = True
        scene.show_orbits = True
        scene.body_runtime = {
            "earth": self.make_body("earth"),
            "saturn": self.make_body("saturn", with_ring=True),
        }
        moon_spec = MoonSpec("moon", "Moon", "earth", 1.0, 1.0, 1.0, 1.0, (255, 255, 255))
        scene.moon_runtime = [MoonRuntime(moon_spec, SimpleNamespace(enabled=True), 1.0)]
        scene.asteroids = [AsteroidRuntime(SimpleNamespace(enabled=True), 2.4, 0.0, 0.0, 100.0, (0, 0, 0))]
        scene.orbit_entities = [SimpleNamespace(enabled=True)]
        scene.ecliptic_entities = [SimpleNamespace(enabled=True)]
        scene.minor_orbit_labels = [MinorOrbitLabel(SimpleNamespace(enabled=True), 1.0, None)]
        return scene

    def test_inspect_mode_keeps_solar_system_visible(self) -> None:
        scene = self.make_scene()
        scene.camera_mode = "inspect"
        scene.inspect_runtime = scene.body_runtime["saturn"]

        SolarSystemScene.apply_scene_visibility(scene)

        self.assertTrue(scene.body_runtime["earth"].entity.enabled)
        self.assertTrue(scene.body_runtime["saturn"].entity.enabled)
        self.assertTrue(scene.body_runtime["saturn"].ring_entities[0].enabled)
        self.assertTrue(scene.body_runtime["saturn"].label.enabled)
        self.assertTrue(scene.moon_runtime[0].entity.enabled)
        self.assertTrue(scene.asteroids[0].entity.enabled)
        self.assertTrue(scene.orbit_entities[0].enabled)
        self.assertTrue(scene.ecliptic_entities[0].enabled)
        self.assertTrue(scene.minor_orbit_labels[0].entity.enabled)

    def test_orbit_mode_restores_system_visibility_flags(self) -> None:
        scene = self.make_scene()
        scene.camera_mode = "orbit"
        scene.inspect_runtime = None
        scene.show_labels = False
        scene.show_moons = False
        scene.show_orbits = False

        SolarSystemScene.apply_scene_visibility(scene)

        self.assertTrue(scene.body_runtime["earth"].entity.enabled)
        self.assertTrue(scene.body_runtime["saturn"].entity.enabled)
        self.assertTrue(scene.body_runtime["saturn"].ring_entities[0].enabled)
        self.assertFalse(scene.body_runtime["earth"].label.enabled)
        self.assertFalse(scene.moon_runtime[0].entity.enabled)
        self.assertTrue(scene.asteroids[0].entity.enabled)
        self.assertFalse(scene.orbit_entities[0].enabled)
        self.assertFalse(scene.ecliptic_entities[0].enabled)
        self.assertFalse(scene.minor_orbit_labels[0].entity.enabled)

    def test_left_click_selects_hovered_body_even_in_free_mode(self) -> None:
        scene = self.make_scene()
        scene.camera_mode = "free"
        scene.mouse = SimpleNamespace(hovered_entity=scene.body_runtime["earth"].entity, collisions=[])
        scene.runtime_from_cursor = lambda: None
        selected = []
        scene.enter_inspect_mode = selected.append

        SolarSystemScene.handle_body_click(scene)

        self.assertEqual(selected, [scene.body_runtime["earth"]])

    def test_left_click_prefers_cursor_pick_over_wrong_hovered_body(self) -> None:
        scene = self.make_scene()
        scene.camera_mode = "orbit"
        scene.mouse = SimpleNamespace(hovered_entity=scene.body_runtime["saturn"].entity, collisions=[])
        scene.runtime_from_cursor = lambda: scene.body_runtime["earth"]
        selected = []
        scene.enter_inspect_mode = selected.append

        SolarSystemScene.handle_body_click(scene)

        self.assertEqual(selected, [scene.body_runtime["earth"]])

    def test_left_click_ignores_body_while_already_inspecting(self) -> None:
        scene = self.make_scene()
        scene.camera_mode = "inspect"
        scene.mouse = SimpleNamespace(hovered_entity=scene.body_runtime["earth"].entity, collisions=[])
        scene.runtime_from_cursor = lambda: scene.body_runtime["earth"]
        selected = []
        scene.enter_inspect_mode = selected.append

        SolarSystemScene.handle_body_click(scene)

        self.assertEqual(selected, [])

    def test_inspect_drag_moves_view_with_mouse_direction(self) -> None:
        scene = self.make_scene()
        scene.view_yaw = 20.0
        scene.view_pitch = 10.0
        scene.inspect_yaw = 6.0
        scene.inspect_pitch = 8.0
        scene.inspect_roll = 0.0
        scene.held_keys = {}
        scene.mouse = SimpleNamespace(left=True, right=False, velocity=(0.10, 0.05))

        SolarSystemScene.update_inspect_controls(scene, 0.0)

        self.assertEqual(scene.view_yaw, 20.0)
        self.assertEqual(scene.view_pitch, 10.0)
        self.assertLess(scene.inspect_yaw, 6.0)
        self.assertLess(scene.inspect_pitch, 8.0)

    def test_inspect_z_x_adjusts_horizon_roll(self) -> None:
        scene = self.make_scene()
        scene.inspect_yaw = 0.0
        scene.inspect_pitch = 8.0
        scene.inspect_roll = 0.0
        scene.held_keys = {"x": 1, "z": 0, "r": 0}
        scene.mouse = SimpleNamespace(left=False, right=False, velocity=(0.0, 0.0))

        SolarSystemScene.update_inspect_controls(scene, 0.5)

        self.assertGreater(scene.inspect_roll, 0.0)

        scene.held_keys = {"x": 0, "z": 1, "r": 0}
        SolarSystemScene.update_inspect_controls(scene, 0.5)

        self.assertAlmostEqual(scene.inspect_roll, 0.0)

    def test_inspect_roll_stops_changing_when_z_x_released(self) -> None:
        scene = self.make_scene()
        scene.inspect_yaw = 0.0
        scene.inspect_pitch = 8.0
        scene.inspect_roll = 17.5
        scene.held_keys = {"x": 0, "z": 0, "r": 0}
        scene.mouse = SimpleNamespace(left=False, right=False, velocity=(0.0, 0.0))

        SolarSystemScene.update_inspect_controls(scene, 1.0)

        self.assertEqual(scene.inspect_roll, 17.5)

    def test_orbit_drag_moves_view_with_mouse_direction(self) -> None:
        scene = self.make_scene()
        scene.view_yaw = 20.0
        scene.view_pitch = 10.0
        scene.held_keys = {}
        scene.mouse = SimpleNamespace(right=True, velocity=(0.10, 0.05))

        SolarSystemScene.update_view_controls(scene, 0.0)

        self.assertLess(scene.view_yaw, 20.0)
        self.assertLess(scene.view_pitch, 10.0)

    def test_enter_inspect_mode_starts_from_planet_local_view(self) -> None:
        scene = self.make_scene()
        scene.view_yaw = 123.0
        scene.view_pitch = 41.0
        scene.inspect_yaw = 77.0
        scene.inspect_pitch = -32.0
        scene.inspect_roll = 19.0
        scene.camera_mode = "orbit"
        scene.follow_index = 1
        scene.view_distance = 999.0
        scene.set_mouse_locked = lambda locked: None
        scene.inspect_distance_for = lambda runtime: 12.0
        scene.show_reference_image = lambda runtime: None
        scene.apply_scene_visibility = lambda: None
        scene.update_camera = lambda force=False: None

        SolarSystemScene.enter_inspect_mode(scene, scene.body_runtime["earth"])

        self.assertEqual(scene.camera_mode, "inspect")
        self.assertIs(scene.inspect_runtime, scene.body_runtime["earth"])
        self.assertIsNone(scene.follow_index)
        self.assertEqual(scene.view_yaw, 123.0)
        self.assertEqual(scene.view_pitch, 41.0)
        self.assertEqual(scene.inspect_yaw, 0.0)
        self.assertEqual(scene.inspect_pitch, 8.0)
        self.assertEqual(scene.inspect_roll, 0.0)
        self.assertEqual(scene.view_distance, 12.0)


if __name__ == "__main__":
    unittest.main()
