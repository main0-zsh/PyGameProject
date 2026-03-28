import pygame
from random import*

pygame.init()

screen_width=800
screen_height=400
screen=pygame.display.set_mode((screen_width,screen_height))

white=(255,255,255)
black=(0,0,0)

clock=pygame.time.Clock()
FPS=30

class Dino:
    def __init__(self):
        self.x=50
        self.y=300
        self.width=40
        self.height=60
        self.is_jumping=False
        self.jump_count=10
        self.gravity=1
    def draw(self):
        pygame.draw.rect(screen, black, (self.x,self.y,self.width,self.height))
    def move(self):
        if self.is_jumping:
            if self.jump_count>=-10:
                neg=1
                if self.jump_count<0:
                    neg=-1
                self.y-=(self.jump_count**2)*0.5*neg
                self.jump_count-=1
            else:
                self.is_jumping=False
                self.jump_count=10
    def get_rect(self):
        return pygame.Rect((self.x,self.y,self.width,self.height))

class Obstacle:
    def __init__(self,x,y,width,height,speed):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.speed=speed
    def draw(self):
        pygame.draw.rect(screen,black,(self.x,self.y,self.width,self.height))
    def move(self):
        self.x-=self.speed
        if self.x<-self.width:
            self.x=screen_width
            self.height+=choice([10,20,30,40,50,-10,-20,-30,-40,-50])
            if self.height>100:
                self.height=100
            elif self.height<50:
                self.height=50
            if self.height==60:
                self.y = 300 + (60 - self.height)
            if self.height == 70:
                self.y = 300 + (60 - self.height)
            if self.height == 80:
                self.y = 300 + (60 - self.height)
            if self.height == 90:
                self.y = 300 + (60 - self.height)
            if obstacle.x + obstacle.width < dino.x:
                obstacle.speed += 0.1
            self.speed+=choice([1,2,3,4,5,6,7,8,9,10,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10])
            if self.speed>=20:
                self.speed=20
            elif self.speed<10:
                self.speed=10
    def get_rect(self):
        return pygame.Rect((self.x,self.y,self.width,self.height))

dino=Dino()
obstacle=Obstacle(800,300,40,randint(50,100),randint(10,15))
score=0
running=True

while running:
    screen.fill(white)
    dino.draw()
    obstacle.draw()
    obstacle.move()

    rect1 = Dino.get_rect(dino)
    rect2 = Obstacle.get_rect(obstacle)

    if rect1.colliderect(rect2):
        dino.x=50
        obstacle.x=800
        score=0

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    keys=pygame.key.get_pressed()
    if not dino.is_jumping:
        if keys[pygame.K_SPACE]:
            dino.is_jumping=True

    dino.move()

    if obstacle.x+obstacle.width<dino.x:
        score+=1
        obstacle.speed+=0.1
    font=pygame.font.SysFont("Arial", 36)
    score_text=font.render("Score:"+str(score),True,black)
    screen.blit(score_text,(10,10))

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()