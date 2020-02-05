import pygame
import sys
from math import cos, sin, radians, sqrt, atan, degrees
from random import randint, uniform, randrange
from pygame.locals import *
from numpy import array

class Game:
    def __init__(self):
        self.w, self.h = pygame.display.get_surface().get_size()
        self.bullets = []
        self.asteroids = []
        self.player = None
        self.score = 0
        self.font = pygame.font.SysFont('freesansbold',60)
    
    def rough_hit(self, object1, object2):
        if (object1.max_r + object2.max_r) <= (sqrt((object1.x-object2.x)**2 + (object2.y-object1.y)**2)):
            return False
        return True
    
    def show_menu(self):
        font = pygame.font.SysFont('freesansbold', 60)
        menuText = font.render('Press space to begin!', 1, (255,255,255), 2)
        screen.blit(menuText, (200,300))

    def draw_background(self):
        screen.fill((0,0,0))
        for i in background:
            pygame.draw.circle(screen,(100,100,100),i,1)

class GameObject:
    def __init__(self, object_type, x, y):
        self.x = x
        self.y = y
        self.velocity = array([0,0],dtype=float)
        self.speed = 0
        
        if object_type == "asteroid":
            self.shape = [[0,0],[0,0],[0,0],[0,0],[0,0]]
            self.size = 4
            self.hp = self.size * 2
            self.angle = randint(0,360)
        elif object_type == "player":
            self.angle = 0
            self.shape = [[self.x,self.y - 15],
                      [self.x - 10,self.y + 10],
                      [self.x + 10,self.y + 10]]
            self.calculateMaxR()

    def move(self):
        x_change = self.speed * sin(radians(self.angle))
        y_change = self.speed * -cos(radians(self.angle))
        self.x += x_change
        self.y += y_change

        for vertex in self.shape:
            vertex[0] += x_change
            vertex[1] += y_change
        
        if self.x - self.max_r > game.w:
            self.x -= game.w + self.max_r
            for vertex in self.shape:
                vertex[0] -= game.w
        elif self.x + self.max_r < 0:
            self.x += game.w - self.max_r
            for vertex in self.shape:
                vertex[0] += game.w
        if self.y - self.max_r > game.h:
            self.y -= game.h + self.max_r
            for vertex in self.shape:
                vertex[1] -= game.h
        elif self.y + self.max_r < 0:
            self.y += game.h - self.max_r
            for vertex in self.shape:
                vertex[1] += game.h
    
    def calculateMaxR(self):
        radii = []
        for i in self.shape:
            dist = sqrt((self.x - i[0])**2 + (self.y - i[1])**2)
            radii.append(dist)
        
        self.max_r = max(radii)

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__("player",400,400)

    def rotate(self,degree):
        self.angle += degree
        for idx,i in enumerate(self.shape):
            x,y = i[0],i[1]
            angleRad = radians(degree % 360)
            newPoint = (x - self.x,y - self.y)
            newPoint = (newPoint[0] * cos(angleRad) - newPoint[1] * sin(angleRad),
                        newPoint[0] * sin(angleRad) + newPoint[1] * cos(angleRad))
            newPoint = (newPoint[0] + self.x, newPoint[1] + self.y)
            self.shape[idx] = [newPoint[0],newPoint[1]]
        
    def accelerate(self):
        if self.speed <= 4:
            self.speed += 0.1

    def decelerate(self):
        if self.speed >= 0:
            self.speed -= 0.1
    
    def check_input(self):
        key = pygame.key.get_pressed()
    
        if key[pygame.K_LEFT]:
            self.rotate(-11)
        elif key[pygame.K_RIGHT]:
            self.rotate(11)
    
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
    
        if key[pygame.K_UP]:
            self.accelerate()
        elif key[pygame.K_DOWN]:
            self.decelerate()

    def draw(self):
        tupleShape = [(self.shape[0][0],self.shape[0][1]),
                      (self.shape[1][0],self.shape[1][1]),
                      (self.shape[2][0],self.shape[2][1])]
        pygame.draw.polygon(screen,(255,255,255),tupleShape,2)

class Asteroid(GameObject):
    def __init__(self, x, y):
        super(Asteroid,self).__init__("asteroid",x,y)
        self.create_shape()
        self.calculateMaxR()
        self.speed = uniform(-5.25/self.size,5.25/self.size)

    def create_shape(self):
        var = 11
        for idx,i in enumerate(self.shape):
            angle = idx * 72
            i[0] = self.x + ((self.size * var) * sin(radians(randrange(angle-var,angle+var) % 360))) \
                   + randint(-self.size, self.size)
            i[1] = self.y + ((self.size * var) * cos(radians(randrange(angle-var,angle+var) % 360))) \
                   + randint(-self.size, self.size)
    
    def collision_with_asteroid(self, object):
        self.speed, object.speed = object.speed, self.speed
        self.angle, object.angle = object.angle, self.angle
    
    def draw(self):
        tupleShape = [(self.shape[0][0],self.shape[0][1]),
                      (self.shape[1][0],self.shape[1][1]),
                      (self.shape[2][0],self.shape[2][1]),
                      (self.shape[3][0],self.shape[3][1]),
                      (self.shape[4][0],self.shape[4][1])]
        pygame.draw.polygon(screen,(255,255,255),tupleShape,2)

pygame.init() 
pygame.font.init() #should be initialised with pygame.init() but wasn't working, adding this line fixed issues. Maybe delete in future
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Asteroidz')
gameStart = False
background = set()
for _ in range(30):
    background.add((randint(0,800),randint(0,600)))

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();sys.exit()
        
        if (event.type == KEYDOWN) and (event.key == K_SPACE) and (gameStart == False):
            game.player = Player()
            for i in range(6):
                asteroid = Asteroid(150*i,100)
                game.asteroids.append(asteroid)

            gameStart = True

    game.draw_background()

    if not gameStart:
        game.show_menu()
    else:
        game.player.check_input()

        temp_asteroids = game.asteroids.copy()
        for idx, asteroid in enumerate(game.asteroids):
            if game.rough_hit(game.player,asteroid):
                #print ("Player and asteroid collided!")
                pass

            for temp_asteroid in temp_asteroids:
                if temp_asteroid != asteroid:
                    if game.rough_hit(temp_asteroid,asteroid):
                        temp_asteroid.collision_with_asteroid(asteroid)
            
            for bullet in game.bullets:
                #compare asteroid with all bullets
                pass
            
            asteroid.move()
            asteroid.draw()
        
        game.player.move()
        game.player.draw()
    
    pygame.display.flip()
    clock.tick(35)