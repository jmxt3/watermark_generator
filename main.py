import io
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def add_svg_watermark(base_image_path, svg_path, output_path, scale=0.12, margin=10):
    """
    Adds an SVG watermark to an image.

    :param base_image_path: Path to the 16:9 background image.
    :param svg_path: Path to the SVG watermark file.
    :param output_path: Path to save the watermarked image.
    :param scale: Scale of the watermark relative to the image width.
    :param margin: Margin from the top-left corner.
    """
    # 1. Load the base image
    try:
        base_img = Image.open(base_image_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading base image: {e}")
        # Create a placeholder 16:9 image if file not found
        print("Creating a placeholder 16:9 image (1920x1080)...")
        base_img = Image.new("RGBA", (1920, 1080), (73, 109, 137, 255))  # Steel Blue

    width, height = base_img.size

    # 2. Convert SVG to ReportLab drawing
    drawing = svg2rlg(svg_path)
    if drawing is None:
        print(f"Error: Could not load SVG from {svg_path}")
        return

    # 3. Render Drawing to a BytesIO object (PNG format)
    # We first render to a PNG in memory because Pillow can't directly handle ReportLab drawings
    img_data = io.BytesIO()
    renderPM.drawToFile(drawing, img_data, fmt="PNG", bg=None, backendFmt="RGBA")
    img_data.seek(0)

    # 4. Load the rendered watermark into Pillow
    watermark = Image.open(img_data).convert("RGBA")

    # 5. Scale the watermark
    # Scale based on the width of the base image
    wm_width = int(width * scale)
    wm_aspect_ratio = watermark.height / watermark.width
    wm_height = int(wm_width * wm_aspect_ratio)
    watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)

    # 6. Position the watermark (Top Left corner)
    position = (margin, margin)

    # 7. Composite the images
    # Create a new transparent layer for the watermark
    transparent = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    transparent.paste(watermark, position)

    # Alpha composite
    watermarked_img = Image.alpha_composite(base_img, transparent)

    # 8. Save the result
    watermarked_img.save(output_path)
    print(f"Successfully saved watermarked image to {output_path}")


def main():
    # Paths
    base_image = "input_image.png"  # This might not exist, script handles it
    svg_watermark = "watermark.svg"
    output_image = "output_watermarked.png"

    print("Starting SVG Watermarking process...")
    add_svg_watermark(base_image, svg_watermark, output_image)


if __name__ == "__main__":
    main()
