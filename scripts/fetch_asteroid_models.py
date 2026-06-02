from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "assets" / "models" / "asteroids"
STATIC_ASSETS_URL = "https://eyes.nasa.gov/assets/static/"


EYES_ASTEROID_MODELS = {
    "bennu": {
        "eyes_id": "101955_bennu",
        "url": "models/101955_bennu/Bennu.gltf",
        "rotate": {"x": 83.0, "z": -168.0},
    },
    "vesta": {
        "eyes_id": "4_vesta",
        "url": "models/4_vesta/4_vesta.gltf",
        "rotate": {"x": 90.0},
    },
    "eros": {
        "eyes_id": "433_eros",
        "url": "models/433_eros/433_eros.gltf",
    },
    "gaspra": {
        "eyes_id": "951_gaspra",
        "url": "models/951_gaspra/gaspra.gltf",
    },
    "ida": {
        "eyes_id": "243_ida",
        "url": "models/generic/asteroid_2/generic_asteroid_2.gltf",
        "rotate": {"y": 90.0},
        "scale": [18.6 * 1.3, 25.4 * 1.3, 77.74],
    },
    "mathilde": {
        "eyes_id": "253_mathilde",
        "url": "models/generic/asteroid_3/generic_asteroid_3.gltf",
        "scale": [33.0, 24.0, 23.0],
    },
}


def download(url: str, destination: Path, *, overwrite: bool = False) -> None:
    if destination.exists() and destination.stat().st_size > 0 and not overwrite:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "UniverseAsteroidModelFetcher/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        destination.write_bytes(response.read())


def download_model(key: str, config: dict[str, object], *, overwrite: bool = False) -> None:
    relative_url = str(config["url"])
    source_url = urljoin(STATIC_ASSETS_URL, relative_url)
    local_dir = MODEL_DIR / key
    local_gltf = local_dir / Path(relative_url).name
    download(source_url, local_gltf, overwrite=overwrite)

    data = json.loads(local_gltf.read_text(encoding="utf-8"))
    base_url = source_url.rsplit("/", 1)[0] + "/"
    for field in ("buffers", "images"):
        for item in data.get(field, []) or []:
            uri = item.get("uri")
            if not uri or uri.startswith("data:"):
                continue
            download(urljoin(base_url, uri), local_dir / uri, overwrite=overwrite)


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, config in EYES_ASTEROID_MODELS.items():
        download_model(key, config, overwrite=True)
        local_gltf = MODEL_DIR / key / Path(str(config["url"])).name
        manifest[key] = {
            **config,
            "local": local_gltf.relative_to(ROOT).as_posix(),
            "source": urljoin(STATIC_ASSETS_URL, str(config["url"])),
        }
        print(f"downloaded {key}: {local_gltf}")

    (MODEL_DIR / "eyes_asteroid_models.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
