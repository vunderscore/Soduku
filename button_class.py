import pygame
from settings import *

#class creates button#
class button:

    def __init__(self,x,y,width,height,text= None,colour=red,highlitedcolour=shadowcolour,function=None,params=None):
        self.buttonimage=pygame.Surface((width,height))
        self.pos=(x,y)
        self.rect=self.buttonimage.get_rect()
        self.rect.topleft=self.pos
        self.text=text
        self.colour=colour
        self.highlitedcolour=highlitedcolour
        self.function=function
        self.params = params
        self.highlited=False
        self.width=width
        self.height=height

#updates details such as mousepos#
    def update(self,mouse):
        if(self.rect.collidepoint(mouse)):
            self.highlited=True
        else:
            self.highlited=False

#draws the button#
    def draw(self,window):
        if(self.highlited):
            self.buttonimage.fill(self.highlitedcolour)
        else:
            self.buttonimage.fill(self.colour)

        if self.text:
            self.drawtext(self.text)
            
        window.blit(self.buttonimage,self.pos)


#executes function when button is clicked#
    def click(self):
        if self.params:
            self.function(self.params)
        else:
            self.function()
            
#draws the buton text#
    def drawtext(self,text):
        global z
        font = pygame.font.SysFont('arial',20,bold=1)
        texter = font.render(text,False,black)
        width,height=texter.get_size()
        x = (self.width - width)//2 
        y = self.height//13
        z=x,y
        self.buttonimage.blit(texter,(x,y))

