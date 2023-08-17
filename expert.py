import pyautogui
from PIL import Image
import functions as f
import keyboard
from time import sleep

x_pos = [69, 97, 125, 153, 181, 209, 237, 265, 293, 321, 349, 377, 405, 433, 461, 489, 517, 545, 573, 601, 629, 657, 685, 713, 741, 769, 797, 825, 853, 881]
y_pos = [233, 261, 289, 317, 345, 373, 401, 429, 457, 485, 513, 541, 569, 597, 625, 653]

while True:
    f.leftClick(474, 174)
    f.leftClick(461, 429)

    end_game = False
    while True:
        no_more_moves = True
        flags = []
        bombs = []
        ones = []
        twos = []
        threes = []
        fours = []
        fives = []
        sixes = []
        sevens = []
        eights = []
        empties = []
        known = []
        img_gui = pyautogui.screenshot("field.png")
        img = Image.open('field.png').load()
        pyautogui.moveTo(1000, 500)

        field = f.scan_field(img, x_pos, y_pos, known, empties, ones, twos, threes, fours, fives, sixes, sevens, eights, flags)
        for row in field:
            if "S" in row:
                end_game = True

        if end_game:
            break

        for row in field:
            print(row)
        print("")
        print("")

        known_fields = known.copy()

        for C in known.copy():
            num_of_neighbors = 0
            if not C in flags and not C in empties:
                num_of_neighbors = int(f.type(C[0], C[1], known, ones, twos, threes, fours, fives, sixes, sevens, eights, empties, flags))
                n = f.flags(f.neighbors(C[0], x_pos, C[1], y_pos), num_of_neighbors, known, flags)

        for C in known.copy():
            num_of_neighbors = 0

            if not C in flags and not C in empties:
                num_of_neighbors = int(f.type(C[0], C[1], known, ones, twos, threes, fours, fives, sixes, sevens, eights, empties, flags))
                n = f.no_mines(f.neighbors(C[0], x_pos, C[1], y_pos), known, flags, num_of_neighbors)


        if known == known_fields:
            made_guess = f.advanced_logic(x_pos, y_pos, known, empties, flags, ones, twos, threes, fours, fives, sixes, sevens, eights)
            if not made_guess:
                guess = f.guess(x_pos, y_pos, known, empties, flags, ones, twos, threes, fours, fives, sixes, sevens, eights)
                f.leftClick(guess[0], guess[1])
            else:
                break
        if keyboard.is_pressed('q'):
            break

    f.leftClick(1000, 500)
    print("")
    print("The game ended!")
    sleep(3)