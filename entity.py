from settings import *

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
    
    