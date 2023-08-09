from scripts.settings import *
        
class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.entity_type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        
    def rect(self):
        return pg.FRect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def update(self, tilemap, movment=(0, 0), delta=0, sprint=False):
        self.collisions = {"up": False, "down": False, "left": False, "right": False}
        
        sprint_ = 1
        if sprint:
            sprint_ = 2
        frame_movment = ((movment[0] + self.velocity[0]), (movment[1] + self.velocity[1]))
        
        
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
                self.pos[0] = entity_rect.x
        
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
                self.pos[1] = entity_rect.y
                
        self.velocity[1] = min(6, self.velocity[1] + 0.1*delta*100)
        
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0
        print(self.collisions)
    
        print(self.velocity)
        
    def render(self, surf):
        surf.blit(self.game.assets[self.entity_type], self.pos)
    
    