from field import field
from dicts import colors, piecesASCII, PiecesDict
from piece import *
import time
from rich.prompt import Confirm

import logging
logging.basicConfig(filename='example.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)

class chessboard:
    def __init__(self):
        self.board = [[field(col,row) for col in range(8)] for row in range(8)]
        self.move_count = 0
        self.gameState = 1
        self.winner = None
        self.moves = []
        self.attacks = []
        self.moveList = []
        self.choosenField= None
            
    def getMoveList(self):return self.moveList

    def translateMoveTo01(self,x,y):
        return 8-y, xWhiteTranslation[x] 

    def translateMoveToHuman(self, x, y):
        return yToHumanTranslation[y], 8-x

    def checkIfFieldHasSameColorASCurrentPlayer(self, x, y):
        if(self.board[x][y].getColorOfFigure() == colors["white"] if self.move_count%2==0 else colors["black"]):
            return True
        else: return False

    def checkRequiremtns(self, value):
        if(len(str(value))!=2): 
                logging.debug("value too long")
                print(errors["BadInput_ToLong"])
                time.sleep(2)
                return False
        if not((96<ord(value[0])<105) and (47<ord(value[1])<57)): 
            print(errors["BadInput_BadChars"])
            time.sleep(2)
            return False
        return True

    def checkIfXYInMoves(self, x,y):
        if((x,y) in self.moves): return True
        else: return False

    def checkIfXYInAttacks(self,x,y):
        if((x,y) in self.attacks): return True
        else: return False

    def InputValue(self, code):       
        print(f'       Player Color: {"black" if self.move_count%2==1 else "white"}')
        print(f'       Possible Commnads: [exit, stop, undo]  Field choosing input looks liek this: "a-h,1-8"')
        if(code == 1): prompt = "       Choose figure: "
        if(code == 2): prompt = "       Choose destination: "
        inp = input(prompt)
        # quiting game - saving state
        if inp in ['exit', 'quit', 'q']:
            wynik = Confirm.ask("       Do you want to quit this game?")
            if wynik: return False
            return True
        # canceling current move
        if inp in ['stop', 'cancel']: 
            if(self.choosenField!=None): 
                self.removePosibleMovesFromBoard() 
                return True
            else: return False
        if inp in ['undo']: 
            self.UndoMove()
            return True
        
        if(self.checkRequiremtns(inp)): 
            x,y = self.translateMoveTo01(inp[0],int(inp[1]))
            if(code == 1):
                return x,y
            if(code == 2):
                if(self.checkIfXYInMoves(x,y) == False and self.checkIfXYInAttacks(x,y) == False): 
                    print(errors["BadInput_IllegalMove"])
                    time.sleep(2)
                    return 1
                else: return x,y
        else: return 1
        
    def newBoard(self, side = None):
        num = 0
        self.gameState = 1
        for a in range(8):
            if(a%2==1): num = 1
            else: num = 0
            for b in range(8):
                self.board[a][b].setBackGroundColor(colors["white"] if num%2==0 else colors["black"]) 
                num+=1
                if(a == 1):
                    self.board[a][b].setFieldOcupant(Pawn(a,b,colors["black"]))
                if(a == 6):
                    self.board[a][b].setFieldOcupant(Pawn(a,b,colors["white"]))
                if(a == 0):
                    if(b in [0,7]):
                        self.board[a][b].setFieldOcupant(Rock(a,b,colors["black"]))
                    elif(b in [1,6]):
                        self.board[a][b].setFieldOcupant(Knight(a,b,colors["black"]))
                    elif(b in [2,5]):
                        self.board[a][b].setFieldOcupant(Bishop(a,b,colors["black"]))
                    elif(b == 3):
                        self.board[a][b].setFieldOcupant(Queen(a,b,colors["black"]))
                    elif(b == 4):
                        self.board[a][b].setFieldOcupant(King(a,b,colors["black"]))
                
                if(a == 7):
                    if(b in [0,7]):
                        self.board[a][b].setFieldOcupant(Rock(a,b,colors["white"]))
                    elif(b in [1,6]):
                        self.board[a][b].setFieldOcupant(Knight(a,b,colors["white"]))
                    elif(b in [2,5]):
                        self.board[a][b].setFieldOcupant(Bishop(a,b,colors["white"]))
                    elif(b == 3):
                        self.board[a][b].setFieldOcupant(Queen(a,b,colors["white"]))
                    elif(b == 4):
                        self.board[a][b].setFieldOcupant(King(a,b,colors["white"]))

    def CheckIfMoveFromFieldIsPossible(self,x,y):

        Field = self.board[x][y]
        Figure = self.board[x][y].getFigure()
        if(Field.isEmpty()):                                      #check if field is empty
            print(errors["FieldIsEmpty"])
            time.sleep(2)
            return False
        if(self.move_count%2==0 and Field.getColorOfFigure() == 'b' #check if field contains current player figure
           or self.move_count%2==1 and Field.getColorOfFigure() == 'w'):
            print(errors["ChoosingEnemyFigure"])
            time.sleep(2)
            return False


        return True
    
    # returns true if everythink fine, false when there is no move from that possition
    def GetPossibleMoves(self,x,y):
        figure = self.board[x][y].getFigure()
        logging.debug(f'RenderPossibleMoves(): choosen figure: {figure} moves and attacks before: {self.moves, self.attacks}')
        
        self.moves, self.attacks = figure.ReturnPossibleMoves(self.board)
        logging.debug(f'RenderPossibleMoves(): moves and attacks after: {self.moves, self.attacks}')
        return True

    # moving figure and saving move to self.list
    def moveFromAtoB(self,x1,y1,x2,y2,capture=None):
        if capture == None: capture = True
        figure1 = self.board[x1][y1].getFigure()
        if(capture):
            
            fig2 = None
            if(self.board[x2][y2].isEmpty() == True): fig2 = None
            else: fig2 = self.board[x2][y2].getFigure().getFigAndCol()
            
            self.moveList.append([figure1.getFigAndCol(),x1,y1,x2,y2,fig2])


        self.board[x2][y2].setFieldOcupant(figure1)
        self.board[x1][y1].removeFieldOcupant()

    def removePosibleMovesFromBoard(self):
        self.moves = []
        self.attacks = []
        self.choosenField= None

    def UndoMove(self):
        if(self.move_count==0): return
        self.removePosibleMovesFromBoard() 
        values = self.moveList.pop()
        self.moveFromAtoB(values[3],values[4],values[1],values[2], False)
        if(values[5]!=None):
                self.board[values[3]][values[4]].undoFieldOcupant()
        self.move_count -=1
        if(self.board[values[1]][values[2]].getFigure().getFigChar() in [PiecesDict["King"],PiecesDict["Rock"],PiecesDict["Pawn"]]):
            moved = self.board[values[1]][values[2]].getFigure().MoveNumber
        if(moved != None and moved == self.move_count):
            self.board[values[1]][values[2]].getFigure().setMovedToFalse()


    def CheckForCastling(self, x,y, x_dest, y_dest):
        figure = self.board[x][y].getFigure()
        if(figure.getFigChar() is PiecesDict["Rock"] and figure.hasMoved == False):
            if(self.move_count%2==0):
                xCheck = 7
            else: xCheck = 0
            kingField = self.board[xCheck][4]
            if(kingField.isEmpty() == True): return False
            kingFig = kingField.getFigure()
            if(kingFig.getFigChar() != PiecesDict["King"]): return False
            if(kingFig.hasMoved == False):
                kingX, kingY = kingFig.getCordinates()
                if(x_dest == xCheck and y_dest in [kingY+1,kingY-1]):
                    kingY2 = 0
                    if(kingY > y): kingY2 = kingY-2
                    else: kingY2 = kingY+2
                    kingFig.setMovedToTrue(self.move_count)
                    figure.setMovedToTrue(self.move_count)
                    self.moveFromAtoB(x, y, x_dest, y_dest)
                    self.moveFromAtoB(kingX, kingY, kingX, kingY2)
                    return True
        return False

    def SelectDestination(self):
        #if(self.choosenField== None): return False
        x,y = self.choosenField
        logging.debug(f'Move(): attempting move() with {x,y}')

        inp = self.InputValue(2)
        if inp == False: return False
        if inp == True: return True
        
        x_dest,y_dest = inp
        
        if (self.CheckForCastling(x,y,x_dest,y_dest) == False):
            if(self.board[x][y].getFigure().getFigChar() in [PiecesDict["King"],PiecesDict["Rock"],PiecesDict["Pawn"]]): 
                self.board[x][y].getFigure().setMovedToTrue(self.move_count)
    
            # if(self.checkIfFieldHasSameColorASCurrentPlayer(x_dest, y_dest)==False and self.board[x_dest][y_dest].isEmpty() == False and self.board[x_dest][y_dest].getFigure().getFigChar()==PiecesDict["King"]):
            #     self.gameState = 0
            #     self.winner = "white" if self.move_count%2==0 else "black"
            #     return True


            self.moveFromAtoB(x,y,x_dest,y_dest)

            # check for Pawn tranformation
            if(x_dest == 0 and self.move_count%2 == 0 and self.board[x_dest][y_dest].getFigure().getFigChar() == PiecesDict["Pawn"]):
                self.board[x_dest][y_dest].setFieldOcupant(Queen(x_dest, y_dest, colors["white"]))
            elif(x_dest == 7 and self.move_count%2 == 1 and self.board[x_dest][y_dest].getFigure().getFigChar() == PiecesDict["Pawn"]):
                self.board[x_dest][y_dest].setFieldOcupant(Queen(x_dest, y_dest, colors["black"]))
                
            self.removePosibleMovesFromBoard() 

            if self.moveList[-1][5] != None and self.moveList[-1][5] in ['kw','kb']:
                self.gameState = 0
                self.winner = "white" if self.moveList[-1][5]=='kb' else "black"

        self.move_count+=1
        return True
        

    def CheckField(self,x,y):
        if(self.CheckIfMoveFromFieldIsPossible(x,y) == False): return False
        self.GetPossibleMoves(x,y)
        if self.moves == None and self.attacks == None: return False

        return True


    def ChooseFigure(self):
        if(self.gameState == 0):
            print(f'       Game Ended Player {self.winner} won!')
            time.sleep(3)
            return 2
        elif(self.gameState == 1):
            #if(self.choosenField!= None): return False
            inp = self.InputValue(1)
            # command in inp - restart method
            if(inp == False or inp == True): 
                return False
            x,y = inp
            self.choosenField= x,y
            if(self.CheckField(x,y)): return True
            else: return False

    def gameStep(self):
        if(self.choosenField == None): 
            ret = self.ChooseFigure()
            if(ret == 1): return False
            elif(ret == 2): return 1
            else: return True
        else: 
            ret = self.SelectDestination()




    
    # return tuple with figurechar and color and value of background color
    def returnBoard(self):
        result = []
        for a in range(8):
            tmp = []
            for b in range(8):
                Field = self.board[a][b]
                if(Field.isEmpty()): tmp.append((str(Field.getBackGroundColor())+'B',Field.getBackGroundColor()))
                else: tmp.append((Field.getPieceAndColor(),Field.getBackGroundColor()))
            result.append(tmp)
        return result, self.moves, self.attacks, self.choosenField


    def printBoard(self, board = None):
        
        #test printing

        if(board == None): board = self.board
        dl = len(board)
        let = ["a","b","c","d","e","f","g","h"]
        num = [8,7,6,5,4,3,2,1]
        let.reverse()
        for a in range(dl):
            print(num[a], end="")    
            for b in range(dl):
                if((a,b) in self.moves):
                    print(f'|ooooooooooooooooo|', end="")    
                elif((a,b) in self.attacks):
                    print(f'|xxxxxxxxxxxxxxxxx|', end="")
                else:
                    fig = board[a][b].getFigure()
                    if(fig):
                        print(f'|FC: {fig.getFigAndCol()} xy: {fig.getCordinates()}|', end="")
                    else:
                        print(f'|-----------------|', end="")
            print()
        print(f' |aaaaaaaaaaaaaaaaa||bbbbbbbbbbbbbbbbb||ccccccccccccccccc||ddddddddddddddddd||eeeeeeeeeeeeeeeee||fffffffffffffffff||ggggggggggggggggg||hhhhhhhhhhhhhhhhh|')
        

        


# do zrobienia
# roszada kurna nie działa


# zapis gry przynajmniej jednej


# 