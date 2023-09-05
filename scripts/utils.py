from scripts.settings import *
from PIL import Image

BASE_IMAGE_PATH = "data/assets/"

def load_image(path):
    img = pg.image.load(BASE_IMAGE_PATH + path).convert_alpha()
    img.set_colorkey((0,0,255))
    return img

def load_images(path):
    images = []
    for image in sorted(os.listdir(BASE_IMAGE_PATH + path)):
        images.append(load_image(path + "/" + image))
    
    return images

class Animation:
    def __init__(self, images, image_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = image_dur
        self.done = False
        self.frame = 0
        
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]

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
        
        
    def update(self, direction, delta, wall_colide):
        speed = .2
        if wall_colide:
            for i in range(len(self.layer_loc)):
                self.scroll[i] += direction * speed * delta * 40
                speed += .2
                if abs(self.scroll[i]) >= self.bg_width:
                    self.scroll[i] = 0
    
    def render(self, surface):
        tiles = math.ceil(DISPLAY[0] / self.bg_width) + 2
        for layer in range(self.layers):
            for i in range(tiles):
                surface.blit(self.images[layer],(i*self.bg_width - self.bg_width + self.scroll[layer],0))

def adaptiv_surface(screen, Display, offset=(0,0)):
    ratio = 320 / 240
    screen_value = screen.get_size()
    screen_ratio = screen_value[0] / screen_value[1]
    window_ratio = (screen_ratio-ratio)

    if window_ratio > 0:
        win_val = screen_value[1] * ratio
        surf = pg.transform.scale(Display, (win_val, screen_value[1]))
    elif window_ratio < 0:
        win_val = screen_value[0] / ratio
        surf = pg.transform.scale(Display, (screen_value[0], win_val))
    else:
        surf = pg.transform.scale(Display, (screen_value[0], screen_value[1]))
    screen.blit(surf, (screen_value[0]//2-surf.get_width()//2 + offset[0],screen_value[1]//2-surf.get_height()//2+offset[1]))