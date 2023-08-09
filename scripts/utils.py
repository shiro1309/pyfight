from scripts.settings import *


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