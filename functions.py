import win32api
import time
import win32con

unknown = (255, 255, 255)
empty = (189, 189, 189)
one = (0, 0, 255)
two = (0, 123, 0)
three = (255, 0, 0)
four = (0, 0, 123)
five = (123, 0, 0)
six = (0, 123, 123)
seven = (0, 0, 0)
eight = (123, 123, 123)

def leftClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def rightClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def append_to_list(type, x, y, known, flags, empties, ones, twos, threes, fours, fives, sixes, sevens, eights):
    if type == "1":
        ones.append((x, y))
        known.append((x, y))
    elif type == "2":
        twos.append((x, y))
        known.append((x, y))
    elif type == "3":
        threes.append((x, y))
        known.append((x, y))
    elif type == "4":
        fours.append((x, y))
        known.append((x, y))
    elif type == "5":
        fives.append((x, y))
        known.append((x, y))
    elif type == "6":
        sixes.append((x, y))
        known.append((x, y))
    elif type == "7":
        sevens.append((x, y))
        known.append((x, y))
    elif type == "8":
        eights.append((x, y))
        known.append((x, y))
    elif type == "!":
        flags.append((x, y))
        known.append((x, y))
    elif type == "0":
        empties.append((x, y))
        known.append((x, y))

def scan_field(img, x_pos, y_pos, known, empties, ones, twos, threes, fours, fives, sixes, sevens, eights, flags):
    field = [""] * len(y_pos)
    for iy, y in enumerate(y_pos):
        for x in x_pos:
            col = color(img, x, y)
            field[iy] += col
            append_to_list(col, x, y, known, flags, empties, ones, twos, threes, fours, fives, sixes, sevens, eights)
    return field

def color(img, x, y):
    col = img[x, y]
    col_2 = img[x, y+1]
    if img[x-10, y-8] == three:
        return "S"
    elif img[x-12, y-12] == unknown:
        if img[x-1, y+5][0] == 21:
            return "!"
        return "/"
    elif col[2] == 255:
        return "1"
    elif col_2 == two:
        return "2"
    elif col[0] == 189:
        return "0"
    elif col_2[0] == 255:
        return "3"
    elif img[x+2, y] == four:
        return "4"
    elif col_2 == five:
        return "5"
    elif col_2 == six:
        return "6"
    elif img[x, y+5] == seven:
        return "7"
    return "!"

def neighbors(x, x_pos, y, y_pos):
    n = []
    for X in range(0, 3):
        for Y in range(0, 3):
            if not X == Y == 1:
                x_ = (X-1)*28 + x
                y_ = (Y-1)*28 + y
                if x_ in x_pos and y_ in y_pos:
                    n.append((x_, y_))
    return n

def empty_neighbors_of_field(neighbors, known):
    empty_neighbors = []
    for n in neighbors:
        if not n in known:
            empty_neighbors.append(n)
    return empty_neighbors
    
def flags(neighbors, num_of_neighbors, known, flags):
    empty_n = empty_neighbors_of_field(neighbors, known)
    num_of_empties = 0

    for N in neighbors:
        if not N in known or N in flags:
            num_of_empties += 1
    if num_of_empties == num_of_neighbors:
        for C in empty_n:
            rightClick(C[0], C[1])
            known.append(C)
            flags.append(C)

def no_mines(neighbors, known, flags, num_of_neighbors):
    num_of_flags = 0
    for n in neighbors:
        if n in flags:
            num_of_flags += 1
    if num_of_flags == num_of_neighbors:
        empty_neighbors = empty_neighbors_of_field(neighbors, known)
        num_of_empty_neighbors = len(empty_neighbors)
        for n in neighbors:
            if not n in known:
                num_of_empty_neighbors += 1
                leftClick(n[0], n[1])
                known.append(n)
        return [empty_neighbors, True]
    return [[], False]

def type(x, y, known, ones, twos, threes, fours, fives, sixes, sevens, eights, empties, flags):
    pos = (x, y)
    T = "0"
    if not pos in known:
        T = "/"
    elif pos in empties:
        T = "0"
    elif pos in flags:
        T = "!"
    elif pos in ones:
        T = "1"
    elif pos in twos:
        T = "2"
    elif pos in threes:
        T = "3"
    elif pos in fours:
        T = "4"
    elif pos in fives:
        T = "5"
    elif pos in sixes:
        T = "6"
    elif pos in sevens:
        T = "7"
    elif pos in eights:
        T = "8"
    return T

def advanced_logic(x_pos, y_pos, known, empties, flags, ones, twos, threes, fours, fives, sixes, sevens, eights):
    made_guess = False
    for y in y_pos:
        if not made_guess:
            for x in x_pos:
                if not made_guess:
                    if (x, y) in known and not (x, y) in flags and not (x, y) in empties:
                        field_neighbors = neighbors(x, x_pos, y, y_pos)
                        num_of_used_flags = 0
                        empty_neighbors = []
                        known_neighbors = []
                        for n in field_neighbors:
                            if n in flags:
                                num_of_used_flags += 1
                            elif n in empties:
                                empty_neighbors.append(n)
                            else:
                                known_neighbors.append(n)
                        num_of_empty_neighbors = len(empty_neighbors)
                        num_of_flags = int(type(x, y, known, ones, twos, threes, fours, fives, sixes, sevens, eights, empties, flags))
                        num_of_needed_flags = num_of_flags - num_of_used_flags
                        if num_of_empty_neighbors > num_of_needed_flags:
                            for n in known_neighbors:
                                if not made_guess:
                                    neighbor_neighbors = neighbors(n[0], x_pos, n[1], y_pos)
                                    num_of_used_neighbor_flags = 0
                                    for N in neighbor_neighbors:
                                        if N in flags:
                                            num_of_used_neighbor_flags += 1
                                    try:
                                        num_of_neighbor_flags = int(type(n[0], n[1], known, ones, twos, threes, fours, fives, sixes, sevens, eights, empties, flags))
                                    except ValueError:
                                        num_of_neighbor_flags = 11
                                    num_of_needed_neighbor_flags = num_of_neighbor_flags - num_of_used_neighbor_flags
                                    empty_neighbors_of_neighbors = empty_neighbors_of_field(neighbor_neighbors, known)
                                    break_loop = False
                                    common_neighbors = []
                                    for N in field_neighbors:
                                        if not N in empty_neighbors_of_neighbors:
                                            break_loop = True
                                            break
                                        else:
                                            common_neighbors.append(N)
                                    new_neighbors = []
                                    for N in empty_neighbors_of_neighbors:
                                        if not N in common_neighbors:
                                            new_neighbors.append(N)
                                    if not break_loop:
                                        if len(new_neighbors) == num_of_needed_neighbor_flags:
                                            for N in new_neighbors:
                                                rightClick(N[0], N[1])
                                                made_guess = True
                                        elif num_of_needed_flags == num_of_needed_neighbor_flags:
                                            for N in new_neighbors:
                                                leftClick(N[0], N[1])
                                                made_guess = True
    return made_guess

def guess(x_pos, y_pos, known, empties, flags, ones, twos, threes, fours, fives, sixes, sevens, eights):
    probabilities = []
    for y in y_pos:
        for x in x_pos:
            if not (x, y) in known:
                n = neighbors(x, x_pos, y, y_pos)
                p = 0
                num_of_known_neighbors = 0
                for N in n:
                    if N in known and not N in flags:
                        num_of_known_neighbors += 1

                        n_n = neighbors(N[0], x_pos, N[1], y_pos)
                        num_of_used_flags = 0
                        num_of_empty_neighbors = 0
                        for C in n_n:
                            if C in flags:
                                num_of_used_flags += 1
                            elif C in empties:
                                num_of_empty_neighbors += 1
                        num_of_flags = int(type(N[0], N[1], known, ones, twos, threes, fours, fives, sixes, sevens, eights, empties, flags))
                        num_of_needed_flags = num_of_flags - num_of_used_flags
                        try:
                            p += num_of_needed_flags / num_of_empty_neighbors
                        except ZeroDivisionError:
                            pass

                try:
                    p /= num_of_known_neighbors
                except ZeroDivisionError:
                    p = 1
                probabilities.append(p)
            else:
                probabilities.append(1)

    min_index = probabilities.index(min(probabilities))
    x_index = min_index % 30
    y_index = int((min_index - x_index) / 30)
    coords = (x_pos[x_index], y_pos[y_index])
    print(coords, probabilities[min_index])
    return coords