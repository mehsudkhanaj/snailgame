""" We need to import arcade library to setup our game structure. """

# Importing necessary libraries
import arcade
import os
import copy
# Set the absolute path of our code directory
os.path.abspath(__file__)
# Loading needed images
background = arcade.load_texture("Images/background.jpg") # background image
human = arcade.load_texture("Images/human_snail.png") # image of human's snail
bot = arcade.load_texture("Images/bot_snail.png") # image of bots's snail
humanSplash = arcade.load_texture("Images/human_splash.png") # image of Human's Splash
botSplash = arcade.load_texture("Images/bot_splash.png") # image of Bot's Splash
ROWS = 10 # number of rows in the grid
COLUMNS = 10 # number of columns in the grid
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_PLAY_WIDTH = 600
GAME_PLAY_HEIGHT = 600
SCREEN_TITLE = "SNAILS - The GridWorld"

board = [] # 2D List for backEnd Matrix

BOX_SIZE = 60 # Size of one box

class Game(arcade.View):
    def __init__(self):
        super().__init__()

        self.initailize_board()
        
        # Identifiers of snails and Splashes locations
        self.human = 1
        self.bot = 2
        self.human_Splash = 10
        self.bot_Splash = 20

        self.state = 0 # Other states can be 50(for Draw), 100(Human Win), 200(Bot win)
        self.game_state = "GameMenu" # Setting this to show menu Screen
        self.turn = 1000 # (Human Turn) if Turn = 2000 (Bot Turn) 
        
        # Score counters
        self.human_score = 0 
        self.bot_score = 0

        self.human_Location = [0,0] # Initial Position of Human Snail is (0,0)
        self.Bot_Location = [9,9] # Initial Position of Bot is (9,9)
    def initailize_board(self):
        #The function is making the back-end 2D matrix
        #for the front end interface Grid.
        for j in range(ROWS):
            row = []
            for i in range(COLUMNS):
                row.append(0)
            board.append(row)
        board[0][0] = 1          # marker of human in the backend matrix is 1
        board[ROWS-1][COLUMNS-1] = 2 # marker of bot in the backend matrix is 2
        
        for j in range(ROWS):
            print()
            for i in range(COLUMNS):
                print(board[i][j], end="  ")
        print()   
        
    player, opponent = 1, 2

    # This function returns true if there are moves
    # remaining on the board. It returns false if
    # there are no moves left to play.
    def isLegalMove(self,newi,newj,currenti,currentj):
        if (newi+1==currenti and newj==currentj) or (newi-1==currenti and newj==currentj) or (newi==currenti and newj+1==currentj) or (newi==currenti and newj-1==currentj):

            return True
        else:
            return False
    def isMovesLeft(self,board) :
        for i in range(len(board)) :
            for j in range(len(board)) :
                if (board[i][j] == 0) :
                    return True
        return False

    # This is the evaluation function as discussed
    # in the previous article ( http://goo.gl/sJgv68 )
    def evaluate(self,board):
        count_p1 = 0
        count_p2 = 0
        for row in range(len(board)):	
            for col in range(len(board)):
                if board[row][col]==1:
                    count_p1+=1
                elif board[row][col]==2:
                    count_p2+=2
        if count_p1>count_p2:
            return 10
        elif count_p2>count_p1:
            return -10
        # Else if none of them have won then return 0
        return 0

    # This is the minimax function. It considers all
    # the possible ways the game can go and returns
    # the value of the board
    def minimax(self,board, depth, isMax,previous_move) :
        score = self.evaluate(board)
        # If Maximizer has won the game return his/her
        # evaluated score
        if (score == 10) :
            return score
        # If Minimizer has won the game return his/her
        # evaluated score
        if (score == -10) :
            return score

        # If there are no more moves and no winner then
        # it is a tie
        if (self.isMovesLeft(board) == False or depth==0) :
            return 0

        # If this maximizer's move
        if (isMax) :	
            best = -1000
            # Traverse all cells
            for i in range(len(board)) :		
                for j in range(len(board)) :
                    if self.isLegalMove(i,j,previous_move[0],previous_move[1]):
                    # Check if cell is empty
                        if (board[i][j]==0) :
                            # Make the move
                            board[i][j] = 2
                            # Call minimax recursively and choose
                            # the maximum value
                            best = max( best, self.minimax(board,depth - 1,not isMax, (i,j)) )
                            # Undo the move
                            board[i][j] = 0
            return best
        # If this minimizer's move
        else :
            best = 1000
            # Traverse all cells
            for i in range(len(board)) :		
                for j in range(len(board)) :
                    if self.isLegalMove(i,j,previous_move[0],previous_move[1]):
                        # Check if cell is empty
                        if (board[i][j] == 0) :
                        
                            # Make the move
                            board[i][j] = 1

                            # Call minimax recursively and choose
                            # the minimum value
                            best = min(best, self.minimax(board, depth - 1, not isMax, (i,j)))

                            # Undo the move
                            board[i][j] = 0
            return best

    # This will return the best possible move for the player
    def findBestMove(self,board,ismax,last_max) :
        bestVal = -1000
        bestMove = (-1, -1)

        # Traverse all cells, evaluate minimax function for
        # all empty cells. And return the cell with optimal
        # value.
        for i in range(len(board)) :	
            for j in range(len(board)) :
                # Check if cell is empty
                if (board[i][j] == 0):
                        if self.isLegalMove(i,j,last_max[0],last_max[1]):
                        # Make the move
                            board[i][j] = self.player
                            # compute evaluation function for this
                            # move.
                            moveVal = self.minimax(board, 8, ismax,last_max)

                            # Undo the move
                            board[i][j] = 0

                            # If the value of the current move is
                            # more than the best value, then update
                            # best/
                            if (moveVal > bestVal) :			
                                bestMove = (i, j)
                                bestVal = moveVal

        print("The value of the best Move is :", bestVal)
        return bestMove
            
    
    # This function will be used to evalute the game state at any time during the game.
    def evaluate_board(self):
        if self.bot_score == 50 and self.human_score == 50:
            self.game_state = "Draw"
           # return 5 # for Draw State
        elif self.bot_score > 50:
            self.game_state = "BotWon"
            #return 10 # for Bot Win
        elif self.human_score > 50:
            self.game_state = "HumanWon"
            #return 1 # for Human Win
        else:
            for i in range(10):
                for j in range(10):
                    if board[i][j] == 0:
                        self.state = 0  # Continue State
            
    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.game_state == "GameMenu":
                self.game_state = "GameOn"
        elif self.game_state == "GameOn":
            box = [x//BOX_SIZE, y//BOX_SIZE]    #Location of box(x,y)
            if(self.is_legal_move(box)):
                self.update_board(box)
                self.evaluate_board()
            else:
                if self.turn == 1000:
                    self.human_score += 0
                    self.turn = 2000
                elif self.turn == 2000:
                    self.bot_score += 0
                    self.turn = 1000
            
    def is_legal_move(self,box):
        # Clicking on grid line (Not Checking and not needed)
        # Clicking on an area out of bounds(outside the GridWorld) (Checking)
        #M oving the Snail onto opponent’s Snail or Trail of Slime (Checking)
        # Playing a move by passing an empty Grid Square (Checking)
        x = box[0]
        y = box[1]
        if x <= GAME_PLAY_WIDTH and y <= GAME_PLAY_HEIGHT: # Checking if clicked out side screen
            
            # The following long if is checking moving on the opponent's slime
            if (self.turn == 1000 and (board[x][y] == 0 or board[x][y] == 10)) or ((self.turn == 2000) and (board[x][y] == 0 or board[x][y] == 20)): 

                #-------- Checking Snail is not bypassing a square Start --------------#
                try: # Using these try and except blocks to ignore index error 
                    left = board[x-1][y]
                except:
                    pass
                try:
                    right = board[x+1][y]
                except:
                    pass
                try:
                    top = board[x][y+1]
                except:
                    pass
                try:
                    bottom = board[x][y-1]
                except:
                    pass
                if self.turn == 1000:
                    if x == 0 and y == 9:
                        if (right == 1 or bottom == 1):
                            return True
                        return False
                    elif x == 9 and y == 0:
                        if (top == 1 or left == 1):
                            return True
                        return False
                    elif x == 0 and y == 0:
                        if (top == 1 or right == 1):
                            return True
                        return False  
                    elif x == 9 or x == 0 or y == 0 or y == 9:
                        if x == 0:
                            if (top == 1 or bottom == 1 or right == 1):
                                return True
                            return False
                        elif x == 9:
                            if (top == 1 or bottom == 1 or left == 1):
                                return True
                            return False
                        elif y == 0:
                            if (left == 1 or top == 1 or right == 1):
                                return True
                            return False
                        elif y == 9:
                            if (left == 1 or bottom == 1 or right == 1):
                                return True
                            return False
                        else:
                            return False
                    elif (x > 0 or x < 9) and (y > 0 or y < 9):
                        if (left == 1 or right == 1 or top == 1 or bottom == 1 ):
                            return True
                        return False
                
                elif self.turn == 2000:
                    if x == 0 and y == 9:
                        if  (right == 2 or bottom == 2):
                            return True
                        return False
                    elif x == 9 and y == 0:
                        if (top == 2 or left == 2):
                            return True
                        return False
                    elif x == 9 and y == 9:
                        if (bottom == 2 or left == 2):
                            return True
                        return False
                    elif x == 9 or x == 0 or y == 0 or y == 9:
                        if x == 0:
                            if (top == 2 or bottom == 2 or right == 2):
                                return True
                            return False
                        elif x == 9:
                            if (top == 2 or bottom == 2 or left == 2):
                                return True
                            return False
                        elif y == 0:
                            if (left == 2 or top == 2 or right == 2):
                                return True
                            return False
                        elif y == 9:
                            if (left == 2 or bottom == 2 or right == 2):
                                return True
                            return False
                        else:
                            return False
                    elif (x > 0 or x < 9) and (y > 0 or y < 9):
                        if  (left == 2 or right == 2 or top == 2 or bottom == 2 ):
                            return True
                        return False
                    #--------Checking Snail is not bypassing a square End--------------#
            else:
                return False
        

        else:
            return False

    def update_board(self,box):
        
        """
        This function is updating backend 2d matrix and player scores.
        box[x,y] is the location where Snail needs to be placed. 
        """

        # Present Location of Bot 
        
        # Present Location of Human
        if self.turn == 1000: 
            hx = self.human_Location[0]
            hy = self.human_Location[1]
            # Desired Location where the mouse is clicked 
            cx = box[0]
            cy = box[1]
            self.turn = 2000      # Changing Turn
            if (board[cx][cy]==0 or board[cx][cy]==10 ):     # -------> HUMAN's TURN <------------
                board[hx][hy] = 10    # Placing Splash on the Present human Location 
                self.human_score += 1 # Increasing Human Score     
                
                if board[cx][cy] == 10: # This will execute when the Human clicks on his Splash(Slippery Functionality for Human)
                    self.human_score -= 1 # No Score should be increased if clicked on splash 
                    if hx == cx and cy > hy:
                        for y in range(hy+1, 10, 1):
                            if y == 9 and board[cx][y]==10:
                                board[cx][y] = 1
                                self.human_Location[0] = cx
                                self.human_Location[1] = y
                                break
                            elif board[cx][y] == 0 or board[cx][y] == 20 or board[cx][y] == 2:
                                board[cx][y-1] = 1
                                self.human_Location[0] = cx
                                self.human_Location[1] = y-1
                                break
                    elif hx == cx and cy < hy:
                        for y in range(hy-1, -1, -1):
                            if y == 0 and board[cx][y] == 10:
                                board[cx][y] = 1
                                self.human_Location[0] = cx
                                self.human_Location[1] = y
                                break
                            elif board[cx][y] == 0 or board[cx][y] == 20 or board[cx][y] == 2:
                                board[cx][y+1] = 1
                                self.human_Location[0] = cx
                                self.human_Location[1] = y+1
                                break
                    elif cx > hx and cy == hy:
                        if cx == 9:              # Right Side Corner case
                            board[cx][cy] = 1
                            self.human_Location = box
                            return
                        for x in range(cx+1, 10, 1):
                            if x == 9 and board[x][cy] == 10:
                                board[x][cy] = 1 
                                self.human_Location[0] = x
                                self.human_Location[1] = cy
                                break
                            elif board[x][cy] == 0 or board[x][cy] == 20 or board[x][cy] == 2:
                                board[x-1][cy] = 1
                                self.human_Location[0] = x-1
                                self.human_Location[1] = cy
                                break
                    elif cx < hx and cy == hy:
                        if cx == 0:             # Left Side Corner case
                            board[cx][cy] = 1
                            self.human_Location = box
                            return
                        for x in range(cx-1, -1, -1):
                            if x == 0 and board[x][cy] == 10:
                                board[x][cy] = 1
                                self.human_Location[0] = x
                                self.human_Location[1] = cy
                                break
                            elif board[x][cy] == 0 or board[x][cy] == 20 or board[x][cy] == 2:
                                board[x+1][cy] = 1
                                self.human_Location[0] = x+1
                                self.human_Location[1] = cy
                                break
                    elif cx == hx and cy == hy: # When Player will click on itself, it will lose the turn and scores will remain the same
                        self.human_score -= 1 
                    #----------------------------------------------------------------------------
                    
                else:                   # This will execute When Human clicks Empty Square
                    board[hx][hy] = 10
                    board[cx][cy] = 1
                    self.human_Location = box
                    #----------------------------------------------------------------------------
                    #----------------------------------------------------------------------------

        print("-----------------------------------------------")
        for j in range(ROWS):
            print()
            for i in range(COLUMNS):
                print(board[i][j], end="\t")
        print()
    def on_update(self, delta_time: float):
        bx = self.Bot_Location[0] 
        by = self.Bot_Location[1]
        if self.turn == 2000:      # -----> BOT's TURN <-----
            new_board = copy.deepcopy(board)
            # # board[bx][by]=20
            # # self.turn = 1000
            bestmove = self.findBestMove(new_board,True,(bx,by))
            box=[bestmove[0],bestmove[1]]
            cx,cy = box[0],box[1]
            self.turn = 1000         # Fliping turn  
            # # board[bestmove[0]][bestmove[1]]=2
            # self.Bot_Location[0] = bestmove[0]
            # self.Bot_Location[1] = bestmove[1]
            # self.bot_score += 1
            if (board[cx][cy]==0 or board[cx][cy]==20 ):
                board[bx][by] = 20       # Putting Splash on the Bot Location
                self.bot_score += 1      # Increasing Bot Score 
                if board[cx][cy] == 20:  # This will execute when the Bot clicks on his Splash(Slippery Functionality for Bot)   
                    self.bot_score -= 1  # Scores should not be added in this case
                    if bx == cx and cy > by:
                        for y in range(by+1, 10, 1):
                            if y == 9 and board[cx][y] == 20:
                                board[cx][y] = 2
                                self.Bot_Location[0] = cx
                                self.Bot_Location[1] = y
                                break
                            elif board[cx][y] == 0 or board[cx][y] == 10 or board[cx][y] == 1:
                                board[cx][y-1] = 2
                                self.Bot_Location[0] = cx
                                self.Bot_Location[1] = y-1
                                break
                    elif bx == cx and cy <  by:
                        for y in range(by-1, -1, -1):
                            if y == 0 and board[cx][y] == 20:
                                board[cx][y] = 2
                                self.Bot_Location[0] = cx
                                self.Bot_Location[1] = y
                                break
                            elif board[cx][y] == 0 or board[cx][y] == 10 or board[cx][y] == 1:
                                board[cx][y+1] = 2
                                self.Bot_Location[0] = cx
                                self.Bot_Location[1] = y+1
                                break
                    elif cx > bx and cy == by:
                        if cx == 9:              # Right Side Corner case
                            board[cx][cy] = 2
                            self.Bot_Location = box
                            return
                        for x in range(cx+1, 10, 1):
                            if x == 9 and board[x][cy] == 20:
                                board[x][cy] = 2
                                self.Bot_Location[0] = x
                                self.Bot_Location[1] = cy
                                break
                            elif board[x][cy] == 0 or board[x][cy] == 10 or board[x][cy] == 1:
                                board[x-1][cy] = 2
                                self.Bot_Location[0] = x-1
                                self.Bot_Location[1] = cy
                                break
                    elif cx < bx and cy == by:
                        if cx == 0:              # Left Side Corner case
                            board[cx][cy] = 2
                            self.Bot_Location = box
                            return
                        for x in range(cx-1, -1, -1):
                            if x == 0 and board[x][cy] == 20:
                                board[x][cy] = 2
                                self.Bot_Location[0] = x
                                self.Bot_Location[1] = cy
                                break
                            elif board[x][cy] == 0 or board[x][cy] == 10 or board[x][cy] == 1:
                                board[x+1][cy] = 2
                                self.Bot_Location[0] = x+1
                                self.Bot_Location[1] = cy
                                break
                    elif cx == bx and cy == by:
                        self.bot_score -= 1 
                    #---------------------------------------------   
                else:    # This will execute When Bot clicks Empty Square
                    board[bx][by] = 20
                    board[cx][cy] = 2
                    self.Bot_Location = box
                    #---------------------------------------------    
    def on_show(self):
        arcade.set_background_color(arcade.color.FLORAL_WHITE)
        

    def on_draw(self):
        arcade.start_render()

        if self.game_state == "GameMenu":
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, background)
            arcade.draw_text("SNAILS", SCREEN_WIDTH-400, SCREEN_HEIGHT-250,
                         arcade.color.FLORAL_WHITE, font_size=100, anchor_x="center")
            arcade.draw_text("The GridWorld", SCREEN_WIDTH-400, SCREEN_HEIGHT-350,
                         arcade.color.FLORAL_WHITE, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Click here to play game", SCREEN_WIDTH-400, SCREEN_HEIGHT/2-200,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        elif self.game_state == "GameOn":
            # setting the background image
            arcade.draw_lrwh_rectangle_textured(0, 0, GAME_PLAY_WIDTH, GAME_PLAY_HEIGHT, background)
            # drawing Lines for playing Snail for Front End Grid.
            for x in range (0, 600, BOX_SIZE):
                arcade.draw_line(0, x, 600, x, arcade.color.FLORAL_WHITE,4)
            for y in range (0, 600, BOX_SIZE):
                arcade.draw_line(y, 0, y, 600, arcade.color.FLORAL_WHITE,4)
                
            arcade.set_background_color(arcade.color.FLORAL_WHITE)
            arcade.draw_text("Human", (GAME_PLAY_WIDTH/2)+400, (GAME_PLAY_HEIGHT/2)+150,
                         arcade.color.DARK_BROWN, font_size=20, anchor_x="center")
            arcade.draw_text(str(self.human_score), (GAME_PLAY_WIDTH/2)+400, (GAME_PLAY_HEIGHT/2)+100,
                 arcade.color.BLACK, font_size=40, anchor_x="center")
            arcade.draw_text(str("Bot"), (GAME_PLAY_WIDTH/2)+400, (GAME_PLAY_HEIGHT/2)+50,
                        arcade.color.DARK_RED, font_size=20, anchor_x="center")
            arcade.draw_text(str(self.bot_score), (GAME_PLAY_WIDTH/2)+400, (GAME_PLAY_HEIGHT/2),
                 arcade.color.BLACK, font_size=40, anchor_x="center")
            if self.turn == 1000:
                arcade.draw_text(str("Turn"), (GAME_PLAY_WIDTH/2)+400, (GAME_PLAY_HEIGHT/2)-100,
                        arcade.color.BLACK, font_size=25, anchor_x="center")
                arcade.draw_text("Human", (GAME_PLAY_WIDTH/2)+400, (GAME_PLAY_HEIGHT/2)-150,
                 arcade.color.DARK_BROWN, font_size=20, font_name='comic', anchor_x="center")
            else:
                arcade.draw_text(str("Turn"), (GAME_PLAY_WIDTH/2)+400, (GAME_PLAY_HEIGHT/2)-100,
                        arcade.color.BLACK, font_size=25, anchor_x="center")
                arcade.draw_text("Bot", (GAME_PLAY_WIDTH/2)+400, (GAME_PLAY_HEIGHT/2)-150,
                 arcade.color.DARK_RED, font_size=20, font_name='comic', anchor_x="center")
            
            # These for loops are maping background 2D Matrix with Front End Grid.
            for i in range(10):
                for j in range(10):
                    if board[i][j] == 1:
                        arcade.draw_lrwh_rectangle_textured(BOX_SIZE*i+9, BOX_SIZE*j, BOX_SIZE-8, BOX_SIZE-2, human)
                    elif board[i][j] == 2:
                        arcade.draw_lrwh_rectangle_textured(BOX_SIZE*i+5, BOX_SIZE*j, BOX_SIZE-8, BOX_SIZE-2, bot)
                    elif board[i][j] == 10:
                        arcade.draw_lrwh_rectangle_textured(BOX_SIZE*i+5, BOX_SIZE*j, BOX_SIZE-8, BOX_SIZE-2, humanSplash)
                    elif board[i][j] == 20:
                        arcade.draw_lrwh_rectangle_textured(BOX_SIZE*i+5, BOX_SIZE*j, BOX_SIZE-8, BOX_SIZE-2, botSplash)
        
        elif self.game_state == "Draw":
            arcade.set_background_color(arcade.color.WHITE)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("It's a Draw :(", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, bold=True, anchor_x="center")
            
        elif self.game_state == "HumanWon":
            arcade.set_background_color(arcade.color.WHITE)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Human Won", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, anchor_x="center")
            arcade.draw_lrwh_rectangle_textured(325, 400, 200, 200, human)
            
        elif self.game_state == "BotWon":
            arcade.set_background_color(arcade.color.WHITE)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Bot Won", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, anchor_x="center")
            arcade.draw_lrwh_rectangle_textured(325, 400, 200, 200, bot) 
    
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    game_view = Game()
    window.show_view(game_view)
    arcade.run()
main()