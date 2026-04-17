# SVG Watermarking with Pillow and uv

This project demonstrates how to add an SVG watermark to a 16:9 image using the [Pillow](https://python-pillow.org/) library. Since Pillow doesn't natively render SVG files, we use `svglib` and `reportlab` to convert the SVG into a PNG-like object in memory before compositing it onto the main image.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your machine.
- An SVG file named `watermark.svg` (included in this repository).
- (Optional) An image named `input_image.png`. If not present, the script will generate a placeholder 1920x1080 "Steel Blue" background.

## Installation

Install the project dependencies and sync the virtual environment using `uv`:

```powershell
uv sync
```

This will automatically create a `.venv` directory and install `Pillow`, `svglib`, and `reportlab`.

## How to Run

Execute the script with `uv`:

```powershell
uv run main.py
```

### Script Features
- **Automatic SVG Conversion**: Converts SVG to a drawing using `svglib` and renders it via `reportlab` directly into a `BytesIO` buffer.
- **Dynamic Scaling**: Scales the watermark to 20% of the base image's width while maintaining the aspect ratio.
- **Smart Positioning**: Automatically places the watermark in the bottom-right corner with a configurable margin.
- **Fallback Support**: Creates a 16:9 placeholder image if the input file is missing, allowing you to test the watermarking logic immediately.

## Output

The result will be saved as `output_watermarked.png` in the project root.
