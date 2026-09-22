# Yas's ASCII Lab

An interactive 3D ASCII & dither art lab: upload a 3D model, image, or video and
render it live as ASCII text art, Bayer-matrix dithering, or noise dithering,
with a full set of presets, color palettes, lighting controls, and PNG/SVG/video
export.

## Running it

It's one static file — no install, no server required:

```bash
open index.html
```

or just double-click `index.html`, or serve the folder with any static file
server (e.g. `python3 -m http.server`) and open it in a browser.

## Features

- **Input**: 3D models (`.obj`, `.glb`, `.gltf`), images, and video, via click-to-upload or drag-and-drop
- **Effects**: ASCII (custom character sets, fonts, resolution, scale, 1- or 3-color mapping), Bayer dithering (2×2 to 16×16), and noise dithering
- **20 built-in presets** across ASCII, dither, and mixed styles, with hover-to-preview
- **Color palettes**: up to 7-color palettes with per-color toggle and reverse
- **Lighting controls**: directional angle and intensity
- **Camera**: zoom in/out buttons plus scroll/pinch zoom, reset-to-fit, auto-rotation toggle
- **Export**: PNG, true vector SVG (ASCII text or a dithered/solid color-block grid — see below), or video, at up to 4x scale
- **Custom pixel-art cursor**

## Project structure

```
index.html      the built, self-contained app — this is what you deploy/open
src/            readable source, organized the way the original React app was:
  app.js          state management + all UI wiring (ports App.tsx / ControlPanel.tsx)
  renderer.js     the Three.js scene/engine (ports ThreeJSRenderer.tsx)
  shaders.js      the GLSL effects: levels, ASCII, dither (ports utils/shaders.ts)
  presets.js      the 20 built-in presets (ports utils/presets.ts)
  three.js        Three.js + addons re-export (ports utils/three.ts)
  styles.css      all styling
  body.html       the page body markup
build.py        merges src/ into index.html — run after editing anything in src/
```

To make a change: edit the relevant file in `src/`, then run:

```bash
python3 build.py
```

which regenerates `index.html`.

## SVG export

Every effect type exports as true vector shapes, not a rasterized screenshot:

- **ASCII** samples the rendered frame and reproduces the shader's own
  luminance → character → color mapping as real `<text>` elements.
- **Bayer / Noise / None** are vectorized as a grid of solid-color `<rect>`
  elements sampled from the actual output — pixel-exact at smaller export
  sizes, a coarser (but still fully vector) mosaic at larger ones, to keep
  element counts sane.

Downloaded filenames say `-vector` or `-raster` so it's obvious which you got
(raster only happens if an ASCII grid would be too dense to vectorize
practically).

## Notes on fidelity

The core logic — the shader math, the Three.js scene setup, the preset data,
and all state/UI behavior — is a direct port of the original source and
matches it exactly. A few pieces were rebuilt from screenshots rather than
original source and are close-but-not-pixel-identical:

- The shadcn/Radix UI primitives (select, slider, switch, accordion, dialog) are
  reimplemented in plain HTML/CSS rather than the original component library.
- The custom cursor artwork (arrow + pointing-hand) **is** the real pixel-art
  from the original file, extracted from its vector path data.

One inherited quirk kept intentionally: video export is encoded as WebM but
named `.mp4` — that's what the original `ThreeJSRenderer.tsx` does.
