class Particle:
    def __init__(self, game, particle_type, pos, velocity=[0, 0], frame=0):
        self.game = game
        self.particle_type = particle_type
        self.pos = pos
        self.velocity = velocity
        self.frame = frame