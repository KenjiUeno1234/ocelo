#!/usr/bin/env python3

BOARD_SIZE = 8
EMPTY = '.'
BLACK = 'B'
WHITE = 'W'
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid-1][mid-1] = WHITE
    board[mid][mid] = WHITE
    board[mid-1][mid] = BLACK
    board[mid][mid-1] = BLACK
    return board

def in_bounds(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def opponent(player):
    return BLACK if player == WHITE else WHITE

def valid_moves(board, player):
    opp = opponent(player)
    moves = set()
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != EMPTY:
                continue
            for dr, dc in DIRECTIONS:
                rr, cc = r + dr, c + dc
                has_opp = False
                while in_bounds(rr, cc) and board[rr][cc] == opp:
                    rr += dr
                    cc += dc
                    has_opp = True
                if has_opp and in_bounds(rr, cc) and board[rr][cc] == player:
                    moves.add((r, c))
                    break
    return sorted(moves)

def apply_move(board, move, player):
    r, c = move
    board[r][c] = player
    opp = opponent(player)
    for dr, dc in DIRECTIONS:
        rr, cc = r + dr, c + dc
        captured = []
        while in_bounds(rr, cc) and board[rr][cc] == opp:
            captured.append((rr, cc))
            rr += dr
            cc += dc
        if captured and in_bounds(rr, cc) and board[rr][cc] == player:
            for cr, cc in captured:
                board[cr][cc] = player

def count_stones(board):
    b = sum(row.count(BLACK) for row in board)
    w = sum(row.count(WHITE) for row in board)
    return b, w

def print_board(board):
    header = '  ' + ' '.join(str(i+1) for i in range(BOARD_SIZE))
    print(header)
    for idx, row in enumerate(board):
        print(str(idx+1) + ' ' + ' '.join(row))


def main():
    board = create_board()
    player = BLACK
    while True:
        moves = valid_moves(board, player)
        if not moves:
            other_moves = valid_moves(board, opponent(player))
            if not other_moves:
                break
            print(f"{player}は置ける場所がありません。パスします。")
            player = opponent(player)
            continue
        print_board(board)
        b, w = count_stones(board)
        print(f"黒: {b} 白: {w}")
        print(f"{player}の番です。 例: 3 4")
        print(f"有効な手: {', '.join(f'({r+1},{c+1})' for r,c in moves)}")
        try:
            inp = input('> ').strip()
        except EOFError:
            print()
            break
        if not inp:
            continue
        try:
            r, c = map(int, inp.split())
            move = (r-1, c-1)
        except ValueError:
            print("入力形式が正しくありません。")
            continue
        if move not in moves:
            print("その場所には置けません。")
            continue
        apply_move(board, move, player)
        player = opponent(player)
    print_board(board)
    b, w = count_stones(board)
    print(f"ゲーム終了 黒: {b} 白: {w}")
    if b > w:
        print("黒の勝ち")
    elif w > b:
        print("白の勝ち")
    else:
        print("引き分け")

if __name__ == '__main__':
    main()
