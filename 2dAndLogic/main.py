from rich.console import Console
from rich.table import Table, Column
from rich import print
from rich import box
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt
from rich.pretty import pprint
from rich.align import Align
from rich.padding import Padding
from rich.text import Text


from chessboard import chessboard
from dicts import piecesASCII, colors, asciiChars

import os
import pickle

side = 'w'
oneTime = True

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

import logging
logging.basicConfig(filename='example.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)
logging.debug("Lanuching Main.py")

console = Console()

def MeinMenuLayout():
    MainMenu = Layout()

    MainMenu.split_column(
        Layout(name="top"),
        Layout(name="between"),
        Layout(name="bottom")
    )

    MainMenu["between"].split_row(
        Layout(name="between-left"),
        Layout(name="between-middle"),
        Layout(name="between-right"),
    )


    text = Text(f' Start New Game       - type "start"\n Credits              - type "credits"\n Exit Aplication      - type "exit"')
    text.stylize("bold green")
    konLewy = Text(piecesASCII['w']['nrw'])
    konPrawy = Text(piecesASCII['w']['nw'])
    konLewy.stylize("bold grey")
    konPrawy.stylize("bold grey")

    MainMenu["top"].update(Align.center("\n\n\n░█████╗░██╗░░██╗███████╗░██████╗░██████╗\n██╔══██╗██║░░██║██╔════╝██╔════╝██╔════╝\n██║░░╚═╝███████║█████╗░░╚█████╗░╚█████╗░\n██║░░██╗██╔══██║██╔══╝░░░╚═══██╗░╚═══██╗\n╚█████╔╝██║░░██║███████╗██████╔╝██████╔╝\n░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░", vertical="middle"))
    MainMenu["bottom"].update("")

    MainMenu["between-middle"].update(Align.center(text, vertical="middle"))
    MainMenu["between-left"].update(Align.center(konLewy, vertical='middle'))
    MainMenu["between-right"].update(Align.center(konPrawy, vertical="middle"))

    return MainMenu

def GamePanelLayout():
    GamePanel = Layout(name="root")

    GamePanel.split_row(
        Layout(name="Info"),
        Layout(name="Chess"),
    )
    GamePanel["Info"].size = 80
    GamePanel["Info"].split_row(
        Layout(name="Info1"),
        Layout(name="Info2"),
    )
    GamePanel["Info2"].visible = False

    return GamePanel

def creditsLayout():
    credits = Layout(name="root")

    credits.split_row(
        Layout(name="left"),
        Layout(name="middle"),
        Layout(name="right"),
    )

    text = Text(f'Wykonanie Sak Jakub')
    text.stylize("bold blue")

    king = Text(piecesASCII['w']['kw'])
    queen = Text(piecesASCII['w']['qw'])
    king.stylize("bold purple")
    queen.stylize("bold purple")
    credits["left"].update(Align.center(king, vertical='middle'))
    credits["right"].update(Align.center(queen, vertical="middle"))
    credits["middle"].update(Align.center(text, vertical="middle"))

    return credits

def resetChessBoard(chessboard, GamePanel):
    table = Table( show_footer=True ,style=None, box=box.MINIMAL)
    let = ["","a","b","c","d","e","f","g","h"]

    ran = range(8)
    if(side == 'b'):
        ran = range(7, -1, -1)

    for a in let:
        table.add_column(a, justify="center", width=9, footer=a)

    board,moves,attacks,position = chessboard.returnBoard()
    moveList = chessboard.getMoveList()

    for a in ran:
        rowNumber = "\n\n" + str(8-a)
            
        valueColFig = []
        valueBckCol = []
        asciitab = []
    
        for b in range(8):
            valueColFig.append(board[a][b][0])
            valueBckCol.append(board[a][b][1])
            if((a,b) == position):
                tmp = Text(piecesASCII[valueBckCol[b]][valueColFig[b]])
                tmp.stylize("bold blue")
                asciitab.append(tmp)
            elif((a,b) in moves):
                tmp = Text(piecesASCII[valueBckCol[b]]['move'])
                tmp.stylize("bold blue")
                asciitab.append(tmp)
            elif((a,b) in attacks):
                tmp = Text(piecesASCII[valueBckCol[b]][valueColFig[b]])
                tmp.stylize("bold red")
                asciitab.append(tmp)
            else:
                asciitab.append(piecesASCII[valueBckCol[b]][valueColFig[b]])
            
        table.add_row(rowNumber, asciitab[0], asciitab[1], asciitab[2], asciitab[3], asciitab[4], asciitab[5], asciitab[6], asciitab[7],)
    
    GamePanel["Chess"].update(Align.center(table, vertical="middle"))
    
    info = [Table( show_footer=True ,style=None, box=box.MINIMAL),Table( show_footer=True ,style=None, box=box.MINIMAL)]

    # figuremoved, x1,y1,x2,y2, None or Figure Destoyed 
    for a in info:
        a.add_column("Move", justify="center", width=4)
        a.add_column("piece", justify="center", width=5)
        a.add_column("orig", justify="center", width=5)
        a.add_column("dest", justify="center", width=5)
        a.add_column("tar", justify="center", width=5)

    if(chessboard.move_count == 0):
        pass
    else:
        i = 1
        for a in moveList:
            x1,y1 = chessboard.translateMoveToHuman(a[1],a[2])
            x2,y2 = chessboard.translateMoveToHuman(a[3],a[4])
            if(i<31):
                
                info[0].add_row(str(i), a[0], str(x1)+str(y1), str(x2)+str(y2), "--" if a[5] == None else a[5])
            else:
                GamePanel["Info2"].visible = True
                info[1].add_row(str(i), a[0], str(a[1])+str(a[2]), str(a[3])+str(a[4]), "--" if a[5] == None else a[5])
            i+=1

    GamePanel["Info1"].update(Align.right(info[0], vertical="middle"))
    GamePanel["Info2"].update(Align.right(info[1], vertical="middle"))


def main():
    lay = 0
    with console.screen():

        inp1 = "What you want do do? - "
        inp2 = "Chose Side w/b - "
        inp3 = "Click enter to continue"
        przerwa = ""
        tmp = console.width/2 - len(inp1)/2
        for a in range(int(tmp)):
            przerwa = przerwa + " "
        promptMainMenu = przerwa + inp1
        promptChoseSide = przerwa + inp2
        promptCredits = przerwa + inp3

        # create layouts
        credits = creditsLayout()
        MainMenu = MeinMenuLayout()
        GamePanel = GamePanelLayout()

        while(True):
            cb = chessboard()
            if(lay == 0):
                cls()
                
                console.print(MainMenu)
                wynik = Prompt.ask(promptMainMenu)
                if(wynik in ['start',"1"]): 
                    

                    side = Prompt.ask(promptChoseSide, choices=['w',"W","b","B"], show_choices=False)
                    if(side in ['w',"W"]):
                        cb.newBoard()
                    else: 
                        cb.newBoard(1)
                        side = 'b'

                    lay = 1
                
                if(wynik in ['credits',2]): lay = 2
                if(wynik in ['exit',3]): lay = 3
            if(lay == 1):
                resetChessBoard(cb,GamePanel)
                cls()
                console.print(GamePanel)
                while(True):
                    
                    retVal = cb.gameStep()
                    resetChessBoard(cb,GamePanel)
                    cls()
                    console.print(GamePanel)
                    if(retVal == 1):
                        lay = 0
                        break

            if(lay == 2):
                console.print(credits)
                Prompt.ask(promptCredits)
                lay = 0
            if(lay == 3):
                exit()
            
if __name__ == "__main__":
    main()


# choose x,y
# show possible moves
# allow to choose where to go
# check if move is correct
# if move is correct move/attack
# move figure to destination
# check for cheks/mates
# 