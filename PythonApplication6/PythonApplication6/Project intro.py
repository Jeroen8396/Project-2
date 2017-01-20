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
        # self.highscore = Highscore(self, self.width, self.height)
        # self.tutorial = Tutorial(self, self.width, self.height)
        # self.pause = Pause(self, self.width, self.height)

    def back(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.application.phase = "intro"
    
    def exit(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_p:
                    self.application.phase = "pause"

    def application_loop(self):
        while not process_events():
            if self.phase == "intro":
                self.intro.draw(self.screen)
            elif self.phase == "game":
                self.game.draw(self.screen)
            """
            elif self.phase == "pause":
                self.pause.draw(self.screen)
            elif self.phase == 'Highscore':
                self.highscore.draw(self.screen) 
            elif self.phase == 'Tutorial':
                self.tutorial.draw(self.screen)"""
            pygame.display.flip()

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
        self.exit_button.mouse_action(screen)
        self.tutorial_button.mouse_action(screen)
        self.highscore_button.mouse_action(screen)
        self.start_button.mouse_action(screen)

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

    def mouse_action (self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.application.phase != "game":
            if self.x + self.w > mouse_pos[0] > self.x and self.y + self.h > mouse_pos[1] > self.y:
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
        
        self.sprites(self.width, self.height)
        self.boats(self.width, self.height)
    
    def sprites(self, width, height):
        # Sprites Lifepoints
        self.BattleshipHP     = pygame.image.load("BattleshipSprite.png")
        self.BattleshipHP     = pygame.transform.scale(self.BattleshipHP, (int(width / 7), int(height / 7)))
        self.DestroyerHP      = pygame.image.load("DestroyerSprite.png")
        self.DestroyerHP      = pygame.transform.scale(self.DestroyerHP, (int(width / 7), int(height / 7)))
        self.GunboatHP        = pygame.image.load("GunboatSprite.png")
        self.GunboatHP        = pygame.transform.scale(self.GunboatHP, (int(width / 7), int(height / 7)))
        
        # Sprites Attack & Movepoints
        self.AttPoint      = pygame.image.load("AttackPoint.png")
        self.AttPoint      = pygame.transform.scale(self.AttPoint, (62, 62))
        self.MovePoint     = pygame.image.load("Movepoint.png")
        self.MovePoint     = pygame.transform.scale(self.MovePoint, (62, 62))
        
        self.ShipMovePushed = pygame.image.load("Move_Button_Pushed.png")
        self.ShipMovePushed = pygame.transform.scale(self.ShipMovePushed, (62, 62))
        self.ShipDefPushed = pygame.image.load("Def_Button_Pushed.png")
        self.ShipDefPushed = pygame.transform.scale(self.ShipDefPushed, (62, 62))
        self.ShipAttPushed = pygame.image.load("Att_Button_Pushed.png")
        self.ShipAttPushed = pygame.transform.scale(self.ShipAttPushed, (62, 62))

    def boats(self, width, height):
        self.width = width
        self.height = height
        self.Battleship = pygame.image.load("Battleship.png")
        self.Battleship = pygame.transform.scale(self.Battleship, (int(width / 31), int(height / 4.7)))
        self.Destroyer = pygame.image.load("Destroyer.png")
        self.Destroyer = pygame.transform.scale(self.Destroyer, (int(width / 24), int(height / 6.2)))
        self.Gunboat = pygame.image.load("Gunboat.png")
        self.Gunboat = pygame.transform.scale(self.Gunboat, (int(width / 15.8), int(height / 9.2)))        

    def draw (self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        screen.blit(self.Background, (0,0))

        # Screen blit Attack & Movepoints
        screen.blit(self.AttPoint, (self.width/12, self.height/4.400))
        screen.blit(self.MovePoint, (self.width/7, self.height/4.400))
        screen.blit(self.AttPoint, (self.width/12, self.height/1.750))
        screen.blit(self.MovePoint, (self.width/7, self.height/1.750))
        screen.blit(self.AttPoint, (self.width/12, self.height/1.110))
        screen.blit(self.MovePoint, (self.width/7, self.height/1.110))

        # Screen blit life sprites
        screen.blit(self.BattleshipHP, (80,500))
        screen.blit(self.DestroyerHP, (80,235))
        screen.blit(self.GunboatHP, (80,23))
        
        # Screen blit topview boats
        screen.blit(self.Battleship, (453.5, 571))
        screen.blit(self.Destroyer, (560, 571))
        screen.blit(self.Gunboat, (755, 571))
        
        if mouse_click[0]:
            if (self.width/82) + 55 > mouse_pos[0] > (self.width/82) and (self.height/25) + 55 > mouse_pos[1] > (self.height/25):
                screen.blit(self.ShipMovePushed, (self.width/82, self.height/25))
            if (self.width/70) + 55 > mouse_pos[0] > (self.width/70) and (self.height/7.300) + 55 > mouse_pos[1] > (self.height/7.300):
                screen.blit(self.ShipDefPushed, (self.width/70, self.height/7.300))  
            if (self.width/82) + 55 > mouse_pos[0] > (self.width/82) and (self.height/4.300) + 55 > mouse_pos[1] > (self.height/4.300):
                screen.blit(self.ShipAttPushed, (self.width/82, self.height/4.300))

            if (self.width/82) + 55 > mouse_pos[0] > (self.width/82) and (self.height/2.580) + 55 > mouse_pos[1] > (self.height/2.580):
                screen.blit(self.ShipMovePushed, (self.width/82, self.height/2.580))
            if (self.width/70) + 55 > mouse_pos[0] > (self.width/70) and (self.height/2.075) + 55 > mouse_pos[1] > (self.height/2.075):
                screen.blit(self.ShipDefPushed, (self.width/70, self.height/2.075))  
            if (self.width/82) + 55 > mouse_pos[0] > (self.width/82) and (self.height/1.739) + 55 > mouse_pos[1] > (self.height/1.739):
                screen.blit(self.ShipAttPushed, (self.width/82, self.height/1.739))

            if (self.width/82) + 55 > mouse_pos[0] > (self.width/82) and (self.height/1.395) + 55 > mouse_pos[1] > (self.height/1.395):
                screen.blit(self.ShipMovePushed, (self.width/82, self.height/1.395))
            if (self.width/70) + 55 > mouse_pos[0] > (self.width/70) and (self.height/1.233) + 55 > mouse_pos[1] > (self.height/1.233):
                screen.blit(self.ShipDefPushed, (self.width/70, self.height/1.233))  
            if (self.width/82) + 55 > mouse_pos[0] > (self.width/82) and (self.height/1.105) + 55 > mouse_pos[1] > (self.height/1.105):
                screen.blit(self.ShipAttPushed, (self.width/82, self.height/1.105))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            self.application.phase = "pause"
        # Application.exit(self)

class Turn:
    def __init__ (self, application):
        self.application = application
        self.turn = 0
    def update(self): 
        self.turn = self.turn + 1
    def name(self):
        if turn == 0:
            Player.player1.name = input("Put in your name")
            Player.player2.name = input("Put in your name")

class Player:
    def __init__ (self, application, turn, name):
        self.application = application
        self.turn = turn
        self.player = name
        self.boat1 = Boats.Gunboat()
        self.boat2 = Boats.Destroyer()
        self.boat3 = Boats.Battleship()
    def Boatlocation (self):
        if Player1:
            y < 100 and y > 101

class Boats:
    def __init__ (self, application, width, height):
        self.application = application
        self.width = width
        self.height = height
    def Battleship(self):
        self.LifePoints = 5
        self.Attrange = 4
        self.Defrange = 5
        self.position = (self.width, self.height)
    def Destroyer(self):
        self.LifePoints = 4
        self.Attrange = 3
        self.Defrange = 4
        self.position = (self.width, self.height)
    def Gunboat(self):
        self.LifePoints = 3
        self.Attrange = 2
        self.Defrange = 3
        self.position = (self.width, self.height)

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
        self.Yes.mouse_action(screen)
        self.No.mouse_action(screen)  
        
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
