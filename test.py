from scripts.settings import *

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
        print(self.scroll)
    
    def render(self, surface):
        tiles = math.ceil(DISPLAY[0] / self.bg_width) + 2
        for layer in range(self.layers):
            for i in range(tiles):
                surface.blit(self.images[layer],(i*self.bg_width - self.bg_width + self.scroll[layer],0))

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

pg.init()
screen = pg.display.set_mode(WIN_RES)
Display = pg.Surface(DISPLAY)


paralax = Paralax("paralax", 4)
start_time = time.time()

movment = [False, False]

movment_val = 0

while True:
    Display.fill((255,255,255))
    
    delta_time = (time.time() - start_time )
    start_time = time.time()

    paralax.update((movment[0] - movment[1]), delta_time)
    paralax.render(Display)

    movment_val += (movment[0] - movment[1])
    #print(movment_val, "      ", paralax.scroll, "       ", math.ceil(DISPLAY[0] / paralax.bg_width) + 2)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                movment[0] = True
            if event.key == pg.K_d:
                movment[1] = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_a:
                movment[0] = False
            if event.key == pg.K_d:
                movment[1] = False

    
    
    
    surf = pg.transform.scale(Display, WIN_RES)
    screen.blit(pg.transform.flip(surf, False, False), (0,0))
    pg.display.update()