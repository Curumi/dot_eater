import math
import pygame
import random
import time

pygame.init()

pacman_images = {
    'up': pygame.image.load('resours/pacman_up.png'),
    'down': pygame.image.load('resours/pacman_down.png'),
    'left': pygame.image.load('resours/pacman_left.png'),
    'right': pygame.image.load('resours/pacman_right.png'),
    'up_left': pygame.image.load('resours/pacman_up_left.png'),
    'up_right': pygame.image.load('resours/pacman_up_right.png'),
    'down_left': pygame.image.load('resours/pacman_down_left.png'),
    'down_right': pygame.image.load('resours/pacman_down_right.png'),
}

class Dot:
    def __init__(self, pos):
        self.pos = pos
        self.collected = False
        self.radius = 5
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, self.color, self.pos, self.radius)

def create_dots(count, size):
    dots = []
    for _ in range(count):
        x = random.randint(50, size[0] - 50)
        y = random.randint(50, size[1] - 50)
        dots.append(Dot((x, y)))
    return dots

def get_direction(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    direction = 'right'

    if dy < 0:
        if dx < 0:
            direction = 'up_left'
        elif dx > 0:
            direction = 'up_right'
        else:
            direction = 'up'
    elif dy > 0:
        if dx < 0:
            direction = 'down_left'
        elif dx > 0:
            direction = 'down_right'
        else:
            direction = 'down'
    else:
        if dx < 0:
            direction = 'left'
        elif dx > 0:
            direction = 'right'

    return direction

def distance(pos1, pos2):
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

def move_towards(pos1, pos2, min_speed=1, max_speed=3):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1

    dist = distance(pos1, pos2)

    if dist < min_speed:
        return pos2

    if dist == 0:
        return pos1

    speed = max(min_speed, min(dist / 5, max_speed))

    dx /= dist
    dy /= dist

    x1 += dx * speed
    y1 += dy * speed

    return (x1, y1)

def show_eat(screen, size):
    font = pygame.font.SysFont(None, 72)
    text = font.render("Eat them all!", True, (255, 255, 255))
    screen.blit(text, (size[0] // 2 - text.get_width() // 2, size[1] // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pac-Man Турнир")
BACKGROUND = (0, 0, 0)
FPS = 60
clock = pygame.time.Clock()

player_pos = [400, 300]

# Счет
player_score = 0

dots = create_dots(50, size)

game_time = 180
start_time = time.time()

# Основной игровой цикл
running = True
while running:
    current_time = time.time()
    elapsed = current_time - start_time
    remaining_time = max(0, game_time - elapsed)

    if remaining_time <= 0:
        running = False
        result = "Время вышло!"
        screen.fill(BACKGROUND)
        font = pygame.font.SysFont(None, 72)
        text = font.render(result, True, (255, 255, 255))
        screen.blit(text, (size[0] // 2 - text.get_width() // 2, size[1] // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    player_direction = get_direction(player_pos, mouse_pos)
    player_pos = list(move_towards(player_pos, mouse_pos))

    if all(dot.collected for dot in dots):
        dots = create_dots(50, size)

    player_rect = pygame.Rect(player_pos[0] - 15, player_pos[1] - 15, 30, 30)

    for dot in dots:
        if not dot.collected:
            dot_rect = pygame.Rect(dot.pos[0] - dot.radius, dot.pos[1] - dot.radius,
                                   dot.radius * 2, dot.radius * 2)

            if player_rect.colliderect(dot_rect):
                dot.collected = True
                player_score += 1

                if player_score == 10:
                    show_eat(screen, size)

    screen.fill(BACKGROUND)

    for dot in dots:
        dot.draw(screen)

    screen.blit(pacman_images[player_direction], (player_pos[0] - 15, player_pos[1] - 15))

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Игрок: {player_score}", True, (255, 255, 255))
    time_text = font.render(f"Время: {int(remaining_time // 60)}:{int(remaining_time % 60):02d}", True, (255, 255, 255))

    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (size[0] - time_text.get_width() - 20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
