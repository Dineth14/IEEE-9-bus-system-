from PIL import Image
import os

src = r"e:\University Files\SEM - 5\EE354 Power Engineering\EE-354 Power Engineering\IEEE-9-bus-system-\Report\9bus.jpg"
dst = r"e:\University Files\SEM - 5\EE354 Power Engineering\EE-354 Power Engineering\IEEE-9-bus-system-\Report\9bus.png"

try:
    with Image.open(src) as img:
        img.save(dst, "PNG")
    print(f"Converted {src} to {dst}")
except Exception as e:
    print(f"Error converting: {e}")
