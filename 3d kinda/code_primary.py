import pygame
import random as r
import time as t
import math as m
import os
from pygame import mixer
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

class Game():
    def __init__(self):
        self.run = True
        self.win = pygame.display.set_mode((1200, 700))
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        self.width, self.height = self.win.get_size()
        self.text_button_list = ["start"]
        self.font = pygame.font.Font("Pixeltype.ttf", 100)
        self.mouse_held = False
        self.lists = [1, 2]
        self.list_id = ["mouse/", "wall/"]
        self.cursor_index = 0
        self.images = []
        for i in range(0, len(self.lists)):
            self.path = "sprites/" + self.list_id[i]
            for n in range(0, self.lists[i]):
                if i == 0:
                    self.images.append(pygame.transform.scale(pygame.image.load(f"{self.path}image_{str(n + 1)}.png").convert_alpha(), (self.height / 30, self.height / 30)))
                else:
                    self.images.append(pygame.transform.scale(pygame.image.load(f"{self.path}image_{str(n + 1)}.png").convert_alpha(), (270 / 9, 270 / 9)))
        self.state = 0
        #mixer.music.load("music.wav")
        #mixer.music.play(-1)
        #mixer.music.set_volume(.1)

    def drawWin(self):
        if self.state == 0:
            self.win.fill((30,30,30))
            for button in text_buttons:
                button.blit()
                button.click()
        else:
            self.win.fill((0,0,0))
            for tile in tiles:
                self.win.blit(tile.image, tile.rect)
            player.scope()
            self.win.blit(player.image, player.rect)
        self.win.blit(self.images[0], self.mouse_rect)
        pygame.display.update()

    def update(self):
        self.fps = self.clock.get_fps()
        self.mouse_rect = pygame.mouse.get_pos()
        self.mouse_rect = self.images[0].get_rect(center = self.mouse_rect)
        self.fps = self.clock.get_fps()
        self.d_t = 90 / (self.fps + 1)
        self.pressed_1, self.pressed_2, self.pressed_3 = pygame.mouse.get_pressed()
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_ESCAPE]:
            self.run = False
        if self.pressed_1 and self.mouse_held == False:
            self.cursor_index = 1
            self.mouse_held = True
        else:
            self.cursor_index = 0
        if self.pressed_1 == False:
            self.mouse_held = False

class TextButton():
    def __init__(self, x, y, font, id, colour):
        self.x = x
        self.y = y
        self.id = id
        self.font = font
        self.colour = colour
        self.rend = self.font.render(str(game.text_button_list[self.id]), False, self.colour)
        self.rect = self.rend.get_rect(center = (self.x, self.y))
    
    def blit(self):
        self.rend = self.font.render(str(game.text_button_list[self.id]), False, self.colour)
        self.rect = self.rend.get_rect(center = (self.x, self.y))
        game.win.blit(self.rend, self.rect)

    def click(self):
        if game.cursor_index == 1 and self.rect.colliderect(game.mouse_rect):
            game.state = 1

class Tile():
    def __init__(self,x,y,id):
        self.x = x
        self.y = y
        self.id = id
        self.image = game.images[self.id]
        self.rect = self.image.get_rect(center = (65 + (30 * self.x), 65 + (30 * self.y)))

class Player():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angle = 90
        self.image = pygame.transform.rotate(game.images[2], self.angle)
        self.rect = self.image.get_rect(center = (65 + (30*self.x), 65 + (30*self.y)))
        self.ray = 0
        self.stop = 0
    

    def turn(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            if self.angle >= 180:
                self.angle = -180
            self.angle += 3
        if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            if self.angle <= -180:
                self.angle = 179
            self.angle -= 3
        if self.keys[pygame.K_w] or self.keys[pygame.K_UP]:
            if self.stop == 0:
                self.x += (m.sin((self.angle + 90) / (180/m.pi)) * (160 / 3600)) 
                self.y += (m.cos((self.angle + 90) / (180/m.pi)) * (160 / 3600))
        self.image = pygame.transform.rotate(game.images[2], self.angle)
        self.rect = self.image.get_rect(center = (65 + (30*self.x), 65 + (30*self.y)))

    def scope(self):
        self.stop = 0
        for i in range(0, 25):
            self.ray = 0
            for n in range(1, 40):
                pygame.draw.line(game.win, (255 - (n * 6),0,0), ((self.x*30)+ 65 + (m.sin((self.angle + 40 + (i * 4)) / (180/m.pi)) * (3.75 * (n - 1))), (self.y*30) + 65 + (m.cos((self.angle + 40 + (i * 4)) / (180/m.pi)) * (3.75 * (n - 1)))), ((self.x*30) + 65 + (m.sin((self.angle + 40 + (i * 4)) / (180/m.pi)) * (3.75 * n)), (self.y*30) + 65 + (m.cos((self.angle + 40 + (i * 4)) / (180/m.pi)) * (3.75 * n))), 2)
                for tile in tiles:
                    if tile.rect.collidepoint((self.x*30) + 65 + (m.sin((self.angle + 40 + (i * 4)) / (180/m.pi)) * (3.75 * n)), (self.y*30) + 65 + (m.cos((self.angle + 40 + (i * 4)) / (180/m.pi)) * (3.75 * n))):
                        if i == 12 and n >= 0 and n <= 2:
                            self.stop = 1
                        pygame.draw.circle(game.win, (255, 0, 255), (((self.x*30) + 65 + (m.sin((self.angle + 40 + (i * 4)) / (180/m.pi)) * (3.75 * n)), (self.y*30) + 65 + (m.cos((self.angle + 40 + (i * 4)) / (180/m.pi)) * (3.75 * n)))), 3)
                        self.surface = pygame.surface.Surface((14, 500))
                        self.surface.fill((169, 162, 10))
                        self.surface.set_alpha(240 - (n * 6))
                        game.win.blit(self.surface, (1100 - (28 * i), 100))
                        self.surface.fill((139, 134, 8))
                        self.surface.set_alpha(240 - (n * 6))
                        game.win.blit(self.surface, (1114 - (28 * i), 100))
                        self.ray = 1
                        break
                if self.ray == 1:
                    break
map = [         
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,1,0,1,1],
    [1,0,1,0,0,1,0,0,1],
    [1,0,0,0,0,1,1,0,1],
    [1,1,1,0,0,0,0,0,1],
    [0,0,1,1,1,1,1,1,1],
]

game = Game()
text_buttons = []
tiles = []
player = Player(6, 2)
text_buttons.append(TextButton((game.width / 2),(game.height / 2), game.font, 0, (0,0,0)))

for i in range(0,9):
    for n in range(0,9):
        if map[i][n] != 0:
            tiles.append(Tile(n,i,map[i][n]))

while game.run:
    game.clock.tick(30)

    MousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False

    game.update()
    game.drawWin()
    player.turn()

pygame.quit()