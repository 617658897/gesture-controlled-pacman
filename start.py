'''
Auther: Haorong Jiang
Date: 2022-01-08 01:44:36
LastEditors: Haorong Jiang
LastEditTime: 2022-03-09 16:05:27
'''
from calendar import c
import os
import random
import sys

import pygame
from pygame import font
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
import Levels

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)


class Color:
    # 自定义颜色
    ACHIEVEMENT = (220, 160, 87)
    VERSION = (220, 160, 87)

    # 固定颜色
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)  # 中性灰
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    SKYBLUE = (0, 191, 255)
    TRANSPARENT = (255, 255, 255, 0)  # 白色的完全透明


BGMPATH = os.path.join(os.getcwd(), 'resources/sounds/bg.mp3')
ICONPATH = os.path.join(os.getcwd(), 'resources/images/icon.png')
FONTPATH = os.path.join(os.getcwd(), 'resources/font/ALGER.TTF')
HEROPATH = os.path.join(os.getcwd(), 'resources/images/pacman.png')
BlinkyPATH = os.path.join(os.getcwd(), 'resources/images/Blinky.png')
ClydePATH = os.path.join(os.getcwd(), 'resources/images/Clyde.png')
InkyPATH = os.path.join(os.getcwd(), 'resources/images/Inky.png')
PinkyPATH = os.path.join(os.getcwd(), 'resources/images/Pinky.png')


class Text:
    def __init__(self, text: str, text_color: Color, font_type: str, font_size: int):
        """
        text: 文本内容，如'大学生模拟器'，注意是字符串形式
        text_color: 字体颜色，如Color.WHITE、COLOR.BLACK
        font_type: 字体文件(.ttc)，如'msyh.ttc'，注意是字符串形式
        font_size: 字体大小，如20、10
        """
        self.text = text
        self.text_color = text_color
        self.font_type = font_type
        self.font_size = font_size

        font = pygame.font.Font(os.path.join(
            'font', (self.font_type)), self.font_size)
        self.text_image = font.render(
            self.text, True, self.text_color).convert_alpha()

        self.text_width = self.text_image.get_width()
        self.text_height = self.text_image.get_height()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        """
        surface: 文本放置的表面
        center_x, center_y: 文本放置在表面的<中心坐标>
        """
        upperleft_x = center_x - self.text_width / 2
        upperleft_y = center_y - self.text_height / 2
        surface.blit(self.text_image, (upperleft_x, upperleft_y))


class Image:
    def __init__(self, img_name: str, ratio=1):
        """
        img_name: 图片文件名，如'background.jpg'、'ink.png',注意为字符串
        ratio: 图片缩放比例，与主屏幕相适应，默认值为0.4
        """
        self.img_name = img_name
        self.ratio = ratio

        self.image_1080x1920 = pygame.image.load(
            os.path.join('image', self.img_name)).convert_alpha()
        self.img_width = self.image_1080x1920.get_width()
        self.img_height = self.image_1080x1920.get_height()

        self.size_scaled = self.img_width * self.ratio, self.img_height * self.ratio

        self.image_scaled = pygame.transform.smoothscale(
            self.image_1080x1920, self.size_scaled)
        self.img_width_scaled = self.image_scaled.get_width()
        self.img_height_scaled = self.image_scaled.get_height()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        """
        surface: 图片放置的表面
        center_x, center_y: 图片放置在表面的<中心坐标>
        """
        upperleft_x = center_x - self.img_width_scaled / 2
        upperleft_y = center_y - self.img_height_scaled / 2
        surface.blit(self.image_scaled, (upperleft_x, upperleft_y))


class ColorSurface:
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height

        self.color_image = pygame.Surface(
            (self.width, self.height)).convert_alpha()
        self.color_image.fill(self.color)

    def draw(self, surface: pygame.Surface, center_x, center_y):
        upperleft_x = center_x - self.width / 2
        upperleft_y = center_y - self.height / 2
        surface.blit(self.color_image, (upperleft_x, upperleft_y))


class ButtonText(Text):
    def __init__(self, text: str, text_color: Color, font_type: str, font_size: int):
        super().__init__(text, text_color, font_type, font_size)
        self.rect = self.text_image.get_rect()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        super().draw(surface, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, command):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            command()


class ButtonImage(Image):
    def __init__(self, img_name: str, ratio=0.4):
        super().__init__(img_name, ratio)
        self.rect = self.image_scaled.get_rect()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        super().draw(surface, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, command):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            command()


class ButtonColorSurface(ColorSurface):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.rect = self.color_image.get_rect()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        super().draw(surface, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, command, *args):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            command(*args)


class InterFace():
    def __init__(self):
        pygame.init()

    def basic_background(self):
        """
        <基本背景><basic_background>\n
        返回值为背景尺寸和背景表面
        """
        # 设置logo和界面标题
        icon_image = pygame.image.load(ICONPATH)
        game_caption = 'Pac-Man'
        pygame.display.set_icon(icon_image)
        pygame.display.set_caption(game_caption)

        # 设置开始界面
        show_ratio = 1
        size = width, height = 606, 606
        screen = pygame.display.set_mode(size)

        # 设置背景贴图
        Image('background.jpg').draw(screen, width / 2, height / 2)

        return size, screen

    def start_interface(self):
        """
        <开始界面><start_interface>
        """
        # 设置<基本背景>
        size, screen = self.basic_background()
        width, height = size

        # 设置<开始界面>文字和贴图
        Image('ink.png', ratio=0.4).draw(
            screen, width * 0.52, height * 0.67)  # 墨印
        Image('achievement_icon.png', ratio=0.25).draw(
            screen, width * 0.93, height * 0.05)  # 成就按钮

        Text('Pac-Game', Color.WHITE, 'HYHanHeiW.ttf', 50).draw(
            screen, width / 2, height * 1 / 3)  # 游戏名
        Text('1.0', Color.VERSION, 'msyh.ttc', 12).draw(
            screen, width / 2, height * 0.97)  # 版本号
        Text('Score', Color.ACHIEVEMENT, 'msyh.ttc', 16).draw(
            screen, width * 0.93, height * 0.09)  # 成就

        button_game_start = ButtonText(
            'Begin', Color.WHITE, 'HYHanHeiW.ttf', 23)  # 开始游戏按钮
        button_game_start.draw(screen, width / 2, height * 2 / 3)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # ！此处为界面切换的关键，即进入另一死循环
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_game_start.handle_event(
                        self.initial_attribute_interface)

            pygame.display.update()

    def initial_attribute_interface(self):
        """
        <初始属性界面><initial_attribute_interface>
        """
        # 设置基本背景
        screen2 = pygame.display.set_mode([606, 606])
        size, screen = self.basic_background()
        width, height = size

        main(screen2)
        # # 放置各种按钮
        # Image('返回.png', ratio=0.38).draw(screen2, width * 0.07, height * 0.047)
        # button_back = ButtonColorSurface(Color.TRANSPARENT, 26, 26)
        # button_back.draw(screen2, width * 0.07, height * 0.047)

        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()

        #         # ！此处为界面切换的关键，即进入另一死循环
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             button_back.handle_event(self.start_interface)

        #     pygame.display.update()


'''Start Game in certain level'''


def startLevelGame(level, screen, font):
    clock = pygame.time.Clock()
    SCORE = 0
    wall_sprites = level.setupWalls(SKYBLUE)
    gate_sprites = level.setupGate(WHITE)
    hero_sprites, ghost_sprites = level.setupPlayers(
        HEROPATH, [BlinkyPATH, ClydePATH, InkyPATH, PinkyPATH])
    food_sprites = level.setupFood(YELLOW, WHITE)
    is_clearance = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(-1)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for hero in hero_sprites:
                        hero.changeSpeed([-1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_RIGHT:
                    for hero in hero_sprites:
                        hero.changeSpeed([1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_UP:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, -1])
                        hero.is_move = True
                elif event.key == pygame.K_DOWN:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, 1])
                        hero.is_move = True
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                    hero.is_move = False
        screen.fill(BLACK)
        for hero in hero_sprites:
            hero.update(wall_sprites, gate_sprites)
        hero_sprites.draw(screen)
        for hero in hero_sprites:
            food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
        SCORE += len(food_eaten)
        wall_sprites.draw(screen)
        gate_sprites.draw(screen)
        food_sprites.draw(screen)
        for ghost in ghost_sprites:
            # 幽灵随机运动(效果不好且有BUG)
            '''
            res = ghost.update(wall_sprites, None)
            while not res:
                    ghost.changeSpeed(ghost.randomDirection())
                    res = ghost.update(wall_sprites, None)
            '''
            # 指定幽灵运动路径
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] += 1
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    ghost.tracks_loc[0] += 1
                elif ghost.role_name == 'Clyde':
                    ghost.tracks_loc[0] = 2
                else:
                    ghost.tracks_loc[0] = 0
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] = 0
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    loc0 = ghost.tracks_loc[0] + 1
                elif ghost.role_name == 'Clyde':
                    loc0 = 2
                else:
                    loc0 = 0
                ghost.changeSpeed(ghost.tracks[loc0][0: 2])
            ghost.update(wall_sprites, None)
        ghost_sprites.draw(screen)
        score_text = font.render("Score: %s" % SCORE, True, RED)
        screen.blit(score_text, [10, 10])
        if len(food_sprites) == 0:
            is_clearance = True
            break
        if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
            is_clearance = False
            break
        pygame.display.flip()
        clock.tick(10)
    return is_clearance


'''Display Text'''


def showText(screen, font, is_clearance, flag=False):
    screen2 = pygame.display.set_mode([606, 606])
    clock = pygame.time.Clock()
    msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [
        [145, 233], [65, 303], [170, 333]]
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [font.render(msg, True, WHITE),
             font.render(
                 'Press ENTER to continue or play again.', True, WHITE),
             font.render('Press ESCAPE to quit.', True, WHITE)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_clearance:
                        if not flag:
                            return
                        else:
                            main(screen2)
                    else:
                        main(screen2)
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
        for idx, (text, position) in enumerate(zip(texts, positions)):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)


def main(screen):
    pygame.mixer.init()
    pygame.mixer.music.load(BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font_small = pygame.font.Font(FONTPATH, 18)
    font_big = pygame.font.Font(FONTPATH, 24)
    for num_level in range(1, Levels.NUMLEVELS+1):
        if num_level == 1:
            level = Levels.Level1()
            is_clearance = startLevelGame(level, screen, font_small)
            if num_level == Levels.NUMLEVELS:
                showText(screen, font_big, is_clearance, True)
            else:
                showText(screen, font_big, is_clearance)


if __name__ == '__main__':
    scene = InterFace()
    scene.start_interface()
