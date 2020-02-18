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
        self.score = 0
        self.font = pygame.font.SysFont('freesansbold',60)
    
    def rough_hit(self, object1, object2):
        if (object1.max_r + object2.max_r) <= (sqrt((object1.x-object2.x)**2 + (object2.y-object1.y)**2)):
            return False
        return True
    
    def show_menu(self):
        font = pygame.font.SysFont('freesansbold', 60)
        menu_text = font.render('Press space to begin!', 1, (255,255,255), 2)
        screen.blit(menu_text, (200,300))

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
            self. max_r = self.calculate_max_r()

    def move(self):
        dx = self.speed * sin(radians(self.angle))
        dy = self.speed * -cos(radians(self.angle))
        self.x += dx
        self.y += dy

        for vertex in self.shape:
            vertex[0] += dx
            vertex[1] += dy

        #if self wraps around screen
        if (self.x - self.max_r) > game.w: #self goes right side
            self.x = self.x - game.w - self.max_r
            for vertex in self.shape:
                vertex[0] = vertex[0] - game.w - self.max_r
        elif (self.x + self.max_r) < 0: #self goes left side
            self.x = self.x + game.w + self.max_r
            for vertex in self.shape:
                vertex[0] = vertex[0] + game.w + self.max_r

        if (self.y - self.max_r) > game.h: #self goes bottom side
            self.y = self.y - game.h - self.max_r
            for vertex in self.shape:
                vertex[1] = vertex[1] - game.h - self.max_r
        elif (self.y + self.max_r) < 0: #self goes top side
            self.y = self.y + game.h + self.max_r
            for vertex in self.shape:
                vertex[1] = vertex[1] + game.h + self.max_r
    
    def calculate_max_r(self):
        radii = []
        for i in self.shape:
            dist = sqrt((self.x - i[0])**2 + (self.y - i[1])**2)
            radii.append(dist)
        
        return max(radii)

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__("player",400,400)
        self.lives = 3

    def rotate(self,degree):
        self.angle += degree

        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
            
        for idx,i in enumerate(self.shape):
            x,y = i[0],i[1]
            angle_rad = radians(degree % 360) #check if mod 360 is needed here
            new_point = (x - self.x,y - self.y)
            new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                        new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
            new_point = (new_point[0] + self.x, new_point[1] + self.y)
            self.shape[idx] = [new_point[0],new_point[1]]
        
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
    
        if key[pygame.K_UP]:
            self.accelerate()
        elif key[pygame.K_DOWN]:
            self.decelerate()
    
    def hit(self):
        if self.lives:
            self.lives -= 1
            #move to start coordinates, flash, and be invinsible for 1 second or so
        else:
            #player is dead
            pass

    def draw(self):
        tuple_shape = [(self.shape[0][0],self.shape[0][1]),
                      (self.shape[1][0],self.shape[1][1]),
                      (self.shape[2][0],self.shape[2][1])]
        pygame.draw.polygon(screen,(255,255,255),tuple_shape,2)

class Asteroid(GameObject):
    def __init__(self, x, y):
        super(Asteroid,self).__init__("asteroid",x,y)
        self.create_shape()
        self.max_r = self.calculate_max_r()
        self.speed = uniform(-5.25/self.size,5.25/self.size)

    def create_shape(self):
        VAR = 11
        for idx,i in enumerate(self.shape):
            angle = idx * 72 #check if mod 360 is needed on lines below
            i[0] = self.x + ((self.size * VAR) * sin(radians(randrange(angle-VAR,angle+VAR) % 360))) \
                   + randint(-self.size, self.size)
            i[1] = self.y + ((self.size * VAR) * cos(radians(randrange(angle-VAR,angle+VAR) % 360))) \
                   + randint(-self.size, self.size)
    
    def collision_with_asteroid(self, object):
        self.speed, object.speed = object.speed, self.speed
        self.angle, object.angle = object.angle, self.angle
    
    def draw(self):
        tuple_shape = [(self.shape[0][0],self.shape[0][1]),
                      (self.shape[1][0],self.shape[1][1]),
                      (self.shape[2][0],self.shape[2][1]),
                      (self.shape[3][0],self.shape[3][1]),
                      (self.shape[4][0],self.shape[4][1])]
        pygame.draw.polygon(screen,(255,255,255),tuple_shape,2)

pygame.init() 
pygame.font.init() #should be initialised with pygame.init() but wasn't working, adding this line fixed issues. Maybe delete in future
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Asteroidz')
game_start = False
background = set()
for _ in range(30):
    background.add((randint(0,800),randint(0,600)))

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();sys.exit()
        
        if (event.type == KEYDOWN) and (event.key == K_SPACE) and (game_start == False):
            player = Player()
            for i in range(6):
                asteroid = Asteroid(150*i,100)
                game.asteroids.append(asteroid)

            game_start = True

    game.draw_background()

    if not game_start:
        game.show_menu()
    else:
        player.check_input()

        temp_asteroids = game.asteroids.copy()
        for idx, asteroid in enumerate(game.asteroids):
            if game.rough_hit(player,asteroid):
                player.hit()

            for temp_asteroid in temp_asteroids: #this is terrible fix these 4 lines make better
                if temp_asteroid != asteroid:
                    if game.rough_hit(temp_asteroid,asteroid):
                        temp_asteroid.collision_with_asteroid(asteroid)
            
            for bullet in game.bullets:
                #compare asteroid with all bullets
                pass
            
            asteroid.move()
            asteroid.draw()
        
        player.move()
        player.draw()
    
    pygame.display.flip()
    clock.tick(35)