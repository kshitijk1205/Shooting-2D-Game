import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pro Shooter Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player class for customization
class Player:
    def __init__(self, type="default"):
        self.width, self.height = 50, 50
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.health = 3
        if type == "speed":  # Fast ship
            self.speed = 10
            self.fire_rate = 20
        elif type == "shooter":  # Rapid-fire ship
            self.speed = 5
            self.fire_rate = 10
        else:  # Default ship
            self.speed = 7
            self.fire_rate = 15
        self.fire_counter = 0

# Enemy class
class Enemy:
    def __init__(self):
        self.width, self.height = 40, 40
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed_x = random.choice([-3, 3])
        self.speed_y = 2

# Power-up class
class PowerUp:
    def __init__(self, x, y, type="speed"):
        self.width, self.height = 20, 20
        self.x = x
        self.y = y
        self.type = type
        self.speed = 3

# Game setup
player = Player("default")  # Change to "speed" or "shooter" for different ships
bullets = []
enemies = []
enemy_bullets = []
power_ups = []
score = 0
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

# Background stars
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]
bg_speed = 2

# Functions
def spawn_enemy():
    enemies.append(Enemy())

def spawn_power_up(x, y):
    if random.random() < 0.1:  # 10% chance
        power_ups.append(PowerUp(x, y, random.choice(["speed", "fire_rate"])))

def draw_text(text, x, y):
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))

# Game loop
spawn_counter = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.fire_counter <= 0:
                bullets.append([player.x + player.width // 2 - 2.5, player.y])
                player.fire_counter = player.fire_rate

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
        player.x += player.speed
    player.fire_counter -= 1

    # Spawn enemies
    spawn_counter += 1
    if spawn_counter >= 20:
        spawn_enemy()
        spawn_counter = 0

    # Update background stars
    stars = [(x, (y + bg_speed) % HEIGHT) for x, y in stars]

    # Update bullets
    for bullet in bullets[:]:
        bullet[1] -= 10
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies[:]:
        enemy.x += enemy.speed_x
        enemy.y += enemy.speed_y
        if enemy.x <= 0 or enemy.x >= WIDTH - enemy.width:
            enemy.speed_x *= -1
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
        if random.random() < 0.02:  # Enemy shoots
            enemy_bullets.append([enemy.x + enemy.width // 2 - 2.5, enemy.y + enemy.height])

    # Update enemy bullets
    for bullet in enemy_bullets[:]:
        bullet[1] += 5
        if bullet[1] > HEIGHT:
            enemy_bullets.remove(bullet)

    # Update power-ups
    for power in power_ups[:]:
        power.y += power.speed
        if power.y > HEIGHT:
            power_ups.remove(power)

    # Collisions (bullets vs enemies)
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 15)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                spawn_power_up(enemy.x, enemy.y)
                break

    # Collisions (player vs enemy bullets/power-ups)
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for bullet in enemy_bullets[:]:
        if player_rect.colliderect(pygame.Rect(bullet[0], bullet[1], 5, 15)):
            enemy_bullets.remove(bullet)
            player.health -= 1
            if player.health <= 0:
                running = False

    for power in power_ups[:]:
        if player_rect.colliderect(pygame.Rect(power.x, power.y, power.width, power.height)):
            power_ups.remove(power)
            if power.type == "speed":
                player.speed += 2
            elif power.type == "fire_rate":
                player.fire_rate = max(5, player.fire_rate - 2)

    # Drawing
    screen.fill((0, 0, 0))  # Black background
    for star_x, star_y in stars:  # Stars
        pygame.draw.circle(screen, WHITE, (star_x, star_y), 2)
    pygame.draw.rect(screen, GREEN, (player.x, player.y, player.width, player.height))  # Player
    for bullet in bullets:  # Player bullets
        pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], 5, 15))
    for bullet in enemy_bullets:  # Enemy bullets
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 5, 15))
    for enemy in enemies:  # Enemies
        pygame.draw.rect(screen, RED, (enemy.x, enemy.y, enemy.width, enemy.height))
    for power in power_ups:  # Power-ups
        color = YELLOW if power.type == "speed" else BLUE
        pygame.draw.rect(screen, color, (power.x, power.y, power.width, power.height))
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Health: {player.health}", 10, 40)

    pygame.display.flip()
    clock.tick(60)

# Game over
draw_text("Game Over!", WIDTH // 2 - 80, HEIGHT // 2 - 20)
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()
sys.exit() 