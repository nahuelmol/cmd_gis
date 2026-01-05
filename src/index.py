import csv
import mercantile
import requests
from PIL import Image, ImageDraw
from io import BytesIO

from src.scrap import extract

class Map:
    def __init__(self, maptype):
        self.bbox = extract('box')
        #bbox = (-68.77, -31.05, -68.74, -31.01)
        #bbox = (-68.77, -31.03, -68.745, -31.01) contexto proximo
        #bbox = (-68.75, -31.027, -68.745, -31.019) solo talacasto
        
        #default values
        self.zoom = 17
        self.csv_file = "Grid"
        self.tile_url = (
                "https://services.arcgisonline.com/ArcGis/rest/services/"
                "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        )
        self.tiles = list(mercantile.tiles(*self.bbox, self.zoom))
        print("Tiles to download:", len(self.tiles))
        self.images = {}
        self.xs  = []
        self.ys  = []
        self.tile_size = 256
        self.r = 5
        self.img = {}
        self.map_img = None

    def base(self):
        for t in self.tiles:
            url = self.tile_url.format(z=t.z, x=t.x, y=t.y)
            r   = requests.get(url)
            img = Image.open(BytesIO(r.content))
            self.images[(t.x, t.y)] = img
            self.xs.append(t.x)
            self.ys.append(t.y)

        min_x, max_x = min(self.xs), max(self.xs)
        min_y, max_y = min(self.ys), max(self.ys)
        width = (max_x - min_x + 1) * self.tile_size
        height= (max_y - min_y + 1) * self.tile_size
        self.map_img = Image.new("RGB", (width, height))

    def with_stats(self):
        for (x, y), img in self.images.items():
            px = (x - min_x) * self.tile_size
            py = (y - min_y) * self.tile_size
            self.map_img.paste(img, (px, py))

        draw = ImageDraw.Draw(self.map_img)
        with open(self.csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lat = float(row["Lat"])
                lon = float(row["Lon"])
                tile= mercantile.tile(lon, lat, self.zoom)
                x_frac, y_frac = mercantile.xy(lon, lat)
                left, bottom, right, top = mercantile.xy_bounds(tile)
                px  = int((x_frac - left) / (right - left) * self.tile_size)
                py  = int((top - y_frac) / (top - bottom) * self.tile_size)
                x_img = (tile.x - min_x) * self.tile_size + px
                y_img = (tile.y - min_y) * self.tile_size + py
                draw.ellipse(
                    (x_img - self.r, 
                     y_img - self.r, 
                     x_img + self.r, 
                     y_img + self.r),
                    fill="red",
                    outline="black")

    def save(self):
        self.map_img.save("finished.png")
        print("Image saved: finished.png")

if __name__ == "__main__":
    command = None
    if (len(sys.argv) > 0):
        command = Command(sys.argv)
    else:
        msg = 'please, be serious, type a valid command'
        sys.exit(msg)
    command.setCommand()
    res, msg = command.setArgs()
    if res == True:
        print(msg)
    res, msg = switch(command)
    print(msg)

