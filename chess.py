# -*- coding: utf-8 -*-
"""
Created on Thu May 16 23:44:29 2024

@author: tamer
"""

class Piece:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, board, position):
        raise NotImplementedError("This method should be implemented by subclasses")

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def valid_moves(self, board, position):
        moves = []
        row, col = position
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Move forward one square
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
            # Move forward two squares if not moved
            if not self.has_moved and 0 <= row + 2 * direction < 8 and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))
        
        # Capture diagonally
        for dc in [-1, 1]:
            if 0 <= col + dc < 8:
                if 0 <= row + direction < 8:
                    target = board[row + direction][col + dc]
                    if target is not None and target.color != self.color:
                        moves.append((row + direction, col + dc))
        
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def valid_moves(self, board, position):
        moves = []
        row, col = position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board[r][c]
                    if target is None:
                        moves.append((r, c))
                    elif target.color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Knight(Piece):
    def valid_moves(self, board, position):
        moves = []
        row, col = position
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves

class Bishop(Piece):
    def valid_moves(self, board, position):
        moves = []
        row, col = position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board[r][c]
                    if target is None:
                        moves.append((r, c))
                    elif target.color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        return moves

class Queen(Piece):
    def valid_moves(self, board, position):
        # Queen's moves are a combination of Rook and Bishop
        moves = Rook(self.color).valid_moves(board, position)
        moves.extend(Bishop(self.color).valid_moves(board, position))
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def valid_moves(self, board, position):
        moves = []
        row, col = position
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))

        # Castling
        if not self.has_moved:
            # Kingside castling
            if board[row][col + 1] is None and board[row][col + 2] is None:
                rook = board[row][col + 3]
                if isinstance(rook, Rook) and not rook.has_moved:
                    moves.append((row, col + 2))
            # Queenside castling
            if board[row][col - 1] is None and board[row][col - 2] is None and board[row][col - 3] is None:
                rook = board[row][col - 4]
                if isinstance(rook, Rook) and not rook.has_moved:
                    moves.append((row, col - 2))
        
        return moves

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        # Pawn setup
        for col in range(8):
            self.board[1][col] = Pawn('black')
            self.board[6][col] = Pawn('white')
        
        # Rook setup
        self.board[0][0] = self.board[0][7] = Rook('black')
        self.board[7][0] = self.board[7][7] = Rook('white')

        # Knight setup
        self.board[0][1] = self.board[0][6] = Knight('black')
        self.board[7][1] = self.board[7][6] = Knight('white')

        # Bishop setup
        self.board[0][2] = self.board[0][5] = Bishop('black')
        self.board[7][2] = self.board[7][5] = Bishop('white')

        # Queen setup
        self.board[0][3] = Queen('black')
        self.board[7][3] = Queen('white')

        # King setup
        self.board[0][4] = King('black')
        self.board[7][4] = King('white')

    def get_piece(self, position):
        row, col = position
        return self.board[row][col]

    def set_piece(self, position, piece):
        row, col = position
        self.board[row][col] = piece

    def display(self):
        for row in self.board:
            print(' '.join(['.' if piece is None else piece.__class__.__name__[0] for piece in row]))

    def is_check(self, color):
        king_position = self.find_king(color)
        if king_position is None:
            return False
        return self.is_position_under_attack(king_position, color)

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def is_position_under_attack(self, position, color):
        opponent_color = 'white' if color == 'black' else 'black'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None and piece.color == opponent_color:
                    if position in piece.valid_moves(self.board, (row, col)):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None and piece.color == color:
                    valid_moves = piece.valid_moves(self.board, (row, col))
                    for move in valid_moves:
                        original_piece = self.get_piece(move)
                        self.set_piece(move, piece)
                        self.set_piece((row, col), None)
                        if not self.is_check(color):
                            self.set_piece((row, col), piece)
                            self.set_piece(move, original_piece)
                            return False
                        self.set_piece((row, col), piece)
                        self.set_piece(move, original_piece)
        return True

def move_piece(board, start_pos, end_pos):
    piece = board.get_piece(start_pos)
    if piece is None:
        print("No piece at the start position!")
        return False

    valid_moves = piece.valid_moves(board.board, start_pos)
    if end_pos in valid_moves:
        original_piece = board.get_piece(end_pos)
        board.set_piece(end_pos, piece)
        board.set_piece(start_pos, None)
        piece.has_moved = True  # Update the pawn's moved status
        if board.is_check(piece.color):
            print("Move puts own king in check!")
            board.set_piece(start_pos, piece)
            board.set_piece(end_pos, original_piece)
            return False
        print(f"Moved {piece.__class__.__name__} from {start_pos} to {end_pos}")
        if board.is_checkmate('white' if piece.color == 'black' else 'black'):
            print(f"Checkmate! {'White' if piece.color == 'black' else 'Black'} wins!")
            return 'checkmate'
        return True
    else:
        print(f"Invalid move for {piece.__class__.__name__} from {start_pos} to {end_pos}")
        return False

def get_position_input(prompt):
    while True:
        try:
            pos = input(prompt)
            row, col = map(int, pos.split(','))
            if 0 <= row < 8 and 0 <= col < 8:
                return row, col
            else:
                print("Invalid position. Please enter values between 0 and 7.")
        except ValueError:
            print("Invalid input format. Please enter row,col (e.g., 6,0).")

def play_game():
    board = Board()
    board.display()
    
    while True:
        start_pos = get_position_input("Enter the start position (row,col) between 0 and 7: ")
        piece = board.get_piece(start_pos)
        if piece is None:
            print("No piece at the start position! Please try again.")
            continue

        valid_moves = piece.valid_moves(board.board, start_pos)
        if not valid_moves:
            print("No valid moves for this piece! Please try again.")
            continue

        print(f"Valid moves for {piece.__class__.__name__} at {start_pos}: {valid_moves}")
        end_pos = get_position_input("Enter the end position (row,col) from the list of valid moves: ")
        if end_pos not in valid_moves:
            print("Invalid move! Please try again.")
            continue

        result = move_piece(board, start_pos, end_pos)
        if result == 'checkmate':
            board.display()
            print("Game over!")
            break
        elif result:
            board.display()
        else:
            print("Please try again with a valid move.")

play_game()

