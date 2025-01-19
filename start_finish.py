import pygame
import os
import sys
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


def design(intro_text, width, height, screen):
    y = 10
    fon = pygame.transform.scale(load_image('background.jpg'), (width, height))
    skin1 = pygame.transform.scale(load_image('mc_image.png', -1), (200, 200))
    skin2 = pygame.transform.scale(load_image('mc_image2.png', -1), (200, 200))
    skin3 = pygame.transform.scale(load_image('mc_image3.png', -1), (200, 200))
    screen.blit(fon, (0, 0))
    screen.blit(skin1, (100, 380))
    screen.blit(skin2, (350, 380))
    screen.blit(skin3, (600, 380))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    pygame.draw.rect(screen, (180, 180, 180), rect=(385, 650, 140, 50))
    f = pygame.font.Font(None, 36)
    text = f.render('НАЧАТЬ', True, (250, 0, 250))
    screen.blit(text, (405, 665))
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


def start_screen(width, height, screen):
    intro_text = ["                                     Blast Zone", "",
                  "Сбивай вражеские космолёты и зарабатывай очки",
                  "    Не дай им тебя сбить или дойти до края поля",
                  "                                 Приятной игры", "",
                  "                                 Выберите скин"]
    design(intro_text, width, height, screen)
    font = pygame.font.Font(None, 50)
    skin1 = pygame.transform.scale(load_image('mc_image.png', -1), (200, 200))
    skin2 = pygame.transform.scale(load_image('mc_image2.png', -1), (200, 200))
    skin3 = pygame.transform.scale(load_image('mc_image3.png', -1), (200, 200))
    skin = None
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
                            intro_rect.y = 290
                            screen.blit(string_rendered, intro_rect)
                        else:
                            time.sleep(0.3)
                            return skin
                    if 100 < x < 300 and 380 < y < 525:
                        design(intro_text, width, height, screen)
                        pygame.draw.rect(screen, (180, 0, 180), rect=(100, 380, 200, 200))
                        pygame.draw.rect(screen, (0, 0, 0), rect=(102, 382, 196, 196))
                        screen.blit(skin1, (100, 380))
                        skin = 'mc_image.png'

                    if 350 < x < 550 and 380 < y < 525:
                        design(intro_text, width, height, screen)
                        pygame.draw.rect(screen, (180, 0, 180), rect=(350, 380, 200, 200))
                        pygame.draw.rect(screen, (0, 0, 0), rect=(352, 382, 196, 196))
                        screen.blit(skin2, (350, 380))
                        skin = 'mc_image2.png'

                    if 600 < x < 800 and 380 < y < 525:
                        design(intro_text, width, height, screen)
                        pygame.draw.rect(screen, (180, 0, 180), rect=(600, 380, 200, 200))
                        pygame.draw.rect(screen, (0, 0, 0), rect=(602, 382, 196, 196))
                        screen.blit(skin3, (600, 380))
                        skin = 'mc_image3.png'
        pygame.display.flip()


def final_screen(width, height, screen, score):
    intro_text = ["             Вы проиграли", "",
                  f"                Ваш счёт: {score}"]
    y = 150
    fon = pygame.transform.scale(load_image('background.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 90)
    text_coord = 50
    pygame.draw.rect(screen, (180, 180, 180), rect=(200, 650, 140, 50))
    pygame.draw.rect(screen, (180, 180, 180), rect=(570, 650, 140, 50))
    f = pygame.font.Font(None, 36)
    text_restart = f.render('ЗАНОВО', True, (250, 0, 250))
    text_exit = f.render('ВЫЙТИ', True, (250, 0, 250))
    screen.blit(text_restart, (215, 665))
    screen.blit(text_exit, (595, 663))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color((250, 100, 200)))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 0
        y += 40
        intro_rect.y = y
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    if 200 <= x <= 340 and 650 <= y <= 700:
                        return True
                    if 570 <= x <= 710 and 650 <= y <= 700:
                        terminate()
        pygame.display.flip()


def terminate():
    pygame.quit()
    sys.exit()
