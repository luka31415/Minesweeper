import pyautogui
from PIL import Image
import functions as f
import keyboard

x_pos = [76, 104, 132, 160, 188, 216, 244, 272, 300]
y_pos = [235, 263, 291, 319, 347, 375, 403, 431, 459]
end_game = False

f.leftClick(189, 177)
f.leftClick(188, 345)

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
            end_game = False

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
        print("Taking guess:")
        guess = f.guess(x_pos, y_pos, known, empties, flags, ones, twos, threes, fours, fives, sixes, sevens, eights)
        f.leftClick(guess[0], guess[1])
        if img[guess[0]-10, guess[1]-8][0:3] == (255, 0, 0):
            break
    if keyboard.is_pressed('q'):
        break
f.leftClick(1000, 500)
print("")
print("The game ended!")