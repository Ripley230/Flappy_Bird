import pygame
import random

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH = 400
HEIGHT = 600
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
SKY_BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Création du fond d'écran
background = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    r = int((y / HEIGHT) * (DARK_BLUE[0] - SKY_BLUE[0]) + SKY_BLUE[0])
    g = int((y / HEIGHT) * (DARK_BLUE[1] - SKY_BLUE[1]) + SKY_BLUE[1])
    b = int((y / HEIGHT) * (DARK_BLUE[2] - SKY_BLUE[2]) + SKY_BLUE[2])
    pygame.draw.line(background, (r, g, b), (0, y), (WIDTH, y))

# Horloge pour contrôler le FPS
clock = pygame.time.Clock()

# Classe pour l'oiseau
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0
        self.gravity = 0.5
        self.frame_index = 0
        self.animation_speed = 0.1
        self.draw_bird()

    def draw_bird(self):
        pygame.draw.ellipse(self.original_image, YELLOW, (0, 5, 40, 30))
        pygame.draw.circle(self.original_image, WHITE, (30, 15), 8)
        pygame.draw.circle(self.original_image, BLACK, (32, 15), 4)
        pygame.draw.polygon(self.original_image, ORANGE, [(40, 20), (50, 23), (40, 26)])
        self.wings = [self.original_image.copy() for _ in range(3)]
        pygame.draw.ellipse(self.wings[0], LIGHT_BLUE, (5, 20, 20, 10))
        pygame.draw.ellipse(self.wings[1], LIGHT_BLUE, (5, 15, 20, 10))
        pygame.draw.ellipse(self.wings[2], LIGHT_BLUE, (5, 25, 20, 10))

    def update(self):
        self.velocity += self.gravity
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.wings):
            self.frame_index = 0
        self.image = self.wings[int(self.frame_index)]

        if self.velocity < 0:
            rotated_image = pygame.transform.rotate(self.image, 20)
        elif self.velocity > 0:
            rotated_image = pygame.transform.rotate(self.image, -20)
        else:
            rotated_image = self.image

        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image

    def jump(self):
        self.velocity = -10

# Classe pour les tuyaux
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.Surface((50, y))
        self.image.fill(GREEN)
        if position == 'top':
            self.rect = self.image.get_rect(topleft=(x, 0))
        else:
            self.rect = self.image.get_rect(bottomleft=(x, HEIGHT))
        self.passed = False

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

# Groupes de sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Création de l'oiseau
bird = Bird()
all_sprites.add(bird)

# Variables du jeu
score = 0
high_score = 0
game_over = False

def create_pipe():
    gap = 200
    y = random.randint(gap + 50, HEIGHT - 50)
    pipe_top = Pipe(WIDTH, y - gap, 'top')
    pipe_bottom = Pipe(WIDTH, HEIGHT - y, 'bottom')
    pipes.add(pipe_top, pipe_bottom)
    all_sprites.add(pipe_top, pipe_bottom)

# Boucle principale du jeu
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.jump()
            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                score = 0
                all_sprites.empty()
                pipes.empty()
                bird = Bird()
                all_sprites.add(bird)

    if not game_over:
        all_sprites.update()

        if len(pipes) == 0 or pipes.sprites()[-1].rect.right < WIDTH - 200:
            create_pipe()

        if pygame.sprite.spritecollide(bird, pipes, False) or bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
            game_over = True
            if score > high_score:
                high_score = score

        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not pipe.passed:
                score += 0.5
                pipe.passed = True

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {int(high_score)}", True, WHITE)
    screen.blit(high_score_text, (10, 50))

    if game_over:
        game_over_text = font.render("Game Over! Press Enter to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
