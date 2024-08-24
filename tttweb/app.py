from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def initialize_board():
    return [['-' for _ in range(3)] for _ in range(3)]

def check_win(board, mark):
    for i in range(3):
        if all(board[i][j] == mark for j in range(3)) or all(board[j][i] == mark for j in range(3)):
            return True
    if all(board[i][i] == mark for i in range(3)) or all(board[i][2-i] == mark for i in range(3)):
        return True
    return False

def check_draw(board):
    return all(cell != '-' for row in board for cell in row)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    row, col = data['row'], data['col']
    mark = data['mark']

    board = request.session.get('board', initialize_board())
    if board[row][col] == '-':
        board[row][col] = mark
        if check_win(board, mark):
            return jsonify({'status': 'win', 'board': board})
        elif check_draw(board):
            return jsonify({'status': 'draw', 'board': board})
        else:
            computer_move(board)
            if check_win(board, 'O'):
                return jsonify({'status': 'computer_win', 'board': board})
            elif check_draw(board):
                return jsonify({'status': 'draw', 'board': board})

    return jsonify({'status': 'continue', 'board': board})

def computer_move(board):
    available = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '-']
    if available:
        row, col = random.choice(available)
        board[row][col] = 'O'

if __name__ == '__main__':
    app.run(debug=True)
