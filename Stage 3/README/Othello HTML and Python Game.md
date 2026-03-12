A Breakdown of the Othello/Reversi game with flowcharts of algorithms. 


**Initialise Board**


![[initialise_board.drawio 1.png]]

This function is called at the start of a new game, It creates a starting board by creating an initial list called board, a for loop is used and loops according to the size variable (which is set at 8). For each iteration, a new list is created called row, another for loop is used to and again loops to the size variable. For each loop, a none is appended to the row list unless it meets the requirements for the starting pieces (being 3,3 4,3 3,4 and 4,4) which are appended when the loops reach the required point. After each nested loop, the row is appended to the board list. Once completed the board is returned. I use a nested loop to make a list of lists therefore the bounds of the array are determined at the start of the game. 


**Print Board**

![[print_board.drawio.png]]

The Print Board function is used for the stage 1 for printing the board to the command line. It is a simple loop which prints the board to the command line. I added extra numbers to make it clearer which tile is which when printing. 

**Legal Move**

![[legal move.drawio.png]]

This function determines if the coordinates given by the player are valid and if so, calls the next function to get the coordinates of the pieces to flip. It adjusts the coordinates to a zero based index to correctly function with the list. It then checks that the coordinates are in the bounds of the list and checks if the space is empty. if these condition are true, it then determines whether there are any opponent pieces directly next to the chosen coordinate that can be outflanked. This is done by calling the get_pieces_to_flip_in_direction function (as seen below). If an empty list is returned then there are no pieces to outflank and therefore it is not a legal move. Once a list is established, then the pieces to flip list is returned. I did all this to ensure that the piece being place is legal according to the rules of the game, where a piece can only be placed next to an opponents piece that will create an outflank. 

**Get Pieces to Flip in Direction**

![[get pieces to flip in direction.drawio.png]]

This function proceeds the Legal Move function where a legal move to determine whether a move is legal by determining if any flips are made. These flips are stored and returned therefore they can be used to make the move. A direction is given as an argument, if an opponents piece is found, the program loops until a players piece is found, which will return the list of pieces to flip, or if the end of the board is reached it returns an empty list as it is not a valid move. A empty list is also returned if the direction leads to an empty space, or the same colour piece as the player. As this is repeated for each direction, if multiple direction contain pieces to flip then all directions that are valid will be stored to the pieces to flip. I use this secondary function to save having to loop back time going back through the board and ensuring that a minimal amount of area is checked. 

**Make Move**

![[make move.drawio.png]]

This function updates the board by taking the player colour, coordinate and pieces to flip which have been determined in the previous functions. This uses the coordinate to place the new piece according to the colour of the current player, and then updates the colours of the coordinates in the pieces to flip to the current colour. The board is the returned to be outputted. Since make moves is used many times, I created a separate function to handle making the move instead of including it in the game engine. 

**Check for Legal Moves**

![[check for legal moves.drawio.png]]

This function is to check whether a player has any legal moves that can be made. This is done by looping through all possible empty spaces and runs the legal move function with the coordinates from the loop. Once a one legal move is found the function is ended and passed as true as there is at least one legal move possible and therefore no need to check the rest of the board. This differs from legal move as it allows the whole board to be checked for legal moves and instead only checking till one is found saving time. 

**Count Pieces**

![[count pieces.drawio.png]]

This function is used to count the number of dark and light pieces are on the board for displaying and determining the winner at the end of the game. A nested loop is used to check each cell checking whether it contains "Dark" or "Light", if none is found then it is skipped. I did this to simply be able to calculate the winner at the end of the game, which can also be used for the flask to update the scores during the game. 


**Ai Components (For Stage 3)** 

The code below is for the Ai Component for stage 3 of the project. This replaces the second (light coloured) player.


**Get All Legal Moves**

![[get all legal moves.drawio.png]]

This function is used to gain every possible move that is legal for the ai to use. This is similar to the check for legal moves function however instead of ending after one legal move is found, each legal move coordinate is recorded and added to a list. For each cell, the legal moves function is called to determine whether the coordinate is valid, if so and it returns flips a a flips list. If the flips list is empty then it is skipped and if it is populated then it is appended to the flips to moves list. which the respective coordinate. This differs from check for legal moves as this stores all the possible legal moves the ai can make and returns them allowing them to be calculated therefore making it as its own separate function. 
**Simulate Board**

![[simulate move.drawio.png]]

This is a simple function to simulate each of the valid moves gained from all legal moves to determine which of the moves gives the best possible outcome. This is done by copying the current state of the board (to ensure that the actual board is not affected), and the possible move is executed and saved to the board copy and returned. I did this so the main board would not be affected but the results are accurate to what the board would show if the move was made. 

**Evaluate Board**

![[evaluate board.drawio.png]]

This function immediately follows the evaluate board function, This calculate currently light and dark pieces on the board. This is done to calculate the new difference between the dark and light colours. The board with the biggest difference for the enemy Ai will be the determined as the best option for the Ai to play. I did this to easily determine which move gave the best outcome for the Ai enemy.   
**Pick Ai Move**

![[pick ai move.drawio.png]]

This function stitches together the previous functions in the Ai section. This replaces the second player in the game engine section. Firstly the find all legal moves function is called to find all the legal coordinates to make moves from. If the list returned is empty then the move is skipped as there are no legal moves for the AI to make. A new list called scored moves is created which will store each move and the score that is gained and the flips it creates. A loop is created to search through each legal coordinate. This is followed by the simulate moves function to be called to gain a potential new board to be scored. This board is then passed through the evaluate board to gain a score for the board. And finally this score with the move and the flips is appended to the scored moves list. Once the loop ends, the scored moves list is sorted by highest score and then the three top moves are taken and one is picked at random, the random move picked is the move returned with the flips to be executed to update the actual board. I encapsulated all the ai components into this function therefore it can be easily implemented into the program to replace the second player without having to drastically change the code of the main game engine. 


**Game Engine**

This is the code for the flask game engine with the Ai instead of the second player. This contains the main functions of the game engine and explanations of the smaller functions used. 

**Hand Move**
![[handle move.drawio (1).png]]

This is the main function that handles when a move is made. This can either be by the player or the AI. The current board and the current player are found from the get_current_board() and get_current_player() which simply just retrieve the player and board from the current session. The algorithm used current player to determine whether it is the player or ai's turn. 

If it is the players turn, the players conditional statement is used. The move is found from the input from the webpage and the legal_move() function is called to determine whether the box that was selected is a valid box. If not an error message will be displayed and the program will terminate, only starting again once the player has selected a valid tile. Once the player selects a valid tile, the move is made using the make_move() function and then the check_game_over() function is called to determine if the game has ended. Then the switch_player() function is called to change to the opponent.

If it is the Ai's turn, the Ai conditional statement is used. The pick_ai_move() function is called to pick the move for the ai. If no move is found then the Ai turn is skipped and passed back to the player. Then the same make move, check game over and switch player functions are called. Once this is done, the results are outputted back to the webpage. 


**Check Game Over**

![[check game over.drawio (1).png]]

This function is used to determine whether any more moves can be made for either the main player or the ai. This is checked after the end of each turn. I did this to ensure that the game is checked whether it can continue constantly and does not get into a state of getting stuck. It calls check_for_legal_moves() function for both the player and ai opponent. If both cannot make any more moves, the count_pieces() function is called to determine the number of light and dark pieces. These are then compared to determine the winner or if there is a draw, and outputted back to the webpage. 
