import math
import pickle
import pandas as pd
from itertools import combinations
import sudoku_v2_addon as s

# A utility function to print grid
def add_dot(target, N):
    def sorter(i):
        if isinstance(i, int):
            return i
        else:
            return 9999999
    for i in range(N-len(target)):
        target.append('.')
    target.sort(key=sorter)


def printing(arr, N):
    for i in range(N):
        for j in range(N):
            print(arr[i][j], end=" ")
        print()

def convert_pandas(grid, N, change=True):
    data = {i: grid[i] for i in range(N)}

    if change:
        return pd.DataFrame(data).transpose()
    else:
        return pd.DataFrame(data)

def get(lis: pd.DataFrame, cor, x: int, N: int):
    r = cor[0]
    c = cor[1]

    if x == 0: #return row
        return lis[c].copy()
    if x == 1: #return col
        return lis.iloc[r].copy()
    if x == 2: #return square
        y = int(math.sqrt(N))
        c_square = c - c % y
        r_square = r - r % y

        cache = []
        for i in range(y):
            for j in range(y):
                cache.append(lis[i+c_square][j+r_square])
        return cache

def get_cell_set(sudoku, N, cor=(0, 0)):
    if sudoku[cor[1]][cor[0]] != 0:
        cache = [sudoku[cor[1]][cor[0]],]
        add_dot(cache, N)
        return cache

    cache = []
    cache.extend(get(sudoku, cor, 0, N))
    cache.extend(get(sudoku, cor, 1, N))
    cache.extend(get(sudoku, cor, 2, N))

    source = list(range(1, N+1))
    lis = [item for item in source if item not in cache]
    lis.sort()

    add_dot(lis, N)
    return lis

def get_preemptive_sets(sudoku, N):
    cache_col = []
    for r in range(N):
        cache = []
        for c in range(N): 
            cache.append(get_cell_set(sudoku, N, (r, c)))
        cache_col.append(cache)
    
    return convert_pandas(cache_col, N)

def change_list(target: pd.DataFrame, source, cor, x: int, N: int):
    if source == False:
        return False

    r = cor[0]
    c = cor[1]
    data_test = {0: source}
    data_test = pd.DataFrame(data_test)
    
    if x == 0: #return row
        check = target[c] == data_test[0]
        check = [item for item in check]
        if False in check:
            target[c] = source
            return True
        else:
            return False

    if x == 1: #return col
        check = target.iloc[r] == data_test[0]
        check = [item for item in check]
        if False in check:
            target.iloc[r] = source
            return True
        else:
            return False

    if x == 2: #return square
        y = int(math.sqrt(N))
        c_square = c - c % y
        r_square = r - r % y

        count = 0
        for i in range(y):
            for j in range(y):
                if target[i+c_square][j+r_square] == data_test[0][i*y+j]:
                    count += 1
                else:
                    target[i+c_square][j+r_square] = source[i*y+j]
        
        if count == 9:
            return False
        else:
            return True
    
    print("ERROR CHECK CHANGE_LIST")
    return False

def generate_p_set(N):
    l = list(range(1, N+1))
    # initializing empty list
    comb = []
     
    #Iterating till length of list
    for i in range(len(l)+1):
        # Generating sub list
        comb += [list(j) for j in combinations(l, i)]
    # Returning list
    return comb
 
def change_p_set(p_set, length, N, p_set_len):
    p_set = pickle.dumps(p_set)
    p_set = pickle.loads(p_set)
    
    #remove dots
    for j in p_set:
        j[:] = (item for item in j if item != '.')
    # a list of sets that has the wanted length
    #p_set_len = [item for item in p_set if len(item) == length]

    #Checks if it has a Preemptive Set
    for p in p_set_len:
        count = 0
        for check in p_set:
            if set(check).issubset(set(p)):
                count += 1
            if count > length:
                break
        
        if count > length:
            continue

        elif count == length:
            #if it has a preemptive set, removes other values from the cells.
            cache = []
            for s in p_set:
                if set(s.copy()).issubset(set(p.copy())) == False:
                    x = [item for item in s if item not in p]
                    cache.append(x)
                else:
                    cache.append(s.copy())
            
            if list(p_set) == cache:
                return False

            for i in cache:
                add_dot(i, N)
        
            return cache

    return False


def scan(sudoku_p_set: pd.DataFrame, N, all_sets):
    #copying set
    set_copy = pickle.dumps(sudoku_p_set)
    set_copy = pickle.loads(set_copy)
    
    check_point = False

    for length in range(2, N+1):
        check_set = [item for item in all_sets if len(item) == length]
        #checking rows
        for i in range(N):
            #p_set = get(set_copy, (0, 6), 2, N) #for testing
            p_set = get(set_copy, (0, i), 0, N)
            p_set_2 = change_p_set(p_set, length, N, check_set)#this checks and gets the set that needs to be changed
            if change_list(sudoku_p_set, p_set_2, (0, i), 0, N):
                #print(f'Change in row: {0, i}')
                check_point = True
            else:
                pass
        
        #checking columns
        for i in range(N):
            p_set = get(set_copy, (i, 0), 1, N)
            p_set_2 = change_p_set(p_set, length, N, check_set)

            if change_list(sudoku_p_set, p_set_2, (i, 0), 1, N):
                #print(f'Change in column: {i, 0}')
                check_point = True
            else:
                pass
        
        #checking squares
        x = int(math.sqrt(N))
        for i in range(x):
            for j in range(x):
                p_set = get(set_copy, (i*3, j*3), 2, N)
                p_set_2 = change_p_set(p_set, length, N, check_set)

                if change_list(sudoku_p_set, p_set_2, (i*3, j*3), 2, N):
                    #print(f'Change in a square: {i*3, j*3}')
                    check_point = True
                else:
                    pass

        #not sure to enable it or not!
        if check_point:
            return False

    return True
    

def renew_sudoku(sudoku, sudoku_p_set, N):
    for c in range(N):
        for r in range(N):
            #sudoku_p_set.to_excel('test.xlsx')
            if sudoku_p_set[c][r][0] != '.' and sudoku_p_set[c][r][1] == '.':
                #print(sudoku_p_set[c][r][:2])
                sudoku[c][r] = sudoku_p_set[c][r][0]
        

def renew_sudoku_p_set(sudoku_p_set, sudoku, N):
    for r in range(N):
        for c in range(N): 
            x = get_cell_set(sudoku, N, (r, c))
            cache_1 = [item for item in sudoku_p_set[c][r] if item != '.']
            cache_2 = [item for item in x if item != '.']
            cache_3 = [item for item in cache_1 if item in cache_2]
            add_dot(cache_3, N)

            sudoku_p_set[c][r] = cache_3

def convert_to_grid(grid, sudoku, N):
    s_cache = sudoku.transpose()
    cache = []
    
    for i in range(N):
        cache.append(list(s_cache[i]))
    grid.clear()
    grid.extend(cache)

def solveSudoku(grid, N):
    all_sets = generate_p_set(N)

    _ = [0] * N
    key1 = [[_]* N]
    key1 = convert_pandas(key1[0], N)

    _ = [False] * N
    key2 = [[_]* N]
    key2 = convert_pandas(key2[0], N)

    sudoku = convert_pandas(grid, N)
    sudoku_p_set = get_preemptive_sets(sudoku, N)
    #sudoku_p_set.to_excel('test1.xlsx')

    count = 0
    safe = True
    for i in range(100):
        if scan(sudoku_p_set, N, all_sets):
            if (sudoku == key1).equals(key2) and count >= 1:
                count = 0
                print("done")
                break
            elif count >= 6:
                safe = False
                print("requires chance")
                break
            count += 1
        else:
            count = 0

        renew_sudoku(sudoku, sudoku_p_set, N)
        renew_sudoku_p_set(sudoku_p_set, sudoku, N)

    if safe:
        convert_to_grid(grid, sudoku, N)
        if __name__ != "__main__":
            return grid
    else:
        convert_to_grid(grid, sudoku, N)

        lis_sudoku_p_set = []
        convert_to_grid(lis_sudoku_p_set, sudoku_p_set, N)
        lis_sudoku_p_set = [[[i for i in item if i != '.'] for item in col] for col in lis_sudoku_p_set] # I hate this
        
        s.solveSudoku(grid, 0, 0, N, lis_sudoku_p_set)
        if __name__ != "__main__":
            return grid
    #sudoku_p_set.to_excel('final.xlsx')


# Driver Code
# 0 means unassigned cells

grid = [[0, 3, 9, 5, 0, 0, 0, 0, 0],
        [0, 0, 1, 8, 0, 9, 0, 7, 0],
        [0, 0, 0, 0, 1, 0, 9, 0, 4],
        [1, 0, 0, 4, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 8, 6, 0],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 1, 0, 0, 9, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 1, 0, 0, 8]]


# N is the size of the 2D matrix N*N


if __name__ == "__main__":
    N = 9
    solveSudoku(grid, N)
    for i in grid: 
        print(i)


# saving the excel
#sudoku_p_set.to_excel(file_name)

#import the excel
#sudoku = pd.read_excel("save.xlsx")

# Check https://www.ams.org/notices/200904/tx090400460p.pdf