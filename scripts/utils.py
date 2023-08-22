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
                if self.image.getpixel(cord) == (0, 255, 0, 255):
                    tilemap[str(x) + ";" + str(y)] = {"type": "vine", "variant": 0, "pos": (x,y)}
        return tilemap

class Animation:
    def __init__(self, images, image_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.image_duration = image_dur
        self.done = False
        self.frame = 0
        
    def copy(self):
        return Animation(self.images, self.image_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.image_duration * len(self.images))
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.image_duration)]
    
class Paralax:
    def __init__(self, path, layers=5):
        self.layers = layers
        self.images = load_images(path)
        self.layer_loc = []
        self.bg_width = self.images[0].get_width()
        self.scroll = 0
        for i in range(layers):
            self.layer_loc.append([0,0])
        
        
    def update(self, direction, delta):
        speed = 1
        self.scroll += direction
        for i , layer_pos in enumerate(self.layer_loc):
            layer_pos[0] += speed * delta * direction * 10
            speed += 0.2
        if abs(self.scroll) >= self.bg_width:
            self.scroll = 0
        if abs(self.scroll) >= self.bg_width - (self.bg_width * 2):
            self.scroll = 0
    
    def render(self, surface):
        for layer in range(self.layers):
            tiles = math.ceil(DISPLAY[0] / self.bg_width) + 2
            for i in range(tiles):
                surface.blit(self.images[layer],(round(self.layer_loc[layer][0] + ((i - 1) * self.bg_width) + self.scroll - self.bg_width, 0), 0))
                
def death_win():
    pass

class Text:
    def __init__(self, text, font, pos, color):
        self.text = text
        self.text_pos = pos
        self.color = color
        self.font = font
        
        self.text_content = self.font.render(text, False, color)
        self.text_rect = self.text_content.get_rect()
        self.text_rect.x = pos[0]
        self.text_rect.y = pos[1]
    
    def render(self, surface, offset=(0, 0)):
        surface.blit(self.text_content, (self.text_rect.x - offset[0], self.text_rect.y - offset[1]))
        
    