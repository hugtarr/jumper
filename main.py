from random import randint
import pygame
from src.config import SPAWN_STEP, WIN_SIZE, WIN_WIDTH, WIN_HEIGHT
from src.player import Player
from src.sprite import Sprite


def main():
    pygame.init()

    window = pygame.Window("Jumper", WIN_SIZE)
    surface = window.get_surface()
    clock = pygame.Clock()


    font = pygame.Font("assets/pixel.ttf", 32)

    button_image = pygame.image.load('assets/platform.png')
    x = WIN_WIDTH/ 2
    y = WIN_HEIGHT / 3 * 2
    button = Sprite([x,y], button_image)
    background_image = pygame.image.load('assets/background.png')
    background_image = pygame.transform.scale(background_image,WIN_SIZE)

    platform_image = pygame.image.load("assets/platform.png")
    platforms = [Sprite([200, 550], platform_image)]
    for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
        platforms.append(Sprite([randint(0, WIN_WIDTH), y], platform_image))
    player_image = pygame.image.load("assets/player.png")
    player = Player([200,450], player_image, 6)
    window.set_icon(player_image)
    running = True
    lose = False

    offset_y = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False


        if not lose:
            player.update(platforms)
            if player.rect.top - offset_y >= WIN_HEIGHT:
                lose = True

            if player.rect.y - offset_y < WIN_HEIGHT / 3:
                offset_y = player.rect.y - WIN_HEIGHT / 3
            if platforms[-1].rect.y - offset_y >= SPAWN_STEP:
                platforms.pop(0)
                y = platforms[-1].rect.y - SPAWN_STEP
                platforms.append(Sprite([randint(0, WIN_WIDTH), y], platform_image))
        surface.blit(background_image)
        for platform in platforms:
            platform.render(surface, -offset_y)
        player.render(surface, -offset_y)
        text = str(round(-offset_y/100))
        img = font.render(text, True, 'black')
        rect = img.get_rect(midtop=[WIN_WIDTH / 2 , 10])
        surface.blit(img, rect)
        if lose:
            img = font.render('Вы проиграли!\n\nВаш результат:' + text, True, 'black')
            rect = img.get_rect(midtop=[WIN_WIDTH / 2 , 10])
            surface.blit(img, rect)

            button.render(surface, 0)
        window.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()