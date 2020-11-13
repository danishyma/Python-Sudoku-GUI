from random import randint

def pick_board():

    num = randint(0, 6)
    # num = 2

    boards = {
        0 : ([
            [5,1,7,6,0,0,0,3,4],
            [2,8,9,0,0,4,0,0,0],
            [3,4,6,2,0,5,0,9,0],
            [6,0,2,0,0,0,0,1,0],
            [0,3,8,0,0,6,0,4,7],
            [0,0,0,0,0,0,0,0,0],
            [0,9,0,0,0,0,0,7,8],
            [7,0,3,4,0,0,5,6,0],
            [0,0,0,0,0,0,0,0,0]
        ]),
        1 : ([
            [3,9,0,0,5,0,0,0,0],
            [0,0,0,2,0,0,0,0,5],
            [0,0,0,7,1,9,0,8,0],
            [0,5,0,0,6,8,0,0,0],
            [2,0,6,0,0,3,0,0,0],
            [0,0,0,0,0,0,0,0,4],
            [5,0,0,0,0,0,0,0,0],
            [6,7,0,1,0,5,0,4,0],
            [1,0,9,0,0,0,2,0,0]
        ]),
        2 : ([
            [8,5,0,0,0,2,4,0,0],
            [7,2,0,0,0,0,0,0,9],
            [0,0,4,0,0,0,0,0,0],
            [0,0,0,1,0,7,0,0,2],
            [3,0,5,0,0,0,9,0,0],
            [0,4,0,0,0,0,0,0,0],
            [0,0,0,0,8,0,0,7,0],
            [0,1,7,0,0,0,0,0,0],
            [0,0,0,0,3,6,0,4,0]
            ]),
        3 : ([
            [0,0,5,3,0,0,0,0,0],
            [8,0,0,0,0,0,0,2,0],
            [0,7,0,0,1,0,5,0,0],
            [4,0,0,0,0,5,3,0,0],
            [0,1,0,0,7,0,0,0,6],
            [0,0,3,2,0,0,0,8,0],
            [0,6,0,5,0,0,0,0,9],
            [0,0,4,0,0,0,0,3,0],
            [0,0,0,0,0,9,7,0,0]
            ]),
        4 : ([
            [0,0,0,0,4,0,0,0,5],
            [0,0,3,5,0,1,0,9,0],
            [0,2,0,9,0,0,0,0,7],
            [0,0,1,0,0,0,0,6,3],
            [0,0,2,0,3,0,8,0,0],
            [3,4,0,0,0,0,2,0,0],
            [8,0,0,0,0,5,0,2,0],
            [0,6,0,3,0,7,9,0,0],
            [9,0,0,0,6,0,0,0,0]
            ]),
        5 : ([
            [9,0,0,0,0,2,0,0,1],
            [0,4,0,1,5,0,0,0,0],
            [0,3,0,4,0,0,7,0,0],
            [0,1,0,0,0,5,0,0,6],
            [4,0,3,0,0,0,2,0,9],
            [6,0,0,8,0,0,0,1,0],
            [0,0,5,0,0,4,0,9,0],
            [0,0,0,0,9,1,0,3,0],
            [1,0,0,7,0,0,0,0,5]
            ]),
        6 : ([
            [7,8,0,4,0,0,1,2,0],
            [6,0,0,0,7,5,0,0,9],
            [0,0,0,6,0,1,0,7,8],
            [0,0,7,0,4,0,2,6,0],
            [0,0,1,0,5,0,9,3,0],
            [9,0,4,0,6,0,0,0,5],
            [0,7,0,3,0,0,0,1,2],
            [1,2,0,0,0,7,4,0,0],
            [0,4,9,2,0,6,0,0,7]
            ])
        }
    
    return boards[num]
