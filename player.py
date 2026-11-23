from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, LINE_WIDTH
import pygame

class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = 0.0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt : float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt : float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        multiplied_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += multiplied_vector

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        self.shot_timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.shot_timer > 0:
            return
        else:
            self.shot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(self.position.x, self.position.y)
            unit_vector = pygame.Vector2(0, 1)
            rotated_vector = unit_vector.rotate(self.rotation)
            scaled_vector = rotated_vector * PLAYER_SHOOT_SPEED
            shot.velocity = scaled_vector