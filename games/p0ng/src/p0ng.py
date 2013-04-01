'''
Created on Mar 21, 2013

@author: redw0lf
'''

if __name__ == '__main__':
    pass

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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.computerControlled = False
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.move = 5
        self.score = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        newpos = self.rect.move((0, self.move))
        newpos.centerx = self.xPos
        if not self.computerControlled:
            self.rect.center = (self.xPos,pos[1])
        else:
            self.rect.center
            if self.rect.top < self.area.top or \
               self.rect.bottom > self.area.bottom:
                self.move = -self.move
                newpos = self.rect.move((0, self.move))
                
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
        self.hasHitBorder = False;

    def update(self):
        "move the fist based on the mouse position"
        
        newpos = self.rect.move((self.move,self.move*self.slope))

        if self.rect.top < self.area.top or \
           self.rect.bottom > self.area.bottom:
            self.slope = -self.slope
            newpos = self.rect.move((self.move,self.move*self.slope))
        if self.rect.left < self.area.left or \
           self.rect.right > self.area.right:
            self.hasHitBorder = True;
        if self.rect.centerx < self.area.centerx:
            self.isLeft = True
        else:
            self.isLeft = False
            
            
        self.rect = newpos
        
    def reverse(self):
            self.move = -self.move
            self.slope = -self.slope
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.hasHitBorder = False
            
    def checkHit(self,target):
        hitbox = target.rect.inflate(-5, -5)
        return hitbox.colliderect(self.rect)





def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((500, 200))
    pygame.display.set_caption('monkey p0ng')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    #Display The Background
  #  screen.blit(background, (0, 0))
#    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()

    leftBar = Bar()
    leftBar.xPos = 25
    rightBar = Bar()
    rightBar.xPos = 475
    rightBar.computerControlled = True
    playBall = Ball()
    
    
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render(str(leftBar.score) + ':' + str(rightBar.score), 1, (250, 250, 250))
       
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
        
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    allsprites = pygame.sprite.RenderPlain((leftBar,rightBar,playBall))
    while 1:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
        allsprites.update()
        if playBall.checkHit(rightBar) or \
           playBall.checkHit(leftBar):
            playBall.reverse()
        if playBall.hasHitBorder and playBall.isLeft:
            leftBar.increaseScore()
            playBall.rect.center = playBall.area.center
            playBall.reverse()
            
        elif playBall.hasHitBorder and not playBall.isLeft:
            rightBar.increaseScore()
            playBall.rect.center = playBall.area.center
            playBall.reverse()
                
        
        text = font.render(str(leftBar.score) + ':' + str(rightBar.score), 1, (250, 250, 250),(0,0,0))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

    #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
            
            

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()