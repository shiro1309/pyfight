from scripts.settings import *

class Spark:
    def __init__(self, pos, angle, speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed

    def update(self, dt):
        self.pos[0] += math.cos(self.angle) * self.speed * dt * 60
        self.pos[1] += math.sin(self.angle) * self.speed * dt * 60

        self.speed = max(0, self.speed - 0.1 * dt * 60)
        return not self.speed

    def render(self, surface, offset=(0,0)):
        render_points = [
            (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi * .5) * self.speed - offset[0], self.pos[1] + math.sin(self.angle + math.pi * .5) * self.speed  - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi * 1.5) * self.speed - offset[0], self.pos[1] + math.sin(self.angle + math.pi * 1.5) * self.speed  - offset[1])
        ]

        pg.draw.polygon(surface, (255, 255, 255), render_points)