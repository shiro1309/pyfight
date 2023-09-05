from scripts.settings import *
from scripts.particle import Particle
from scripts.spark import Spark

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
        self.animate_offset = (-3, -3)
        self.flip = False
        self.set_action("idle")

        self.frame_rate = 1 / 48
        self.frame_sum = 0
        self.animation_sum = 0

        self.last_movment = [0, 0]
        
    def rect(self):
        return pg.FRect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.entity_type + "/" + self.action].copy()
    
    def animation_frame(self):
        if time.time() - self.game.true_start >= self.animation_sum + self.frame_rate:
            self.animation_sum += self.frame_rate
            self.animation.update()
        
    def update(self, tilemap, movment=(0, 0)):
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        
        frame_movment = (movment[0] + self.velocity[0], movment[1] + self.velocity[1])
        
        
        self.pos[0] += frame_movment[0] * self.game.delta_time * 60
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movment[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_movment[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movment[1]  * self.game.delta_time * 60
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movment[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_movment[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = entity_rect.y
        
        if movment[0] > 0:
            self.flip = False
        if movment[0] < 0:
            self.flip = True
        
        self.last_movment = movment

        self.velocity[1] = min(5, self.velocity[1] + 0.1 * self.game.delta_time * 60)

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation_frame()
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pg.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.animate_offset[0], self.pos[1] - offset[1] + self.animate_offset[1]))

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "enemy", pos, size)

        self.walking = 0

    def update(self, tilemap, movment=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if self.collisions["left"] or self.collisions["right"]:
                    self.flip = not self.flip
                movment = (movment[0] - 0.5 if self.flip else 0.5, movment[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1 * self.game.delta_time * 60)
            if not self.walking:
                distance = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(distance[0]) < 100):
                    if (self.flip and distance[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and distance[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], 1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
                        

        elif random.random() < 0.01 * self.game.delta_time * 60:
            self.walking = random.randint(30, 120)

        super().update(tilemap, movment=movment)

        if movment[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screen_shake = max(16, self.game.screen_shake)
                for i in range(30):
                    angle = random.random() * math.pi * 2 
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect(), angle, speed))
                    self.game.particles.append(Particle(self.game, "particle", self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5 * self.game.delta_time, math.sin(angle + math.pi) * speed * 0.5 * self.game.delta_time], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True

    def render(self, surface, offset):
        super().render(surface, offset=offset)

        if self.flip:
            surface.blit(pg.transform.flip(self.game.assets["gun"], True, False), (self.rect().centerx - 4 - self.game.assets["gun"].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surface.blit(self.game.assets["gun"], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))
        

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        
        self.dashing = 0
        
    def update(self, tilemap, movment=(0, 0)):
        super().update(tilemap, movment=movment)
        self.movment = movment
        
        self.air_time += 1 * self.game.delta_time * 60

        if self.air_time > 180:
            self.game.dead += 1

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
                
        if int(abs(self.dashing)) in {60,50}:
            for i in range(20):
                angle = random.random() * 2 * math.pi
                speed = random.random() *.5 + 0.5
                particle_velocity = [math.cos(angle) * speed * self.game.delta_time * 60, math.sin(angle) * speed * self.game.delta_time * 60]
                self.game.particles.append(Particle(self.game, "particle", self.rect().center, velocity=particle_velocity, frame=random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1 * self.game.delta_time * 60)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1 * self.game.delta_time * 60)
        if int(abs(self.dashing)) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if int(abs(self.dashing)) == 51:
                self.velocity[0] *= .1 * self.game.delta_time * 60
            particle_velocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, "particle", self.rect().center, velocity=particle_velocity, frame=random.randint(0, 7)))

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1  * self.game.delta_time * 60, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1  * self.game.delta_time * 60, 0)
        
    
    def render(self, surface, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surface, offset=offset)
    
    def jump(self):
        
        if self.wall_slide:
            if self.flip and self.last_movment[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1 * self.game.delta_time * 60)
                return True
            
            elif not self.flip and self.last_movment[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1* self.game.delta_time * 60)
                return True

        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True
        
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60