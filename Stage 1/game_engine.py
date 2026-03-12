import components    

def cli_coords_input():
    
    while True:
        user_input = input("Enter coordinates (x,y): ") #prompt for user
        try: #checks whether the input is entered correctly
            x_str, y_str = user_input.split(',') #splits where the comma is places 
            x = int(x_str.strip()) #stores x value
            y = int(y_str.strip()) #stores y value
            if x < 1 or x > 8 or y < 1 or y > 8: #chekcs if the values are within range of the board 
                print("Coordinates must be between 1 and 8. Please try again.")
                continue
            return (x, y)
        except ValueError: #error message if values are inputted incorrectly
            print("Invalid input. Please enter coordinates in the format 'x,y' where x and y are integers.")


def simple_game_loop():
    print("Welcome to Othello! Let the game begin.")
    
    #intialise the board 
    board = components.initalise_board(8)

    #set a move counter to 60.
    movecounter = 60 
    
    #player colours and staring with dark player 
    colours = ['Dark', 'Light'] 
    current_player_index = 0

    #loop for each turn 
    while movecounter > 0:
        components.print_board(board) #call the print board function to display the board to the command line
        current_colour = colours[current_player_index] #get the colour of the current player who's turn it is
        
        #checks if there are any legal moves for the player to make 
        if not components.check_for_legal_moves(board, current_colour):
            print(f"No legal moves for {current_colour}. Passing turn.") #output if there a no legal moves available for that player 
            
            current_player_index = 1 - current_player_index #switch to the other player
            other_colour = colours[current_player_index] #switch to other colour 
            
            if not components.check_for_legal_moves(board, other_colour): #checks if the other player has any legal moves
                print("No legal moves for either player. Game over!") #if not then end game as no player can make a move 
                break 
            continue 


        #loop untill a legal input is made 
        LegalMoveMade = False 
        while not LegalMoveMade and movecounter > 0:
            print(f"{current_colour}'s turn.")
            
            coords = cli_coords_input() #call function to get user input for coordinates
        
            pieces_to_flip = components.legal_move(current_colour, coords, board) #calls the function to gain the coordinates of pieces to flip

            if pieces_to_flip: #runs if the list is not empty 
                
                LegalMoveMade = True #set to true to end the while loop 
                
                board = components.make_move(board, current_colour, coords, pieces_to_flip) #execute the move and flip the pieces
                
                movecounter -= 1 #decrease the move counter by 1
                
                current_player_index = 1 - current_player_index #change to the other player
            else:
                
                print("Illegal move, please try again.") #output if the move is illegal and runs the loop again for new input

    
    components.print_board(board) #prints the board at the end of the game

    #count each colour pieces on the board 
    dark_count, light_count = components.count_pieces(board)
    print("GAME OVER")
    print(f"Final Score: Dark: {dark_count}, Light: {light_count}")
    
    #determine which colour has more pieces and declare the winner
    if dark_count > light_count:
        print("Dark wins!")
    elif light_count > dark_count:
        print("Light wins!")
    else:
        print("It's a draw!")
        
#example usage
if __name__ == "__main__":
    simple_game_loop()