from scripts.settings import *
from scripts.particle import Particle

import random
        
class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.entity_type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        
        self.action = ""
        self.animate_offset = (-3, 0)
        self.flip = False
        self.set_action("idle")
        self.frame_rate = 1 / 24
        
    def rect(self):
        return pg.FRect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.entity_type + "/" + self.action].copy()
        
    def update(self, tilemap, movment=(0, 0), delta=0, sprint=False):
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        
        frame_movment = list(((movment[0] + self.velocity[0]), (movment[1] + self.velocity[1])))
        
        sprint_ = 1
        if sprint:
            sprint_ = 2
        
        self.pos[0] += frame_movment[0] * delta * 100 * sprint_
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movment[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_movment[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = round(entity_rect.x, 0)
        
        self.pos[1] += frame_movment[1] * delta * 100
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movment[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_movment[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = round(entity_rect.y, 0)
        
        if movment[0] > 0:
            self.flip = False
        if movment[0] < 0:
            self.flip = True
        
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1*delta*100)
        
        self.game.animation_sum += self.game.delta_time
        if self.game.animation_sum >= self.frame_rate:
            self.game.animation_sum = 0
            self.animation.update()
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pg.transform.flip(self.animation.img(), self.flip, False), (round(self.pos[0], 0) - offset[0] + self.animate_offset[0], round(self.pos[1], 0) - offset[1] + self.animate_offset[1]))
    
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.last_movment = [0, 0]
        self.dashing = 0
        
    def update(self, tilemap, movment=(0, 0), delta=0, sprint=False):
        super().update(tilemap, movment=movment, delta=delta, sprint=sprint)
        self.movment = movment
        
        self.air_time += 1 * delta / 0.0167
        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 1

        self.wall_slide = False
        if self.collisions["left"] or self.collisions["right"] and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], .5)
            if self.collisions["right"]:
                self.flip = False
            else:
                self.flip = True
            self.set_action("wall_slide")

        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action("jump")
            elif self.movment[0] != 0:
                self.set_action("run")
            else:
                self.set_action("idle")
        
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) >= 51 and abs(self.dashing) <= 52:
                self.velocity[0] *= .1
            particle_velocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, "particle", self.pos ,velocity=particle_velocity, frame=random.randint(0,3)))
        #if abs(self.dashing) in {60, 50}:
        #    for i in range(20):
        #        angle = random.random() * math.pi * 2
        #        speed = random.random() * 0.5 + 0.5
        #        particle_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
        #        self.game.particle.append(Particle(self.game, "particle", self.rect().center,velocity=particle_velocity, frame=random.randint(0,3)))

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        self.last_movment = movment
    
    def render(self, surface, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surface, offset=offset)
    
    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movment[0] < 0:
                self.velocity[0] = 5.5
                self.velocity[1] = -3.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            
            elif not self.flip and self.last_movment[0] > 0:
                self.velocity[0] = -5.5
                self.velocity[1] = -3.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True

        elif self.jumps:
            self.velocity[1] = -4
            self.jumps -= 1
            self.air_time = 6
            return True
        
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60