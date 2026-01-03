import csv
import mercantile
import requests
from PIL import Image, ImageDraw
from io import BytesIO

bbox = (-68.77, -31.05, -68.74, -31.01)
#bbox = (-68.77, -31.03, -68.745, -31.01) contexto proximo
#bbox = (-68.75, -31.027, -68.745, -31.019) solo talacasto
zoom = 17
csv_file = "Grid"
tile_url = (
        "https://services.arcgisonline.com/ArcGis/rest/services/"
        "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)
tiles = list(mercantile.tiles(*bbox, zoom))
print("Tiles to download:", len(tiles))
images = {}
xs  = []
ys  = []

for t in tiles:
    url = tile_url.format(z=t.z, x=t.x, y=t.y)
    r   = requests.get(url)
    img = Image.open(BytesIO(r.content))
    images[(t.x, t.y)] = img
    xs.append(t.x)
    ys.append(t.y)

tile_size = 256
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
width = (max_x - min_x + 1) * tile_size
height= (max_y - min_y + 1) * tile_size
map_img = Image.new("RGB", (width, height))

for (x, y), img in images.items():
    px = (x - min_x) * tile_size
    py = (y - min_y) * tile_size
    map_img.paste(img, (px, py))

draw = ImageDraw.Draw(map_img)
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        lat = float(row["Lat"])
        lon = float(row["Lon"])
        tile= mercantile.tile(lon, lat, zoom)
        x_frac, y_frac = mercantile.xy(lon, lat)
        left, bottom, right, top = mercantile.xy_bounds(tile)
        px  = int((x_frac - left) / (right - left) * tile_size)
        py  = int((top - y_frac) / (top - bottom) * tile_size)
        x_img = (tile.x - min_x) * tile_size + px
        y_img = (tile.y - min_y) * tile_size + py
        r = 5
        draw.ellipse(
            (x_img - r, y_img - r, x_img + r, y_img + r),
            fill="red",
            outline="black")


map_img.save("satelital_image.png")
print("Image saved: satelital_image.png")




