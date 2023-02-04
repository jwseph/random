import random

class Board:
    cell_display = ' XO'
    size = 5
    winning_states = [
        (0, 1, 2, 3), (1, 2, 3, 4),
        (5, 6, 7, 8), (6, 7, 8, 9),
        (10, 11, 12, 13), (11, 12, 13, 14),
        (15, 16, 17, 18), (16, 17, 18, 19),
        (20, 21, 22, 23), (21, 22, 23, 24),
        (0, 5, 10, 15), (5, 10, 15, 20),
        (1, 6, 11, 16), (6, 11, 16, 21),
        (2, 7, 12, 17), (7, 12, 17, 22),
        (3, 8, 13, 18), (8, 13, 18, 23),
        (4, 9, 14, 19), (9, 14, 19, 24),
        (0, 6, 12, 18), (6, 12, 18, 24),
        (5, 11, 17, 23), (1, 7, 13, 19),
        (3, 7, 11, 15), (8, 12, 16, 20),
        (4, 8, 12, 16), (9, 13, 17, 21),
    ]
    dp = {}
    def __init__(self, cells=None):
        self.cells = cells or [0]*Board.size**2
        self.remaining = None
    def win(self):
        for (c_i0, *c_is) in self.winning_states:
            first = self.cells[c_i0]
            if first != 0 and all(self.cells[c_i] == first for c_i in c_is):
                return first
        return 0
    def __repr__(self):
        grid = zip(*(iter(self.cells),)*Board.size)
        return '\n---+---+---+---+---\n'.join(' '+' | '.join(Board.cell_display[cell] for cell in row)+' ' for row in grid)
        # return '\n'.join(''.join(Board.cell_display[cell] for cell in row) for row in grid)
    def __hash__(self):
        res = 0
        for cell in self.cells: res = Board.size*res+(1+cell)
        return res
    def get_remaining(self):
        if self.remaining is None:
            self.remaining = [i for i, cell in enumerate(self.cells) if cell == 0]
        return self.remaining
    def get_move(self, *, best=True):
        def make_rigid(ev):
            return ev if best else 1 if ev == 1 else -1 if ev == -1 else 0
        player = self.get_player()
        fun = {1: max, -1: min}[player]
        all_is = [
            (make_rigid(f_board.eval()), i)
            for i, f_board in enumerate(self.get_future_boards())
        ]
        random.shuffle(all_is)
        best_i = fun(all_is, key=lambda _: _[0])[1]
        return self.get_remaining()[best_i]
    def make_move(self, move):
        self.cells[move] = self.get_player()
        self.remaining = None
    def full(self):
        return len(self.get_remaining()) == 0
    def get_player(self):
        return len(self.get_remaining())%2*2-1
    def get_future_boards(self):
        f_boards = []
        for r_i in self.get_remaining():  # For remaining index in remaining indices
            f_board = Board(self.cells[:])  # Create a copy board
            f_board.cells[r_i] = self.get_player()  # Choose the chosen reamining cell as player
            f_boards.append(f_board)  # Add future copy board
        return f_boards
    def eval(self) -> float:  # 1: first player wins, -1: second player wins, 0: tie
        h = hash(self)
        if h in Board.dp: return Board.dp[h]  # Return memoized value
        if self.win() != 0:
            Board.dp[h] = float(self.win())  # Returns winner if there is one
            return Board.dp[h]
        if self.full(): return 0  # Tie when there are no cells remaining
        player = self.get_player()  # Current player
        f_boards = self.get_future_boards()
        futures = [f_board.eval() for f_board in f_boards]  # Future solve results
        if any(future == player for future in futures):
            Board.dp[h] = float(player)  # Player wins if future allows the player to win
            return Board.dp[h]
        Board.dp[h] = sum(futures)/len(futures)
        return Board.dp[h]


if __name__ == '__main__':
    import time
    print('Welcome to Tic Tac Toe!')
    print('Enter your moves as an integer x in the range [0, 9)')
    print('See if you can beat the computer (TicTacTockfish engine)')
    COMPUTER = random.randint(0, 1)*2-1  # -1 or 1
    print('Computer goes' if COMPUTER == 1 else 'You go', 'first this time')
    b = Board()
    t = time.perf_counter()
    b.eval()
    print(f'Computer: "Solved the game in {time.perf_counter()-t:.3}s"')
    print()
    while not b.win() and not b.full():
        print(b)
        print(f'Eval bar: {"+" if b.eval() > 0 else ""}{b.eval():.3f}{" M" if abs(b.eval()) == 1 else ""}\n')
        if b.get_player() == COMPUTER:
            b.make_move(b.get_move(best=False))
            print('(Computer turn)\n')
            continue
        remaining = b.get_remaining()
        print(f'Remaining cells: [{" ".join(map(str, remaining))}]')
        choice = int(input(f'Choice ({Board.cell_display[-COMPUTER]}): '))
        print()
        assert choice in remaining
        b.make_move(choice)
    print(b)
    print(f'Eval bar: {"+" if b.eval() > 0 else ""}{b.eval():.3f}{" M" if abs(b.eval()) == 1 else ""}\n')
    print('Computer: "ggs"')
    print('Game result:', 'Computer wins!' if b.win() == COMPUTER else 'Player wins!' if b.win() == -COMPUTER else 'Tie')