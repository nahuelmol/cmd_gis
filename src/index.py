import csv
import mercantile
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import pandas as pd

from src.scrap import extract

class Map:
    def __init__(self, maptype):
        self.bbox = extract('box')
        #bbox = (-68.765, -31.05, -68.74, -31.01) contexto con sierra
        #bbox = (-68.77, -31.03, -68.74, -31.01) 
        #bbox = (-68.75, -31.027, -68.745, -31.01) baños 
        
        #default values
        self.zoom = 17
        self.csv_file = "Grid"
        SERVICES = [
            "https://services.arcgisonline.com/ArcGis/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}",

            "https://api.mapbox.com/styles/v1/{username}/{style_id}/static/"
            "{overlay}/{lon},{lat},{zoom},{bearing},{pitch}|{bbox}|{auto}/{width}x{height}?{access_token}"
        ]
        self.service = "ARCGIS"
        self.tile_url = SERVICES[0]
        self.tiles = list(mercantile.tiles(*self.bbox, self.zoom))
        self.images = {}
        self.xs  = []
        self.ys  = []
        self.tile_size = 256
        self.r = 5
        self.img = None
        self.map_img = None

        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

        self.px = None
        self.py = None
        self.mapname = ''

    def base(self):
        print("Tiles to download:", len(self.tiles))
        for t in self.tiles:
            if self.service == "ARCGIS":
                self.url = self.tile_url.format(z=t.z, x=t.x, y=t.y)
            elif self.service == "MAPBOX":
                self.url = self.tile_url.format( username=self.username,
                                            style_id="satellite-v9",
                                            overlay=0,
                                            lon=0,
                                            lat=0,
                                            zoom=self.zoom,
                                            bearing=0,
                                            pitch=0,
                                            bbox=self.bbox,
                                            auto=0,
                                            width=400,
                                            height=400)
            else:
                return False, 'not recognized service'

            #headers = {"User-Agent":"Mozilla/5.0"}
            r   = requests.get(self.url)
            img = Image.open(BytesIO(r.content))
            self.images[(t.x, t.y)] = img
            self.xs.append(t.x)
            self.ys.append(t.y)

        self.min_x, self.max_x = min(self.xs), max(self.xs)
        self.min_y, self.max_y = min(self.ys), max(self.ys)
        width = (self.max_x - self.min_x + 1) * self.tile_size
        height= (self.max_y - self.min_y + 1) * self.tile_size
        self.map_img = Image.new("RGB", (width, height))

        for (x, y), img in self.images.items():
            self.px = (x - self.min_x) * self.tile_size
            self.py = (y - self.min_y) * self.tile_size
            self.map_img.paste(img, (self.px, self.py))
        self.mapname = "base.png"

    def add_profiles(self):
        lon_min, lat_min, lon_max, lat_max = extract('box')
        lat_origin = lat_max
        lon_origin = lon_min
        self.map_img    = Image.open("base.png").convert("RGB")
        draw            = ImageDraw.Draw(self.map_img)
        width, height   = self.map_img.size
        lat_width = lat_max-lat_min
        lon_width = lon_max-lon_min

        self.csv_file = "Grid"
        data = pd.read_csv(self.csv_file)
        for row in data.itertuples(index=False):
            lon_d   = abs(row[4]) - abs(lon_origin)
            lat_d   = abs(row[5]) - abs(lat_origin)
            font    = ImageFont.load_default()
            nst     = row[0]
            tw, th  = font.getmask(str(nst)).size
            offset  = 4
            r = 6
            #3's rule
            y = (height/ lat_width) * abs(lat_d)
            x = (width / lon_width) * abs(lon_d)

            text_x = x - tw // 2
            text_y = y - r - th - offset
            x1 = text_x-1
            y1 = text_y-1
            x2 = text_x+tw+2
            y2 = text_y+th+2
            draw.rectangle((x1, y1, x2, y2), fill="white", outline="white")
            draw.text((text_x, text_y), str(nst), fill="black", font=font)
            draw.ellipse(
                (x - r, 
                 y - r, 
                 x + r, 
                 y + r),
                fill="red",
                outline="black")
        self.mapname = 'map_with_points.png'

    def sheet(self):
        lon_min, lat_min, lon_max, lat_max = extract('box')
        #inlat = 0.004
        #inlon = 0.004
        lat_origin = lat_max
        lon_origin = lon_min
        self.map_img    = Image.open("base.png").convert("RGB")
        draw            = ImageDraw.Draw(self.map_img)
        width, height   = self.map_img.size
        nlines = 3
        stepx = width / (nlines+1)
        stepy = height/ (nlines+1)
        acx = 0
        acy = 0
        for i in range(nlines):
            acx = acx + stepx
            acy = acy + stepy
            xline = (acx, 0, acx, height)
            yline = (0, acy, width, acy)
            draw.line(xline, fill="black", width=2)
            draw.line(yline, fill="black", width=2)
        self.mapname = 'map_with_sheet.png'

    def zebra(self):
        lon_min, lat_min, lon_max, lat_max = extract('box')
        #inlat = 0.004
        #inlon = 0.004
        lat_origin = lat_max
        lon_origin = lon_min
        self.map_img    = Image.open("base.png").convert("RGB")
        draw            = ImageDraw.Draw(self.map_img)
        width, height   = self.map_img.size
        nlines = 4
        stepx = width / (nlines)
        stepy = height/ (nlines)
        acx = 0
        acy = 0
        color = "black"
        for i in range(nlines):
            lineu  = (acx, 0, acx + stepx, 0)
            lined  = (acx, height, acx + stepx, height)
            linel  = (0, acy, 0, acy + stepy)
            liner  = (width, acy, width, acy + stepy)
            draw.line(lineu, fill=color, width=16)
            draw.line(lined, fill=color, width=16)
            draw.line(linel, fill=color, width=16)
            draw.line(liner, fill=color, width=16)
            if color == "black":
                color = "white"
            else:
                color = "black"
            acx = acx + stepx
            acy = acy + stepy
        self.mapname = 'map_with_zebra.png'

    def legend(self):
        imagename = "base"
        self.map_img    = Image.open('{}.png'.format(imagename))
        width, height   = self.map_img.size
        draw = ImageDraw.Draw(self.map_img)

        fontsize = 40
        margin   = 40
        location_fb = height - (fontsize + margin)
        try:
            font = ImageFont.truetype("arial.ttf", fontsize)
        except IOError:
            font = ImageFont.load_default() 
            print("Specific font not found, using default font.")

        text = "This is an exmaple legend!"
        margin_x = 40
        position = (margin_x, location_fb) 
        text_color = (0, 0, 0)

        background_color = "white"
        left, top, right, bottom = draw.textbbox(position, text, font=font)
        draw.rectangle((left, top, right, bottom), fill=background_color)
        draw.text(position, text, fill=text_color, font=font)
        self.mapname = '{}_with_legend.png'.format(imagename)

    def scalebar(self):
        imagname = "base"
        lon_min, lat_min, lon_max, lat_max = extract('box')
        self.map_img    = Image.open('{}.png'.format(imagname))
        draw = ImageDraw.Draw(self.map_img)
        width, height   = self.map_img.size
        self.mapname = '{}_with_scalebar.png'.format(imagname)

        fontsize = 40
        text_margin = 10
        try:
            font = ImageFont.truetype("arial.ttf", fontsize)
        except IOError:
            font = ImageFont.load_default() 
            print("Specific font not found, using default font.")

        #100 = 0.0009
        lond = abs(lon_max - lon_min)
        px50 = 0.0009 * (width/lond)
        xmargin = 20
        white_l = width - ((px50*2) + xmargin)
        white_r = width - (px50 + xmargin)
        black_l = width - (px50 + xmargin)
        black_r = width - xmargin
        ymargin = 20
        top = height - (20 + ymargin)
        bottom = height - (ymargin)
        draw.rectangle((white_l, top, white_r, bottom), fill="white")
        draw.rectangle((black_l, top, black_r, bottom), fill="black")
        font_loc = top - (fontsize + text_margin)
        position = (black_l, font_loc) 
        text = "100m"
        left, top, right, bottom = draw.textbbox(position, text, font=font)
        draw.text(position, text, fill="black", font=font)

    
    def save(self):
        self.map_img.save(self.mapname)
        print("Image saved: {}".format(self.mapname))

if __name__ == "__main__":
    command = None
    if (len(sys.argv) > 0):
        command = Command(sys.argv)
    else:
        msg = 'please, be serious, type a valid command'
        sys.exit(msg)
    command.setCommand()
    res, msg = command
