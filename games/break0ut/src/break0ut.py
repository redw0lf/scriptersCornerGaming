'''
Created on Mar 25, 2013

@author: redw0lf
'''
import pygame, sys,os,random
from pygame.locals import * 

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join('../data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


#classes for our game objects
class Bar(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self, yPos):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.computerControlled = False
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.move = 5
        self.image=pygame.transform.rotate(self.image,90)
        self.rect = self.image.get_rect()
        
        self.yPos = yPos

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        newpos = self.rect.move((self.move,0))
        newpos.centery = self.yPos
        if not self.computerControlled:
            self.rect.center = (pos[0],self.yPos)
        else:
            self.rect.center
            if self.rect.left < self.area.left or \
               self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move,0))
                
            self.rect = newpos
    def increaseScore(self):
        """increases the score of the desired bar"""
        self.score = self.score+1


class Ball(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('nicubunu_Monkey_head.png', -1)
        self.image = pygame.transform.scale(self.image,(25,25))
        self.rect.w =25
        self.rect.h =25
        self.slope = 1
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.move = -2
        self.rect.center = self.area.center

    def update(self):
        "move the fist based on the mouse position"
        
        

        "lets the ball reflect from the walls"
        if self.rect.top < self.area.top or \
           self.rect.bottom > self.area.bottom:
            self.slope = -self.slope
            
        if self.rect.left < self.area.left or \
           self.rect.right > self.area.right:
            self.move = -self.move
            self.slope = -self.slope
        newpos = self.rect.move((self.move,self.move*self.slope))
        self.rect = newpos
        
    def reverse(self):
            self.slope = -self.slope
            
            
    def checkHit(self,target):
        hitbox = target.rect.inflate(-2, -2)
        
        return hitbox.colliderect(self.rect)
    
def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('break0ut')
    pygame.mouse.set_visible(0)
    
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    #Display The Background
    #  screen.blit(background, (0, 0))
    #    pygame.display.flip()

    #Prepare Game Objects
    clock = pygame.time.Clock()

    gameBar = Bar(screen.get_height()-50)
    

    playBall = Ball()
    

    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    allsprites = pygame.sprite.RenderPlain((gameBar,playBall))
    while 1:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
        
        
        "if ball has hit the bar reverse the ball"        
        if playBall.checkHit(gameBar):
            playBall.reverse()


        
   

    #Draw Everything
        allsprites.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()
