import random


HIT_CHAR = 'x'
MISS_CHAR = 'o'
BLANK_CHAR = '.'
HORIZONTAL = 'h'
VERTICAL = 'v'
MAX_MISSES = 20
SHIP_SIZES = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}
NUM_ROWS = 10
NUM_COLS = 10
ROW_IDX = 0
COL_IDX = 1
MIN_ROW_LABEL = 'A'
MAX_ROW_LABEL = 'J'


def get_random_position():

    row_choice = chr(
                    random.choice(
                        range(
                            ord(MIN_ROW_LABEL),
                            ord(MIN_ROW_LABEL) + NUM_ROWS
                        )
                    )
    )

    col_choice = random.randint(0, NUM_COLS - 1)

    return (row_choice, col_choice)


def play_battleship():
   

    print("Let's Play Battleship!\n")

    game_over = False

    while not game_over:

        game = Game()
        game.display_board()

        while not game.is_complete():
            pos = game.get_guess()
            result = game.check_guess(pos)
            game.update_game(result, pos)
            game.display_board()

        game_over = end_program()

    print("Goodbye.")

### DO NOT EDIT ABOVE (with the exception of MAX_MISSES) ###


class Ship:
    def __init__(self, name, start_position, orientation):
        
        self.name = name
        self.start_position = start_position
        self.orientation = orientation
        self.sunk = False
        if orientation == VERTICAL:
            vertical_dict = {start_position: False}
            for ascii_number in range(ord(start_position[ROW_IDX]), ord(start_position[ROW_IDX]) + SHIP_SIZES[name]):
                vertical_dict[(chr(ascii_number), start_position[COL_IDX])] = False
            self.positions = vertical_dict
        elif orientation == HORIZONTAL:
            horizontal_dict = {start_position: False}
            for row_number in range(start_position[COL_IDX], (start_position[COL_IDX] + SHIP_SIZES[name])):
                horizontal_dict[(start_position[ROW_IDX], row_number)] = False
            self.positions = horizontal_dict


class Game:

    def __init__(self, max_misses = MAX_MISSES):
        
        self.max_misses = max_misses
        self.ships = []
        self.guesses = []
        self.board = {}
        self.initialize_board()
        Game.create_and_place_ships(self)

    def initialize_board(self):
        
        for letter in range(ord(MIN_ROW_LABEL), ord(MAX_ROW_LABEL) + 1):
            temporary_list = ['.'] * NUM_ROWS
            self.board[chr(letter)] = temporary_list


    ########## DO NOT EDIT #########

    _ship_types = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]


    def display_board(self):
        

        print()
        print("  " + ' '.join('{}'.format(i) for i in range(len(self.board))))
        for row_label in self.board.keys():
            print('{} '.format(row_label) + ' '.join(self.board[row_label]))
        print()

    ########## DO NOT EDIT #########

    def in_bounds(self, start_position, ship_size, orientation):
        
        if orientation == VERTICAL:
            if (ord(start_position[ROW_IDX]) + ship_size) in range(ord(MIN_ROW_LABEL), ord(MAX_ROW_LABEL) + 1):
                return True
            else:
                return False
        elif orientation == HORIZONTAL:
            if (start_position[COL_IDX] + ship_size) in range(NUM_COLS):
                return True
            else:
                return False

    def overlaps_ship(self, start_position, ship_size, orientation):
        
        coordinates = []
        if orientation == HORIZONTAL:
            for column in range(start_position[COL_IDX], start_position[COL_IDX] + ship_size):
                coordinates.append((start_position[ROW_IDX], column))
        elif orientation == VERTICAL:
            for row in range(ord(start_position[ROW_IDX]), ord(start_position[ROW_IDX]) + ship_size):
                coordinates.append((chr(row), start_position[COL_IDX]))
        for existing_ship in self.ships:
            for existing_ship_position in existing_ship.positions.keys():
                if existing_ship_position in coordinates:
                    return True
        return False

    def place_ship(self, start_position, ship_size):
       
        orientation = HORIZONTAL
        if Game.in_bounds(self, start_position, ship_size, orientation) and not Game.overlaps_ship(self, start_position, ship_size, orientation):
            return 'h'
        orientation = VERTICAL
        if Game.in_bounds(self, start_position, ship_size, orientation) and not Game.overlaps_ship(self, start_position, ship_size, orientation):
            return 'v'
        else:
            return None

    def create_and_place_ships(self):
        
        for various_ships in Game._ship_types:
            random_position = get_random_position()
            ship_to_add = Game.place_ship(self, random_position, SHIP_SIZES.get(various_ships))
            while ship_to_add == None:
                random_position = get_random_position()
                ship_to_add = Game.place_ship(self, random_position, SHIP_SIZES.get(various_ships))
            ship_object = Ship(various_ships, random_position, ship_to_add)
            self.ships.append(ship_object)

    def get_guess(self):
        
        row_input = None
        while row_input not in range(ord(MIN_ROW_LABEL), ord(MAX_ROW_LABEL) + 1):
            row_input = input("Enter a row: ")
            if row_input.isalpha():
                row_input = ord(row_input)
        col_input = None
        while col_input not in range(NUM_COLS):
            col_input = input("Enter a column: ")
            if col_input.isalnum():
                col_input = int(col_input)
        return (chr(row_input), col_input)

    def check_guess(self, position):
        
        for existing_ship in self.ships:
            for existing_ship_positions in existing_ship.positions.keys():
                if position == existing_ship_positions:
                    if not existing_ship.positions[position]:
                        existing_ship.positions[position] = True
                    if not False in existing_ship.positions.values():
                        print("You sunk the {}!".format(existing_ship.name))
                        existing_ship.sunk = True
                    return True
                if not position in existing_ship.positions.keys() or existing_ship.positions[position]:
                    return False

    def update_game(self, guess_status, position):
        
        if guess_status:
            board_list = self.board[position[ROW_IDX]]
            if board_list[position[COL_IDX]] == '.':
                board_list[position[COL_IDX]] = 'x'
                self.board[position[ROW_IDX]] = board_list
            pass
        elif not guess_status:
            board_list = self.board[position[ROW_IDX]]
            if board_list[position[COL_IDX]] == '.':
                board_list[position[COL_IDX]] = 'o'
                self.board[position[ROW_IDX]] = board_list
            self.guesses.append(position)

    def is_complete(self):
       
        if len(self.guesses) == MAX_MISSES:
            print("SORRY! NO GUESSES LEFT.")
            return True
        for sample_ships in self.ships:
            if sample_ships.sunk == False:
                return False
        print("YOU WIN!")
        return True



def end_program():
    
    user_input = None
    while user_input != 'Y' or user_input != 'y' or user_input != 'N' or user_input != 'n':
        user_input = input("Play again (Y/N)? ")
        if user_input == 'Y' or user_input == 'y':
            return False
        if user_input == "N" or user_input == 'n':
            return True

def main():
    

    play_battleship()




main()
