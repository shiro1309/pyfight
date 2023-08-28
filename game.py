import time
import random

from scripts.settings import *
from scripts.entity import *
from scripts.utils import load_image, load_images, Map_creation, Animation, Paralax, Text, TextButton
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.menu import *
from scripts.rain import raindrop

class App:
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode(WIN_RES, pg.DOUBLEBUF)
        self.Display = pg.Surface(DISPLAY)
        
        self.movment = [False, False, False, False]
        
        self.clock = pg.time.Clock()
        self.delta_time = 0.0
        
        self.sprint = False
        self.sprint_check = False
        self.sprint_time = [2, 0]
        
        self.colors = {
            "red": (255,0,0),
            "green": (0, 255, 0),
            "blue" : (0, 0, 255)
        }
        
        self.fonts = {
            "fancy": pg.font.Font("data/assets/fonts/Bitmgothic.ttf", 32),
            "standard": pg.font.Font("data/assets/fonts/8bitlim.ttf", 32),
            "simple": pg.font.Font("data/assets/fonts/FFFFORWA.TTF", 32),
        }
        
        self.text = Text("how does it work?", self.fonts["standard"], self.colors["red"], 100, 100)
        
        self.assets = {
            "player": load_image("entity/player/player_13.png"),
            "clouds": load_images("clouds"),
            "grass": load_images("tile/grass"),
            "dirt": load_images("tile/dirt"),
            "vine": load_images("tile/vine"),
            "player/idle": Animation(load_images("entity/player/idle"), image_dur=3),
            "player/run" : Animation(load_images("entity/player/run"), image_dur= 2),
            "player/death" : Animation(load_images("entity/player/death"), image_dur=12),
            "player/jump" : Animation(load_images("entity/player/jump")),
        }
        
        self.menu = Menu(self, self.Display)
        self.menu_active = False
        
        self.paralax = Paralax("paralax", 4)
        #self.clouds = Clouds(self.assets["clouds"], count=0)
        
        self.player = Player(self, (100,50), (8,16))
        
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load("map.json")
        self.scroll = [0,0]
        
        self.animation_sum = 0.0
        
        self.start_time = time.time()
        
        self.raindrops = []
        self.rain_sum = 0.0
        self.test12 = TextButton(100, 100, self.text)
        
        
    def update(self):
        self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
 
        self.delta_time = time.time() - self.start_time
        self.start_time = time.time()
        
        #if self.movment[0]:
        #    self.player.velocity[0] = -.2
        #    if self.sprint:
        #        self.player.velocity[0] = -.4
        #if self.movment[2]:
        #    self.player.velocity[0] = .2
        #    if self.sprint:
        #        self.player.velocity[0] = .4
        
        if self.menu_active:
            self.menu.run()
            self.start_time = time.time()
            self.menu_active = False
            self.movment = [False, False, False, False]
        

        if self.sprint:
            self.sprint_time[0] -= self.delta_time

        if self.sprint_time[0] <= 0:
            self.sprint_time[0] = 0
            self.sprint = False
            if self.sprint_check == False:
                self.sprint_check = True
                self.sprint_time[1] = .2
            self.sprint_time[1] -= self.delta_time
            if self.sprint_time[1] <= 0:
                self.sprint_time[0] = 0
        
        if self.sprint == False and self.sprint_time[1] <= 0.001:
            self.sprint_time[0] = 2
            self.sprint_time[1] = 0
        
        
        if self.player.velocity[0] > 0:
            self.player.velocity[0] = max(0, self.player.velocity[0] - 0.5 * self.delta_time)
        elif self.player.velocity[0] < 0:
            self.player.velocity[0] = min(0, self.player.velocity[0] + 0.5 * self.delta_time)
        else:
            self.player.velocity[0] = 0
        
        self.player.update(self.tilemap, (self.movment[2] - self.movment[0], 0), self.delta_time, self.sprint)
        self.paralax.update(self.movment[0] - self.movment[2], self.delta_time)
        #self.clouds.update(self.delta_time)
        
        self.scroll[0] += (self.player.rect().centerx - self.Display.get_width() / 2 - self.scroll[0])
        self.scroll[1] += (self.player.rect().centery - self.Display.get_height() / 2 - self.scroll[1])
        self.render_scroll = (int(round(self.scroll[0], 0)), int(round(self.scroll[1], 0)))
        
        #self.rain_sum += self.delta_time
        #if self.rain_sum >= 1/120:
        #    self.rain_sum = 0
        #    self.raindrops.append(raindrop(random.randint(25,35), offset=self.render_scroll))
        
        #self.test12.update((self.mouse_x, self.mouse_y))
        
        pg.display.set_caption(f'{self.clock.get_fps() :.0f} pyfight')
    
    def render(self):
        self.Display.fill((0,0,0))
        
        self.paralax.render(self.Display)
        #self.clouds.render(self.Display, offset=self.render_scroll)
        self.tilemap.render(self.Display, offset=self.render_scroll)
        
        #for rain in self.raindrops:
        #    kill = rain.update(self.delta_time, offset=self.render_scroll)
        #    rain.render(self.Display, offset=self.render_scroll)
        #    if kill:
        #        self.raindrops.remove(rain)
        
        # text
        #self.test12.render(self.Display, offset=self.render_scroll)
        
        self.player.render(self.Display, offset=self.render_scroll)
        
        surf = pg.transform.scale(self.Display, WIN_RES)
        self.screen.blit(pg.transform.flip(surf, False, False), (0,0))
        
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
                
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.menu_active = not self.menu_active
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.movment[2] = True
                    self.player.velocity[0] = .2
                if event.key == pg.K_w or event.key == pg.K_UP:
                    if self.player.air_time <= 6:
                        self.movment[1] = True
                        self.player.velocity[1] = -5
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.movment[0] = True
                    self.player.velocity[0] = -.2
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.movment[3] = True
                if event.key == pg.K_LSHIFT and self.sprint_time[1] <= .001:
                    self.sprint = True
                
            if event.type == pg.KEYUP:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.movment[2] = False
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.movment[1] = False
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.movment[0] = False
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.movment[3] = False
                if event.key == pg.K_LSHIFT:
                    self.sprint = False
                        
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.mouse_x //= RENDER_SCALE
        self.mouse_y //= RENDER_SCALE
       
    def run(self):
        self.is_running = True
        
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()
                
if __name__ == '__main__':
    app = App()
    app.run()
