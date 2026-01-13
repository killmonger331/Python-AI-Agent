import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )
    def update(self, dt):
        self.position += self.velocity * dt
    def split(self):
        log_event("asteroid_split")
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            return
        self.kill()
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        base_vel = self.velocity
        vel_a = base_vel.rotate(angle)
        vel_b = base_vel.rotate(-angle)
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vel_a * 1.2
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vel_b * 1.2
            
