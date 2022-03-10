subtract_set = {1,2,3,4,5,6,7,8,9}
"""
sudoku = [
[9, 0, 0, 2, 5, 0, 0, 0, 3],
 [0, 4, 0, 9, 0, 0, 0, 7, 0],
 [0, 0, 0, 0, 3, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 1, 7],
 [6, 0, 8, 0, 0, 0, 9, 0, 5],
 [3, 2, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 7, 0, 0, 0, 0],
 [0, 7, 0, 0, 0, 1, 0, 9, 0],
 [5, 0, 0, 0, 6, 3, 0, 0, 1]
]
"""


def check_horizontal(i,j, sudoku):
    return subtract_set - set(sudoku[i])


def check_vertical(i, j, sudoku):
    ret_set = []
    for x in range(9):
        ret_set.append(sudoku[x][j])
    return subtract_set - set(ret_set)


def check_square(i, j, sudoku):
    first = [0,1,2]
    second = [3,4,5]
    third = [6,7,8]
    find_square = [first, second, third]
    for l in find_square:
        if i in l:
            row = l
        if j in l:
            col = l
    return_set = []
    for x in row:
        for y in col:
            return_set.append(sudoku[x][y])
    return subtract_set - set(return_set)


def get_poss_vals(i, j, sudoku):
    poss_vals = list(check_square(i, j, sudoku) \
                    .intersection(check_horizontal(i, j, sudoku)) \
                    .intersection(check_vertical(i, j, sudoku)))
    return poss_vals


def explicit_solver(sudoku):
    finished = False
    while not finished:
        print("starting new round")
        finished = True
        new_numbers = 0
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0:
                    poss_vals = get_poss_vals(i, j, sudoku)
                    #print(poss_vals)
                    if len(poss_vals) == 1:
                        sudoku[i][j] = list(poss_vals)[0]
                        new_numbers += 1
                    else:
                        #print("Using implicit solver")
                        if implicit_solver(i,j,sudoku):
                            new_numbers += 1
                        else:
                            finished = False
        if new_numbers == 0:
            print("Didn't find a solution.")
            break
        else:
            print("Found {} new numbers".format(new_numbers))
    return sudoku, finished


def implicit_solver(i, j, sudoku):
    poss_vals = get_poss_vals(i, j, sudoku)
    
    # Check row
    row_poss = []
    for y in range(9):
        if y == j:
            continue
        if sudoku[i][y] == 0:
            for val in get_poss_vals(i, y, sudoku):
                row_poss.append(val)
    if len(set(poss_vals)-set(row_poss)) == 1:
        sudoku[i][j] = list(set(poss_vals)-set(row_poss))[0]
        return True

    # Check column
    col_poss = []
    for x in range(9):
        if x == i:
            continue
        if sudoku[x][j] == 0:
            for val in get_poss_vals(x, j, sudoku):
                col_poss.append(val)
    if len(set(poss_vals)-set(col_poss)) == 1:
        sudoku[i][j] = list(set(poss_vals)-set(col_poss))[0]
        return True

    # Check square
    first = [0, 1, 2]
    second = [3, 4, 5]
    third = [6, 7, 8]
    find_square = [first, second, third]
    for l in find_square:
        if i in l:
            row = l
        if j in l:
            col = l
    square_poss = []
    for x in row:
        for y in col:
            if sudoku[x][y] == 0:
                for val in get_poss_vals(x, y, sudoku):
                    square_poss.append(val)
    if len(set(poss_vals)-set(square_poss)) == 1:
        sudoku[i][j] = list(set(poss_vals)-set(square_poss))[0]
        return True

    # If no new value was found
    return False


def main(sudoku):
    try:
        result, finished = explicit_solver(sudoku)
        print("Finished: {}".format(finished))
        for row in result:
            print(row)
    except Exception as e:
        print(e)
        print("Didn't finish :(")


#if __name__=="__main__":
#    main(sudoku)