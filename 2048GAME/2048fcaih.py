import pygame,sys,time
from pygame.locals import *
from random import *
#identify colors with RGB

White = (255,255,255)
DarkSalmon = (233, 150, 122)
CornflowerBlue = (100, 149, 237)
MediumAquamarine = (102, 205, 170)
LightSlateGray	 = (119, 136, 153)
SeaGreen= (46, 139, 87)
LightCoral = (139,195,74)
Teal = (0,150,136)
SteelBlue  = (70, 130, 180)
RosyBrown = (188, 143, 143)
Pink = (234,30,99)
BabyBlue =  (0, 255, 255)
#asign each number to identical color
color_dict = {
    0:White,
    2:DarkSalmon,
    4:SeaGreen	,
    8:RosyBrown	,
    16:BabyBlue,
    32:MediumAquamarine,
    64:Teal,
    128:LightCoral,
    256:Pink,
    512:CornflowerBlue,
    1024:SteelBlue,
    2048:LightSlateGray	
}

 #sent the number and return this color

def getColor(i):
    return color_dict[i]

#identify the boarder size of GUI
BoardSize = 4
#initialize total score
TOTAL_POINTS = 0
#identify defult score
DEFAULT_SCORE = 2
#safely initializes all imported pygame modules regardless if modules actually meet to be initialze
pygame.init()
#initialize a window or screen for display
Window = pygame.display.set_mode((400,500),0,32)
#set the title to window 
pygame.display.set_caption("2048GAME")
#identify the font of numbers
FONT = pygame.font.SysFont("Impact",30)
#identify the font of total score
Font_Score = pygame.font.SysFont("Impact",40)
#initialize the game matrix
GameMatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

undoMat = []

def main(fromLoaded = False):
  #initialize the game by choose to square to start  from them  
    if not fromLoaded:
        RandomSquare()
        RandomSquare()
    printMatrix()


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if CanWeGo() == True:
                if event.type == KEYDOWN:
                    if isArrow(event.key):
                        rotations = getRotations(event.key)
                        addToUndo()
                        for i in range(0,rotations):
                            rotateMatrix()

                        if Borders():
                            MOVING()
                            Merge()
                            RandomSquare()

                        for j in range(0,(4-rotations)%4):
                            rotateMatrix()
                            
                        printMatrix()
            else: # just checking wait
                GameOver()

            if event.type == KEYDOWN:
                global BoardSize

                if event.key == pygame.K_r:
                 
                    Replay()
                if 50<event.key and 56 > event.key:
                    
                    BoardSize = event.key - 48
                    Replay()
                if event.key == pygame.K_s:
                   
                    saveGameState()
                elif event.key == pygame.K_l:
                    loadGameState()
                    
                elif event.key == pygame.K_u:
                    undo()
                   
        pygame.display.update()



#this function helps in check that it is possible to move or not

def Borders():
    for i in range(0,BoardSize):
        for j in range(1,BoardSize):
            if GameMatrix[i][j-1] == 0 and GameMatrix[i][j] > 0:
                return True 
            elif (GameMatrix[i][j-1] == GameMatrix[i][j]) and GameMatrix[i][j-1] != 0:
                return True
    return False
    # This module moves 
def MOVING():
    for i in range(0,BoardSize):
        for j in range(0,BoardSize-1):
            
            while GameMatrix[i][j] == 0 and sum(GameMatrix[i][j:]) > 0:
                for k in range(j,BoardSize-1):
                    GameMatrix[i][k] = GameMatrix[i][k+1]
                GameMatrix[i][BoardSize-1] = 0


#this function is used for merging
def Merge():
    global TOTAL_POINTS

    for i in range(0,BoardSize):
        for k in range(0,BoardSize-1):
            if GameMatrix[i][k] == GameMatrix[i][k+1] and GameMatrix[i][k] != 0:
                GameMatrix[i][k] = GameMatrix[i][k]*2
                GameMatrix[i][k+1] = 0 # this was not intailized so the k value was going out the range value so by this we ever we merge the files it assigns the present value to zero and merge the number with the ahead value 
                TOTAL_POINTS += GameMatrix[i][k]
                MOVING()


#  this module helps in getting an random tile 
def RandomSquare():
    c = 0
    for i in range(0,BoardSize):
        for j in range(0,BoardSize):
            if GameMatrix[i][j] == 0:
                c += 1
    
    k = floor(random() * BoardSize * BoardSize)
    print("keep going")

    while GameMatrix[floor(k/BoardSize)][k%BoardSize] != 0:
        k = floor(random() * BoardSize * BoardSize)

    GameMatrix[floor(k/BoardSize)][k%BoardSize] = 2



#  this is used to get floor value out of the given value to the module
def floor(n):
    return int(n - (n % 1 ))  
# This module is used to print the given matrix
def printMatrix():
        Window.fill(White)
        global BoardSize
        global TOTAL_POINTS

        for i in range(0,BoardSize):
            for j in range(0,BoardSize):
                pygame.draw.rect(Window,getColor(GameMatrix[i][j]),(i*(400/BoardSize),j*(400/BoardSize)+100,400/BoardSize,400/BoardSize))
                label = FONT.render(str(GameMatrix[i][j]),1,(0,0,0))
                label2 = Font_Score.render("YourScore:"+str(TOTAL_POINTS),1,(0,0,0))
                Window.blit(label,(i*(400/BoardSize)+30,j*(400/BoardSize)+130))
                Window.blit(label2,(10,20))


# We can call this an checker module

def CanWeGo():
    for i in range(0,BoardSize ** 2): # This was having an error as that is 4 power of 2
        if GameMatrix[floor(i/BoardSize)][i%BoardSize] == 0:
            return True
    
    for i in range(0,BoardSize):
        for j in range(0,BoardSize-1):
            if GameMatrix[i][j] == GameMatrix[i][j+1]:
                return True
            elif GameMatrix[j][i] == GameMatrix[j+1][i]:
                return True
    return False

# this function return an matrix rather than we can call it an list
def LinearMatrix():

    mat = []
    for i in range(0,BoardSize ** 2):
        mat.append(GameMatrix[floor(i/BoardSize)][i%BoardSize])

    mat.append(TOTAL_POINTS)
    return mat

#  this function is the main reason to make the covert linearn function
def addToUndo():
    undoMat.append(LinearMatrix())   
#  This function is used to mix up the matrix after a button/move is done by the user 
def rotateMatrix():
    for i in range(0,int(BoardSize/2)):
        for k in range(i,BoardSize- i- 1):
            temp1 = GameMatrix[i][k]
            temp2 = GameMatrix[BoardSize - 1 - k][i]
            temp3 = GameMatrix[BoardSize - 1 - i][BoardSize - 1 - k]
            temp4 = GameMatrix[k][BoardSize - 1 - i]

            GameMatrix[BoardSize - 1 - k][i] = temp1
            GameMatrix[BoardSize - 1 - i][BoardSize - 1 - k] = temp2
            GameMatrix[k][BoardSize - 1 - i] = temp3
            GameMatrix[i][k] = temp4

# when you dont have any place in the matrix or you are out of move then this module is called so it is in the else part of the main func

def GameOver():
    global TOTAL_POINTS

    Window.fill(White)

    label = Font_Score.render("Game Over!",1,(255,0,0))
    label2 = Font_Score.render("Score : "+str(TOTAL_POINTS),1,(255,0,0))
    label3 = FONT.render("press 'R' to play again!! ",1,(255,0,0))

    Window.blit(label,(50,100))
    Window.blit(label2,(50,200))
    Window.blit(label3,(50,300))

# This module is to Replay

def Replay():
    global TOTAL_POINTS
    global GameMatrix

    TOTAL_POINTS = 0
    Window.fill(White)
    GameMatrix = [[0 for i in range(0,BoardSize)] for j in range(0,BoardSize) ]
    main()


# This help you find the which arrow is keep_goinged by the user
def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

def getRotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2 
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3

# calling the main
main()



