from sudoku_boards import pick_board

backtracks = 0

# This list helps to check each 3x3 based on current input
sectors = [ [0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3],
            [0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6],
            [0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9] ]

def find_next_empty(puzzle):
    '''Find empty cells (designeted by 0) to be solved return its position or None if there isn't one ''' 
    for r in range(9):
        for c in range(9): 
            if puzzle[r][c] == 0:
                return r, c

    return None, None  # no left empty spaces returns None

def check_guess(puzzle, pos,  guess):
    '''Checks if the guess is in each row, column and 3x3 grid - if it is it breaks out of the look for a new guess 
    if not it continues to search returning valid guess - there's code to be added in case of diagonal sudoku
    '''
    
    # Check rows
    for i in range(len(puzzle[0])):
        if puzzle[pos[0]][i] == guess and pos[1] != i:
            return False

    # Check column
    for i in range(len(puzzle)):
        if puzzle[i][pos[1]] == guess and pos[0] != i:
            return False

    # Check 3x3 grids
    row_start = (pos[1] // 3) * 3 # gets the first row position from the 3x3 grid accordindly to the empty space we are looking
    col_start = (pos[0] // 3) * 3 # gets the first column position from the 3x3 grid accordindly to the empty space we are looking

    for i in range(col_start, col_start + 3):
        for j in range(row_start, row_start + 3):
            if puzzle[i][j] == guess and (i,j) != pos:
                return False
                
    return True

    #check diagonal
    # i = 0
    # for row in range(9):
    #     if guess == input[row][i]:
    #         return False
    #     i += 1

    #check inverse diagonal
    # i = 0
    # for col in range(8, -1, -1):
    #     if guess == input[i][col]:
    #         print(input[i][col])
    #     i += 1

def optimization(puzzle, row, col, guess):
    '''Addes rules to optimize the search, looking for missing numbers on 3x3 grids narrowing the guesses vs col and row 
    and calls the check_guess function to see if it doesn't violate sudoku rules
    '''
    global sectors

    puzzle[row][col] = guess
    opt_guess = [(row, col, guess)]


    for k in range(len(sectors)):

        sectinfo = []

        # make a list of missing numbers
        vset = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for x in range(sectors[k][0], sectors[k][1]):
            for y in range(sectors[k][2], sectors[k][3]):
                if puzzle[x][y] != 0 and puzzle[x][y] in vset: 
                    vset.remove(puzzle[x][y])

        # attach the list to each empty cell on the 3x3 with its index
        for x in range(sectors[k][0], sectors[k][1]):
            for y in range(sectors[k][2], sectors[k][3]):
                if puzzle[x][y] == 0:
                    sectinfo.append([x, y, vset.copy()])
        
        for m in range(len(sectinfo)):
            sin = sectinfo[m]
            
            # for each row of the puzzle search which are not whithin the sectinfo FKA (each empty from 3x3 with a vset of missing numbers) 
            rowv = set()
            for y in range(9):
                rowv.add(puzzle[sin[0]][y])
            left = sin[2].difference(rowv)
            
            # the same with columns
            colv = set()
            for x in range(9):
                colv.add(puzzle[x][sin[1]])
            left = left.difference(colv)
                         
            # check if the list left has only one number
            if len(left) == 1:
                val = left.pop()
                if check_guess(puzzle, (sin[0], sin[1]), val):
                    puzzle[sin[0]][sin[1]] = val
                    opt_guess.append((sin[0], sin[1], val))

    return opt_guess


def backtrack(puzzle, opt_guess):
    '''Undo the previous steps every time it reaches a dead end and the puzzled is not finished'''
    for i in range(len(opt_guess)):
        puzzle[opt_guess[i][0]][opt_guess[i][1]] = 0
    return

def solve_sudoku(puzzle):
    ''' # 1 Finds the next empty cell 
        # 2 Create a for loop with guesses 1 to 9 
        # 3 Check if the guess doesn't violate sudoku rules (guess is not present in row/col/3x3 grid)
        # 4 Recursively call solve_sudoku until finishes the puzzle if True and Backtrack if False
    '''
    global backtracks 

    row, col = find_next_empty(puzzle) # 1
    if row is None:
        return True 
    
    for guess in range(1, 10): # 2
        if check_guess(puzzle, (row, col), guess): # 3
            # puzzle[row][col] = guess  # place the returned valid guess at that spot on the puzzle otherwise pick another guess
            
            opt_guess = optimization(puzzle, row, col, guess)

            if solve_sudoku(puzzle): # 4
                return True
            backtracks += 1 # Counter for backtracks
            backtrack(puzzle, opt_guess) # 4 False 

            # puzzle[row][col] = 0 # 

    return False # as we used naive checking each possibility if False = its unsolvable

def print_board(board_template):
    print("\n")
    print("---------------------")
    for i in range(9):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(9):
            if j == 3 or j == 6:
                line += "| "
            line += str(board_template[i][j])+" "
        print(line)
    print("---------------------")
    print ('Backtracks = ', backtracks)
    print("\n")
    return

def call_solve():
    board = (pick_board())
    solve_sudoku(board)
    print_board(board)


# call_solve()
