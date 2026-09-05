import random
import os

# Clears the terminal screen for a cleaner game display.
# Time complexity: O(1)
def clear_screen(): os.system("cls" if os.name == "nt" else "clear")

class Player:
    # Initializes a player with empty name and symbol fields.
    # Time complexity: O(1)
    def __init__(self):
        self.name = ""
        self.symbol = ""

    # Prompts the user to enter a valid alphabetic name until it is accepted.
    # Time complexity: O(k), where k is the number of input attempts.
    def choose_name(self):
        while True:
            name = input("Enter your name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name. LETTERS ONLY!")

    # Prompts the user to choose a valid single-letter symbol.
    # Time complexity: O(k), where k is the number of input attempts.
    def choose_symbol(self):
        while True:
            symbol = input(f"\n{self.name}, choose your symbol (single letter): ")
            if symbol.isalpha() and len(symbol) == 1:
                self.symbol = symbol.upper()
                break
            print("Invalid symbol. SINGLE LETTER ONLY! or LETTER ONLY!")

    # Stores the player's symbol in uppercase form.
    # Time complexity: O(1)
    def set_symbol(self, symbol): self.symbol = symbol.upper()


class ComputerPlayer(Player):
    # Creates the computer player and assigns its default name.
    # Time complexity: O(1)
    def __init__(self):
        super().__init__()
        self.name = "Computer"

    # Ensures the computer keeps the fixed name "Computer".
    # Time complexity: O(1)
    def choose_name(self): self.name = "Computer"

    # Chooses a symbol different from the human player's symbol from the alphabet.
    # Time complexity: O(n), where n is the number of available letters.
    def choose_symbol(self, human_symbol):
        letters = [chr(code) for code in range(ord('A'), ord('Z') + 1)]
        available = [letter for letter in letters if letter != human_symbol.upper()]
        self.symbol = random.choice(available)


class Menu:
    # Displays the main menu and validates the user's selection.
    # Time complexity: O(k), where k is the number of invalid attempts.
    def dislpay_main_menu(self):
        print("==" * 40, "\n\t\t\tWelcome to X-O game!\n", "==" * 40, "\n1. Play 2 Players\n2. Play against Computer\n3. Quit Game\n", "--" * 40)
        while True:
            try:
                choice = int(input("\nEnter your choice: "))
                if choice in {1, 2, 3}: return choice
                print("Enter a valid number!")
            except ValueError as e:
                print(f"\nError, not a valid input: {e}")
            except EOFError as e:
                print("\nInput closed. Exiting game.")
                raise SystemExit from e

    # Displays the end-of-game menu and validates the next action.
    # Time complexity: O(k), where k is the number of invalid attempts.
    def display_end_game_menu(self):
        while True:
            try:
                
                print("++" * 30)
                print("\t\t\tGame Over!")
                print("1. Restart Game")
                print("2. Quit Game")
                print("++" * 30)
                choice = int(input("Enter your choice: "))

                if choice in {1, 2}: return choice
                print("Enter a valid input!")
                
            except ValueError as e: print(f"\nError, not a valid input: {e}")
            except EOFError as e:
                print("\nInput closed. Exiting game.")
                raise SystemExit from e


class Board:
    # Creates a fresh 9-cell board numbered from 1 to 9.
    # Time complexity: O(n), where n is the board size.
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    # Prints the board in a 3x3 layout.
    # Time complexity: O(n), where n is the number of board cells.
    def display_board(self):
        for i in range(0, len(self.board), 3):
            print("|".join(self.board[i:i+3]))
            if i < 6: print("-" * 5)

    # Places a symbol on the board if the selected cell is valid.
    # Time complexity: O(1)
    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    # Checks whether a chosen cell is in range and still empty.
    # Time complexity: O(1)
    def is_valid_move(self, choice): return False if 1 <= choice <= 9 else self.board[choice - 1].isdigit()

    # Resets the board back to its default numbered state.
    # Time complexity: O(n), where n is the board size.
    def reset_board(self): self.board = [str(i) for i in range(1, 10)]

class Game:
    # Initializes the game state, players, board, and menu references.
    # Time complexity: O(1)
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = random.randint(0, 1)
        self.vs_computer = False

    # Starts the overall game flow by showing the menu and choosing the mode.
    # Time complexity: O(1)
    def start_game(self):
        choice = self.menu.dislpay_main_menu()

        if choice in (1, 2): self.start_game_mode(choice)
        elif choice == 3: self.quit_game()
        else: print("Enter a valid number!")

    # Starts the selected game mode and configures players.
    # Time complexity: O(1)
    def start_game_mode(self, choice):
        self.vs_computer = choice == 2
        self.setup_players()
        self.play_game()

    # Sets up the players for either two-human or human-vs-computer mode.
    # Time complexity: O(p), where p is the number of players.
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

    # Runs the main game loop until a win or draw ends the match.
    # Time complexity: O(m), where m is the number of turns played.
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

    # Restarts the board and begins a new round with a random starting player.
    # Time complexity: O(n), where n is the board size.
    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = random.randint(0, 1)
        self.play_game()

    # Checks all possible winning combinations to see if a player has won.
    # Time complexity: O(1), because there are always 8 winning patterns.
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

    # Checks whether every cell has been filled and no moves remain.
    # Time complexity: O(n), where n is the number of cells.
    def check_draw(self): return all(not cell.isdigit() for cell in self.board.board)

    # Picks a random valid move for the computer player.
    # Time complexity: O(n), where n is the number of empty cells.
    def get_computer_move(self):
        available_moves = [index + 1 for index, cell in enumerate(self.board.board) if cell.isdigit()]
        return random.choice(available_moves)

    # Executes one full turn for the current player and switches turns afterward.
    # Time complexity: O(k), where k is the number of invalid moves attempted.
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
                        
                except ValueError as e: print("Error, invalid input, ", e)
                except EOFError as e:
                    print("\nInput closed. Exiting game.")
                    raise SystemExit from e

        self.switch_player()

    # Switches the game turn from the current player to the other player.
    # Time complexity: O(1)
    def switch_player(self): self.current_player_index = 1 - self.current_player_index

    # Displays the final farewell message and ends the game session.
    # Time complexity: O(1)
    def quit_game(self):
        clear_screen()
        print("\n\t\t\tTHANK YOU FOR PLAYING!\n", "==" * 40, "\n\t\t\t    X-O Game Ended!\n", "==" * 40, "\n\t\t\t  GOOD BYE GOFY BOY!")

if __name__ == "__main__":
    game = Game()
    game.start_game()
