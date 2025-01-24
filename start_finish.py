import pygame
import os
import sys
import sqlite3
import time


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


def design(intro_text, width, height, screen, level):
    y = 40
    fon = pygame.transform.scale(load_image('background.jpg'), (width, height))
    skin1 = pygame.transform.scale(load_image('mc_image.png', -1), (200, 200))
    skin2 = pygame.transform.scale(load_image('mc_image2.png', -1), (200, 200))
    skin3 = pygame.transform.scale(load_image('mc_image3.png', -1), (200, 200))
    screen.blit(fon, (0, 0))
    screen.blit(skin1, (100, 280))
    screen.blit(skin2, (350, 280))
    screen.blit(skin3, (600, 280))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    pygame.draw.rect(screen, (180, 180, 180), rect=(385, 650, 140, 50))
    f = pygame.font.Font(None, 36)
    f_blast_zone = pygame.font.Font(None, 65)
    text = f.render('НАЧАТЬ', True, (250, 0, 250))
    screen.blit(text, (405, 665))
    blast_zone = f_blast_zone.render('BLAST ZONE', True, (250, 30, 130))
    screen.blit(blast_zone, (300, 30))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color((250, 100, 200)))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        y += 40
        intro_rect.y = y
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    screen.blit(font.render('Выберите уровень сложности', True, (250, 100, 200)), (200, 500))
    pygame.draw.rect(screen, (180, 180, 180), rect=(170, 570, 140, 40))
    pygame.draw.rect(screen, (180, 180, 180), rect=(370, 570, 170, 40))
    pygame.draw.rect(screen, (180, 180, 180), rect=(590, 570, 170, 40))
    screen.blit(f.render('Легко', True, (250, 0, 200)), (205, 580))
    screen.blit(f.render('Нормально', True, (250, 0, 200)), (390, 580))
    screen.blit(f.render('Тяжело', True, (250, 0, 200)), (630, 580))
    if level == 1:
        pygame.draw.rect(screen, (100, 100, 100), rect=(170, 570, 140, 40))
        screen.blit(f.render('Легко', True, (250, 0, 200)), (205, 580))
    elif level == 2:
        pygame.draw.rect(screen, (100, 100, 100), rect=(370, 570, 170, 40))
        screen.blit(f.render('Нормально', True, (250, 0, 200)), (390, 580))
    elif level == 3:
        pygame.draw.rect(screen, (100, 100, 100), rect=(590, 570, 170, 40))
        screen.blit(f.render('Тяжело', True, (250, 0, 200)), (630, 580))
    elif level == 0:
        screen.blit(font.render('Выберите уровень сложности', True, (250, 0, 0)), (200, 500))


def start_screen(width, height, screen):
    f = pygame.font.Font(None, 36)
    intro_text = ["Сбивай вражеские космолёты и зарабатывай очки",
                  "    Не дай им тебя сбить или дойти до края поля",
                  "                                 Приятной игры", "",
                  "                                 Выберите скин"]
    design(intro_text, width, height, screen, None)
    font = pygame.font.Font(None, 50)
    skin1 = pygame.transform.scale(load_image('mc_image.png', -1), (200, 200))
    skin2 = pygame.transform.scale(load_image('mc_image2.png', -1), (200, 200))
    skin3 = pygame.transform.scale(load_image('mc_image3.png', -1), (200, 200))
    skin = None
    level = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    if 385 <= x <= 525 and 650 <= y <= 700:
                        if skin is None:
                            string_rendered = font.render(intro_text[-1], 1, pygame.Color((250, 0, 0)))
                            intro_rect = string_rendered.get_rect()
                            intro_rect.x = 20
                            intro_rect.y = 240
                            screen.blit(string_rendered, intro_rect)
                        if level is None or level == 0:
                            screen.blit(font.render('Выберите уровень сложности', True, (250, 0, 0)), (200, 500))
                            level = 0
                        if level > 0 and skin is not None:
                            time.sleep(0.3)
                            return skin, level
                    if 110 < x < 290 < y < 470:
                        design(intro_text, width, height, screen, level)
                        pygame.draw.rect(screen, (180, 0, 180), rect=(110, 290, 180, 180))
                        pygame.draw.rect(screen, (0, 0, 0), rect=(112, 292, 176, 176))
                        screen.blit(skin1, (100, 280))
                        skin = 'mc_image.png'

                    if 360 < x < 540 and 290 < y < 470:
                        design(intro_text, width, height, screen, level)
                        pygame.draw.rect(screen, (180, 0, 180), rect=(360, 290, 180, 180))
                        pygame.draw.rect(screen, (0, 0, 0), rect=(362, 292, 176, 176))
                        screen.blit(skin2, (350, 280))
                        skin = 'mc_image2.png'

                    if 610 < x < 790 and 290 < y < 470:
                        design(intro_text, width, height, screen, level)
                        pygame.draw.rect(screen, (180, 0, 180), rect=(610, 290, 180, 180))
                        pygame.draw.rect(screen, (0, 0, 0), rect=(612, 292, 176, 176))
                        screen.blit(skin3, (600, 280))
                        skin = 'mc_image3.png'

                    if 170 < x < 310 and 570 < y < 610:
                        level = 1
                        pygame.draw.rect(screen, (100, 100, 100), rect=(170, 570, 140, 40))
                        screen.blit(f.render('Легко', True, (250, 0, 200)), (205, 580))
                        screen.blit(font.render('Выберите уровень сложности', True, (250, 100, 200)), (200, 500))
                        pygame.draw.rect(screen, (180, 180, 180), rect=(370, 570, 170, 40))
                        pygame.draw.rect(screen, (180, 180, 180), rect=(590, 570, 170, 40))
                        screen.blit(f.render('Нормально', True, (250, 0, 200)), (390, 580))
                        screen.blit(f.render('Тяжело', True, (250, 0, 200)), (630, 580))

                    if 370 < x < 540 and 570 < y < 610:
                        level = 2
                        pygame.draw.rect(screen, (100, 100, 100), rect=(370, 570, 170, 40))
                        screen.blit(f.render('Нормально', True, (250, 0, 200)), (390, 580))
                        screen.blit(font.render('Выберите уровень сложности', True, (250, 100, 200)), (200, 500))
                        pygame.draw.rect(screen, (180, 180, 180), rect=(170, 570, 140, 40))
                        pygame.draw.rect(screen, (180, 180, 180), rect=(590, 570, 170, 40))
                        screen.blit(f.render('Легко', True, (250, 0, 200)), (205, 580))
                        screen.blit(f.render('Тяжело', True, (250, 0, 200)), (630, 580))

                    if 590 < x < 760 and 570 < y < 610:
                        level = 3
                        pygame.draw.rect(screen, (100, 100, 100), rect=(590, 570, 170, 40))
                        screen.blit(f.render('Тяжело', True, (250, 0, 200)), (630, 580))
                        screen.blit(font.render('Выберите уровень сложности', True, (250, 100, 200)), (200, 500))
                        pygame.draw.rect(screen, (180, 180, 180), rect=(170, 570, 140, 40))
                        pygame.draw.rect(screen, (180, 180, 180), rect=(370, 570, 170, 40))
                        screen.blit(f.render('Легко', True, (250, 0, 200)), (205, 580))
                        screen.blit(f.render('Нормально', True, (250, 0, 200)), (390, 580))

        pygame.display.flip()


def final_screen(width, height, screen, score, username, record_score, total):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    request = f"""UPDATE Users
            SET score = '{record_score}',
            total = '{total}'
            WHERE user = '{username}'"""
    cur.execute(request)
    con.commit()
    con.close()
    fon = pygame.transform.scale(load_image('background.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    f_blast_zone = pygame.font.Font(None, 65)
    blast_zone = f_blast_zone.render('BLAST ZONE', True, (250, 30, 130))
    screen.blit(blast_zone, (300, 30))
    font = pygame.font.Font(None, 90)
    lose_text = font.render("Вы проиграли", True, (250, 100, 200))
    screen.blit(lose_text, lose_text.get_rect(center=(450, 200)))
    score_text = f_blast_zone.render(f"Cчёт: {score}", True,(250, 100, 200))
    screen.blit(score_text, score_text.get_rect(center=(450, 300)))
    record_text = f_blast_zone.render(f"Рекорд: {record_score}", True, (250, 100, 200))
    screen.blit(record_text, record_text.get_rect(center=(450, 380)))
    total_text = f_blast_zone.render(f"Общий счёт: {total}", True, (250, 100, 200))
    screen.blit(total_text, total_text.get_rect(center=(450, 460)))
    pygame.draw.rect(screen, (180, 180, 180), rect=(200, 650, 140, 50))
    pygame.draw.rect(screen, (180, 180, 180), rect=(570, 650, 140, 50))
    f = pygame.font.Font(None, 36)
    text_restart = f.render('ЗАНОВО', True, (250, 0, 250))
    text_exit = f.render('ВЫЙТИ', True, (250, 0, 250))
    screen.blit(text_restart, (215, 665))
    screen.blit(text_exit, (595, 663))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    if 200 <= x <= 340 and 650 <= y <= 700:
                        return
                    if 570 <= x <= 710 and 650 <= y <= 700:
                        terminate()
        pygame.display.flip()


def terminate():
    pygame.quit()
    sys.exit()


def info(username):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    result = cur.execute("""SELECT user FROM Users """).fetchall()
    if username not in [i[0] for i in result]:
        request = f"""INSERT INTO Users(user,score,total) VALUES('{username}', 0, 0)"""
        cur.execute(request)
        con.commit()
    result = cur.execute(f"""SELECT score, total FROM Users where user = '{username}' """).fetchall()
    con.close()
    return result[0][0], result[0][1]


def login():
    size = width, height = 900, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('background.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont(None, 100)
    f = pygame.font.Font(None, 55)
    f_blast_zone = pygame.font.Font(None, 65)
    blast_zone = f_blast_zone.render('BLAST ZONE', True, (250, 30, 130))
    username = ""
    limit = True
    active_input = False
    empty = False

    while True:
        screen.blit(fon, (0, 0))
        screen.blit(blast_zone, (300, 30))
        if empty:
            text1 = f.render('Введите ваше имя', True, (255, 0, 0))
        else:
            text1 = f.render('Введите ваше имя', True, (255, 50, 150))
        screen.blit(text1, (260, 100))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    if 100 < x < 800 and 250 < y < 350:
                        active_input = not active_input
                    elif 360 < x < 540 and 550 < y < 620:
                        if not username:
                            empty = True
                        else:
                            score, total = info(username)
                            time.sleep(0.5)
                            return username, score, total
                    else:
                        active_input = False

            elif event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                    if len(username) < 12:
                        limit = True
                else:
                    if limit:
                        username += event.unicode
                        empty = False
        if active_input:
            pygame.draw.rect(screen, (150, 150, 150), rect=(100, 250, 700, 100))
        else:
            pygame.draw.rect(screen, (100, 100, 100), rect=(100, 250, 700, 100))
        if len(username) == 12:
            limit = False
            screen.blit(f.render('Максимальное число символов: 12', True, (250, 0, 0)), (120, 400))

        text_surf = font.render(username, True, (255, 50, 150))
        screen.blit(text_surf, text_surf.get_rect(center=(450, 300)))
        pygame.draw.rect(screen, (150, 150, 150), rect=(360, 550, 180, 70))
        screen.blit(f.render('Войти', True, (255, 50, 150)), (390, 568))
        pygame.display.flip()
