import pygame, sys
from random import choice, randrange

screen_dimensions = (1280, 700)

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.set_pos(pos)
        self.speed = speed

    def set_pos(self, pos, constraint_screen=False):
        self.rect = self.image.get_rect(center = pos)
        if constraint_screen:
            self.constraint_screen();

    def update(self):
        x_speed, y_speed = self.speed
        self.rect.centerx += x_speed
        self.rect.centery += y_speed

        if self.is_off_screen():
            self.kill()

    def is_off_screen(self):
        width, height = screen_dimensions
        return self.rect.left >= width or self.rect.right <= 0 or self.rect.top <= 0 or self.rect.bottom >= height

    def constraint_screen(self):
        width, height = screen_dimensions
        if self.rect.right >= width:
            self.rect.right = width
        elif self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.bottom >= height:
            self.rect.bottom = height
        elif self.rect.top <= 0:
            self.rect.top = 0

class SpaceShip(BaseSprite):
    def __init__(self, path, pos, speed):
        super().__init__(path, pos, speed)

class Meteor(BaseSprite):
    def __init__(self, path, pos, speed):
        super().__init__(path, pos, speed)

    def is_off_screen(self):
        width, height = screen_dimensions
        return self.rect.top >= height

class Laser(BaseSprite):
    def __init__(self, path, pos, speed):
        super().__init__(path, pos, speed)

    def is_off_screen(self):
        return self.rect.bottom <= 0


pygame.init()
pygame.mouse.set_visible(False)

font = pygame.font.Font(None, 34)
big_font = pygame.font.Font(None, 120)

screen = pygame.display.set_mode(screen_dimensions)
clock = pygame.time.Clock()

shield = pygame.image.load('assets/shield.png')
health = 5

score = 0

spaceship = SpaceShip('assets/spaceship.png', (640, 350), (0, 0))
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add( spaceship )

meteor_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()

METEORSPAWN = pygame.USEREVENT
pygame.time.set_timer(METEORSPAWN, 250)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            spaceship.set_pos(event.pos, constraint_screen=True)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if health > 0:
                laser = Laser('assets/Laser.png', event.pos, (0, -10))
                laser_group.add(laser)
            else:
                health = 5
                score = 0
                meteor_group.empty()
        elif event.type == METEORSPAWN:
            meteor = Meteor(choice(['assets/Meteor1.png', 'assets/Meteor2.png', 'assets/Meteor3.png']), (randrange(0, 1280), (randrange(-500, -50))), (randrange(-1, 1), randrange(1, 25)))
            meteor_group.add(meteor)

            if health > 0:
                score += 1

    screen.fill((42, 45, 51))

    debug_display = font.render(f"Lasers: {len(laser_group)} Asteroids: {len(meteor_group)}", True, [255,255,255])
    screen.blit(debug_display, debug_display.get_rect(bottomright=screen_dimensions))

    debug_display = font.render(f"Score: {score}", True, [255,255,255])
    screen.blit(debug_display, debug_display.get_rect(topright=(screen_dimensions[0], 0)))

    # Collision check

    if health:
        if pygame.sprite.spritecollide(spaceship, meteor_group, True):
            health -= 1

    for lasers in laser_group:
        if pygame.sprite.spritecollide(laser, meteor_group, True):
            laser.kill()

    for index in range(health):
        screen.blit(shield, (10 + index * 40, 10))

    laser_group.update()
    laser_group.draw(screen)

    if health > 0:
        spaceship_group.draw(screen)
    else:
        game_over_text = big_font.render("Game Over!", True, [255,255,255])
        screen.blit(game_over_text, game_over_text.get_rect(center = (screen_dimensions[0] /2 , screen_dimensions[1] / 2)))

    meteor_group.update()
    meteor_group.draw(screen)

    pygame.display.update()
    clock.tick(120)
