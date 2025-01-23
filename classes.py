import os
import sys
import pygame
import random
import time

pygame.init()
size = width, height = 900, 800
screen = pygame.display.set_mode(size)
score = 0
durability = 100


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

    def __init__(self, all_sprites, mc_image, x=500, y=700):
        global durability
        global score
        durability = 100
        score = 0
        super().__init__(all_sprites)
        self.alive = True
        image = load_image(mc_image, -1)
        image = pygame.transform.scale(image, (100, 100))
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy_image1.png", -1)
    image = pygame.transform.scale(image, (60, 60))
    image_exp = load_image("explose.png", -1)
    image_exp = pygame.transform.scale(image_exp, (70, 70))

    def __init__(self, enemy_sprites, enemy_list, pos=None):
        super().__init__(enemy_sprites)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randint(100, 840)
        self.rect.y = 0
        self.explos = False
        self.alive = True
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

    def update(self, mc, all_sprites, level):
        global durability
        global score
        if self.explos:
            self.image = Enemy.image_exp
            self.alive = False
            now_ex = time.time()
            if now_ex - self.start_ex >= 0.065:
                self.rect.x = -100
                self.rect.y = 500
        if pygame.sprite.collide_mask(self, mc):
            if level == 1:
                durability -= 25
            elif level == 2:
                durability -= 50
            else:
                durability = 0
            self.explos = True
        if self.rect.bottom >= 800:
            if level == 2:
                score -= 1
            elif level == 3:
                mc.alive = False
            self.explos = True
        if self.alive:
            self.rect = self.rect.move(0, 1)
            self.now = time.time()
            if self.now - self.start >= 1.7:
                EnemyWeapon(self.rect.left + self.rect.width / 2, self.rect.bottom, all_sprites=all_sprites)
                self.start = self.now


class Enemy2(Enemy):
    image = load_image("enemy_image2.png", -1)
    image = pygame.transform.scale(image, (80, 80))

    def __init__(self, enemy_sprites, enemy_list, pos=None):
        super().__init__(enemy_sprites, enemy_list)
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

    def __init__(self, enemy_sprites, enemy_list):
        super().__init__(enemy_sprites, enemy_list)
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


class EnemyWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.Surface((4, 20),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('red'),
                         (0, 0, 4, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.alive = True

    def update(self, mc, all_sprites, enemy_list, enemy_sprites, level):
        global durability
        if pygame.sprite.collide_mask(self, mc):
            if level == 1:
                durability -= 25
            elif level == 2:
                durability -= 50
            else:
                durability = 0
            self.rect.x = 1000
            self.rect.y = 1000
            self.alive = False
        if self.alive:
            self.rect = self.rect.move(0, 1)


class MainWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y, mc, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.Surface((4, 30),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('white'),
                         (0, 0, 4, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.alive = True

    def update(self, mc, all_sprites, enemy_list, enemy_sprites, level):
        global score
        for i in enemy_list:
            if pygame.sprite.collide_mask(self, i):
                score = score + 1
                self.alive = False
                self.rect.y = -100
                if type(i) == Enemy:
                    i.explos = True
                    i.start_ex = time.time()
                elif type(i) == Enemy2:
                    enemy = Enemy(enemy_sprites, enemy_list, (i.rect.x + 10, i.rect.y + 10))
                    i.rect.x = -100
                    i.alive = False
                    enemy_list.append(enemy)
                elif type(i) == Enemy3:
                    enemy = Enemy2(enemy_sprites, enemy_list, (i.rect.x + 10, i.rect.y + 10))
                    i.rect.x = -100
                    i.alive = False
                    enemy_list.append(enemy)
        if self.alive:
            self.rect = self.rect.move(0, -5)


def show_score():
    return score


def show_durability():
    return durability


def terminate():
    pygame.quit()
    sys.exit()
