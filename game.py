import pygame
import random
import os
import sys
import time

pygame.init()
size = width, height = 910, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
score = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class MainCharacter(pygame.sprite.Sprite):
    image = load_image("mc_image.png", -1)
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = MainCharacter.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 500
        self.rect.y = 700


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy_image1.png", -1)
    image = pygame.transform.scale(image, (60, 60))
    image_exp = load_image("explose.png", -1)
    image_exp = pygame.transform.scale(image_exp, (70, 70))

    def __init__(self, pos=None):
        super().__init__(enemy_sprites)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randint(100, 840)
        self.rect.y = 0
        self.explos = False
        self.start = time.time()
        self.start_ex = time.time()
        if pos is None:
            self.now = 0
            while True:
                flag = False
                self.rect.x = random.randint(100, 840)
                for i in enemy_list:
                    if pygame.sprite.collide_mask(self, i):
                        flag = True
                        break
                if not flag:
                    break
        else:
            self.rect.x = pos[0]
            self.rect.y = pos[1]

    def update(self):
        if self.explos:
            self.image = Enemy.image_exp
            now_ex = time.time()
            if now_ex - self.start_ex >= 0.065:
                self.rect.y = 1000
        self.rect = self.rect.move(0, 1)
        self.now = time.time()
        if self.now - self.start >= 1.7:
            EnemyWeapon(self.rect.left + self.rect.width / 2, self.rect.bottom)
            self.start = self.now




class Enemy2(Enemy):
    image = load_image("enemy_image2.png", -1)
    image = pygame.transform.scale(image, (80, 80))

    def __init__(self, pos=None):
        super().__init__()
        self.image = Enemy2.image
        self.rect = self.image.get_rect()
        if pos is None:
            while True:
                flag = False
                self.rect.x = random.randint(100, 820)
                for i in enemy_list:
                    if pygame.sprite.collide_mask(self, i):
                        flag = True
                        break
                if not flag:
                    break
        else:
            self.rect.x = pos[0]
            self.rect.y = pos[1]


class Enemy3(Enemy):
    image = load_image("enemy_image3.png", -1)
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self):
        super().__init__()
        self.image = Enemy3.image
        self.rect = self.image.get_rect()
        while True:
            flag = False
            self.rect.x = random.randint(100, 800)
            for i in enemy_list:
                if pygame.sprite.collide_mask(self, i):
                    flag = True
                    break
            if not flag:
                break


class MainWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.Surface((4, 30),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('white'),
                         (0, 0, 4, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global score
        for i in enemy_list:
            if pygame.sprite.collide_mask(self, i):
                score = score + 1
                self.rect.y = 0
                if type(i) == Enemy:
                    i.explos = True
                    i.start_ex = time.time()
                elif type(i) == Enemy2:
                    enemy = Enemy((i.rect.x + 10, i.rect.y + 10))
                    i.rect.y = 1000
                    enemy_list.append(enemy)
                elif type(i) == Enemy3:
                    enemy = Enemy2((i.rect.x + 10, i.rect.y + 10))
                    i.rect.y = 1000
                    enemy_list.append(enemy)
        self.rect = self.rect.move(0, -5)


class EnemyWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.Surface((4, 20),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('red'),
                         (0, 0, 4, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.collide_mask(self, mc):
            mc.rect.x = 1000
            self.rect.x = 1000
        self.rect = self.rect.move(0, 1)


freq = [1, 1, 1, 2, 2, 3]
enemy_list = []
running = True
mc = MainCharacter()
k_a = False
k_d = False
k_w = False
k_s = False
f = pygame.font.Font(None, 36)

start = time.time()
enemy_start = time.time()
frame = 0
text1 = f.render('Score', True,
                 (180, 0, 0))

while running:
    text2 = f.render(str(score), True, (180, 0, 0))
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                k_a = True
            elif event.key == pygame.K_d:
                k_d = True
            if event.key == pygame.K_w:
                k_w = True
            elif event.key == pygame.K_s:
                k_s = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                k_a = False
            elif event.key == pygame.K_d:
                k_d = False
            if event.key == pygame.K_w:
                k_w = False
            elif event.key == pygame.K_s:
                k_s = False
    now = time.time()

    if now - enemy_start >= 1.6:
        x = random.choice(freq)
        if x == 1:
            enemy = Enemy()
        elif x == 2:
            enemy = Enemy2()
        if x == 3:
            enemy = Enemy3()
        enemy_list.append(enemy)
        enemy_start = now
    if now - start >= 0.22:
        mw = MainWeapon(mc.rect.left + mc.rect.width / 2, mc.rect.top)
        start = now
    if k_a and mc.rect.left >= 100:
        mc.rect.x -= 1
    if k_d and mc.rect.right <= 900:
        mc.rect.x += 1
    if k_s and mc.rect.bottom <= 800:
        mc.rect.y += 1
    if k_w and mc.rect.top >= 0:
        mc.rect.y -= 1
    all_sprites.update()
    clock.tick(200)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (192, 192, 192), rect=(0, 0, 100, 800))
    all_sprites.draw(screen)
    enemy_sprites.draw(screen)
    if frame % 3 == 0:
        enemy_sprites.update()
    frame += 1
    screen.blit(text1, (15, 50))
    screen.blit(text2, (35, 80))
    pygame.display.flip()

pygame.quit()
