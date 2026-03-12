import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import components

# --- Flask App Setup ---
app = Flask(__name__)
#secret key for session management
app.secret_key = 'key' 

# The board size for the game
BOARD_SIZE = 8
# The path where saved games will be stored
SAVE_FILE = 'othello_save.json'


#game state management functions

def initialize_game_state():
    #intialise the board and the players turn
    session['board'] = components.initalise_board(BOARD_SIZE)
    session['current_player'] = 'Dark' #dark starts first
    session['game_log'] = ["Game started. Dark's turn."]

def get_current_board():
    #return the current board 
    return session.get('board', components.initalise_board(BOARD_SIZE))

def get_current_player():
    #return the current player
    return session.get('current_player', 'Dark')

def switch_player():
    #switches the player
    session['current_player'] = 'Light' if session['current_player'] == 'Dark' else 'Dark'

def check_game_over(board, current_player): #for checking when the game is over
    #check if the current player has any moves
    current_player_can_move = components.check_for_legal_moves(board, current_player)
    
    #check if the opponent has any moves
    opponent = 'Light' if current_player == 'Dark' else 'Dark'
    opponent_can_move = components.check_for_legal_moves(board, opponent)

    if current_player_can_move:
        return None #game continues

    if not current_player_can_move and opponent_can_move:
        #pass the turn to the next player 
        return (current_player + " Pass")
    
    #game ends if neither player can move
    dark_count, light_count = components.count_pieces(board)
    
    if dark_count > light_count:
        winner = 'Dark'
    elif light_count > dark_count:
        winner = 'Light'
    else:
        winner = 'Draw'
        
    return f"Game Over! Dark: {dark_count}, Light: {light_count}. Winner: {winner}"

#file handling section.

@app.route('/save_game')
def save_game():
    try:
        #save the current game session to a json file
        game_state = {
            'board': session.get('board'),
            'current_player': session.get('current_player'),
            'game_log': session.get('game_log')
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(game_state, f)
        return jsonify({'status': 'success', 'message': 'Game saved successfully!'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Error saving game: {e}'})

@app.route('/load_game')
def load_game():
    #load the game from the saved json file
    try:
        with open(SAVE_FILE, 'r') as f:
            game_state = json.load(f)
        
        # Restore the session with the loaded data
        session['board'] = game_state['board']
        session['current_player'] = game_state['current_player']
        session['game_log'] = game_state.get('game_log', ["Game loaded."])
        
        return jsonify({'status': 'success', 'message': 'Game loaded successfully!'})
    #excpetion handling is the file cannot be found or failed to load
    except FileNotFoundError:
        return jsonify({'status': 'fail', 'message': 'No saved game found.'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Error loading game: {e}'})

#flask routes for game interaction

@app.route('/')
def index():
    #rendering the main game page 
    if 'board' not in session:
        initialize_game_state()
        
    #get current score for display
    dark_count, light_count = components.count_pieces(get_current_board())

    #display the game board, current player and scores for each player 
    return render_template(
        'index.html', 
        game_board=get_current_board(),
        current_player=get_current_player(),
        dark_score=dark_count,
        light_score=light_count
    )

@app.route('/reset')
def reset_game(): #for resetting the game
    initialize_game_state()
    return redirect(url_for('index'))

#new move route with ai included instead of second player 
@app.route('/move')
def handle_move():
    board = get_current_board()
    player = get_current_player()

    #human move section
    if player == "Dark": 
        try: #get input from the user through the webpage and split into x and y coordinates
            x = int(request.args.get('x'))
            y = int(request.args.get('y'))
        except (TypeError, ValueError):
            return jsonify({'status': 'fail', 'message': 'Invalid coordinates.'})

        flips = components.legal_move(player, (x, y), board) #find the flips for the move, if none are availble then repeat till one is found
        if not flips:
            return jsonify({'status': 'fail', 'message': 'Illegal move.'})

        board = components.make_move(board, player, (x, y), flips) #make the move on the board
        session['board'] = board
        session['game_log'].append(f"Dark played ({x}, {y}).")

        # Check game end
        result = check_game_over(board, player) #check if the game is over after the human move
        if result:
            session['game_log'].append(result) #append the results to the page 
            return jsonify({
                'status': 'finished',
                'board': board,
                'finished': result
            })

        switch_player()  #switch to ai 

    #ai move section
    ai_player = get_current_player()
    if ai_player == "Light":
        move = components.pick_ai_move(board, "Light") #cal the pick ai move function to decide the ai's move

        if move is None: #if there is no move available for the ai then pass the turn back to the human player
            session['game_log'].append("AI has no legal moves. Passing turn.")
            switch_player()
            return jsonify({
                'status': 'success',
                'board': board,
                'player': get_current_player(),
                'message': "AI passed."
            })

        (x, y), flips = move #unpack the move and flips from the ai's decision
        board = components.make_move(board, "Light", (x, y), flips) #make the ai's move on the board
        session['board'] = board
        session['game_log'].append(f"AI played ({x}, {y}).")

        result = check_game_over(board, "Light") #check if the game is over after the ai move
        if result:
            session['game_log'].append(result) #print to the webpage
            return jsonify({
                'status': 'finished',
                'board': board,
                'finished': result
            })

        switch_player() #return to human player

    return jsonify({ #print to the webpage 
        'status': 'success',
        'board': board,
        'player': get_current_player(),
        'message': 'Move complete.'
    })



if __name__ == '__main__':
    app.run(debug=True)