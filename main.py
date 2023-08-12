import sys
import time

from scripts.settings import *
from scripts.entity import *
from scripts.utils import load_image, load_images, Map_creation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class App:
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode(WIN_RES, pg.DOUBLEBUF)
        
        self.movment = [False, False, False, False]
        
        self.clock = pg.time.Clock()
        self.delta_time = 0.0
        
        self.sprint = False
        self.sprint_check = False
        self.sprint_time = [2, 0]
        
        self.assets = {
            "player": load_image("entity/player/player_1.png"),
            "clouds": load_images("clouds"),
            "grass": load_images("tile/grass"),
            "dirt": load_images("tile/dirt"),
        }
        
        self.map = Map_creation("map/map.png")
        self.tilemap = self.map.map_extraction()
        
        self.clouds = Clouds(self.assets["clouds"], count=100)
        
        self.player = PhysicsEntity(self, "player", (100,50), (8,16))
        
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.Display = pg.Surface(DISPLAY)
        self.scroll = [0,0]
        self.animation_sum = 0.0
        
        self.start_time = time.time()
        
    def update(self):
        self.clock.tick(10)
        self.time = pg.time.get_ticks() * 0.001

        self.delta_time = time.time() - self.start_time
        self.start_time = time.time()
        
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
        
        self.player.update(self.tilemap, (self.movment[2] - self.movment[0], 0), self.delta_time, self.sprint)
        self.clouds.update(self.delta_time)
        
        self.scroll[0] += (self.player.rect().centerx - self.Display.get_width() / 2 - self.scroll[0]) * self.delta_time * 3
        self.scroll[1] += (self.player.rect().centery - self.Display.get_height() / 2 - self.scroll[1]) * self.delta_time * 3
        self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        
        self.animation_sum += self.delta_time
        if self.animation_sum >= 0.0208:
            self.animation_sum = 0
        
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')
    
    def render(self):
        self.Display.fill((100,100,100))
        
        self.clouds.render(self.Display, offset=self.render_scroll)
        self.tilemap.render(self.Display, offset=self.render_scroll)
        self.player.render(self.Display, offset=self.render_scroll)
        
        surf = pg.transform.scale(self.Display, WIN_RES)
        self.screen.blit(surf, (0,0))
        
        pg.display.flip()

    def handle_events(self):
        
        if self.player.velocity[0] > 0:
            self.player.velocity[0] = max(0, self.player.velocity[0] - 0.5 * self.delta_time)
        elif self.player.velocity[0] < 0:
            self.player.velocity[0] = min(0, self.player.velocity[0] + 0.5 * self.delta_time)
        else:
            self.player.velocity[0] = 0
        
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.movment[2] = True
                    self.player.velocity[0] = .2
                if event.key == pg.K_w or event.key == pg.K_UP:
                    #if self.player.air_time <= 6:
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
        
        
        if self.movment[0]:
            self.player.velocity[0] = -.2
            if self.sprint:
                self.player.velocity[0] = -.6
        if self.movment[2]:
            self.player.velocity[0] = .2
            if self.sprint:
                self.player.velocity[0] = .6
       
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
