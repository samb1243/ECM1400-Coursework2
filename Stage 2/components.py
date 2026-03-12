def initalise_board(size): #create the othello board
    board = [] #empty board
    for i in range(size):
        row = []
        for j in range(size): #make each row of the board
            #set the initial four pieces in the center of the board
            if i == 3 and j == 3:
                row.append('Light')
            elif i == 3 and j == 4:
                row.append('Dark')
            elif i == 4 and j == 3:
                row.append('Dark')
            elif i == 4 and j == 4:
                row.append('Light')
            else:
                row.append(None) #empty cell
        board.append(row) #append the row to the board
    
    return board
        
def print_board(board):
    size = len(board)

    #print column numbers 
    print("       " + "   ".join(f"{i:^6}" for i in range(1, size + 1)))

    for idx, row in enumerate(board, start=1):
        #print table with row number in the beginning
        print(f"{idx:^6} " + " | ".join(f"{cell or 'None':^6}" for cell in row))

        
#for checking if the move is legal and returning the pieces to flip
def legal_move(colour, coodinate, board):
    x, y = coodinate
    #adjusting for 0-indexed list
    x -= 1  
    y -= 1  
    
    #create local variable for board size 
    board_size = len(board)
    
    #check if coordinates are out of bounds
    if not (0 <= x < board_size and 0 <= y < board_size):
        return [] #invalid coordinates
        
    #check if space is empty 
    if board[y][x] is not None:
        return []
    
    #directions to check for outflanking
    directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    pieces_to_flip = []
    
    #check each direction for outflanking
    for dx, dy in directions:
        pieces_to_flip.extend(get_pieces_to_flip_in_direction(board, colour, x, y, dx, dy))
        
    if not pieces_to_flip:
        return [] #returns an empty list if the move is illegal
    else:
        return pieces_to_flip #returns the list of coordinates to flip

#function to flip the peices in a given direction
def get_pieces_to_flip_in_direction(board, colour, x, y, dx, dy):
    opponent = 'Dark' if colour == 'Light' else 'Light' #determine which colour to flip to 
    
    pieces_to_flip = [] #list sto store pieces to flip
    nx, ny = x + dx, y + dy #the next cell in the given direction
    
    #loop untill we reach the edge of the board
    while 0 <= nx < len(board) and 0 <= ny < len(board):
        cell = board[ny][nx]
        if cell == opponent: #found an opponents piece to flip
            pieces_to_flip.append((nx, ny)) #temporarily store the flipped pieces
        elif cell == colour: 
            return pieces_to_flip # found player's colour meaning a valid outflank has been reached 
        else: #cell is None
            return [] #no outflank so return empty list
        
        #move to next cell in direction
        nx += dx
        ny += dy
        
    return [] #reached end of board without finding player's colour


        
#function to execute the move and flip the pieces
def make_move(board, colour, coordinate, pieces_to_flip):
    x, y = coordinate
    #adjusting for 0-indexed list
    x -= 1
    y -= 1
    
    #place the player's piece
    board[y][x] = colour
    
    #flip the outflanked pieces
    for fx, fy in pieces_to_flip:
        board[fy][fx] = colour
        
    return board

#function to check for any legal moves for a player
def check_for_legal_moves(board, colour):
    size = len(board)
    for y in range(size):
        for x in range(size):
            #check if the cell is empty which can be a potential move 
            if board[y][x] is None:
                # calls legal_move to check if placing a piece here is legal
                if legal_move(colour, (x + 1, y + 1), board):
                    return True #found at least one legal move
    return False

#function to count the pieces on the board
def count_pieces(board):
    dark_count = 0
    light_count = 0
    for row in board:
        for cell in row:
            if cell == 'Dark': #count for dark peices 
                dark_count += 1
            elif cell == 'Light': #count for light peices
                light_count += 1
    return dark_count, light_count