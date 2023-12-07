from dicts import *

import logging
logging.basicConfig(filename='example.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)


class Piece:
    def __init__(self,x,y,figCol):
        self.x = x
        self.y = y
        self.color = figCol
        self.figure = None
        self.isDefKing = False

    
    def getFigAndCol(self):
        return self.figure + self.color

    def getFigChar(self): return self.figure

    def getFigCol(self): return self.color

    def changeCordinates(self,x,y):
        self.x = x
        self.y = y

    def getCordinates(self):
        return self.x, self.y

    def ReturnPossibleMoves(self,board): return 
        


class Pawn(Piece):
    def __init__(self,x, y, figCol):
        super().__init__(x,y, figCol)
        self.figure = PiecesDict["Pawn"]
        self.hasMoved = False
        self.MoveNumber = None
    
    
    def setMovedToTrue(self, count):
        self.hasMoved = True
        self.MoveNumber = count

    def setMovedToFalse(self):
        self.hasMoved = False
        self.MoveNumber = None

    def leftAttack(self, board): 
        yy = self.y-1
        if(self.color == colors["white"]):
            xx = self.x-1
        else:
            xx = self.x+1
        col = board[xx][yy].getColorOfFigure()
        if(board[xx][yy].isEmpty() or col == self.color): return None
        return xx,yy
        
    def rightAttack(self, board): 
        yy = self.y+1
        if(self.color == colors["white"]):
            xx = self.x-1
        else:
            xx = self.x+1
        col = board[xx][yy].getColorOfFigure()
        if(board[xx][yy].isEmpty() or col == self.color): return None
        return xx,yy
        


    def ReturnPossibleMoves(self,board):
        logging.debug(f'Pawn attemping ReturnPossibleMoves() Method')
        logging.debug(f'Pawn Figure info: {self.x,self.y,self.color,self.figure}')
        moves = []
        attacks = []


        if(self.color == colors["white"]):
            xDirection = lambda a, b : (a - b)
        else: xDirection = lambda a, b : (a + b)

        for a in range(1,3 if self.hasMoved==False else 2):
            xTarget = xDirection(self.x, a)
            logging.debug(F'Pawn attempting check on board[x-a][y]: {board[xTarget][self.y].isEmpty()}')
            logging.debug(F'Pawn attempting check on board[x-a][y]: {board[xTarget][self.y]} {xTarget , self.y}')
            if(7<xTarget<0):
                pass
            elif board[xTarget][self.y].isEmpty() is True:
                moves.append((xTarget, self.y))
                logging.debug(f'Pawn {xTarget, self.y} is empty appended moves {moves}')
            else: break

        if(self.y==0):
            t = self.rightAttack(board)
            if(t): attacks.append(t)
        elif(self.y==7):
            t = self.leftAttack(board)
            if(t): attacks.append(t)
        else:
            t = self.rightAttack(board)
            if(t): attacks.append(t)
            t = self.leftAttack(board)
            if(t): attacks.append(t)
        logging.debug(f'Pawn ReturnPossibleMove(): returning values: {moves, attacks}')
        return moves, attacks

class Bishop(Piece):
    def __init__(self, x, y, figCol):
        super().__init__(x, y, figCol)
        self.figure = PiecesDict["Bishop"]


    def ReturnPossibleMoves(self,board):
        moves = []
        attacks = []
        

        x , y  = self.x,self.y
        while(x >= 0 and y >= 0):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if (self.x == x and self.y == y): pass
                else: break  
            else: 
                attacks.append((x,y)) 
                break
            x-=1
            y-=1
        
        x , y  = self.x,self.y
        while(x <= 7 and y <= 7):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if (self.x == x and self.y == y): pass
                else: break  
            else: 
                attacks.append((x,y)) 
                break
            x+=1
            y+=1

        x , y  = self.x,self.y
        while(x >= 0 and y <= 7):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if (self.x == x and self.y == y): pass
                else: break  
            else: 
                attacks.append((x,y)) 
                break
            x-=1
            y+=1
        
        x , y  = self.x,self.y
        while(x <= 7 and y >= 0):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if (self.x == x and self.y == y): pass
                else: break  
            else: 
                attacks.append((x,y)) 
                break
            x+=1
            y-=1
        
        return moves, attacks

class Knight(Piece):
    def __init__(self, x, y, figCol):
        super().__init__(x, y, figCol)
        self.figure = PiecesDict["Knight"]

    def ReturnPossibleMoves(self, board):
        moves = []
        attacks = []
        x, y = self.x, self.y
        possiblities = [
            (x+1,y-2),(x-1,y-2),(x+1,y+2),(x-1,y+2), # horizontal
            (x+2,y-1),(x+2, y+1),(x-2,y+1),(x-2,y-1), # vertical
        ]        

        for a in possiblities:
            x,y = a
            if not (x < 0 or x > 7 or y < 0 or y > 7):
                if(board[x][y].isEmpty()): moves.append((x,y))
                elif(board[x][y].getColorOfFigure() != self.getFigCol()): attacks.append((x,y))
        return moves, attacks

class Rock(Piece):
    def __init__(self, x, y, figCol):
        super().__init__(x, y, figCol)
        self.figure = PiecesDict["Rock"]
        self.hasMoved = False
        self.MoveNumber = None
    
    def setMovedToTrue(self, count):
        self.hasMoved = True
        self.MoveNumber = count

    def setMovedToFalse(self):
        self.hasMoved = False
        self.MoveNumber = None

    def ReturnPossibleMoves(self, board):
        moves = []
        attacks = []
        
        # valPLus = lambda a : a+1
        # valMinus = lambda a : a-1
        # val = None
        # equalsList = [lambda x : x>=0, lambda x:x<=7]
        # valueList = [lambda a : a-1, lambda a : a-1]
        # for a in range(4):
        #     if(a%2==0): val = lambda a:a+1
        #     else: val = lambda a:a+1
        #    
        #     while(equalsList[a%2==0]):
        #         if(board[x][y].isEmpty()): moves.append((x,y))
        #         elif(board[x][y].getColorOfFigure() == self.color): 
        #             if(self.x == x and self.y ==y): pass
        #             else: break 
        #         else: 
        #             attacks.append((x,y))
        #             break 




        

        x , y = self.x, self.y
        while(x >= 0):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if(self.x == x and self.y ==y): pass
                else: break 
            else: 
                attacks.append((x,y))
                break 
            x-=1
        x , y = self.x, self.y
        while(x <= 7):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if(self.x == x and self.y ==y): pass
                else: break 
            else: 
                attacks.append((x,y))
                break 
            x+=1
        x , y = self.x, self.y
        while(y >= 0):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if(self.x == x and self.y ==y): pass
                else: break 
            else: 
                attacks.append((x,y))
                break 
            y-=1
        x , y = self.x, self.y
        while(y <= 7):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if(self.x == x and self.y ==y): pass
                else: break 
            else: 
                attacks.append((x,y)) 
                break 
            y+=1
        return moves, attacks

class Queen(Piece):
    def __init__(self, x, y, figCol):
        super().__init__(x, y, figCol)
        self.figure = PiecesDict["Queen"]

    def ReturnPossibleMoves(self, board):
        moves = []
        attacks = []
        #horizontal
        x , y = self.x, self.y            
        while(x >= 0):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if(self.x == x and self.y ==y): pass
                else: break 
            else: 
                attacks.append((x,y))
                break 
            x-=1
        x , y = self.x, self.y
        while(x <= 7):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if(self.x == x and self.y ==y): pass
                else: break 
            else: 
                attacks.append((x,y))
                break 
            x+=1
        x , y = self.x, self.y
        while(y >= 0):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if(self.x == x and self.y ==y): pass
                else: break 
            else: 
                attacks.append((x,y))
                break 
            y-=1
        x , y = self.x, self.y
        while(y <= 7):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if(self.x == x and self.y ==y): pass
                else: break 
            else: 
                attacks.append((x,y)) 
                break 
            y+=1
        
        # diagonal 

        x , y  = self.x,self.y
        while(x >= 0 and y >= 0):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if (self.x == x and self.y == y): pass
                else: break  
            else: 
                attacks.append((x,y)) 
                break
            x-=1
            y-=1
        
        x , y  = self.x,self.y
        while(x <= 7 and y <= 7):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if (self.x == x and self.y == y): pass
                else: break  
            else: 
                attacks.append((x,y)) 
                break
            x+=1
            y+=1

        x , y  = self.x,self.y
        while(x >= 0 and y <= 7):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if (self.x == x and self.y == y): pass
                else: break  
            else: 
                attacks.append((x,y)) 
                break
            x-=1
            y+=1
        
        x , y  = self.x,self.y
        while(x <= 7 and y >= 0):
            if(board[x][y].isEmpty()): moves.append((x,y))
            elif(board[x][y].getColorOfFigure() == self.color): 
                if (self.x == x and self.y == y): pass
                else: break  
            else: 
                attacks.append((x,y)) 
                break
            x+=1
            y-=1
        return moves, attacks

class King(Piece):
    def __init__(self, x, y, figCol):
        super().__init__(x, y, figCol)
        self.figure = PiecesDict["King"]
        self.hasMoved = False
        self.MoveNumber = None
    
    def setMovedToTrue(self, count):
        self.hasMoved = True
        self.MoveNumber = count

    def setMovedToFalse(self):
        self.hasMoved = False
        self.MoveNumber = None

    def checkForDanger(self, moves, attacks):
        for a in moves:
            pass

    def ReturnPossibleMoves(self, board):
        moves = []
        attacks = []
        x, y = self.x, self.y
        possiblities = [
            (x-1,y-1),(x-1,y),(x-1,y+1),
            (x,y-1),(x,y+1),
            (x+1,y-1),(x+1,y),(x+1,y+1),
        ]
        for a in possiblities:
            x, y = a
            if not(x < 0 or x > 7 or y < 0 or y > 7):
                if(board[x,y].isEmpty()): moves.append((x,y))       
                elif(board[x][y].getColorOfFigure() != self.getFigCol()): attacks.append((x,y))
        return moves, attacks
    


    
    def checkForDanger(self):
        pass



        