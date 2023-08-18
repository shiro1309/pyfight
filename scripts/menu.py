from scripts.settings import *

class Menu:
    def __init__(self, game, surface):
        self.game = game
        self.surface = surface
        
    def update(self):
        pass
    
    def render(self):
        pass
    
    def event_handler(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self.event_handler()
            self.update()
            self.render()