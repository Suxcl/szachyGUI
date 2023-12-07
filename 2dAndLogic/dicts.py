import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')



piecesASCII = {
    'w' : {
        'wB' : "⠀⠀⠀⠀⠀⠀⠀⠀⠀\n         \n         \n         \n         ",
        'pw' : "⠀⠀⠀⠀⠀⠀⠀⠀⠀\n ( )   \n / \   \n /   \  \n         ",
        'pb' : "         \n (|)   \n /|\   \n /|||\  \n         ",
        'rw' : "         \n [ ''' ] \n |   |  \n |   |  \n         ",
        'rb' : "         \n [ ''' ] \n | | |  \n | | |  \n         ",
        'bw' : "⠀⠀⠀⠀.⠀⠀⠀⠀\n / \   \n / \   \n /_ _\  \n         ",
        'bb' : "⠀⠀⠀⠀.⠀⠀⠀⠀\n /|\   \n /|\   \n /_|_\  \n         ",
        'nw' : "⠀⠀__   \n  /  \  \n   / /  \n  /_ _\ \n         ",
        'nb' : "⠀⠀__    \n  //|\  \n   ///  \n  /_|_\ \n         ",
        'qw' : '        \n\/\ /\/ \n \   /  \n /_ _\  \n         ',
        'qb' : '        \n \/\|/\/ \n \ | /  \n /_|_\  \n         ',
        'kw' : '⠀⠀⠀⠀+⠀⠀⠀⠀\n ⠀/\|/\ \n  \   /  \n  |_ _|  \n         ',
        'kb' : '⠀⠀⠀⠀+⠀⠀⠀⠀\n⠀⠀/\|/\⠀⠀\n \ | /  \n |_|_|  \n         ',
        'nrw': "   __   \n  /  \  \n  \ \   \n /_ _\  \n         ",
        'move':'        \n        \n {   }  \n        \n         ',
    }

    ,
    'b' : {
        'bB' : "---------\n---------\n---------\n---------\n---------",
        'pw' : "---------\n---( )---\n---/ \---\n--/   \--\n---------",
        'pb' : "---------\n---(|)---\n---/|\---\n--/|||\--\n---------",
        'rw' : "---------\n-[ ''' ]-\n--|   |--\n--|   |--\n---------",
        'rb' : "---------\n-[ ''' ]-\n--| | |--\n--| | |--\n---------",
        'bw' : "----.----\n---/ \---\n---/ \---\n--/_ _\--\n---------",
        'bb' : "----.----\n---/|\---\n---/|\---\n--/_|_\--\n---------",
        'nw' : "----__---\n---/  \--\n----/ /--\n---/_ _\-\n---------",
        'nb' : "----__---\n---//|\--\n----///--\n---/_|_\-\n---------",
        'qw' : '---------\n-\/\ /\/-\n--\   /--\n--/_ _\--\n---------',
        'qb' : '---------\n-\/\|/\/-\n--\ | /--\n--/_|_\--\n---------',
        'kw' : '----+----\n--/\|/\--\n--\   /--\n--|_ _|--\n---------',
        'kb' : '----+----\n--/\|/\--\n--\ | /--\n--|_|_|--\n---------',
        'move':"---------\n---------\n--{   }--\n---------\n---------",
    },
}

PiecesDict = {
    "Pawn":'p',
    "Bishop":'b',
    "Knight":'n',
    "Rock":'r',
    "Queen":'q',
    "King":'k'
}

asciiChars = {
    'b' : {
        'p':'♟︎',
        'b':'♝',
        'n':'♞',
        'r':'♜',
        'q':'♛',
        'k':'♚',
    },
    'w' : {
        'p':'♙',
        'b':'♗',
        'n':'♘',
        'r':'♖',
        'q':'♕',
        'k':'♔',
    }
}


colors = {
    "black":'b',
    "white":'w',
}

xWhiteTranslation = {
    'a':0,
    'b':1,
    'c':2,
    'd':3,
    'e':4,
    'f':5,
    'g':6,
    'h':7,
}

yToHumanTranslation = {
    7:'h',
    6:'g',
    5:'f',
    4:'e',
    3:'d',
    2:'c',
    1:'b',
    0:'a',
}



errors = {
    "FieldIsEmpty":"       To pole jest puste",
    "ChoosingEnemyFigure":"       Figura na tym polu należy do przeciwnika",
    "KingInDanger":"       Twój król jest zagrożony",
    "PieceIsDefendingKing":"       Dana figura broni króla",
    "BadInput_ToLong":"       Podana wartość jest jest za długa i nie odnosi się do żadnego pola",
    "BadInput_BadChars":"       Podana wartość nie odnosi się do żadnego pola",
    "BadInput_IllegalMove" : "       This move cannot be done by this figure"

}
strings = {
    "chosingFigureInput":"Choose figure: "
}