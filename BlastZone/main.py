import pygame
import random
import time
from classes import MainCharacter, Enemy, Enemy2, Enemy3, MainWeapon
from classes import load_image, show_score, terminate, show_durability
from start_finish import start_screen, final_screen, login


def main(username, record_score, total):
    pygame.init()
    size = width, height = 900, 800
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    freq = [1, 1, 1, 2, 2, 3]
    enemy_list = []
    k_a = False
    k_d = False
    k_w = False
    k_s = False

    start = time.time()
    enemy_start = time.time()
    frame = 0
    f = pygame.font.Font(None, 36)
    f1 = pygame.font.Font(None, 30)
    text1 = f.render('СЧЁТ', True,
                     (180, 0, 0))
    text_record_score1 = f1.render('РЕКОРД', True, (180, 0, 0))

    text_pause1 = f.render('ПАУЗА', True, (180, 0, 0))
    text_pause2 = f.render('SPACE', True, (180, 0, 0))
    text_exit1 = f.render('ВЫЙТИ', True, (180, 0, 0))
    text_exit2 = f.render('ESC', True, (180, 0, 0))
    text_durability1 = 'ПРОЧНОСТЬ'

    background = pygame.transform.scale(load_image('background.jpg'), (800, 800))
    pause = False
    mc_image, level = start_screen(width, height, screen)
    mc = MainCharacter(all_sprites, mc_image)
    while True:
        durability = show_durability()
        score = show_score()
        if score > record_score:
            record_score = score
        text2 = f.render(str(score), True, (180, 0, 0))
        text_durability2 = f.render(str(durability) + '%', True, (180, 0, 0))
        text_record_score2 = f.render(str(record_score), True, (180, 0, 0))
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    k_a = True
                elif event.key == pygame.K_d:
                    k_d = True
                if event.key == pygame.K_w:
                    k_w = True
                elif event.key == pygame.K_s:
                    k_s = True
                if event.key == pygame.K_SPACE:
                    pause = not pause
                if event.key == pygame.K_ESCAPE:
                    mc.alive = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    k_a = False
                elif event.key == pygame.K_d:
                    k_d = False
                if event.key == pygame.K_w:
                    k_w = False
                elif event.key == pygame.K_s:
                    k_s = False
        if not pause:
            now = time.time()
            if now - enemy_start >= 1.6:
                x = random.choice(freq)
                if x == 1:
                    enemy = Enemy(enemy_sprites, enemy_list=enemy_list)
                elif x == 2:
                    enemy = Enemy2(enemy_sprites, enemy_list=enemy_list)
                if x == 3:
                    enemy = Enemy3(enemy_sprites, enemy_list=enemy_list)
                enemy_list.append(enemy)
                enemy_start = now
            if now - start >= 0.22:
                mw = MainWeapon(mc.rect.left + mc.rect.width / 2, mc.rect.top, mc, all_sprites)
                start = now
            if k_a and mc.rect.left >= 100:
                mc.rect.x -= 1
            if k_d and mc.rect.right <= 900:
                mc.rect.x += 1
            if k_s and mc.rect.bottom <= 800:
                mc.rect.y += 1
            if k_w and mc.rect.top >= 0:
                mc.rect.y -= 1
            all_sprites.update(mc, all_sprites, enemy_list, enemy_sprites, level)
            clock.tick(200)
            screen.blit(background, (100, 0))

            pygame.draw.rect(screen, (150, 150, 150), rect=(0, 0, 100, 800))
            all_sprites.draw(screen)
            enemy_sprites.draw(screen)
            if frame % 4 == 0:
                enemy_sprites.update(mc, all_sprites, level)

            frame += 1
            screen.blit(text1, (18, 40))
            screen.blit(text2, text2.get_rect(center=(50, 90)))
            screen.blit(text_pause1, (10, 460))
            screen.blit(text_pause2, (10, 500))
            screen.blit(text_exit1, (6, 550))
            screen.blit(text_exit2, (25, 590))
            screen.blit(text_durability2, (20, 400))
            screen.blit(text_record_score1, (6, 700))
            screen.blit(text_record_score2, text_record_score2.get_rect(center=(50, 670)))
            let_y = 150
            for i in text_durability1:
                let = f.render(i, True, (180, 0, 0))
                screen.blit(let, (10, let_y))
                let_y += 25
            if durability == 100:
                pygame.draw.rect(screen, (180, 0, 0), rect=(60, 150, 10, 225))
            elif durability == 75:
                pygame.draw.rect(screen, (180, 0, 0), rect=(60, 206, 10, 169))
            elif durability == 50:
                pygame.draw.rect(screen, (180, 0, 0), rect=(60, 262, 10, 113))
            elif durability == 25:
                pygame.draw.rect(screen, (180, 0, 0), rect=(60, 318, 10, 56))
            else:
                pygame.draw.rect(screen, (180, 0, 0), rect=(60, 368, 10, 6))

            if not mc.alive or durability == 0:
                time.sleep(1)
                final_screen(width, height, screen, score, username, record_score, total + score)
                main(username, record_score, total+score)
            pygame.display.flip()


username, record_score, total = login()
main(username, record_score, total)
pygame.quit()
