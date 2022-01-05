import numpy as np
import random

#checks if number is valid for the given postion for the given board#
def valid(num,y,x,board):

    for i in range(len(board)):
        if(board[y][i]==num):
            return False
    for i in range(len(board)):
        if(board[i][x]==num):
            return False
    y1=y//3
    x1=x//3
    for i in range(y1*3,(y1*3)+3):
        for j in range(x1*3,(x1*3)+3):
            if(board[i][j]==num):
                return False
    return True

#creates a board with random places filled#
def boardcreate():
    board=[[0 for i in range(9)]for i in range(9) ]
    for i in range(15):
        y=random.randint(0,8)
        x=random.randint(0,8)
        num=random.randint(1,9)
        while(not valid(num,y,x,board)):
            y=random.randint(0,8)
            x=random.randint(0,8)
            num=random.randint(1,9)
        else:
            board[y][x]=num
    return board

#solves the randomly filled board
def solve(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j]==0):
                for n in range(1,10):
                    if(valid(n,i,j,board)):
                        board[i][j]=n
                        if(solve(board)):
                            return board
                        board[i][j]=0
                else:
                    return False
    else:
        return True

#randomly inputs spaces to the solved board
def spaceout(board,n=1):
    if(n==1):
        for i in range(47):
            a=random.randint(0,8)
            b=random.randint(0,8)
            board[a][b]=0
    elif(n==2):
        for i in range(53):
            a=random.randint(0,8)
            b=random.randint(0,8)
            board[a][b]=0
    elif(n==3):
        for i in range(59):
            a=random.randint(0,8)
            b=random.randint(0,8)
            board[a][b]=0

    return board

#creates the final board
def finalcreate(x=1):
    crb1=boardcreate()

    sb1=solve(crb1)

    fb=spaceout(sb1,x)
    
    return fb


#finalboard=finalcreate()
#print(np.matrix(finalboard))






#spacedboard= spaceout(sb1,1)

#print(np.matrix(spacedboard))

## NOT NEEDED ATM BUT CHECK IF REUIRED ##

#board1=[[0 for i in range(9)]for i in range(9) ]

#def createboard(board):
   # for y in range(9):
       # for x in range(9):
         #   n=random.randint(1,9)
          #  board[y][x]=n

    #return board
