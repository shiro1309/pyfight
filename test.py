from scripts.settings import *

from scripts.rain import raindrop
import random


start_time = time.time()
pg.init()
screen = pg.display.set_mode(WIN_RES)
Display = pg.Surface(DISPLAY)

rain_list = []

#rain_test = raindrop(25)
rain_val = 0
while True:
    Display.fill((255,255,255))
    
    delta_time = (time.time() - start_time )
    start_time = time.time()
    rain_val += delta_time
    if rain_val > 1/120:
        rain_val = 0
        rain_list.append(raindrop(random.randint(25,35)))
        
    print(1 / delta_time)
    
    for rain in rain_list:
        kill = rain.upadte(delta_time)
        rain.render(Display)
        if kill:
            rain_list.remove(rain)
    
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
    
    
    surf = pg.transform.scale(Display, WIN_RES)
    screen.blit(pg.transform.flip(surf, False, False), (0,0))
    pg.display.update()