from __future__ import annotations

import io
import html
from collections import deque
from pathlib import Path
import math
import random
import re
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parents[1]
TEXTURE_DIR = ROOT / "assets" / "textures"


TEXTURE_URLS = {
    "mercury": "https://maps.jpl.nasa.gov/tmaps/pix/mer0muu2.jpg",
    "venus": "https://maps.jpl.nasa.gov/tmaps/pix/ven0ajj2.jpg",
    "mars": "https://maps.jpl.nasa.gov/tmaps/pix/mar0kuu2.jpg",
    "jupiter": "https://maps.jpl.nasa.gov/tmaps/pix/jup0vss1.jpg",
    "saturn": "https://maps.jpl.nasa.gov/tmaps/pix/sat0fds1.jpg",
    "uranus": "https://maps.jpl.nasa.gov/tmaps/pix/ura0fss1.jpg",
    "neptune": "https://maps.jpl.nasa.gov/tmaps/pix/nep0fds1.jpg",
    "pluto": "https://maps.jpl.nasa.gov/tmaps/pix/plu0rss1.jpg",
    "phobos": "https://maps.jpl.nasa.gov/tmaps/pix/mar1kuu2.jpg",
    "deimos": "https://maps.jpl.nasa.gov/tmaps/pix/mar2kuu2.jpg",
    "io": "https://maps.jpl.nasa.gov/tmaps/pix/jup1vss2.jpg",
    "europa": "https://maps.jpl.nasa.gov/tmaps/pix/jup2vss2.jpg",
    "ganymede": "https://maps.jpl.nasa.gov/tmaps/pix/jup3vss2.jpg",
    "callisto": "https://maps.jpl.nasa.gov/tmaps/pix/jup4vss2.jpg",
    "enceladus": "https://maps.jpl.nasa.gov/tmaps/pix/sat2vss2.jpg",
    "titan": "https://maps.jpl.nasa.gov/tmaps/pix/sat6fss1.jpg",
    "iapetus": "https://maps.jpl.nasa.gov/tmaps/pix/sat8vss2.jpg",
    "titania": "https://maps.jpl.nasa.gov/tmaps/pix/ura3vuu2.jpg",
    "triton": "https://maps.jpl.nasa.gov/tmaps/pix/nep1vuu2.jpg",
}


JPL_TIFF_URLS = {
    "mercury": "https://maps.jpl.nasa.gov/tmaps/pix/mer0muu2.tif",
    "mars": "https://maps.jpl.nasa.gov/tmaps/pix/mar0kuu2.tif",
    "pluto": "https://maps.jpl.nasa.gov/tmaps/pix/plu0rss1.tif",
}


NASA_EARTH_URLS = {
    "earth": "https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg",
    "earth_night_source": "https://eoimages.gsfc.nasa.gov/images/imagerecords/79000/79765/dnb_land_ocean_ice.2012.13500x6750.jpg",
    "earth_clouds_source": "https://eoimages.gsfc.nasa.gov/images/imagerecords/57000/57747/cloud_combined_2048.jpg",
}


SUN_SOURCE_IMAGE_URL = (
    "https://assets.science.nasa.gov/dynamicimage/assets/science/psd/photojournal/pia/pia26/pia26681/"
    "PIA26681.jpg?crop=faces%2Cfocalpoint&fit=clip&h=4096&w=4096"
)
VENUS_SOURCE_IMAGE_URL = "https://science.nasa.gov/wp-content/uploads/2023/05/venus-single.png"


NASA_IMAGE_URLS = {
    "sun_source": SUN_SOURCE_IMAGE_URL,
    "venus_source": VENUS_SOURCE_IMAGE_URL,
    "jupiter_source": "https://science.nasa.gov/wp-content/uploads/2023/09/PIA07782.jpg",
}


NASA_REFERENCE_PAGES = {
    "saturn_source": "https://science.nasa.gov/photojournal/saturn-in-color/",
    "uranus_source": "https://science.nasa.gov/photojournal/uranus-final-image/",
    "neptune_source": "https://science.nasa.gov/photojournal/neptune-true-color-of-clouds/",
    "asteroid_source": "https://science.nasa.gov/resource/bennu-mosaic/",
}


NASA_ASTEROID_IMAGE_URLS = {
    "vesta": "https://images-assets.nasa.gov/image/PIA14778/PIA14778~orig.jpg",
    "ida": "https://images-assets.nasa.gov/image/PIA00135/PIA00135~orig.jpg",
    "mathilde": "https://images-assets.nasa.gov/image/PIA02477/PIA02477~orig.jpg",
    "eros": "https://images-assets.nasa.gov/image/PIA02467/PIA02467~orig.jpg",
    "gaspra": "https://images-assets.nasa.gov/image/PIA00119/PIA00119~orig.jpg",
    "bennu": (
        "https://assets.science.nasa.gov/content/dam/science/psd/solar/2023/09/b/"
        "bennu_dec10.jpg/jcr:content/renditions/cq5dam.web.1280.1280.jpeg"
    ),
}


ASTEROID_CUTOUT_THICKNESS = {
    "vesta": 0.54,
    "ida": 0.36,
    "mathilde": 0.48,
    "eros": 0.31,
    "gaspra": 0.38,
    "bennu": 0.50,
}


PALETTES = {
    "sun": ((255, 224, 98), (255, 119, 24), (255, 247, 180)),
    "moon": ((104, 104, 100), (173, 171, 164), (62, 62, 60)),
    "ceres": ((83, 79, 72), (145, 136, 122), (55, 52, 48)),
    "rhea": ((133, 132, 128), (205, 204, 197), (72, 72, 70)),
    "miranda": ((121, 124, 120), (193, 198, 191), (66, 68, 67)),
    "oberon": ((82, 79, 76), (146, 143, 136), (45, 43, 42)),
}


def download(url: str, destination: Path, *, overwrite: bool = False, minimum_bytes: int = 2048) -> None:
    if not overwrite and destination.exists() and destination.stat().st_size > minimum_bytes:
        return
    request = urllib.request.Request(url, headers={"User-Agent": "UniverseTextureFetcher/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        destination.write_bytes(response.read())


def download_image_as_jpeg(url: str, destination: Path, *, overwrite: bool = False, minimum_bytes: int = 2048) -> None:
    if not overwrite and destination.exists() and destination.stat().st_size > minimum_bytes:
        return
    request = urllib.request.Request(url, headers={"User-Agent": "UniverseTextureFetcher/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
    image = Image.open(io.BytesIO(data)).convert("RGB")
    image.save(destination, quality=94)


def download_page_image(page_url: str, destination: Path, *, overwrite: bool = False) -> None:
    if not overwrite and destination.exists() and destination.stat().st_size > 2048:
        return
    request = urllib.request.Request(page_url, headers={"User-Agent": "UniverseTextureFetcher/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8", "ignore")

    match = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', page)
    if not match:
        raise RuntimeError(f"No og:image found at {page_url}")

    image_url = html.unescape(match.group(1))
    download_image_as_jpeg(image_url, destination, overwrite=True, minimum_bytes=2048)


def smooth_noise(width: int, height: int, seed: int, scale: int = 5) -> np.ndarray:
    rng = np.random.default_rng(seed)
    data = rng.random((height, width), dtype=np.float32)
    image = Image.fromarray(np.uint8(data * 255), "L")
    for radius in (scale, scale * 2, scale * 4):
        image = image.filter(ImageFilter.GaussianBlur(radius=radius))
    return np.asarray(image, dtype=np.float32) / 255.0


def save_rgb(path: Path, rgb: np.ndarray, quality: int = 94) -> None:
    Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB").save(path, quality=quality)


def reference_mean_color(source: Path | None, fallback: tuple[int, int, int]) -> np.ndarray:
    if not source or not source.exists():
        return np.array(fallback, dtype=np.float32)
    image = Image.open(source).convert("RGB").resize((256, 256), Image.Resampling.LANCZOS)
    data = np.asarray(image, dtype=np.float32)
    brightness = data.mean(axis=2)
    mask = brightness > 18.0
    if not np.any(mask):
        return np.array(fallback, dtype=np.float32)
    return data[mask].mean(axis=0)


def grade_to_reference(rgb: np.ndarray, source: Path | None, strength: float = 0.35) -> np.ndarray:
    if not source or not source.exists():
        return rgb
    target = reference_mean_color(source, (180, 180, 180))
    current = np.maximum(rgb.reshape(-1, 3).mean(axis=0), 1.0)
    ratio = np.clip(target / current, 0.45, 1.85)
    return rgb * (1.0 - strength) + rgb * ratio * strength


def generate_venus_visible(path: Path, source: Path | None = None, width: int = 4096, height: int = 2048) -> None:
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :]
    lat = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    noise = smooth_noise(width, height, 612, 13)
    detail = smooth_noise(width, height, 613, 5)
    streaks = 0.5 + 0.5 * np.sin((x * 9.5 + lat * 2.4 + noise * 0.85) * math.tau)
    belts = 0.5 + 0.5 * np.sin((lat * 7.5 + detail * 0.42) * math.tau)
    contrast = np.clip(0.58 * streaks + 0.34 * belts + 0.38 * detail, 0.0, 1.0)

    base = np.array([222, 184, 113], dtype=np.float32)
    bright = np.array([252, 226, 165], dtype=np.float32)
    shadow = np.array([175, 126, 72], dtype=np.float32)
    rgb = shadow + (bright - shadow) * contrast[:, :, None]
    polar_haze = np.clip((np.abs(lat) - 0.58) / 0.35, 0.0, 1.0)
    rgb = rgb * (1.0 - polar_haze[:, :, None] * 0.18) + base * polar_haze[:, :, None] * 0.18
    rgb = grade_to_reference(rgb, source, 0.30)
    save_rgb(path, rgb)


def generate_saturn_visible(path: Path, source: Path | None = None, width: int = 4096, height: int = 2048) -> None:
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :]
    lat = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    noise = smooth_noise(width, height, 711, 19)
    detail = smooth_noise(width, height, 712, 7)
    broad = np.sin((lat * 5.2 + noise * 0.20) * math.tau)
    fine = np.sin((lat * 23.0 + x * 0.75 + detail * 0.35) * math.tau)
    band = np.clip(0.50 + 0.20 * broad + 0.12 * fine + 0.18 * detail, 0.0, 1.0)

    cream = np.array([221, 198, 145], dtype=np.float32)
    gold = np.array([192, 158, 100], dtype=np.float32)
    pale = np.array([244, 225, 176], dtype=np.float32)
    rgb = gold + (pale - gold) * band[:, :, None]
    equator = np.exp(-(lat / 0.28) ** 2)
    rgb = rgb * (1.0 - equator[:, :, None] * 0.20) + cream * equator[:, :, None] * 0.20
    polar = np.clip((np.abs(lat) - 0.68) / 0.32, 0.0, 1.0)
    rgb *= 1.0 - polar[:, :, None] * 0.16
    rgb = grade_to_reference(rgb, source, 0.28)
    save_rgb(path, rgb)


def generate_uranus_visible(path: Path, source: Path | None = None, width: int = 4096, height: int = 2048) -> None:
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :]
    lat = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    noise = smooth_noise(width, height, 811, 21)
    band = 0.5 + 0.5 * np.sin((lat * 7.0 + noise * 0.22 + x * 0.10) * math.tau)
    polar = np.clip((np.abs(lat) - 0.45) / 0.55, 0.0, 1.0)
    base = np.array([148, 211, 210], dtype=np.float32)
    pale = np.array([188, 236, 230], dtype=np.float32)
    shadow = np.array([102, 170, 180], dtype=np.float32)
    rgb = shadow + (pale - shadow) * (0.56 + 0.16 * band + 0.22 * polar)[:, :, None]
    rgb = grade_to_reference(rgb, source, 0.42)
    save_rgb(path, rgb)


def generate_neptune_visible(path: Path, source: Path | None = None, width: int = 4096, height: int = 2048) -> None:
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :]
    lat = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    noise = smooth_noise(width, height, 911, 17)
    detail = smooth_noise(width, height, 912, 5)
    bands = 0.5 + 0.5 * np.sin((lat * 10.0 + noise * 0.34 + x * 0.25) * math.tau)
    base = np.array([74, 116, 178], dtype=np.float32)
    deep = np.array([40, 76, 138], dtype=np.float32)
    pale = np.array([128, 178, 220], dtype=np.float32)
    rgb = deep + (pale - deep) * (0.48 + 0.22 * bands + 0.16 * detail)[:, :, None]

    image = Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB")
    draw = ImageDraw.Draw(image, "RGBA")
    rng = random.Random(922)
    for _ in range(28):
        lon = rng.random() * width
        lat_px = int(height * rng.uniform(0.22, 0.78))
        length = rng.randrange(120, 440)
        thickness = rng.randrange(4, 16)
        draw.ellipse((lon - length, lat_px - thickness, lon + length, lat_px + thickness), fill=(220, 235, 255, rng.randrange(22, 78)))
    dark_x = int(width * 0.62)
    dark_y = int(height * 0.58)
    draw.ellipse((dark_x - 150, dark_y - 55, dark_x + 150, dark_y + 55), fill=(22, 45, 96, 95))
    image = image.filter(ImageFilter.GaussianBlur(0.75))
    if source and source.exists():
        rgb = np.asarray(image, dtype=np.float32)
        image = Image.fromarray(np.uint8(np.clip(grade_to_reference(rgb, source, 0.32), 0, 255)), "RGB")
    image.save(path, quality=94)


def generate_asteroid_texture(path: Path, source: Path | None = None, width: int = 1024, height: int = 512) -> None:
    base_noise = smooth_noise(width, height, 1003, 4)
    detail_noise = smooth_noise(width, height, 1009, 1)

    if source and source.exists():
        reference = Image.open(source).convert("L").resize((width, height), Image.Resampling.LANCZOS)
        reference_data = np.asarray(reference, dtype=np.float32) / 255.0
    else:
        reference_data = base_noise

    tone = np.clip(reference_data * 0.55 + base_noise * 0.30 + detail_noise * 0.25, 0.0, 1.0)
    low = np.array([45, 43, 41], dtype=np.float32)
    high = np.array([151, 146, 136], dtype=np.float32)
    rgb = low + (high - low) * tone[:, :, None]
    image = Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB")
    draw = ImageDraw.Draw(image, "RGBA")
    rng = random.Random(1007)
    for _ in range(520):
        x = rng.randrange(width)
        y = rng.randrange(height)
        r = int(rng.triangular(1, 24, 5))
        shade = rng.randrange(24, 92)
        draw.ellipse((x - r, y - r, x + r, y + r), outline=(22, 22, 22, shade), width=max(1, r // 6))
        if r > 5:
            draw.arc((x - r, y - r, x + r, y + r), 215, 30, fill=(215, 210, 198, shade), width=max(1, r // 7))
    image.filter(ImageFilter.GaussianBlur(0.18)).save(path, quality=92)


def estimate_solar_disk(data: np.ndarray) -> tuple[float, float, float]:
    height, width, _ = data.shape
    red = data[:, :, 0]
    green = data[:, :, 1]
    blue = data[:, :, 2]
    warm = (red > 34.0) & (green > 22.0) & (red > blue * 1.25) & (green > blue * 1.05)
    warm[int(height * 0.93) :, :] = False

    if not np.any(warm):
        radius = min(width, height) * 0.42
        return width * 0.5, height * 0.48, radius

    luminance = red * 0.46 + green * 0.44 + blue * 0.10
    weights = np.where(warm, np.clip(luminance - 20.0, 0.0, None), 0.0)
    y_indices, x_indices = np.indices((height, width), dtype=np.float32)
    total = float(weights.sum())
    center_x = float((x_indices * weights).sum() / total)
    center_y = float((y_indices * weights).sum() / total)

    distances = np.sqrt((x_indices[warm] - center_x) ** 2 + (y_indices[warm] - center_y) ** 2)
    radius = float(np.quantile(distances, 0.89) / math.sqrt(0.89))
    radius = max(min(width, height) * 0.28, min(radius, min(width, height) * 0.47))
    return center_x, center_y, radius


def bilinear_sample_rgb(data: np.ndarray, sample_x: np.ndarray, sample_y: np.ndarray) -> np.ndarray:
    height, width, _ = data.shape
    sample_x = np.clip(sample_x, 0.0, width - 1.001)
    sample_y = np.clip(sample_y, 0.0, height - 1.001)
    x0 = np.floor(sample_x).astype(np.int32)
    y0 = np.floor(sample_y).astype(np.int32)
    x1 = np.minimum(x0 + 1, width - 1)
    y1 = np.minimum(y0 + 1, height - 1)
    wx = (sample_x - x0).astype(np.float32)
    wy = (sample_y - y0).astype(np.float32)

    top = data[y0, x0] * (1.0 - wx[..., None]) + data[y0, x1] * wx[..., None]
    bottom = data[y1, x0] * (1.0 - wx[..., None]) + data[y1, x1] * wx[..., None]
    return top * (1.0 - wy[..., None]) + bottom * wy[..., None]


def estimate_planet_disk(data: np.ndarray) -> tuple[float, float, float]:
    height, width, _ = data.shape
    luminance = data[:, :, 0] * 0.299 + data[:, :, 1] * 0.587 + data[:, :, 2] * 0.114
    threshold = max(10.0, float(np.quantile(luminance, 0.78)) * 0.42)
    mask = luminance > threshold
    if not np.any(mask):
        radius = min(width, height) * 0.42
        return width * 0.5, height * 0.5, radius

    weights = np.where(mask, np.clip(luminance - threshold, 0.0, None) + 1.0, 0.0)
    y_indices, x_indices = np.indices((height, width), dtype=np.float32)
    total = float(weights.sum())
    center_x = float((x_indices * weights).sum() / total)
    center_y = float((y_indices * weights).sum() / total)

    distances = np.sqrt((x_indices[mask] - center_x) ** 2 + (y_indices[mask] - center_y) ** 2)
    radius = float(np.quantile(distances, 0.94))
    radius = max(min(width, height) * 0.22, min(radius, min(width, height) * 0.49))
    return center_x, center_y, radius


def flatten_source_lighting(rgb: np.ndarray, strength: float = 0.72) -> np.ndarray:
    image = Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB")
    broad = image.filter(ImageFilter.GaussianBlur(radius=max(18, min(image.size) // 12)))
    data = np.asarray(image, dtype=np.float32)
    smooth = np.asarray(broad, dtype=np.float32)
    lum = np.maximum(data[:, :, 0] * 0.299 + data[:, :, 1] * 0.587 + data[:, :, 2] * 0.114, 1.0)
    smooth_lum = np.maximum(smooth[:, :, 0] * 0.299 + smooth[:, :, 1] * 0.587 + smooth[:, :, 2] * 0.114, 1.0)
    target_lum = float(np.median(lum))
    correction = np.clip(target_lum / smooth_lum, 0.55, 1.85) ** strength
    return np.clip(data * correction[:, :, None], 0, 255)


def fill_dark_space_background(rgb: np.ndarray) -> np.ndarray:
    luminance = rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114
    threshold = max(5.0, min(34.0, float(np.quantile(luminance, 0.86)) * 0.18))
    surface = luminance > threshold
    if np.count_nonzero(surface) < rgb.shape[0] * rgb.shape[1] * 0.02:
        return rgb

    filled = rgb.copy()
    median_surface = np.median(rgb[surface], axis=0)
    dark = ~surface
    filled[dark] = median_surface
    return filled


def asteroid_mask_from_rgb(rgb: np.ndarray) -> Image.Image:
    luminance = rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114
    threshold = max(9.0, min(56.0, float(np.quantile(luminance, 0.90)) * 0.35))
    mask = luminance > threshold
    mask = center_connected_component(mask)
    image = Image.fromarray(np.uint8(mask) * 255, "L")
    image = image.filter(ImageFilter.MedianFilter(5))
    image = image.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(5))
    return image


def center_connected_component(mask: np.ndarray) -> np.ndarray:
    if not np.any(mask):
        return mask
    height, width = mask.shape
    ys, xs = np.nonzero(mask)
    center_x = width * 0.5
    center_y = height * 0.5
    seed_index = int(np.argmin((xs - center_x) ** 2 + (ys - center_y) ** 2))
    seed = (int(ys[seed_index]), int(xs[seed_index]))

    visited = np.zeros_like(mask, dtype=bool)
    component = np.zeros_like(mask, dtype=bool)
    queue: deque[tuple[int, int]] = deque([seed])
    visited[seed] = True
    while queue:
        y, x = queue.popleft()
        if not mask[y, x]:
            continue
        component[y, x] = True
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if ny < 0 or ny >= height or nx < 0 or nx >= width or visited[ny, nx]:
                continue
            visited[ny, nx] = True
            if mask[ny, nx]:
                queue.append((ny, nx))
    return component if np.any(component) else mask


def expanded_bbox(bbox: tuple[int, int, int, int], size: tuple[int, int], padding_ratio: float = 0.08) -> tuple[int, int, int, int]:
    left, top, right, bottom = bbox
    width, height = size
    padding = int(max(right - left, bottom - top) * padding_ratio)
    return (
        max(0, left - padding),
        max(0, top - padding),
        min(width, right + padding),
        min(height, bottom + padding),
    )


def radial_shape_boundary(mask: Image.Image, samples: int = 192) -> tuple[list[list[float]], tuple[float, float]]:
    data = np.asarray(mask, dtype=np.uint8) > 24
    height, width = data.shape
    y_indices, x_indices = np.indices((height, width), dtype=np.float32)
    if not np.any(data):
        boundary = []
        for index in range(samples):
            angle = math.tau * index / samples
            x = math.cos(angle)
            y = math.sin(angle)
            boundary.append([x, y, 0.5 + x * 0.5, 0.5 - y * 0.5])
        return boundary, (0.5, 0.5)

    center_x = float(x_indices[data].mean())
    center_y = float(y_indices[data].mean())
    half_extent = max(width, height) * 0.5
    max_radius = math.hypot(width, height)
    step_count = max(80, int(max_radius * 1.4))
    radii = np.linspace(0.0, max_radius, step_count, dtype=np.float32)
    boundary = []

    for index in range(samples):
        angle = math.tau * index / samples
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        sample_x = np.rint(center_x + cos_a * radii).astype(np.int32)
        sample_y = np.rint(center_y + sin_a * radii).astype(np.int32)
        inside = (sample_x >= 0) & (sample_x < width) & (sample_y >= 0) & (sample_y < height)
        hits = np.where(inside & data[np.clip(sample_y, 0, height - 1), np.clip(sample_x, 0, width - 1)])[0]
        if hits.size:
            hit_index = int(hits[-1])
            x = float(sample_x[hit_index])
            y = float(sample_y[hit_index])
        else:
            x = center_x + cos_a * half_extent * 0.62
            y = center_y + sin_a * half_extent * 0.62
        scene_x = (x - center_x) / half_extent
        scene_y = -(y - center_y) / half_extent
        u = max(0.0, min(1.0, x / max(1.0, width - 1.0)))
        v = max(0.0, min(1.0, 1.0 - y / max(1.0, height - 1.0)))
        boundary.append([scene_x, scene_y, u, v])

    center_uv = (
        max(0.0, min(1.0, center_x / max(1.0, width - 1.0))),
        max(0.0, min(1.0, 1.0 - center_y / max(1.0, height - 1.0))),
    )
    return boundary, center_uv


def generate_asteroid_cutout_and_shape(source: Path, cutout_path: Path, key: str, max_size: int = 1024) -> dict[str, object]:
    image = Image.open(source).convert("RGBA")
    rgb = np.asarray(image.convert("RGB"), dtype=np.float32)
    mask = asteroid_mask_from_rgb(rgb)
    bbox = mask.getbbox()
    if not bbox:
        bbox = (0, 0, image.width, image.height)
    bbox = expanded_bbox(bbox, image.size)

    image = image.crop(bbox)
    mask = mask.crop(bbox)
    scale = min(1.0, max_size / max(image.width, image.height))
    if scale < 1.0:
        size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
        image = image.resize(size, Image.Resampling.LANCZOS)
        mask = mask.resize(size, Image.Resampling.LANCZOS)

    alpha = mask.filter(ImageFilter.GaussianBlur(1.0))
    alpha = Image.eval(alpha, lambda value: 0 if value < 18 else min(255, int((value - 18) * 1.18)))
    cutout = image.convert("RGBA")
    cutout.putalpha(alpha)
    cutout.save(cutout_path)

    boundary, center_uv = radial_shape_boundary(alpha)
    return {
        "boundary": boundary,
        "center_uv": center_uv,
        "thickness": ASTEROID_CUTOUT_THICKNESS.get(key, 0.42),
        "source": source.name,
        "cutout": cutout_path.name,
    }


def generate_reprojected_planet_texture(
    path: Path,
    source: Path,
    width: int = 4096,
    height: int = 2048,
    *,
    sample_scale: float = 0.82,
    flatten_lighting: bool = True,
    disk: tuple[float, float, float] | None = None,
    fill_space_background: bool = False,
) -> None:
    image = Image.open(source).convert("RGB")
    source_data = np.asarray(image, dtype=np.float32)
    center_x, center_y, radius = disk if disk else estimate_planet_disk(source_data)
    if fill_space_background:
        source_data = fill_dark_space_background(source_data)

    lon = np.linspace(-math.pi, math.pi, width, endpoint=False, dtype=np.float32)
    output = np.empty((height, width, 3), dtype=np.float32)
    chunk_size = 128
    for row_start in range(0, height, chunk_size):
        row_end = min(height, row_start + chunk_size)
        v = (np.arange(row_start, row_end, dtype=np.float32) + 0.5) / height
        lat = (0.5 - v) * math.pi
        surface_x = np.cos(lat)[:, None] * np.sin(lon)[None, :]
        surface_y = np.sin(lat)[:, None]
        sample_x = center_x + surface_x * radius * sample_scale
        sample_y = center_y - surface_y * radius * sample_scale
        output[row_start:row_end] = bilinear_sample_rgb(source_data, sample_x, sample_y)

    if flatten_lighting:
        output = flatten_source_lighting(output)
    Image.fromarray(np.uint8(np.clip(output, 0, 255)), "RGB").filter(ImageFilter.GaussianBlur(0.10)).save(path, quality=96)


def generate_sun(path: Path, source: Path | None = None, width: int = 4096, height: int = 2048, *, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        return

    if source and source.exists():
        source_image = Image.open(source).convert("RGB")
        source_data = np.asarray(source_image, dtype=np.float32)
        center_x, center_y, radius = estimate_solar_disk(source_data)

        lon = np.linspace(-math.pi, math.pi, width, endpoint=False, dtype=np.float32)
        output = np.empty((height, width, 3), dtype=np.float32)
        chunk_size = 128
        for row_start in range(0, height, chunk_size):
            row_end = min(height, row_start + chunk_size)
            v = (np.arange(row_start, row_end, dtype=np.float32) + 0.5) / height
            lat = (0.5 - v) * math.pi
            surface_x = np.cos(lat)[:, None] * np.sin(lon)[None, :]
            surface_y = np.sin(lat)[:, None]
            sample_x = center_x + surface_x * radius * 0.62
            sample_y = center_y - surface_y * radius * 0.62
            output[row_start:row_end] = bilinear_sample_rgb(source_data, sample_x, sample_y)

        detail = smooth_noise(width, height, 47, 4)
        granulation = smooth_noise(width, height, 53, 1)
        output *= 0.96 + detail[:, :, None] * 0.12 + granulation[:, :, None] * 0.055
        output = np.clip(output * 1.10, 0, 255)
        Image.fromarray(np.uint8(output), "RGB").filter(ImageFilter.GaussianBlur(0.12)).save(path, quality=96)
        return

    granules = smooth_noise(width, height, 11, 2)
    cells = smooth_noise(width, height, 29, 9)
    magnetic = smooth_noise(width, height, 47, 21)
    lat = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    bands = 0.08 * np.sin(np.linspace(0, math.tau * 34, height, dtype=np.float32))[:, None]
    heat = np.clip(0.50 + granules * 0.58 + cells * 0.32 + magnetic * 0.22 + bands - np.abs(lat) * 0.07, 0, 1)
    rgb = np.dstack([
        np.clip(210 + heat * 45, 0, 255),
        np.clip(58 + heat * 165, 0, 255),
        np.clip(4 + heat * 78, 0, 255),
    ]).astype(np.float32)
    rgb = grade_to_reference(rgb, source, 0.18)
    Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB").filter(ImageFilter.GaussianBlur(0.28)).save(path, quality=94)


def generate_sun_glow(path: Path, size: int = 1536, *, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        return

    axis = np.linspace(-1.0, 1.0, size, dtype=np.float32)
    x = axis[None, :]
    y = axis[:, None]
    radius = np.sqrt(x * x + y * y)
    falloff = (
        np.exp(-(radius / 0.16) ** 2) * 0.58
        + np.exp(-(radius / 0.36) ** 2) * 0.34
        + np.exp(-(radius / 0.82) ** 2) * 0.18
    )
    edge_fade = np.clip((1.0 - radius) / 0.22, 0.0, 1.0)
    alpha = np.clip(falloff * edge_fade * 255.0, 0, 230)

    tint = np.clip(radius, 0.0, 1.0)[:, :, None]
    center = np.array([255, 248, 210], dtype=np.float32)
    mid = np.array([255, 178, 48], dtype=np.float32)
    edge = np.array([255, 104, 18], dtype=np.float32)
    rgb = center * (1.0 - np.minimum(tint * 2.0, 1.0)) + mid * np.minimum(tint * 2.0, 1.0)
    rgb = rgb * (1.0 - np.maximum((tint - 0.48) / 0.52, 0.0)) + edge * np.maximum((tint - 0.48) / 0.52, 0.0)

    image = Image.fromarray(np.dstack([np.uint8(np.clip(rgb, 0, 255)), np.uint8(alpha)]), "RGBA")
    image.filter(ImageFilter.GaussianBlur(1.4)).save(path)


def generate_clouds(path: Path, tint: tuple[int, int, int], seed: int, opacity: int = 170) -> None:
    if path.exists():
        return
    width, height = 2048, 1024
    base = smooth_noise(width, height, seed, 9)
    detail = smooth_noise(width, height, seed + 41, 3)
    lat = np.linspace(-1.0, 1.0, height, dtype=np.float32)[:, None]
    mask = np.clip(base * 1.45 + detail * 0.75 - 0.82 - np.abs(lat) * 0.18, 0, 1)
    alpha = np.uint8(np.clip(mask**1.7 * opacity, 0, 255))
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[:, :, 0] = tint[0]
    rgb[:, :, 1] = tint[1]
    rgb[:, :, 2] = tint[2]
    Image.fromarray(np.dstack([rgb, alpha]), "RGBA").filter(ImageFilter.GaussianBlur(0.45)).save(path)


def convert_cloud_map(source: Path, destination: Path) -> None:
    if not source.exists():
        return

    image = Image.open(source).convert("L")
    if image.width != 2048 or image.height != 1024:
        image = image.resize((2048, 1024), Image.Resampling.LANCZOS)

    cloud = np.asarray(image, dtype=np.float32) / 255.0
    alpha = np.uint8(np.clip((cloud - 0.10) / 0.72, 0.0, 1.0) ** 1.25 * 210)
    rgb = np.full((image.height, image.width, 3), 255, dtype=np.uint8)
    Image.fromarray(np.dstack([rgb, alpha]), "RGBA").filter(ImageFilter.GaussianBlur(0.35)).save(destination)


def resize_rgb_texture(source: Path, destination: Path, size: tuple[int, int]) -> None:
    if not source.exists():
        return
    image = Image.open(source).convert("RGB")
    if image.size != size:
        image = image.resize(size, Image.Resampling.LANCZOS)
    data = np.asarray(image, dtype=np.uint8).copy()
    Image.fromarray(data, "RGB").save(destination, quality=92)


def generate_night_lights(day_path: Path, destination: Path) -> None:
    if destination.exists() and destination.stat().st_size > 2048:
        return

    width, height = 2048, 1024
    base = Image.new("RGB", (width, height), (0, 0, 0))
    if day_path.exists():
        day = Image.open(day_path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
        data = np.asarray(day, dtype=np.float32) / 255.0
        blue = data[:, :, 2]
        green = data[:, :, 1]
        red = data[:, :, 0]
        land = np.clip((green + red * 0.8 - blue * 1.25 - 0.05) * 2.2, 0.0, 1.0)
        dim_land = np.uint8(land[:, :, None] * np.array([16, 12, 8], dtype=np.float32))
        base = Image.fromarray(dim_land, "RGB")

    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow, "RGBA")
    cities = [
        (-74.0, 40.7, 19), (-118.2, 34.1, 13), (-87.6, 41.9, 14), (-95.4, 29.8, 10),
        (-0.1, 51.5, 17), (2.4, 48.9, 16), (13.4, 52.5, 13), (37.6, 55.8, 13),
        (31.2, 30.0, 16), (44.4, 33.3, 10), (77.2, 28.6, 17), (72.9, 19.1, 16),
        (116.4, 39.9, 17), (121.5, 31.2, 18), (114.1, 22.3, 14), (139.7, 35.7, 18),
        (126.9, 37.6, 14), (103.8, 1.35, 13), (151.2, -33.9, 12), (28.0, -26.2, 10),
        (-46.6, -23.6, 14), (-58.4, -34.6, 12), (-99.1, 19.4, 14), (30.5, 50.4, 10),
    ]
    rng = random.Random(501)
    for lon, lat, size in cities:
        x = int((lon + 180.0) / 360.0 * width)
        y = int((90.0 - lat) / 180.0 * height)
        for radius, alpha in ((size * 4, 22), (size * 2, 52), (size, 185)):
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(255, 198, 92, alpha))
        for _ in range(size * 8):
            px = int(rng.gauss(x, size * 3.0)) % width
            py = max(0, min(height - 1, int(rng.gauss(y, size * 1.6))))
            draw.point((px, py), fill=(255, 224, 138, rng.randrange(90, 210)))

    glow = glow.filter(ImageFilter.GaussianBlur(1.1))
    base = Image.alpha_composite(base.convert("RGBA"), glow).convert("RGB")
    base.save(destination, quality=90)


def generate_cratered(path: Path, palette: tuple[tuple[int, int, int], ...], seed: int) -> None:
    if path.exists():
        return
    width, height = 2048, 1024
    low, mid, high = palette
    noise = smooth_noise(width, height, seed, 5)
    detail = smooth_noise(width, height, seed + 3, 2)
    tone = np.clip(noise * 0.65 + detail * 0.45, 0, 1)
    rgb = np.zeros((height, width, 3), dtype=np.float32)
    for channel in range(3):
        rgb[:, :, channel] = low[channel] * (1 - tone) + high[channel] * tone
    image = Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB")
    draw = ImageDraw.Draw(image, "RGBA")
    rng = random.Random(seed)
    for _ in range(1400):
        x = rng.randrange(width)
        y = rng.randrange(height)
        r = int(rng.triangular(2, 42, 7))
        shade = rng.randrange(20, 95)
        draw.ellipse((x - r, y - r, x + r, y + r), outline=(30, 30, 30, shade), width=max(1, r // 7))
        if r > 8:
            draw.arc((x - r, y - r, x + r, y + r), 210, 35, fill=(240, 240, 230, shade), width=max(1, r // 8))
    image.filter(ImageFilter.GaussianBlur(radius=0.25)).save(path, quality=90)


def make_assets() -> None:
    TEXTURE_DIR.mkdir(parents=True, exist_ok=True)
    for key, url in TEXTURE_URLS.items():
        destination = TEXTURE_DIR / f"{key}.jpg"
        try:
            download(url, destination)
            print(f"downloaded {key}")
        except Exception as exc:
            print(f"skipped {key}: {exc}")

    for key, url in JPL_TIFF_URLS.items():
        destination = TEXTURE_DIR / f"{key}.jpg"
        try:
            download_image_as_jpeg(url, destination, overwrite=True, minimum_bytes=64_000)
            print(f"downloaded {key} tiff")
        except Exception as exc:
            print(f"skipped {key} tiff: {exc}")

    for key, url in NASA_EARTH_URLS.items():
        suffix = ".png" if url.endswith(".png") else ".jpg"
        destination = TEXTURE_DIR / f"{key}{suffix}"
        try:
            download(url, destination, overwrite=True, minimum_bytes=64_000)
            print(f"downloaded {key}")
        except Exception as exc:
            print(f"skipped {key}: {exc}")

    for key, url in NASA_IMAGE_URLS.items():
        destination = TEXTURE_DIR / f"{key}.jpg"
        try:
            download_image_as_jpeg(url, destination, overwrite=True, minimum_bytes=64_000)
            print(f"downloaded {key}")
        except Exception as exc:
            print(f"skipped {key}: {exc}")

    for key, page_url in NASA_REFERENCE_PAGES.items():
        destination = TEXTURE_DIR / f"{key}.jpg"
        try:
            download_page_image(page_url, destination, overwrite=True)
            print(f"downloaded {key}")
        except Exception as exc:
            print(f"skipped {key}: {exc}")

    for key, url in NASA_ASTEROID_IMAGE_URLS.items():
        destination = TEXTURE_DIR / f"{key}_source.jpg"
        try:
            download_image_as_jpeg(url, destination, overwrite=True, minimum_bytes=8_000)
            print(f"downloaded {key}_source")
        except Exception as exc:
            print(f"skipped {key}_source: {exc}")

    generate_sun(TEXTURE_DIR / "sun.jpg", TEXTURE_DIR / "sun_source.jpg", overwrite=True)
    generate_sun_glow(TEXTURE_DIR / "sun_glow.png", overwrite=True)
    if (TEXTURE_DIR / "venus_source.jpg").exists():
        generate_reprojected_planet_texture(
            TEXTURE_DIR / "venus.jpg",
            TEXTURE_DIR / "venus_source.jpg",
            sample_scale=0.74,
            flatten_lighting=True,
        )
    if (TEXTURE_DIR / "jupiter_source.jpg").exists():
        resize_rgb_texture(TEXTURE_DIR / "jupiter_source.jpg", TEXTURE_DIR / "jupiter.jpg", (4096, 2048))
    for key in ("saturn", "uranus", "neptune"):
        texture_path = TEXTURE_DIR / f"{key}.jpg"
        resize_rgb_texture(texture_path, texture_path, (4096, 2048))
    for key in NASA_ASTEROID_IMAGE_URLS:
        source_path = TEXTURE_DIR / f"{key}_source.jpg"
        if source_path.exists():
            generate_reprojected_planet_texture(
                TEXTURE_DIR / f"{key}.jpg",
                source_path,
                width=2048,
                height=1024,
                sample_scale=0.88,
                flatten_lighting=True,
                fill_space_background=True,
            )
    generate_asteroid_texture(TEXTURE_DIR / "asteroid.jpg", TEXTURE_DIR / "asteroid_source.jpg")
    convert_cloud_map(TEXTURE_DIR / "earth_clouds_source.jpg", TEXTURE_DIR / "earth_clouds.png")
    generate_clouds(TEXTURE_DIR / "earth_clouds.png", (255, 255, 255), 101, 178)
    resize_rgb_texture(TEXTURE_DIR / "earth_night_source.jpg", TEXTURE_DIR / "earth_night.jpg", (5400, 2700))
    generate_night_lights(TEXTURE_DIR / "earth.jpg", TEXTURE_DIR / "earth_night.jpg")
    generate_clouds(TEXTURE_DIR / "venus_clouds.png", (255, 221, 160), 122, 210)

    for index, key in enumerate(("moon", "ceres", "rhea", "miranda", "oberon")):
        generate_cratered(TEXTURE_DIR / f"{key}.jpg", PALETTES[key], 200 + index * 17)


if __name__ == "__main__":
    make_assets()
