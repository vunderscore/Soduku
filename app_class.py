from settings import *
import pygame
import sqlite3
import matplotlib.pyplot as plt 
import numpy as np
from button_class import *
from boardcreator import *

#creating the game#
class App:

    def __init__(self):
        pygame.init()

        
        self.window= pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('sudoku')
        self.running= True
        self.sel=None
        self.mousepos=None
        self.state=1
        self.finished= False
        self.cellchanged = False
        self.plotter=False
        self.font=pygame.font.SysFont("arial",colsize//2)
        self.current_time=0
        self.finishedtime=0
        self.tries=0
        self.ntry=None
        self.fintime= None

        conn= sqlite3.connect('sudoku1.db')
        cur=conn.cursor()
        cur.execute("""CREATE TABLE info (
                         try integer,
                         ftime integer  
                         )""") 
        conn.commit()
        
        xlist=[]
        ylist=[]
        self.incorrectcells=[]
        self.playingbuttons=[]
        
        self.lockedcells=[]
        self.board=[]

        self.createpuzzle(1)
        self.load()
        

    def run(self):
        

        while self.running :
            if(self.state==1):
                self.playing_event()
                self.playing_update()
                self.playing_draw()

        self.droptable()

        

# plyaing state

    def playing_event(self):
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                self.running= False
            # user clicks
            if(event.type==pygame.MOUSEBUTTONDOWN):
                sel=self.mouseboardpos()
                if(sel):
                    self.sel=sel
                else:
                    self.sel=None
                    for button in self.playingbuttons:
                        if button.highlited:
                            button.click()
            # user inputs a character from keyboard
            if(event.type==pygame.KEYDOWN):
                if (self.sel != None and self.sel not in self.lockedcells):
                    if (self.checkint(event.unicode)):
                        #changing/inputing cells
                        self.board[self.sel[1]][self.sel[0]]=int(event.unicode)
                        self.cellchanged = True


    def playing_update(self):

        self.mousepos=pygame.mouse.get_pos()

        
        for button in self.playingbuttons:
            button.update(self.mousepos)


        #checking the cells

        if(self.cellchanged):
            self.incorrectcells=[]
            if(self.allcellsfilled()):
                #checking if cells are correct
                self.checkallcells()
                if(len(self.incorrectcells)==0):
                    self.finished=True

        #getting time            
        #getting finished time

        if(self.finished):
            self.finishedtime=pygame.time.get_ticks() - self.current_time 
            self.current_time=self.finishedtime
            print(self.finishedtime)
            self.tries=self.tries+1

            #inputing values into sql table#
            self.sqlint(self.tries,self.finishedtime)
            self.getinfo()
            print(self.ntry,self.fintime)

            #creating time delay#
            pygame.time.delay(1000)

            #plotting the graph based on user performance#
            self.finished=False
            if(self.tries>=5):
                self.plotter= True
            if(self.plotter):
                self.plot()
                self.plotter=False
        
            
# the drawing function which takes care of all the visual remarks on the window surface#
    def playing_draw(self):
        self.window.fill(white)

        for button in self.playingbuttons:
            button.draw(self.window)

        self.drawselsquare(self.window,self.sel)

        self.shadelockedcells(self.window,self.lockedcells)
        
        self.shadeincorrectcells(self.window,self.incorrectcells)

        self.drawnumbers(self.window,self.board)

        self.drawboard(self.window)

        pygame.display.update()

        self.cellchanged = False


#  BOARD FUNCTIONS

    def allcellsfilled(self):
        for row in self.board:
            for n in row:
                if(n==0):
                    return False
        return True

#function to check if entered values are valid#
    def checkallcells(self):
        self.checkrowcells()
        self.checkcolcells()
        self.checkminigrid()

#checks the row#
    def checkrowcells(self):
        for yidx,row in enumerate(self.board):
            possibles=[1,2,3,4,5,6,7,8,9]
            for xidx in range(9):
                value=self.board[yidx][xidx]
                if(value in possibles):
                    possibles.remove(value)
                else:
                    if((xidx,yidx) not in self.lockedcells and [xidx,yidx] not in self.incorrectcells ):
                        self.incorrectcells.append([xidx,yidx])
                    if((xidx,yidx) in self.lockedcells):
                        for i in range(9):
                            if(self.board[yidx][i] == value and (i,yidx) not in self.lockedcells):
                                self.incorrectcells.append([i,yidx])
#checks the columns#
    def checkcolcells(self):
        for xidx in range(9):
            possibles=[1,2,3,4,5,6,7,8,9]
            for yidx,row in enumerate(self.board):
                value=self.board[yidx][xidx]
                if(value in possibles):
                    possibles.remove(value)
                else:
                    if((xidx,yidx) not in self.lockedcells and [xidx,yidx] not in self.incorrectcells):
                        self.incorrectcells.append([xidx,yidx])
                    if((xidx,yidx) in self.lockedcells):
                        for i,row in enumerate(self.board):
                            if(self.board[i][xidx] == value and (xidx,i) not in self.lockedcells):
                                self.incorrectcells.append([xidx,i])
#checks the blocks#
    def checkminigrid(self):
        for y in range(3):
            for x in range(3):
                possibles=[1,2,3,4,5,6,7,8,9]
                for i in range(3):
                    for j in range(3):
                        yidx=y*3 + i
                        xidx=x*3 + j
                        value=self.board[xidx][yidx]
                        if(value in possibles):
                            possibles.remove(value)
                        else:
                            if((xidx,yidx) not in self.lockedcells and [xidx,yidx] not in self.incorrectcells):
                                self.incorrectcells.append([xidx,yidx])
                            if((xidx,yidx) in self.lockedcells):
                                for k in range(3):
                                    for l in range(3):
                                        yidx2=y*3 + k
                                        xidx2=x*3 + l
                                        if(self.board[xidx2][yidx2]==value and (xidx2,yidx2) not in self.lockedcells):
                                            self.incorrectcells.append([xidx2,yidx2])



#  HELP FUNCTIONS

#creates the 2d array which contains the board#
    def createpuzzle(self,z=1):
        y=finalcreate(z)


        self.board = y
        self.load()

#draws the outline of the grid#
    def drawboard(self,window):
        pygame.draw.rect(window,black,(boardpos[0],boardpos[1],WIDTH-250,HEIGHT-250),2)

        for i in range(9):
            if(i%3==0 and i!=0):
                pygame.draw.line(window,red,(boardpos[0]+(i*colsize),boardpos[1]),(boardpos[0]+(i*colsize),boardpos[1]+450),2)
                pygame.draw.line(window,red,(boardpos[0],boardpos[1]++(i*colsize)),(boardpos[0]+450,boardpos[1]+(i*colsize)),2)


            else:
                pygame.draw.line(window,black,(boardpos[0]+(i*colsize),boardpos[1]),(boardpos[0]+(i*colsize),boardpos[1]+450))
                pygame.draw.line(window,black,(boardpos[0],boardpos[1]++(i*colsize)),(boardpos[0]+450,boardpos[1]+(i*colsize)))

# checks if mouse position within board#
    def mouseboardpos(self):
        if(self.mousepos!=None):
            if(self.mousepos[0] < boardpos[0] or self.mousepos[1] < boardpos[1] ):
                return False
            if(self.mousepos[0] > boardpos[0]+boardsize or self.mousepos[1] > boardpos[1]+boardsize ):
                return False
            return ((self.mousepos[0]-boardpos[0])//colsize,((self.mousepos[1]-boardpos[1])//colsize))

#draws the selected square#
    def drawselsquare(self,window,pos):
        if(self.sel != None):
            pygame.draw.rect(window,lblue,((pos[0]*colsize)+boardpos[0],(pos[1]*colsize)+boardpos[1],colsize,colsize))

#loads/appends the buttons listed#
    def loadbuttons(self):
        self.playingbuttons.append(button( 20, 30, WIDTH//7, 40,
                                           function = self.checkallcells,
                                           colour = lblue,
                                           text='check'))
        self.playingbuttons.append(button( 140, 30, WIDTH//7, 40,
                                           function = self.createpuzzle,
                                           params = 1,
                                           colour = green,
                                           text='easy'))
        self.playingbuttons.append(button( 260, 30, WIDTH//7, 40,
                                           function = self.createpuzzle,
                                           params = 2,
                                           colour = purple,
                                           text='medium'))
        self.playingbuttons.append(button( 380, 30, WIDTH//7, 40,
                                           function = self.createpuzzle,
                                           params = 3,
                                           colour = lred,
                                           text='hard'))

#blits text to the window surface#
    def texttoscreen(self,window,text,pos,colour=black):
        fontimage=self.font.render(text,False,colour)
        fontwidth=fontimage.get_width()
        fontheight=fontimage.get_height()
        pos[0]+=(colsize-fontwidth)//2
        pos[1]+=(colsize-fontheight)//2
        window.blit(fontimage,pos)

#draws the numbers in the 2d array#
    def drawnumbers(self,window,board):
        for yidx,row in enumerate(board):
            for xidx,num in enumerate(row):
                if(num!=0):
                    pos=[(xidx*colsize)+boardpos[0],(yidx*colsize)+boardpos[1]]
                    self.texttoscreen(window,str(num),pos)

#marks the icorrect blocks#
    def shadeincorrectcells(self,window,incorrect):
        for square in incorrect:
            pygame.draw.rect(window,lred,(square[0]*colsize + boardpos[0],square[1]*colsize + boardpos[1],colsize,colsize))

#load function is used to call the buttons and cell colours correctly#
    def load(self):
        self.playingbuttons=[]
        self.loadbuttons()
        self.lockedcells = []
        self.incorrectcells = []
        self.finished = False

        # making non blank cells locked
        for yid, row in enumerate(self.board):
            for xid, num in enumerate(row):
                if(num!=0):
                    self.lockedcells.append((xid,yid))

#marks preexisting squares#
    def shadelockedcells(self,window,lockedarray):
        for square in lockedarray:
            pygame.draw.rect(window,shadowcolour,(square[0]*colsize + boardpos[0],square[1]*colsize + boardpos[1],colsize,colsize))

#checks if the given value is a integer#
    def checkint(self,character):
        try:
            int(character)
            return True

        except:
            return False

    # SQL INTEGRATION 

#inserts values to the table#
    def sqlint(self,tries,time):
        conn=sqlite3.connect('sudoku1.db')
        cur = conn.cursor()
      

        cur.execute("INSERT INTO info VALUES(?,?)",(tries,time/1000))
        conn.commit()
        conn.close()

#retrieves the data#
    def getinfo(self):
        conn=sqlite3.connect('sudoku1.db')
        cur = conn.cursor()

        cur.execute("SELECT try FROM info")

        self.ntry = cur.fetchall()

        cur.execute("SELECT ftime FROM info")

        self.fintime = cur.fetchall()
        

        conn.commit()
        conn.close()

# drops table #
    def droptable(self):
        conn=sqlite3.connect('sudoku1.db')
        cur = conn.cursor()

        cur.execute("DROP TABLE info")

        conn.commit()
        conn.close()

# GRAPH

#plots the graph
    def plot(self,):
        plt.plot(self.ntry,self.fintime,color='r')
        plt.xlabel('try')
        plt.ylabel('time(s)')
        plt.title('Progress in Time')
        plt.show()







        



