from tkinter import *
import sudoku as s1
import sudoku_v2 as s2
import math
import time
import json


class Sudoku:
    def saveButton(self):
        self.sudokuSave = []
        for _val in self.items[2]:
            val = _val[0].get()
            self.sudokuSave.append(val)

        with open('tests.json', 'r') as f:
            dic = json.load(f)

        dic['save'] = self.sudokuSave
        with open('tests.json', 'w') as f:
            json.dump(dic, f)

    def reset(self):
        for _target in self.items[2]:
            target = _target[0]

            target.delete(0, END)
            target.configure(fg='#FFFFFF')



    def load(self, name):
        with open('tests.json', 'r') as f:
            dic = json.load(f)
        
        for _target, val in zip(self.items[2], dic[name]):
            target = _target[0]

            target.delete(0, END)
            target.insert(0, f"{val}")
            target.configure(fg='#FFFFFF')

    def setAL(self, n):
        self.al = n

    def message(self, n):
        if n == 0:
            self.messageText.set("Welcome to Sudoku Solver!")
        if n == 1:
            self.messageText.set("Invalid enter for the sudoku!")
        if n == 2:
            self.messageText.set("Calculating...")
        if n == 3:
            self.messageText.set(
                f"Found in {round(time.time() - self.start_time, 5)} seconds!\nUsed Al_1...")
        if n == 3.5:
            self.messageText.set(
                f"Found in {round(time.time() - self.start_time, 5)} seconds!\nUsed Al_2...")
        if n == 4:
            self.messageText.set("Can not find an answer!")
        if n == 5:
            self.messageText.set("One number is used twice!")

    def show_solution(self, grid):
        answer = [n for row in grid for n in row]
        count = 0

        for _cell in self.items[2]:
            cell = _cell[0]
            val = cell.get()

            if val == "":
                cell.delete(0, END)
                cell.insert(0, answer[count])
                cell.configure(fg='#6F6F6F')

            else:
                pass

            count += 1

    def checkSafe(self, grid):
        # find number
        N = self.n**2
        for row in range(N):
            for column in range(N):
                if grid[row][column] != 0:
                    number = grid[row][column]

                    # Check if we find the same num
                    # in the similar row , we
                    # return false
                    for x in range(N):
                        if x == column:
                            continue
                        if grid[row][x] == number:
                            return (False, [row, column], [row, x])

                    # Check if we find the same num in
                    # the similar column , we
                    # return false
                    for x in range(N):
                        if x == row:
                            continue
                        if grid[x][column] == number:
                            return (False, [row, column], [x, column])

                    # Check if we find the same num in
                    # the particular 3*3 matrix,
                    # we return false
                    cache = int(math.sqrt(N))

                    startRow = row - row % cache
                    startCol = column - column % cache
                    for i in range(cache):
                        for j in range(cache):
                            if i + startRow == row and j + startCol == column:
                                continue
                            if grid[i + startRow][j + startCol] == number:
                                return (False, [row, column], [i + startRow, j + startCol])

        return (True,)

    def crack(self):
        safe = True
        total_change = 0
        self.sudoku = []
        for i in range(self.n**2):
            self.sudoku.append([])

        count = 0
        for _cell in self.items[2]:
            cell = _cell[0]
            val = cell.get()
            try:
                val = int(val)
                if 0 < val <= self.n**2:
                    self.sudoku[count // self.n**2].append(val)
                    cell.configure(fg='#FFFFFF')
                    total_change += 1
                else:
                    cell.configure(fg='#E40000')
                    safe = False

            except:
                if val == "":
                    self.sudoku[count // self.n**2].append(0)
                    total_change += 1
                else:
                    cell.configure(fg='#E40000')
                    safe = False
            count += 1

        if total_change == 0:
            safe = False

        if safe:
            grid = self.sudoku.copy()

            safe_2 = self.checkSafe(grid)
            if safe_2[0]:
                self.message(2)
                self.start_time = time.time()
                if self.al == 1:
                    if(s1.solveSudoku(grid, 0, 0, self.n**2)):
                        self.message(3)
                        self.show_solution(grid)

                    else:
                        self.message(4)
                else:
                    answer = s2.solveSudoku(grid, self.n**2)
                    if answer:
                        print(grid)
                        self.message(3.5)
                        self.show_solution(grid)

                    else:
                        self.message(4)

            else:
                r, c = safe_2[1]
                cell = self.items[2][r*(self.n**2) + c][0]
                cell.configure(fg='#E40000')

                r, c = safe_2[2]
                cell = self.items[2][r*(self.n**2) + c][0]
                cell.configure(fg='#E40000')

                self.message(5)

        else:
            self.message(1)

    def gen_items(self):
        f = ('Times', 105-self.n*22)
        self.items[2] = []
        self.items[3] = []
        for rows in self.cells:
            for columns in rows:
                item = Entry(window, width=2, font=f)
                self.items[2].append([item, [columns[1][0], columns[1][1]]])

        for line in self.lines[0]:  # column
            item = Label(window, text="|", font=f)
            self.items[3].append([item, [line[0], line[1]]])

        for line in self.lines[1]:  # row
            item = Label(window, text="-", font=f)
            self.items[3].append([item, [line[0], line[1]]])

        for item in self.items[2]:
            show_me(item)

        for item in self.items[3]:
            show_me(item)

    def gen_scale(self):
        item = self.items[0][1][0]
        n = int(item.get())
        if 1 < n < 6:
            self.n = n

            cells = []
            lines_column = []
            lines_row = []
            r = self.row_start
            count_row = 0
            for i in range(n**2):  # row
                c = self.column_start
                cache = []
                count_column = 0
                for _i in range(n**2):  # column
                    count_column += 1
                    cache.append([0, (r, c)])
                    if count_column % n == 0:
                        lines_column.append([r, c+1])
                    c += 2

                cells.append(cache)
                count_row += 1
                if count_row % n == 0:
                    lines_row.append([r+1, self.column_start])
                r += 2

            self.cells = cells
            self.lines = (lines_column, lines_row)

            self.gen_items()
            self.message(0)
            show_main()

        else:
            item.delete(0, END)
            item.insert(0, "Invalid Number! (Limit is 5)")

    def __init__(self, items) -> None:
        self.row_start = 5
        self.column_start = 4
        self.items = items

        self.al = 1

        self.messageText = StringVar()

        item = Label(window, textvariable=self.messageText, font=('Verdana', 18))
        self.items[1].append([item, [4, 0]])


# function Setup
def hide_me(item):
    item[0].grid_forget()


def show_me(item):
    item[0].grid(row=item[1][0], column=item[1][1])


def hide_main():
    for item in sudoku.items[0]:
        show_me(item)

    for item in sudoku.items[1]:
        hide_me(item)

    for item in sudoku.items[2]:
        hide_me(item)

    for item in sudoku.items[3]:
        hide_me(item)


def show_main():
    for item in sudoku.items[0]:
        hide_me(item)

    for item in sudoku.items[1]:
        show_me(item)


large_font = ('Verdana', 20)

# Window Setup
window = Tk()
window.geometry("1680x1080")
window.title("Sudoku Solver")
icon = PhotoImage(file='icon.png')
window.iconphoto(True, icon)

# Inputs
scale_input = Entry(window, width=30, font=large_font)
scale_input.insert(0, "3")


# Buttons
scaleButton = Button(window, text="Generate", command=lambda: Sudoku.gen_scale(
    sudoku), width=14, height=1, font=large_font)
backButton = Button(window, text="Back", command=hide_main,
                    width=7, height=1, font=large_font)
resetButton = Button(window, text="Reset", command=lambda: Sudoku.reset(
    sudoku), width=7, height=1, font=large_font)
startButton = Button(window, text="Crack", command=lambda: Sudoku.crack(
    sudoku), width=7, height=1, font=large_font)

saveButton = Button(window, text="Save", command=lambda: Sudoku.saveButton(
    sudoku), width=7, height=1, font=large_font)
loadButton = Button(window, text="Load", command=lambda: Sudoku.load(
    sudoku, 'save'), width=7, height=1, font=large_font)

test1Button = Button(window, text="Test1", command=lambda: Sudoku.load(
    sudoku, 'test1'), width=7, height=1, font=large_font)
test2Button = Button(window, text="Test2", command=lambda: Sudoku.load(
    sudoku, 'test2'), width=7, height=1, font=large_font)

al1Button = Button(window, text="Al_1", command=lambda: Sudoku.setAL(
    sudoku, 1), width=7, height=1, font=large_font)
al2Button = Button(window, text="Al_2", command=lambda: Sudoku.setAL(
    sudoku, 2), width=7, height=1, font=large_font)



#     ===START===
items = {
    0: [],
    1: [],
    2: [],
    3: []
}


items[0].append([scaleButton, [1, 0]])
items[0].append([scale_input, [1, 1]])


items[1].append([backButton, [1, 0]])
items[1].append([resetButton, [2, 0]])

items[1].append([saveButton, [1, 1]])
items[1].append([loadButton, [2, 1]])

items[1].append([test1Button, [1, 2]])
items[1].append([test2Button, [2, 2]])

items[1].append([startButton, [3, 0]])
items[1].append([al1Button, [3, 1]])
items[1].append([al2Button, [3, 2]])


sudoku = Sudoku(items)


hide_main()

window.resizable(width=True, height=True)
window.mainloop()
