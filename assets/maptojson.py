import json
from pathlib import Path
from PIL import Image


# --------------------------------------------------
# Configuration
# --------------------------------------------------

WIDTH = 780
HEIGHT = 420

# Get the folder containing this Python script
script_dir = Path(__file__).resolve().parent

# Input and output files
image_path = script_dir / "worldmap.png"
output_path = script_dir / "worldmap.json"


# --------------------------------------------------
# Check that the image exists
# --------------------------------------------------

if not image_path.exists():
    raise FileNotFoundError(
        f"Could not find worldmap.png at:\n{image_path}"
    )


# --------------------------------------------------
# Open and resize the image
# --------------------------------------------------

print(f"Opening image: {image_path}")

with Image.open(image_path) as img:
    # Resize to 195x105
    img = img.resize((WIDTH, HEIGHT))

    # Convert to RGBA so we can read the alpha channel
    img_rgba = img.convert("RGBA")

    # --------------------------------------------------
    # Convert image to binary data
    # --------------------------------------------------
    #
    # Transparent pixel (alpha == 0) -> "0"
    # Non-transparent pixel (alpha > 0) -> "1"
    #

    binary_data = []

    for y in range(HEIGHT):
        row = ""

        for x in range(WIDTH):
            r, g, b, a = img_rgba.getpixel((x, y))

            if a == 0:
                row += "0"
            else:
                row += "1"

        binary_data.append(row)


# --------------------------------------------------
# Verify dimensions
# --------------------------------------------------

assert len(binary_data) == HEIGHT, (
    f"Expected {HEIGHT} rows, got {len(binary_data)}"
)

for y, row in enumerate(binary_data):
    assert len(row) == WIDTH, (
        f"Row {y} expected length {WIDTH}, got {len(row)}"
    )


# --------------------------------------------------
# Save as JSON
# --------------------------------------------------

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(binary_data, f, separators=(",", ":"))


# --------------------------------------------------
# Done
# --------------------------------------------------

print("Conversion complete!")
print(f"Input : {image_path}")
print(f"Output: {output_path}")
print(f"Size  : {WIDTH} x {HEIGHT}")
print(f"Rows  : {len(binary_data)}")
print(f"Cols  : {len(binary_data[0])}")
