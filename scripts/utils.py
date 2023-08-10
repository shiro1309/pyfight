from scripts.settings import *
from PIL import Image

BASE_IMAGE_PATH = "data/assets/"

def load_image(path):
    img = pg.image.load(BASE_IMAGE_PATH + path).convert_alpha()
    img.set_colorkey((255,0,0))
    return img

def load_images(path):
    images = []
    for image in sorted(os.listdir(BASE_IMAGE_PATH + path)):
        images.append(load_image(path + "/" + image))
    
    return images

class Map_creation:
    def __init__(self, image_path):
        self.image = Image.open("data/" + image_path)
        self.map = self.image.load()
        self.height = self.image.height
        self.width = self.image.width

    def map_extraction(self):
        tilemap = {}
        for x in range(self.width):
            for y in range(self.height):
                cord = x,y
                if self.image.getpixel(cord) == (255, 255, 255, 255):
                    tilemap[str(x) + ";" + str(y)] = {"type": "grass", "variant": 0, "pos": (x,y)}
                if self.image.getpixel(cord) == (0, 0, 0, 255):
                    tilemap[str(x) + ";" + str(y)] = {"type": "dirt", "variant": 0, "pos": (x,y)}
        return tilemap    

class Animations:
    def __init__(self, images, image_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.image_dur = image_dur
        self.done = False
        self.frame = 0