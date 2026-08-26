import random
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter your name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name. LETTERS ONLY!")

    def choose_symbol(self):
        while True:
            symbol = input(f"\n{self.name}, choose your symbol (single letter): ")
            if symbol.isalpha() and len(symbol) == 1:
                self.symbol = symbol.upper()
                break
            print("Invalid symbol. SINGLE LETTER ONLY! or LETTER ONLY!")

    def set_symbol(self, symbol):
        self.symbol = symbol.upper()


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()
        self.name = "Computer"

    def choose_name(self):
        self.name = "Computer"

    def choose_symbol(self, human_symbol):
        letters = [chr(code) for code in range(ord('A'), ord('Z') + 1)]
        available = [letter for letter in letters if letter != human_symbol.upper()]
        self.symbol = random.choice(available)


class Menu:
    def dislpay_main_menu(self):
        print("==" * 40, "\n\t\t\tWelcome to X-O game!\n", "==" * 40, "\n1. Play 2 Players\n2. Play against Computer\n3. Quit Game\n", "--" * 40)
        while True:
            try:
                choice = int(input("\nEnter your choice: "))
                if choice in (1, 2, 3):
                    return choice
                print("Enter a valid number!")
            except ValueError as e:
                print(f"\nError, not a valid input: {e}")

    def display_end_game_menu(self):
        while True:
            try:
                print("++" * 30)
                print("\t\t\tGame Over!")
                print("1. Restart Game")
                print("2. Quit Game")
                print("++" * 30)
                choice = int(input("Enter your choice: "))

                if choice in (1, 2): return choice
                print("Enter a valid input!")
            except ValueError as e:
                print(f"\nError, not a valid input: {e}")


class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        for i in range(0, len(self.board), 3):
            print("|".join(self.board[i:i+3]))
            if i < 6: print("-" * 5)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        if not 1 <= choice <= 9:
            return False
        return self.board[choice - 1].isdigit()

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]

class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = random.randint(0, 1)
        self.vs_computer = False

    def start_game(self):
        choice = self.menu.dislpay_main_menu()

        if choice == 1:
            self.vs_computer = False
            self.setup_players()
            self.play_game()

        elif choice == 2:
            self.vs_computer = True
            self.setup_players()
            self.play_game()

        elif choice == 3: self.quit_game()
        else:
            print("Enter a valid number!")

    def setup_players(self):
        if self.vs_computer:
            print("\nPlayer 1, Enter your details:")
            self.players[0].choose_name()
            self.players[0].choose_symbol()
            self.players[1] = ComputerPlayer()
            self.players[1].choose_symbol(self.players[0].symbol)
            clear_screen()
            print("--" * 40)
            return

        for number, player in enumerate(self.players, start=1):
            print(f"\nPlayer {number}, Enter your details:")
            player.choose_name()
            player.choose_symbol()
            clear_screen()
            print("--" * 40)

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win():
                winner = self.players[1 - self.current_player_index]
                clear_screen()
                self.board.display_board()
                print(f"\n\t\t\tCongratulations! {winner.name} wins!")
                choice = self.menu.display_end_game_menu()

                if choice == 1: self.restart_game()
                elif choice == 2:
                    self.quit_game()
                    break

                else: print("Enter a valid input!")

            elif self.check_draw():
                clear_screen()
                self.board.display_board()
                print("\n\t\t\tIt's a draw!")
                choice = self.menu.display_end_game_menu()

                if choice == 1: self.restart_game()
                elif choice == 2:
                    self.quit_game()
                    break

                else: print("Enter a valid input!")
            clear_screen()

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = random.randint(0, 1)
        self.play_game()

    def check_win(self):
        win_compinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],

            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],

            [0, 4, 8],
            [2, 4, 6]
        ]

        for combo in win_compinations:
            first = self.board.board[combo[0]]
            if first.isdigit(): continue
            if first == self.board.board[combo[1]] == self.board.board[combo[2]]: return True
        return False

    def check_draw(self):
       return all(not cell.isdigit() for cell in self.board.board)

    def get_computer_move(self):
        available_moves = [index + 1 for index, cell in enumerate(self.board.board) if cell.isdigit()]
        return random.choice(available_moves)

    def play_turn(self):
        player = self.players[self.current_player_index]
        clear_screen()
        self.board.display_board()
        print(f"{player.name}'s turn, with symbol ({player.symbol})")

        if self.vs_computer and player.name == "Computer":
            cell_choice = self.get_computer_move()
            self.board.update_board(cell_choice, player.symbol)
            print(f"Computer chose cell {cell_choice}")
            input("Press Enter to continue...")
            
        else:
            while True:
                try:
                    cell_choice = int(input("Choose a cell (1-9): "))
                    if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol): break
                    else: print("Invalid move!, try agine.")
                except ValueError as e:
                    print("Error, invalid input, ", e)

        self.switch_player()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def quit_game(self):
        clear_screen()
        print("\n\t\t\tTHANK YOU FOR PLAYING!\n", "==" * 40, "\n\t\t\t    X-O Game Ended!\n", "==" * 40, "\n\t\t\t  GOOD BYE GOFY BOY!")

game = Game()
game.start_game()