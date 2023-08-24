from scripts.settings import *

class Menu:
    def __init__(self, game, surface):
        self.game = game
        self.surface = surface
        
    def update(self):
        pass
    
    def render(self):
        self.game.render()
    
    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.event_handler()
            self.update()
            self.render()