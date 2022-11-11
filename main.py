'''
main page
'''
from calendar import c
import os
import random
import sys

import pygame
from pygame import font
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
import Levels
import pacman


class Color:
    ACHIEVEMENT = (220, 160, 87)
    VERSION = (220, 160, 87)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    SKYBLUE = (0, 191, 255)
    TRANSPARENT = (255, 255, 255, 0)


ICONPATH = os.path.join(os.getcwd(), 'resources/images/icon.png')


class Text:
    def __init__(self, text: str, text_color: Color, font_type: str, font_size: int):
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
        # Image('ink.png', ratio=0.4).draw(
        #     screen, width * 0.52, height * 0.67)  # 墨印
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

        pacman.main(screen2)
