from scripts.settings import *
from scripts.utils import ratio_surf

from game import Game


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_RES, pg.DOUBLEBUF | pg.RESIZABLE)
        self.Display = pg.Surface(DISPLAY)
        self.game = Game(self)

    def update(self):
        pass

    def render(self):
        self.Display.fill((255,255,255))
        ratio_surf(self.screen, self.Display)
        pg.display.update()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game.run()
            
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
        while True:
            self.event_handler()
            self.update()
            self.render()

if __name__ == '__main__':
    app = App()
    app.run()