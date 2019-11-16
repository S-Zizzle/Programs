import pygame
import sys
from math import cos, sin, radians, sqrt
from random import randint, uniform, randrange
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Asteroidz')
gameStart = False

#circle collission detection for rough calculation
#if circle collission detection says objects are close
#then call a more acurate algorithm to actually check if it's been hit

#sutherland hodgeman

#for each asteroid, have it calculate the max radius of it's shape, so that 
#doing rough check for collision is easy, you just check that max radii 
#compared to distance between object and asteroid

class Game():
    def __init__(self):
        self.w, self.h = pygame.display.get_surface().get_size()
        self.bullets = set()
        self.asteroids = set()
        self.player = Player()
        self.score = 0
        self.font = pygame.font.SysFont('freesansbold',60)
        self.background = set()
    
    def show_menu(self):
        menuText = game.font.render("Press space to begin!", 1, (255, 255, 255), 2)
        screen.blit(menuText, (self.w/4, self.h/2))

    def create_background(self):
        for _ in range(30):
            self.background.add((randint(0,self.w),randint(0,self.h)))

    def draw_background(self):
        screen.fill((0,0,0))
        for i in self.background:
            pygame.draw.circle(screen,(100,100,100),i,1)
    
    def move(self, object):
        x = object.velocity * cos(radians((90-object.angle) % 360))
        y = -(object.velocity * sin(radians((90-object.angle) % 360)))
        
        object.x += x
        object.y += y
        for vertex in object.shape:
            vertex[0] += x
            vertex[1] += y
            
        if object.x > self.w:
            object.x -= self.w
            for vertex in object.shape:
                vertex[0] -= self.w
        elif object.x < 0:
            object.x += self.w
            for vertex in object.shape:
                vertex[0] += self.w
        if object.y > self.h:
            object.y -= self.h
            for vertex in object.shape:
                vertex[1] -= self.h
        elif object.y < 0:
            object.y += self.h
            for vertex in object.shape:
                vertex[1] += self.h
    
    def calculateMaxR(self, object):
        radii = []
        for i in object.shape:
            radii.append(sqrt(i[0]**2 + i[1]**2))
        
        return max(radii)
    
    def rough_hit(self, object1, object2):
        if (object1.max_r + object2.max_r) <= (sqrt((object1.x-object2.x)**2 + (object1.y-object2.y)**2)):
            return True
        else:
            return False

class Player():
    def __init__(self):
        self.x = 400
        self.y = 400
        self.angle = 0
        self.shape = [[self.x,self.y - 15],
                      [self.x - 10,self.y + 10],
                      [self.x + 10,self.y + 10]]
        self.velocity = 0
        self.max_r = game.calculateMaxR(self)

    def rotate(self,degree):
        for idx,i in enumerate(self.shape):
            x,y = i[0],i[1]
            angleRad = radians(degree % 360)
            newPoint = (x - self.x,y - self.y)
            newPoint = (newPoint[0] * cos(angleRad) - newPoint[1] * sin(angleRad),
                        newPoint[0] * sin(angleRad) + newPoint[1] * cos(angleRad))
            newPoint = (newPoint[0] + self.x, newPoint[1] + self.y)
            self.shape[idx] = [newPoint[0],newPoint[1]]
        
    def accelerate(self):
        if self.velocity < 4:
            self.velocity += 0.1
        elif self.velocity >= 4:
            self.velocity = 4
    
    def decelerate(self):
        if self.velocity > 0:
            self.velocity -= 0.2
        elif self.velocity <= 0:
            self.velocity = 0
    
    def check_input(self):
        key = pygame.key.get_pressed()
    
        if key[pygame.K_LEFT]:
            self.angle -= 7
            self.rotate(-7)
        elif key[pygame.K_RIGHT]:
            self.angle += 7
            self.rotate(7)
    
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

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = randint(0,360)
        self.shape = [[0,0],[0,0],[0,0],[0,0],[0,0]]
        self.size = 4
        self.create_shape()
        self.velocity = uniform((2.5/self.size)*0.5,(2.5/self.size)*3)
        self.hp = self.size * 2
        self.max_r = game.calculateMaxR(self)
    
    def create_shape(self):
        var = 11
        for idx,i in enumerate(self.shape):
            angle = idx * 72
            i[0] = self.x + ((self.size * var) * sin(radians(randrange(angle-var,angle+var) % 360))) \
                   + randint(-self.size, self.size)
            i[1] = self.y + ((self.size * var) * cos(radians(randrange(angle-var,angle+var) % 360))) \
                   + randint(-self.size, self.size)
    
    def draw(self):
        tupleShape = [(self.shape[0][0],self.shape[0][1]),
                      (self.shape[1][0],self.shape[1][1]),
                      (self.shape[2][0],self.shape[2][1]),
                      (self.shape[3][0],self.shape[3][1]),
                      (self.shape[4][0],self.shape[4][1])]
        pygame.draw.polygon(screen,(255,255,255),tupleShape,2)

game = Game()
game.create_background()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if (event.type == KEYDOWN) and (event.key == K_SPACE) and (gameStart == False):
            gameStart = True
            player = Player()
            for i in range(6):
                asteroid = Asteroid(randint(0,game.w),randint(0,game.h))
                game.asteroids.add(asteroid)
    
    game.draw_background()
    if gameStart:
        player.check_input()
        game.move(player)
        for asteroid in game.asteroids:
            game.move(asteroid)
            if game.rough_hit(player, asteroid):
                print ('Rough hit')

            asteroid.draw()
        
        player.draw()
    else:
        game.show_menu()

    pygame.display.flip()
    clock.tick(35)