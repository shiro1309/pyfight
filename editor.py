import sys
import time
import json

from scripts.settings import *
from scripts.utils import load_images, Map_creation
from scripts.tilemap import Tilemap

RENDER_SCALE = 4.0

class Editor:
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode(WIN_RES, pg.DOUBLEBUF)
        
        self.movment = [False, False, False, False]
        
        self.clock = pg.time.Clock()
        self.delta_time = 0.0
        
        self.assets = {
            "grass": load_images("tile/grass"),
            "dirt": load_images("tile/dirt"),
            "vine": load_images("tile/vine"),
        }
        
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        
        #self.map = Map_creation("map/map.png")
        #self.tilemap = self.map.map_extraction()
        
        self.Display = pg.Surface(DISPLAY)
        self.scroll = [0,0]
        self.tilemap = Tilemap(self, tile_size=16)
        
        try:
            self.tilemap.load("map.json")
        except FileNotFoundError:
            pass
        
        self.start_time = time.time()
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        
    def update(self):
        self.clock.tick()
        
        self.scroll[0] += (self.movment[2] - self.movment[0]) * 2
        self.scroll[1] += (self.movment[3] - self.movment[1]) * 2
        
        self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        self.current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant]
        self.current_tile_img.set_alpha(100)
        
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}  {self.scroll}')
    
    def render(self):
        self.Display.fill((0, 0, 0))
        
        if self.ongrid:
            self.Display.blit(self.current_tile_img, (self.tile_pos[0] * self.tilemap.tile_size - self.scroll[0], self.tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
        else:
            self.Display.blit(self.current_tile_img, self.mouse_pos)
        
        self.tilemap.render(self.Display, offset=self.render_scroll)
        
        self.Display.blit(self.current_tile_img, (5,5))
        
        surf = pg.transform.scale(self.Display, WIN_RES)
        self.screen.blit(surf, (0,0))
        
        pg.display.flip()

    def handle_events(self):
        
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_pos = (self.mouse_pos[0] / RENDER_SCALE, self.mouse_pos[1] / RENDER_SCALE)
        self.tile_pos = (int((self.mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size), int((self.mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size))
        
        if self.clicking and self.ongrid:
            self.tilemap.tilemap[str(self.tile_pos[0]) + ";" + str(self.tile_pos[1])] = {"type": self.tile_list[self.tile_group], "variant": self.tile_variant, "pos": self.tile_pos}
            
        if self.right_clicking:
            self.tile_loc = str(self.tile_pos[0]) + ";" + str(self.tile_pos[1])
            if self.tile_loc in self.tilemap.tilemap:
                del self.tilemap.tilemap[self.tile_loc]
            for tile in self.tilemap.offgrid_tiles.copy():
                tile_img = self.assets[tile["type"]][tile["variant"]]
                tile_r = pg.Rect(tile["pos"][0] - self.scroll[0], tile["pos"][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                if tile_r.collidepoint(self.mouse_pos):
                    self.tilemap.offgrid_tiles.remove(tile)
                
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True
                    if not self.ongrid:
                        self.tilemap.offgrid_tiles.append({"type": self.tile_list[self.tile_group], "variant": self.tile_variant, "pos": (self.mouse_pos[0] + self.scroll[0], self.mouse_pos[1] + self.scroll[1])})
                if event.button == 3:
                    self.right_clicking = True
                    
                if self.shift:
                    if event.button == 4:
                        self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                    if event.button == 5:
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                else:
                    if event.button == 4:
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                    if event.button == 5:
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.movment[2] = True
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.movment[1] = True
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.movment[0] = True
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.movment[3] = True
                if event.key == pg.K_LSHIFT:
                    self.shift = True
                if event.key == pg.K_g:
                    self.ongrid = not self.ongrid
                if event.key == pg.K_o:
                    self.tilemap.save("map.json")
            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                if event.button == 3:
                    self.right_clicking = False
            
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
                    self.shift = False
       
    def run(self):
        self.is_running = True
        
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()
                
if __name__ == '__main__':
    app = Editor()
    app.run()