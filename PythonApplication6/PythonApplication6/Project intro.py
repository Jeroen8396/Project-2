# Copyright 2017
# Simon de Bakker, Raoul van Duivenvoorde, Jeroen de Schepper

import pygame
from pygame.locals import*
import sys
import math

class Application:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.size = (self.width, self.height)
    
        pygame.init()
    
        self.screen = pygame.display.set_mode((self.size))#, pygame.FULLSCREEN)
        self.phase = "intro"
        self.intro = Intro(self, self.width, self.height)
        self.game = Game(self, self.width, self.height)
        self.highscore = Highscore(self, self.width, self.height)
        self.tutorial = Tutorial(self, self.width, self.height)
        self.pause = Pause(self, self.width, self.height)

    def back(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.application.phase = "intro"
    
    def exit(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.application.phase = "pause"

    def application_loop(self):
        while not process_events():
            if self.phase == "intro":
                self.intro.draw(self.screen)
            elif self.phase == "game":
                self.game.draw(self.screen)
            elif self.phase == "pause":
                self.pause.draw(self.screen)
            elif self.phase == 'Highscore':
                self.highscore.draw(self.screen) 
            elif self.phase == 'Tutorial':
                self.tutorial.draw(self.screen)
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

class Intro:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg") #easteregg
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.exit_button = Button(self.application, 'Exit', (width/15), (height/1.25), 170, 50)
        self.tutorial_button = Button(self.application, 'Tutorial', (width/15), (height/1.4), 170, 50)
        self.highscore_button = Button(self.application, 'Highscore', (width/15), (height/1.6), 170, 50)
        self.start_button = Button(self.application, 'Start', (width/15), (height/1.86), 170, 50)
        self.width = width
        self.height = height

    def draw (self, screen):
        screen.blit(self.Background,(0, 0))
        title_text = self.font.render("BattlePort", 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9)))
        self.exit_button.draw(screen)
        self.tutorial_button.draw(screen)
        self.highscore_button.draw(screen)
        self.start_button.draw(screen)

class Button:
    def __init__(self, application, text, x, y, w, h):
        self.application = application
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.surface = pygame.Surface((w, h))
        self.font = pygame.font.Font(None, 45)

    def draw (self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.x + 170 > mouse_pos[0] > self.x and self.y + 50 > mouse_pos[1] > self.y:
            screen.blit(self.surface, (self.x, self.y))
            button_text = self.font.render(self.text, 1, (255,255,255))
            screen.blit(button_text,(( self.x + 5), (self.y + 11)))
            if mouse_click[0]:
                print (self.text)
                if self.text == 'Start':
                    self.application.phase = "game"
                elif self.text == 'Tutorial':
                    self.application.phase = 'Tutorial'
                elif self.text == 'Highscore':
                    self.application.phase = "Highscore"
                elif self.text == '  Yes':
                    self.application.phase = "intro"
                elif self.text == '   No':
                    self.application.phase = "game"
                elif self.text == 'Exit':
                    sys.exit()
        else:
            screen.blit(self.surface, (self.x, self.y))
            button_text = self.font.render(self.text, 1, (255,120,0))
            screen.blit(button_text,((self.x + 5), (self.y + 11)))

class Game:
    def __init__ (self, application, width, height):
        self.pause = Pause
        self.surface = pygame.Surface((width, height))
        self.application = application
        self.Background = pygame.image.load("Speelbord.png")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.width = width
        self.height = height
        
        # Buttons ship actions
        self.Ship1Move      = Button(self.application, '', (width/70), (height/22.80), 55, 55)
        self.Ship1Def       = Button(self.application, '', (width/70), (height/7.300), 55, 55)
        self.Ship1Att       = Button(self.application, '', (width/70), (height/4.300), 55, 55)
        self.Ship2Move      = Button(self.application, '', (width/70), (height/2.580), 55, 55)
        self.Ship2Def       = Button(self.application, '', (width/75), (height/2.075), 55, 55)
        self.Ship2Att       = Button(self.application, '', (width/75), (height/1.739), 55, 55)
        self.Ship3Move      = Button(self.application, '', (width/75), (height/1.395), 55, 55)
        self.Ship3Def       = Button(self.application, '', (width/75), (height/1.233), 55, 55)
        self.Ship3Att       = Button(self.application, '', (width/75), (height/1.105), 55, 55)

        self.BAttPoint1     = Button(self.application, '', (width/12), (height/4.400), 62, 62)
        self.BMovePoint1    = Button(self.application, '', (width/7 ), (height/4.400), 62, 62)
        self.BAttPoint2     = Button(self.application, '', (width/12), (height/1.750), 62, 62)
        self.BMovePoint2    = Button(self.application, '', (width/7 ), (height/1.750), 62, 62)
        self.BAttPoint3     = Button(self.application, '', (width/12), (height/1.110), 62, 62)
        self.BMovePoint3    = Button(self.application, '', (width/7 ), (height/1.110), 62, 62)

        # Sprites Lifepoints
        self.Battleship     = pygame.image.load("BattleshipSprite.png")
        self.Battleship     = pygame.transform.scale(self.Battleship, (int(width / 7), int(height / 7)))
        self.Destroyer      = pygame.image.load("DestroyerSprite.png")
        self.Destroyer      = pygame.transform.scale(self.Destroyer, (int(width / 7), int(height / 7)))
        self.Gunboat        = pygame.image.load("GunboatSprite.png")
        self.Gunboat        = pygame.transform.scale(self.Gunboat, (int(width / 7), int(height / 7)))
        
        # Sprites Attack & Movepoints
        self.AttPoint1      = pygame.image.load("AttackPoint.png")
        self.AttPoint1      = pygame.transform.scale(self.AttPoint1, (62, 62))
        self.MovePoint1     = pygame.image.load("Movepoint.png")
        self.MovePoint1     = pygame.transform.scale(self.MovePoint1, (62, 62))
        self.AttPoint2      = pygame.image.load("AttackPoint.png")
        self.AttPoint2      = pygame.transform.scale(self.AttPoint2, (62, 62))
        self.MovePoint2     = pygame.image.load("Movepoint.png")
        self.MovePoint2     = pygame.transform.scale(self.MovePoint2, (62, 62))
        self.AttPoint3      = pygame.image.load("AttackPoint.png")
        self.AttPoint3      = pygame.transform.scale(self.AttPoint3, (62, 62))
        self.MovePoint3     = pygame.image.load("Movepoint.png")
        self.MovePoint3     = pygame.transform.scale(self.MovePoint3, (62, 62))

    def draw (self, screen):
        screen.blit(self.Background, (0,0))

        # Screen blit Attack & Movepoints
        screen.blit(self.AttPoint1, (self.width/12, self.height/4.400))
        screen.blit(self.MovePoint1, (self.width/7, self.height/4.400))
        screen.blit(self.AttPoint2, (self.width/12, self.height/1.750))
        screen.blit(self.MovePoint2, (self.width/7, self.height/1.750))
        screen.blit(self.AttPoint3, (self.width/12, self.height/1.110))
        screen.blit(self.MovePoint3, (self.width/7, self.height/1.110))

        # Screen blit life sprites
        screen.blit(self.Battleship, (80,500))
        screen.blit(self.Destroyer, (80,235))
        screen.blit(self.Gunboat, (80,23))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            self.application.phase = "pause"
        Application.exit(self)
        
class Pause:
    def __init__ (self, application, width, height):
        self.application = application
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('arial', 150)
        self.font1 = pygame.font.SysFont('arial', 50)

        self.Yes = Button(self.application, '  Yes', (self.width/2.75), (self.height/1.7), 100, 55)
        self.No  = Button(self.application, '   No', (self.width/1.82), (self.height/1.7), 100, 55)
        
    def draw(self, screen):
        title_text = self.font.render("Pause", 1, (255,120,0))
        screen.blit(title_text,((self.width / 2.8) , (self.height / 6)))
        title_text1 = self.font1.render("Do you want to quit the game?", 1, (255,120,0))
        screen.blit(title_text1,((self.width / 3.5) , (self.height / 2.5)))
        self.Yes.draw(screen)
        self.No.draw(screen)  
        
class Highscore:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.width = width
        self.height = height 

    def draw (self, screen):
        screen.blit(self.Background,(0,0))
        title_text = self.font.render("Highscore", 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9)))
        Application.back(self)
    
class Tutorial:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.width = width
        self.height = height 

    def draw (self, screen):
        screen.blit(self.Background,(0,0))
        title_text = self.font.render("Tutorial", 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9)))
        Application.back(self)
          
def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def program():
    application = Application()
    application.application_loop()

program()
