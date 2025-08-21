import pygame as p 
from pygame.locals import *
from random import randint
from time import time 

p.mixer.init()
p.init()

win_width, win_height = 1000, 800
rocket_width = 80
monster_width, monster_height = 80, 50
asteroid_width, asteroid_height = 80, 80
bullet_width = 15
score_limit = 10
skipped_limit = 3
window = p.display.set_mode((win_width, win_height))
p.display.set_caption('Шутер')
timer = p.time.Clock()
backround = p.transform.scale(p.image.load('galaxy.jpg'), (win_width, win_height))
heart = p.transform.scale(p.image.load('heart.png'), (150, 150))
# p.mixer.music.load('space.ogg')
# p.mixer.music.play()
# fire = p.mixer.Sound('fire.ogg')
class GameSprite(p.sprite.Sprite):
    def __init__(self, image_path, speed, x, y, width, height):
        p.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = p.transform.scale(p.image.load(image_path), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = p.key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif keys_pressed[K_d] and self.rect.x < win_width - rocket_width:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 5, self.rect.centerx - bullet_width / 2, self.rect.top, bullet_width, 20)
        bullets.add(bullet)
        # fire.play()

class Enemy(GameSprite):
    def update(self):
        global counter_skipped
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 0 - monster_height
            self.rect.x = randint(0, win_width - monster_width)
            counter_skipped += 1
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 0 - asteroid_height
            self.rect.x = randint(0, win_width - asteroid_width)

rocket = Player('rocket.png', 10, 0, 680, 80, 120)
monsters = p.sprite.Group()
asteroids = p.sprite.Group()
bullets = p.sprite.Group()
WHITE = (255, 255, 255)
RED = (178, 34, 34)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
DARK_YELLOW = (184, 134, 11)
DARK_RED = (139, 0, 0)
BLACK = (0, 0, 0)
colors = [DARK_RED, DARK_YELLOW, DARK_GREEN]
counter_score = 0
counter_skipped = 0
num_fire = 0
lifes = 3

for i in range(5):
    monster_speed = randint(1, 3)
    monster_x = randint(0, win_width - monster_width)
    monster_y = 0 - monster_height
    monster = Enemy('ufo.png', monster_speed, monster_x, monster_y, monster_width, monster_height)
    monsters.add(monster)

for i in range(2):
    asteroid_speed = randint(1, 3)
    asteroid_x = randint(0, win_width - asteroid_width)
    asteroid_y = 0 - asteroid_height
    asteroid = Asteroid('asteroid.png', asteroid_speed, asteroid_x, asteroid_y, asteroid_width, asteroid_height)
    asteroids.add(asteroid)

run = True
finish = False
rel_time = False
while run:
    events = p.event.get()
    for event in events:
        if event.type == p.QUIT:
            run = False
        if event.type == p.KEYDOWN:
            if event.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    num_fire += 1
                elif num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start_time = time()


    if not finish:    
            
        group_collides = p.sprite.groupcollide(bullets, monsters, True, True)
        if group_collides:
            monster_speed = randint(1, 3)
            monster_x = randint(0, win_width - monster_width)
            monster_y = 0 - monster_height
            monster = Enemy('ufo.png', monster_speed, monster_x, monster_y, monster_width, monster_height)
            monsters.add(monster)
            counter_score += 1
        window.blit(backround, (0, 0))
        rocket.draw()
        rocket.move()
        monsters.draw(window)
        bullets.draw(window)
        monsters.update()
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(heart, (840, 2))
        text_score = p.font.SysFont('Arial', 50).render(f'Счет: {counter_score}', True, WHITE)
        text_skipped = p.font.SysFont('Arial', 50).render(f'Пропущено: {counter_skipped}', True, WHITE)
        text_lifes = p.font.SysFont('Arial', 100).render(f'{lifes}', True, colors[lifes - 1])
        window.blit(text_score, (10, 20))
        window.blit(text_skipped, (10, 60))
        window.blit(text_lifes, (900, 40))
        if rel_time:
            end_time = time()
            if end_time - start_time >= 1:
                rel_time = False
                num_fire = 0
            else:
                text_reload = p.font.SysFont('Arial', 50).render('Wait, reload...', True, RED)
                window.blit(text_reload, (400, win_height - 125))

        if p.sprite.spritecollide(rocket, asteroids, True) or p.sprite.spritecollide(rocket, monsters, True):
            lifes -= 1

        if lifes <= 0 or counter_skipped >= skipped_limit:
            fail = p.font.SysFont('Arial', 100).render('YOU LOSE!', True, RED)
            window.blit(fail, (300, 300))
            text_lifes = p.font.SysFont('Arial', 100).render('0', True, BLACK)
            window.blit(heart, (840, 2))
            window.blit(text_lifes, (900, 40))
            finish = True

        if counter_score >= score_limit:
            win = p.font.SysFont('Arial', 100).render('YOU WIN!', True, GREEN)
            window.blit(win, (300, 300))
            finish = True
    p.display.update()
    timer.tick(60)
