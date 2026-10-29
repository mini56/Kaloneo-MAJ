#!/usr/bin/env python3
"""Reconstruit miniatures et catalogue à partir des originaux déposés sur GitHub."""
import hashlib
import io
import json
import re
import unicodedata
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "originaux"
THUMBS = ROOT / "miniatures"
CATALOGUE = ROOT / "catalogue.json"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
MAX_SIZE = 30 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 50_000_000

def slug(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-") or "image"

def main():
    data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    allowed = {c["id"] for c in data["categories"]}
    THUMBS.mkdir(exist_ok=True)
    entries = []
    used = set()
    if not SRC.exists():
        raise SystemExit("Dossier originaux introuvable")
    originals = sorted((p for p in SRC.rglob("*") if p.is_file() and p.suffix.lower() in EXTS), key=lambda x: x.as_posix().casefold())
    wanted = set()
    for p in originals:
        rel = p.relative_to(SRC)
        category = rel.parts[0] if len(rel.parts) > 1 else "divers"
        if category not in allowed:
            raise ValueError(f"Catégorie inconnue {category!r} pour {p}; utiliser un sous-dossier autorisé")
        size = p.stat().st_size
        if size > MAX_SIZE:
            raise ValueError(f"Image trop volumineuse : {p}")
        name = slug(p.stem)
        ident = f"{category}-{name}"
        if ident in used:
            raise ValueError(f"Identifiant en double : {ident} ; renommer un fichier")
        used.add(ident)
        try:
            with Image.open(p) as im:
                if im.format not in ("PNG", "JPEG", "WEBP", "GIF", "BMP"):
                    raise ValueError(f"Format non pris en charge : {p}")
                im = ImageOps.exif_transpose(im)
                im.thumbnail((240, 240), Image.Resampling.LANCZOS)
                if im.mode not in ("RGB", "RGBA"):
                    im = im.convert("RGBA" if "transparency" in im.info else "RGB")
                out = io.BytesIO()
                im.save(out, format="WEBP", quality=78, method=6)
        except (UnidentifiedImageError, OSError) as e:
            raise ValueError(f"Image invalide : {p}") from e
        thumb = THUMBS / f"{ident}.webp"
        thumb.write_bytes(out.getvalue())
        wanted.add(thumb)
        entries.append({
            "id": ident,
            "titre": p.stem.replace("_", " ").replace("-", " "),
            "categorie": category,
            "miniature": thumb.relative_to(ROOT).as_posix(),
            "fichier": p.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "taille_octets": size
        })
    for old in THUMBS.glob("*.webp"):
        if old not in wanted:
            old.unlink()
    data["images"] = entries
    CATALOGUE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Catalogue généré : {len(entries)} image(s)")

if __name__ == "__main__":
    main()
