import random 

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth
        
    def update(self, delta):
        self.pos[0] += self.speed * delta * 100

    def render(self, surf, offset=(0, 0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))
        
class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []
        
        for i in range(count):
            self.clouds.append(Cloud((random.random() * 999999, random.random() * 999999), random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random() * 0.06 + 0.02))
            
        self.clouds.sort(key=lambda x: x.depth)
        
    def update(self, delta):
        for cloud in self.clouds:
            cloud.update(delta)
            
    def render(self, surf, offset=(0, 0)):
        n = 0
        for cloud in self.clouds:
            n += 1
            cloud.render(surf, offset=offset)