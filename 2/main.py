import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Setting up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animal vs Humans - Side Scroller")

# Load Images (Ensure the images are in the same directory as this file)
player_image = pygame.image.load('player.png')  # Add your own image here
enemy_image = pygame.image.load('enemy.png')  # Add your own image here
projectile_image = pygame.image.load('projectile.png')  # Add your own image here

# Clock for controlling frame rate
clock = pygame.time.Clock()

# ------------------- CLASSES ------------------- #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.speed_x = 0
        self.speed_y = 0
        self.jump_power = 15
        self.gravity = 0.8
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            self.speed_x = 5
        else:
            self.speed_x = 0

        if keys[pygame.K_SPACE] and self.rect.bottom == SCREEN_HEIGHT:
            self.speed_y = -self.jump_power

        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Prevent player from falling below the ground
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0

    def shoot(self):
        # Create and add a projectile sprite when player presses 'f'
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(projectile_image, (20, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 7

    def update(self):
        self.rect.x += self.speed_x
        # Remove projectile if it goes off the screen
        if self.rect.x > SCREEN_WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 50
        self.speed_x = random.randint(2, 5)

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()  # Remove enemy once off-screen


class Collectible(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((30, 30))
        if type == "health":
            self.image.fill((0, 255, 0))  # Green for health
        elif type == "life":
            self.image.fill((0, 0, 255))  # Blue for extra life
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 500)
        self.rect.y = SCREEN_HEIGHT - 50

    def update(self):
        self.rect.x -= 3  # Move collectible leftward
        if self.rect.right < 0:
            self.kill()  # Remove once off-screen


# ------------------- SET UP GROUPS ------------------- #
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Game variables
score = 0
level = 1
enemy_spawn_time = 1000  # in milliseconds
collectible_spawn_time = 5000  # in milliseconds

# Spawn enemies and collectibles
pygame.time.set_timer(pygame.USEREVENT + 1, enemy_spawn_time)
pygame.time.set_timer(pygame.USEREVENT + 2, collectible_spawn_time)

# ------------------- GAME LOOP ------------------- #
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shooting projectiles
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            player.shoot()

        # Spawn enemies
        if event.type == pygame.USEREVENT + 1:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Spawn collectibles
        if event.type == pygame.USEREVENT + 2:
            collectible = Collectible(random.choice(["health", "life"]))
            all_sprites.add(collectible)
            collectibles.add(collectible)

    # Update all sprites
    all_sprites.update()

    # Check for collisions between projectiles and enemies
    hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    if hits:
        score += 100  # Add 100 points for each enemy defeated

    # Check for collisions between player and collectibles
    collect_hits = pygame.sprite.spritecollide(player, collectibles, True)
    for hit in collect_hits:
        if hit.type == "health":
            player.health += 20
        elif hit.type == "life":
            player.lives += 1

    # Drawing everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Display instructions
    instructions = "Press LEFT/RIGHT to move, SPACE to jump, F to shoot"
    instructions_text = font.render(instructions, True, BLACK)
    screen.blit(instructions_text, (10, SCREEN_HEIGHT - 40))

    pygame.display.flip()

pygame.quit()
