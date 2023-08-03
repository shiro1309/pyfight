from settings import *
import sys
from entity import *
from data.scripts.collisions import *

class App:
    
    G = .2
    
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode(WIN_RES, pg.DOUBLEBUF)
        
        self.player = Player(16,8, 100, 50, 100, 10, 40, [False, False, False, False])
        self.Island = Object(-100, 100, 400, 100)
        
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        
        self.is_running = True
        
        self.temp_surf = pg.Surface((8, 16))
        self.Island_surf = pg.image.load("data/assets/mainisland-export.png")
        self.Display = pg.Surface(DISPLAY)
        self.scroll = [0,0,0,0]
        self.spawn_area = [pg.Rect(-100,0,100,100), pg.Rect(0,0,100,100), pg.Rect(100,0,100,100), pg.Rect(200,0,100,100)]
        
        
    def update(self):
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')
        self.clock.tick(60)
    
    def render(self):
        self.Display.fill((0,0,0))
        
        for spawn in self.spawn_area:
            spawn.x += self.scroll[0]
            pg.draw.rect(self.Display, (255,0,0), spawn, 4)
        
        self.temp_surf.fill((255,255,255))
        self.Display.blit(self.temp_surf, (self.player.hitbox.x, self.player.hitbox.y))
        self.Display.blit(self.Island_surf, (self.Island.hitbox.x, self.Island.hitbox.y))
        
        surf = pg.transform.scale(self.Display, WIN_RES)
        self.screen.blit(surf, (0,0))
        #self.screen.blit(self.Display, (0,0))
        
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.player.movment[0] = True
                if event.key == pg.K_w or event.key == pg.K_UP:
                    if self.player.air_time <= 6:
                        self.player.movment[1] = True
                        self.player.vertical_momentum = -5
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.player.movment[2] = True
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.player.movment[3] = True
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.player.movment[0] = False
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.player.movment[1] = False
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.player.movment[2] = False
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.player.movment[3] = False
        
        
        self.scroll = [0,0,self.scroll[2], self.scroll[3]]
        if self.player.movment[0]:
            self.scroll[0] -= 2
            self.scroll[2] -= 2
        if self.player.movment[2]:
            self.scroll[0] += 2
            self.scroll[2] += 2
        
        self.scroll[1] = self.player.vertical_momentum
        
        self.player.vertical_momentum += self.G
        if self.player.vertical_momentum >= 3:
            self.player.vertical_momentum = 3
        
        self.Island.hitbox.x += self.scroll[0]
        
        # check for platform collision
        self.player.hitbox, player_collision = move(self.player.hitbox, self.scroll, self.Island.hitbox)
        
        if player_collision["bottom"]:
            self.player.vertical_momentum = 0
            self.player.air_time = 0
        else:
            self.player.air_time += 1
       
    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()
                
if __name__ == '__main__':
    app = App()
    app.run()
