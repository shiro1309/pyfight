import time
import random

from scripts.settings import *
from scripts.entity import *
from scripts.utils import load_image, load_images, Animation, ratio_surf, Paralax
from scripts.tilemap import Tilemap
from scripts.particle import Particle, multi_render_particles
from scripts.spark import Spark

class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_RES, pg.RESIZABLE)

        self.Display = pg.Surface(DISPLAY)
        
        self.movment = [False, False, False, False]
        
        self.clock = pg.time.Clock()
        
        self.assets = {
            "clouds": load_images("clouds"),
            "grass": load_images("tile/grass"),
            "dirt": load_images("tile/dirt"),
            "vine": load_images("tile/vine"),
            "player/idle": Animation(load_images("entity/player/idle"), image_dur=6),
            "player/run" : Animation(load_images("entity/player/run"), image_dur=4),
            "player/death" : Animation(load_images("entity/player/death"), image_dur=12),
            "player/jump" : Animation(load_images("entity/player/jump")),
            "player/wall_slide" : Animation(load_images("entity/player/test")),
            "particle/particle": Animation(load_images("particle/particle"), image_dur=4, loop=False),
            "enemy/idle": Animation(load_images("entity/enemy/idle"), image_dur=6),
            "enemy/run": Animation(load_images("entity/enemy/run"), image_dur=4),
            "gun": load_image("gunt.png"),
            "projectile": load_image("projectile.png"),
        }
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.paralax = Paralax("paralax", 4)
        self.player = Player(self, (50,50), (8,16))

        self.true_start = time.time()
        self.tick = False
        self.load_level(0)

    def load_level(self, level_id):
        
        self.tilemap.load("data/map/" + str(level_id) + ".json")

        self.enemies = []
        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
            else:
                self.enemies.append(Enemy(self, spawner["pos"], (8, 15)))

        self.particles = []
        self.projectiles = []
        self.sparks = []

        self.scroll = [0,0]
        
        self.start_time = time.time()

    def update(self):
        if self.tick:
            self.clock.tick(120)
        else:
            self.clock.tick(FPS)

        self.delta_time = time.time() - self.start_time
        self.start_time = time.time()

        for enemy in self.enemies.copy():
            kill = enemy.update(self.tilemap, (0,0))
            if kill:
                self.enemies.remove(enemy)

        self.player.update(self.tilemap, (self.movment[2] - self.movment[0], 0))

        paralax_y = self.player.collisions["right"] == False and self.player.collisions["left"] == False
        self.paralax.update(self.movment[0] - self.movment[2], self.delta_time, paralax_y)
        
        self.scroll[0] += (self.player.rect().centerx - self.Display.get_width() / 2 - self.scroll[0])
        self.scroll[1] += (self.player.rect().centery - self.Display.get_height() / 2 - self.scroll[1])
        self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        
        pg.display.set_caption(f'{self.clock.get_fps() :.0f} pyfight')
    
    def render(self):
        self.screen.fill((103, 49, 71))
        self.Display.fill((85,85,85))

        self.paralax.render(self.Display)
        self.tilemap.render(self.Display, offset=self.render_scroll)

        for enemy in self.enemies.copy():
            enemy.render(self.Display, offset=self.render_scroll)
        
        self.player.render(self.Display, offset=self.render_scroll)
        for projectile in self.projectiles.copy():
            projectile[0][0] += projectile[1]  * self.delta_time * 60
            projectile[2] += 1 * self.delta_time * 60
            img = self.assets["projectile"]
            self.Display.blit(img, (projectile[0][0] - img.get_width() / 2 - self.render_scroll[0], projectile[0][1] - img.get_height() / 2 - self.render_scroll[1]))
            if self.tilemap.solid_check(projectile[0]):
                self.projectiles.remove(projectile)
                for i in range(4):
                    self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
            elif projectile[2] > 360:
                self.projectiles.remove(projectile)
            elif abs(self.player.dashing) < 50:
                if self.player.rect().collidepoint(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(30):
                        angle = random.random() * math.pi * 2 
                        speed = random.random() * 5
                        self.sparks.append(Spark(self.player.rect(), angle, speed))
                        self.particles.append(Particle(self, "particle", self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5 * self.delta_time, math.sin(angle + math.pi) * speed * 0.5 * self.delta_time], frame=random.randint(0, 7)))

        for spark in self.sparks.copy():
            kill = spark.update(self.delta_time)
            spark.render(self.Display, offset=self.render_scroll)
            if kill:
                self.sparks.remove(spark)

        #multi_render_particles(self.Display, offset=self.render_scroll, particles=self.particles)
        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(self.Display, offset=self.render_scroll)
            if kill:
                self.particles.remove(particle)
        
        ratio_surf(self.screen, self.Display)


        pg.display.update()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.movment[2] = True
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.player.jump()
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.movment[0] = True

                if event.key == pg.K_b:
                    self.tick = not self.tick
                if event.key == pg.K_x:
                    self.player.dash()
                
            if event.type == pg.KEYUP:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.movment[2] = False
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.movment[0] = False

        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        screen_value = self.screen.get_size()
        self.mouse_x //= screen_value[0] / DISPLAY[0]
        self.mouse_y //= screen_value[1] / DISPLAY[1]
       
    def run(self):
        self.is_running = True
        
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
                
App().run()
