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
        self.scroll = []
        for i in range(layers):
            self.layer_loc.append([0,0])
        for i in range(layers):
            self.scroll.append(0)
        
        
    def update(self, direction, delta):
        speed = .2
        for i , layer_pos in enumerate(self.layer_loc):
            layer_pos[0] += speed * delta * direction
            self.scroll[i] += direction * speed
            speed += .2
            if abs(self.scroll[i]) >= self.bg_width:
                self.scroll[i] = 0
    
    def render(self, surface):
        tiles = math.ceil(DISPLAY[0] / self.bg_width) + 2
        for layer in range(self.layers):
            for i in range(tiles):
                surface.blit(self.images[layer],(i*self.bg_width - self.bg_width + self.scroll[layer],0))
                
def death_win():
    pass

class Text:
    def __init__(self, text, font, color, x, y):
        self.x = x
        self.y = y
        self.text_content = font.render(text, False, color)
    
    def render(self, surface, offset=(0, 0)):
        surface.blit(self.text_content, (self.x - offset[0], self.y - offset[1]))
        
class TextButton:
    def __init__(self, x, y, text,):
        self.text = text
        self.rect = self.text.text_content.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    
    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
        
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def render(self, surface, offset=(0,0)):
        pg.draw.rect(surface, (100,100,100), (self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height))
        surface.blit(self.text.text_content, (self.rect.x - offset[0], self.rect.y - offset[1]))
        
class ImageButton:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                print("helle")
        
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def render(self, surface, offset=(0,0)):
        pg.draw.rect(surface, (100,100,100), (self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height))
        surface.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))