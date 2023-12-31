class Particle:
    def __init__(self, game, particle_type, pos, velocity=[0, 0], frame=0):
        self.game = game
        self.particle_type = particle_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets["particle/" + particle_type].copy()
        self.animation.frame = frame

    def update(self):
        kill = False
        if self.animation.done:
            kill = True
        
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill

    def render(self, surface, offset=(0,0)):
        img = self.animation.img()
        surface.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))

def multi_render_particles(surface, offset=(0,0), particles=None):
    for particle in particles.copy():
        kill = particle.update()
        particle.render(surface, offset=offset)
        if kill:
            particles.remove(particle)