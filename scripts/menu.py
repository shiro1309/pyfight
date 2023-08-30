from scripts.settings import *
from scripts.utils import ratio_surf
import time

class Menu:
    def __init__(self, game, surface):
        self.game = game
        self.surface = surface
        self.menu_surface = pg.Surface(DISPLAY)
        self.option_surface = pg.Surface((100, DISPLAY[1]))
        self.clock = pg.time.Clock()
        
    def update(self):
        for i in range(50000):
            er = i


        self.delta_time = time.time() - self.start_time
        self.start_time = time.time()
        self.option_surface.fill((255,255,255))
        self.option_surface.set_alpha(100)
        pg.display.set_caption(f'{1/self.delta_time :.0f} pyfight')
    
    def render(self):

        self.menu_surface.blit(self.game_surface, (0,0))
        self.menu_surface.blit(self.option_surface, (0,0))
        
        ratio_surf(self.game.screen, self.menu_surface)
        pg.display.update()
    
    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    def run(self, game_surface):
        self.start_time = time.time()
        self.running = True
        self.game_surface = game_surface
        while self.running:
            self.event_handler()
            self.update()
            self.render()