#!/usr/bin/env python3
"""Catalogue auto des images, à la racine ou dans bibliotheque-images/originaux."""
import hashlib
import io
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote
from PIL import Image, ImageOps, UnidentifiedImageError

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SRC = HERE / "originaux"
THUMBS = HERE / "miniatures"
CATALOGUE = HERE / "catalogue.json"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
MAX_SIZE = 30 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 50_000_000
EXCLUDED_ROOT = {".git", ".github", "bibliotheque-images"}
REPO_RAW = "https://raw.githubusercontent.com/mini56/Kaloneo-MAJ/main/"

def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "image"

def discovered_files():
    result = []
    for p in REPO.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in EXTS:
            continue
        rel = p.relative_to(REPO)
        if rel.parts[0] in {".git", ".github"}:
            continue
        if rel.parts[0] == "bibliotheque-images" and (len(rel.parts) < 2 or rel.parts[1] != "originaux"):
            continue
        if p.is_symlink():
            continue
        result.append(p)
    return sorted(result, key=lambda p: p.relative_to(REPO).as_posix().casefold())

def classify(rel, known):
    parts = rel.parts
    # An image in bibliotheque-images/originaux/<category>/...
    if parts[0] == "bibliotheque-images":
        category = parts[2] if len(parts) > 3 else "divers"
    # An image in a category folder at the root
    else:
        category = parts[0] if len(parts) > 1 else "divers"
        # Root folders such as Horizontales, Verticales, Carrees:
        # use descriptive filename prefix, rather than orientation.
        if slug(category) in {"horizontales", "verticales", "carrees"}:
            match = re.match(r"(.+?)_[HVC]_\d+$", rel.stem, re.I)
            if match:
                category = match.group(1)
            else:
                category = "divers"
    code = slug(category)
    if code not in known:
        known[code] = {"id": code, "nom": category.replace("_", " ").replace("-", " ")}
    return code

def main():
    data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    known = {c["id"]: c for c in data.get("categories", [])}
    THUMBS.mkdir(parents=True, exist_ok=True)
    entries, wanted = [], set()
    for p in discovered_files():
        rel = p.relative_to(REPO)
        size = p.stat().st_size
        if size > MAX_SIZE:
            raise ValueError(f"Image trop lourde ({size} octets): {rel}")
        category = classify(rel, known)
        # Path hash prevents clashes between identically named files in different folders.
        ident = f"{category}-{slug(p.stem)}-{hashlib.sha256(rel.as_posix().encode()).hexdigest()[:10]}"
        # Nom de miniature court, sans repeter la categorie deja presente dans le fichier.
        # Le suffixe court empeche les collisions entre dossiers.
        thumb_name = f"{slug(p.stem)}-{hashlib.sha256(rel.as_posix().encode()).hexdigest()[:8]}.webp"
        thumb = THUMBS / thumb_name
        try:
            with Image.open(p) as im:
                if im.format not in ("PNG", "JPEG", "WEBP", "GIF", "BMP"):
                    raise ValueError(f"Format non pris en charge: {rel}")
                im = ImageOps.exif_transpose(im)
                im.thumbnail((240, 240), Image.Resampling.LANCZOS)
                if im.mode not in ("RGB", "RGBA"):
                    im = im.convert("RGBA" if "transparency" in im.info else "RGB")
                out = io.BytesIO()
                im.save(out, format="WEBP", quality=78, method=6)
            if not thumb.exists() or thumb.read_bytes() != out.getvalue():
                thumb.write_bytes(out.getvalue())
        except (UnidentifiedImageError, OSError) as ex:
            raise ValueError(f"Image illisible: {rel}") from ex
        wanted.add(thumb)
        entries.append({
            "id": ident,
            "titre": p.stem.replace("_", " ").replace("-", " "),
            "categorie": category,
            "miniature": f"miniatures/{thumb.name}",
            # Absolute URLs handle images outside the catalogue directory.
            "fichier": REPO_RAW + quote(rel.as_posix(), safe="/"),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "taille_octets": size
        })
    for old in THUMBS.glob("*.webp"):
        if old not in wanted:
            old.unlink()
    data["categories"] = sorted(known.values(), key=lambda x: x["nom"].casefold())
    data["images"] = entries
    CATALOGUE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Catalogue: {len(entries)} image(s), {len(data['categories'])} catégories")

if __name__ == "__main__":
    main()
