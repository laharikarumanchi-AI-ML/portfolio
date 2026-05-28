"""Generate the OG (Open Graph) social-preview image for the portfolio.

Run from the portfolio repo root:
    python scripts/make_og_image.py

Outputs `public/og-default.png` (1200 x 630 px) styled to match the
minimal-academic landing page: paper background, serif name in ink,
sans-serif sub-line in muted gray, thin rule.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --- design tokens (mirror src/styles/global.css) ---
PAPER = (250, 250, 247)   # #fafaf7
INK = (26, 26, 26)        # #1a1a1a
MUTED = (85, 85, 85)      # #555
RULE = (216, 216, 211)    # #d8d8d3

W, H = 1200, 630
MARGIN = 96

NAME = "Lahari Karumanchi"
TAGLINE = "Code-as-action agents · RAG · classical ML"
META = "Third-year CS @ CVR  ·  Recruiting for Summer 2026 ML/SWE internships"


def _try_fonts(candidates: list[tuple[str, int]]) -> ImageFont.FreeTypeFont:
    """Try each (path, size) pair in order; return the first that loads."""
    for path, size in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    # Last-resort default — bitmap font (will look bad but won't crash).
    return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # System serif candidates (macOS first, then a couple of generic linux paths).
    serif_big = _try_fonts([
        ("/System/Library/Fonts/Supplemental/Iowan Old Style.ttc", 92),
        ("/System/Library/Fonts/Supplemental/Charter.ttc", 92),
        ("/System/Library/Fonts/Supplemental/Georgia.ttf", 92),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 92),
    ])
    sans_mid = _try_fonts([
        ("/System/Library/Fonts/HelveticaNeue.ttc", 36),
        ("/System/Library/Fonts/Helvetica.ttc", 36),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36),
    ])
    sans_small = _try_fonts([
        ("/System/Library/Fonts/HelveticaNeue.ttc", 24),
        ("/System/Library/Fonts/Helvetica.ttc", 24),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24),
    ])

    # Layout: vertically centered block of name + tagline + rule + meta.
    name_y = 200
    draw.text((MARGIN, name_y), NAME, font=serif_big, fill=INK)

    tagline_y = name_y + 130
    draw.text((MARGIN, tagline_y), TAGLINE, font=sans_mid, fill=MUTED)

    # Thin rule
    rule_y = tagline_y + 80
    draw.line([(MARGIN, rule_y), (W - MARGIN, rule_y)], fill=RULE, width=2)

    # Meta line below the rule
    meta_y = rule_y + 24
    draw.text((MARGIN, meta_y), META, font=sans_small, fill=MUTED)

    out = Path(__file__).resolve().parent.parent / "public" / "og-default.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
