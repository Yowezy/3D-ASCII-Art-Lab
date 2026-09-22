#!/usr/bin/env python3
"""
Builds index.html from the readable sources in src/.

The app ships as one self-contained HTML file (so it can be opened
directly, hosted on GitHub Pages, or dropped anywhere as a static file),
but the JS is authored as separate ES modules under src/ for readability.
This script inlines them in dependency order and writes index.html.

Usage:
    python3 build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
THREE_VERSION = "0.160.0"


def strip_exports_and_imports(text: str, import_lines: list[str]) -> str:
    for line in import_lines:
        text = text.replace(line, "")
    return re.sub(r"(?m)^export (const|class|function)", r"\1", text)


def main() -> None:
    shaders = strip_exports_and_imports(
        (SRC / "shaders.js").read_text(),
        ["import * as THREE from './three.js';\n"],
    )
    renderer = strip_exports_and_imports(
        (SRC / "renderer.js").read_text(),
        [
            "import { THREE, OrbitControls, OBJLoader, GLTFLoader, EffectComposer, RenderPass, ShaderPass } from './three.js';\n",
            "import { LevelsEffect, ASCIIEffect, DitherEffect, createAsciiCharTexture, createPaletteTexture } from './shaders.js';\n",
        ],
    )
    presets = re.sub(r"(?m)^export (const|function)", r"\1", (SRC / "presets.js").read_text())
    app = (SRC / "app.js").read_text()

    merged = "\n".join([
        "// ===== three.js core + addons (CDN, pinned version) =====",
        "import * as THREE from 'three';",
        "import { OrbitControls } from 'three/addons/controls/OrbitControls.js';",
        "import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';",
        "import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';",
        "import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';",
        "import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';",
        "import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';",
        "",
        shaders.strip(),
        "",
        renderer.strip(),
        "",
        presets.strip(),
        "",
        app.strip(),
        "",
    ])

    css = (SRC / "styles.css").read_text()
    body = (SRC / "body.html").read_text()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>Yas's ASCII Lab</title>
<meta name="description" content="Interactive 3D ASCII &amp; dither lab — upload a 3D model, image, or video and render it as live ASCII art or dithered color output." />
<style>
{css}
</style>
<script type="importmap">
{{
  "imports": {{
    "three": "https://cdn.jsdelivr.net/npm/three@{THREE_VERSION}/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@{THREE_VERSION}/examples/jsm/"
  }}
}}
</script>
</head>
<body>
{body}
<script type="module">
{merged}
</script>
</body>
</html>
"""

    out = ROOT / "index.html"
    out.write_text(html)
    print(f"Wrote {out} ({len(html.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
