import pygame
import time
import sys
from sudoku_boards import pick_board
from sudoku_solution_opt import check_guess, solve_sudoku
import tkinter as tk
from tkinter import messagebox 

class Board:
    
    def __init__(self, resolution, window):
        self.board = (pick_board())
        self.rows = 9
        self.cols = 9
        self.grid_width = 540
        self.grid_height = 540
        self.resolution = resolution
        self.window = window
        self.cell = [[Cube(self.board[i][j], i, j) for j in range(self.cols)] for i in range(self.rows)]
        self.model = None
        self.selected = None
        self.strikes = 0
    
    def update_model(self):
        '''Creates an version of the puzzle with the accepted values and the current guess, the current guess will be 0 again if wrong'''
        self.model = [[self.cell[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    

    def place(self, val):
        '''Check value and add to cell/model only if correct'''
        row, col = self.selected
        if self.cell[row][col].value == 0:
            self.cell[row][col].set_val(val)
            self.update_model()

        if check_guess(self.model, (row, col), val) and solve_sudoku(self.model):
            # print(self.model)
            return True
        else:
            self.cell[row][col].set_val(0)
            self.cell[row][col].set_temp(0)
            self.update_model()
            return False

    def sketch(self, val):
        '''Creates a temporary sketch for a guess'''
        row, col = self.selected
        self.cell[row][col].set_temp(val)
        
    def click(self, mouse):
        '''Returns position of click'''
        if mouse[0] < self.grid_width and mouse[1] < self.grid_height:
            gap = self.grid_width / 9
            x = mouse[0] // gap
            y = mouse[1] // gap
            return (int(y),int(x))
        else:
            return None    
    
    def select(self, row, col):
        '''Selects position defined on the handle keys function'''
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell[i][j].selected = False
        self.row = 1
        self.col = 1
        self.cell[row][col].selected = True
        self.selected = (row, col)

    def draw_lines(self):
        '''Draws the puzzle lines in cubes and ticker 3x3 grids'''
        teal = (0, 128, 128)
        # Add 3x3 Lines in teal
        gap = self.grid_width / 9
        for i in range(10):
            if i % 3 == 0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(self.window, teal, (5, i * gap + 5), (self.grid_width + 5, i * gap + 5), thick)
            pygame.draw.line(self.window, teal, (i * gap + 5, 5), (i * gap + 5, self.grid_height + 5), thick)

        # Addthe values to cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cell[i][j].draw(self.window)

    def draw_buttons(self, btn_width, btn_height, mouse):
        '''Adds the menu buttons bellow the puzzle'''
        btn_color = (170,170,170)
        btn_hover = (100,100,100)
        white = (255, 255, 255)

        # Set the font ans texts
        font = pygame.font.SysFont('Corbel', 25)
        font2 = pygame.font.SysFont('Corbel', 18)
        text_restart = font.render('restart', True , white) 
        text_pause = font.render('pause', True , white) 
        text_refresh = font2.render('clr guesses', True , white)

        # Restart btn on hover  
        if btn_width <= mouse[0] <= btn_width+100 and btn_height <= mouse[1] <= btn_height+40:  
            pygame.draw.rect(self.window, btn_color, (btn_width, btn_height, 100, 40)) 
        else: 
            pygame.draw.rect(self.window, btn_hover, (btn_width, btn_height, 100, 40)) 

        # Pause btn on hover  
        if btn_width+120 <= mouse[0] <= btn_width+220 and btn_height <= mouse[1] <= btn_height+40:   
            pygame.draw.rect(self.window, btn_color, (btn_width+120, btn_height, 100, 40)) 
        else: 
            pygame.draw.rect(self.window, btn_hover, (btn_width+120, btn_height, 100, 40))

        # Refresh btn on hover  
        if btn_width+240 <= mouse[0] <= btn_width+340 and btn_height <= mouse[1] <= btn_height+40:   
            pygame.draw.rect(self.window, btn_color, (btn_width+240, btn_height, 100, 40)) 
        else: 
            pygame.draw.rect(self.window, btn_hover, (btn_width+240, btn_height, 100, 40)) 

        # Superimposing the text onto button s
        self.window.blit(text_restart, (btn_width+16, btn_height+6)) 
        self.window.blit(text_pause, (btn_width+141, btn_height+6)) 
        self.window.blit(text_refresh, (btn_width+251, btn_height+10)) 

    def clear(self):
        '''Clears only selected temporary value'''
        row, col = self.selected
        if self.cell[row][col].value == 0:
            self.cell[row][col].set_temp(0)

    def clear_all(self):
        '''Clears all temporary values'''
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cell[i][j].value == 0:
                    self.cell[i][j].set_temp(0)
    
    def complete(self):
        '''Checks if no cells are 0'''
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cell[i][j].value == 0:
                    return False
        return True

    def exit_message(self):
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()
        MsgBox = tk.messagebox.askquestion('Exit Application','Are you sure you want to exit the application', icon = 'warning')
        if MsgBox == 'yes':
            pygame.quit()
            sys.exit()
            root.destroy()
    
    def pause_message(self):
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()
        tk.messagebox.showinfo('Game paused','Click OK to resume')
        root.destroy()

    def win_message(self):
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()
        MsgBox = tk.messagebox.askquestion('You win!','Congratulations. Do you want to play again')
        if MsgBox == 'no':
            pass
        else:
            self.board = (pick_board())
            self.cell = [[Cube(self.board[i][j], i, j) for j in range(self.cols)] for i in range(self.rows)] 
            self.strikes = 0 
            self.draw_lines() 

    def handle_keys(self, btn_width, btn_height, mouse, key):
        '''Defines each key event'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_message()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_message() 
                elif event.key == pygame.K_1: 
                    key = 1
                elif event.key == pygame.K_2:
                    key = 2
                elif event.key == pygame.K_3:
                    key = 3
                elif event.key == pygame.K_4:
                    key = 4
                elif event.key == pygame.K_5:
                    key = 5
                elif event.key == pygame.K_6:
                    key = 6
                elif event.key == pygame.K_7:
                    key = 7
                elif event.key == pygame.K_8:
                    key = 8
                elif event.key == pygame.K_9:
                    key = 9
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    self.clear()
                    key = None
                elif event.key == pygame.K_UP:
                    if self.selected == None:
                        current = (0, 0)
                        self.select(current[0], current[1])
                    if (self.selected[0]-1) != (-10) and (self.selected[0]-1) != (-1):
                        self.select(self.selected[0]-1, self.selected[1])
                    key = None
                elif event.key == pygame.K_DOWN:
                    if self.selected == None:
                        current = (0, 0)
                        self.select(current[0], current[1])
                    if (self.selected[0]+1) < 9:
                        self.select(self.selected[0]+1, self.selected[1])
                    key = None
                elif event.key  == pygame.K_LEFT:
                    if self.selected == None:
                        current = (1, 0)
                        self.select(current[0], current[1])
                    if self.selected[1]-1 >= 0:
                        self.select(self.selected[0], self.selected[1]-1)
                    key = None
                elif event.key  == pygame.K_RIGHT:
                    if self.selected == None:
                        current = (0, 0)
                        self.select(current[0], current[1])
                    if self.selected[1]+1 <= 8:
                        self.select(self.selected[0], self.selected[1]+1)
                    key = None
                elif event.key == pygame.K_RETURN:
                    i, j = self.selected
                    if self.cell[i][j].temp != 0:
                        if self.place(self.cell[i][j].temp):
                            print("Valid")
                        else:
                            print("Wrong")
                            self.strikes += 1
                            key = None

                        if self.complete():
                            self.win_message()
                            print("You win!")
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                clicked = self.click(mouse)
                if clicked:
                    self.select(clicked[0], clicked[1])
                    key = None
                # Restart btn
                if btn_width <= mouse[0] <= btn_width+100 and btn_height <= mouse[1] <= btn_height+40: 
                    self.board = (pick_board())
                    self.cell = [[Cube(self.board[i][j], i, j) for j in range(self.cols)] for i in range(self.rows)]
                    self.strikes = 0 
                    self.draw_lines() 
                # Pause btn 
                elif btn_width+120 <= mouse[0] <= btn_width+220 and btn_height <= mouse[1] <= btn_height+40: 
                    self.pause_message() 
                # Refresh btn 
                elif btn_width+240 <= mouse[0] <= btn_width+340 and btn_height <= mouse[1] <= btn_height+40: 
                    self.clear_all()

        if self.selected and key != None:
            self.sketch(key)

    def draw_strikes(self, board):
        '''Adds Strikes to the window'''
        red = (255, 0 , 0)
        font = pygame.font.SysFont("Corbel", 25)

        text = font.render("X " * self.strikes, 1, red)
        self.window.blit(text, (20, 610))
        

    def draw_time(self, play_time):
        black = (0, 0, 0)
     
        font = pygame.font.SysFont("Corbel", 25)
        
        seconds = play_time % 60
        minutes = play_time // 60
        hours = play_time // 3600

        timer = f"Time: {hours}:{minutes:02}:{seconds:02}"

        text = font.render(timer, True, black)
        self.window.blit(text, (550 - 160, 562))

class Cube:
    def __init__(self, value, row, col):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = 540
        self.height = 540
        self.selected = False

    def draw(self, window):
        '''Adds the numbers and the select red square to the screen'''
        main_font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = (self.col * gap) + 5
        y = (self.row * gap) + 5

        if self.temp != 0 and self.value == 0:
            text = main_font.render(str(self.temp), 1, (128,128,128))
            window.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = main_font.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(window, (255, 0, 0), (x,y, gap ,gap), 2)

    def set_val(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def main():
    # pygame.init()
    pygame.font.init()

    # Window Title
    pygame.display.set_caption("Sudoku Game")
    icon = pygame.image.load('sudoku.png')
    pygame.display.set_icon(icon)

    # Set windows size
    resolution = (550, 650)
    window = pygame.display.set_mode(resolution)

    # Set buttons size in relation to the window
    btn_width = resolution[0] / 40
    btn_height = resolution[1] - 95

    board = Board(resolution, window)

    start = time.time()

    key = None

    running = True
    while running: 

        window.fill((255,255,255))
        
        # Mouse position
        mouse = pygame.mouse.get_pos()

        board.draw_lines()
        board.draw_buttons(btn_width, btn_height, mouse)
        board.handle_keys(btn_width, btn_height, mouse, key)
        board.draw_strikes(board)

        play_time = round(time.time() - start)
        board.draw_time(play_time)
  

        pygame.display.update()

if __name__ == "__main__":
  main()


