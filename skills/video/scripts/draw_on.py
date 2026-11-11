#!/usr/bin/env python3
"""Render a small, deterministic SVG draw-on sequence without dependencies."""
import argparse
import json
import math
from pathlib import Path
import re


def number(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'{name} debe estar entre {low} y {high}')
    return float(value)


def render(data, count):
    width = int(number(data.get('width', 1080), 'width', 1, 4096))
    height = int(number(data.get('height', 1920), 'height', 1, 4096))
    strokes = data.get('strokes')
    if not isinstance(strokes, list) or not 1 <= len(strokes) <= 100:
        raise ValueError('strokes debe contener entre 1 y 100 trazos')
    segments = []
    for stroke in strokes:
        if not isinstance(stroke, dict):
            raise ValueError('cada trazo debe ser un objeto')
        color = stroke.get('color', '#ffffff')
        if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
            raise ValueError('color debe ser #RRGGBB')
        thickness = number(stroke.get('width', 4), 'stroke width', 0.1, 100)
        points = stroke.get('points')
        if not isinstance(points, list) or not 2 <= len(points) <= 1000:
            raise ValueError('cada trazo requiere 2 a 1000 puntos')
        coords = []
        for point in points:
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError('cada punto debe ser [x,y] normalizado')
            coords.append((number(point[0], 'x', 0, 1) * width, number(point[1], 'y', 0, 1) * height))
        for a, b in zip(coords, coords[1:]):
            length = math.dist(a, b)
            if length:
                segments.append((a, b, length, color, thickness))
    if len(segments) > 2000:
        raise ValueError('máximo 2000 segmentos')
    total = sum(s[2] for s in segments)
    if not total:
        raise ValueError('los trazos no tienen longitud')
    for frame in range(count):
        remaining = total * frame / (count - 1)
        lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
        for (x1, y1), (x2, y2), length, color, thickness in segments:
            if remaining <= 0:
                break
            ratio = min(1, remaining / length)
            x, y = x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio
            lines.append(f'<path d="M {x1:.3f} {y1:.3f} L {x:.3f} {y:.3f}" fill="none" stroke="{color}" stroke-width="{thickness:g}" stroke-linecap="round"/>')
            remaining -= length
        lines.append('</svg>')
        yield '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='JSON con strokes y puntos normalizados')
    parser.add_argument('output', type=Path, help='directorio nuevo para SVG y manifest')
    parser.add_argument('--frames', type=int, default=30)
    parser.add_argument('--fps', type=int, default=30)
    args = parser.parse_args()
    if not 2 <= args.frames <= 600 or not 1 <= args.fps <= 120:
        parser.error('frames debe ser 2–600 y fps 1–120')
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('la entrada debe ser un objeto JSON')
        frames = list(render(data, args.frames))
        args.output.mkdir(parents=True, exist_ok=False)
        for i, svg in enumerate(frames):
            (args.output / f'frame_{i:04d}.svg').write_text(svg, encoding='utf-8')
        manifest = {'frames': args.frames, 'fps': args.fps, 'duration_seconds': args.frames / args.fps,
                    'pattern': 'frame_%04d.svg', 'background': 'transparent'}
        (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    except (ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
