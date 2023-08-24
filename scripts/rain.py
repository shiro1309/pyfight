from scripts.settings import *

import random

class raindrop:
    def __init__(self, length, offset=(0,0)):
        self.length = length
        self.angle = ((random.random() - .5) * 25 ) * (math.pi / 180)
        #self.color = (54, 106, 145, 0)
        self.color = (17, 18, 18)
        self.start_pos = (random.randint(-50 + offset[0], DISPLAY[0] + offset[0] + 50), -30 + offset[1])
        self.x_angle = math.sin(self.angle)
        self.y_angle = math.cos(self.angle)
        self.end_pos = (self.start_pos[0] + (math.sin(self.angle) * self.length), self.start_pos[1] + (math.cos(self.angle) * self.length))
        self.speed = random.randint(200, 300)
        
    def update(self, delta, offset=(0, 0)):
        kill = False
        
        self.start_pos = (self.start_pos[0] + (self.x_angle * delta * self.speed), self.start_pos[1] + (self.y_angle * delta * self.speed))
        self.end_pos = (self.end_pos[0] + (self.x_angle * delta * self.speed), self.end_pos[1] + (self.y_angle * delta * self.speed))
        
        if self.start_pos[1] >= DISPLAY[1] + offset[1]:
            kill = True
        return kill
            
    
    def render(self, surface, offset=(0,0)):
        pg.draw.line(surface, self.color, (self.start_pos[0] - offset[0], self.start_pos[1] - offset[1]), (self.end_pos[0]- offset[0], self.end_pos[1]- offset[1]))
        
class Raindrops:
    def __init__(self, game):
        pass

    def update(self):
        pass
    
    def render(self, surface, offset=(0,0)):
        pass