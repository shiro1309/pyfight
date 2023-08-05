from scripts.settings import *

class Player:
    def __init__(self, height, width, x, y, health, defense, attack, movment):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.health = health
        self.defense = defense
        self.attack = attack
        self.movment = movment
        self.hitbox = pg.Rect(x, y, width, height)
        self.vertical_momentum = 3
        self.air_time = 6

class Enemy:
    def __init__(self, height, width, x, y, health, defense, attack):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.health = health
        self.defense = defense
        self.attack = attack
        self.hitbox = pg.Rect(x, y, width, height)

class Object:
    def __init__(self, x, y, width, height):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.hitbox = pg.Rect(x, y, width, height)
        
class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.entity_type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        
    def update(self, movment=(0, 0), delta=0, sprint=False):
        sprint_ = 1
        if sprint:
            sprint_ = 2
        frame_movment = ((movment[0] + self.velocity[0]) * 100 * sprint_, (movment[1] + self.velocity[1]) * 100 * sprint_)
        
        self.pos[0] += frame_movment[0] * delta
        self.pos[1] += frame_movment[1]
    
    def render(self, surf):
        surf.blit(self.game.assets["player"], self.pos)
    
    