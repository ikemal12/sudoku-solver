import numpy as np 

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    # make sure the starting state of the board is valid first before starting to solve it
    if not check_valid_board(sudoku):
        return np.full((9, 9), -1)
        
    # find the solution if one exists
    if solve_sudoku(sudoku):
        return sudoku
    else:
        return np.full((9, 9), -1)
    
def solve_sudoku(grid):
    '''Solves given sudoku recursively using a backtracking algorithm'''
    remaining_options = precompute_remaining_options(grid)
    row, col = find_empty_cell(grid, remaining_options)

    # if no empty cell is found, the sudoku is solved
    if row == -1 and col == -1:  
        return True

    # sort by the number of remaining options, least remaining options first
    sorted_options = sorted(
        ((i, j, remaining_options[i][j]) for i in range(9) for j in range(9) if grid[i][j] == 0),
        key=lambda x: x[2]  
    )

    for i, j, _ in sorted_options:
        for num in range(1, 10):
            if is_valid(grid, i, j, num):
                grid[i][j] = num
                
                update_options(grid, remaining_options, i, j, num)  # update remaining options
                
                if solve_sudoku(grid):
                    return True
                
                # backtrack if solution not found
                grid[i][j] = 0 
                # revert options on backtrack
                update_options(grid, remaining_options, i, j, 0)  
                
        return False  # if no valid number is found, backtrack immediately

    return False

def is_valid(grid, row, col, num):
    '''Enforces constraints when placing a given value in a cell'''
    # check row and column
    if num in grid[row] or num in [grid[i][col] for i in range(9)]:
        return False

    # check subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False

    return True

def check_valid_board(grid):
    '''Checks the starting state of a given sudoku is valid'''
    # check rows and columns for numbers that appear more than once
    for val in range(9):
        if not check_used_numbers(grid[val][:]) or not check_used_numbers(grid[:][val]):
            return False
        
    # check subgrids for numbers that appear more than once
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid = grid[i:i+3, j:j+3]
            if not check_used_numbers(subgrid.flatten()):
                return False
            
    return True
    
def check_used_numbers(line):
    '''Check for duplicate values in a given row or column'''
    line = [val for val in line if val != 0] # filter out the 0s
    return len(line) == len(set(line)) 

def precompute_remaining_options(grid):
    '''Precalculates the number of remaining options for each empty cell'''
    remaining_options = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        # store row values to avoid repeated set creation
        row_vals = set(grid[i]) 
        for j in range(9):
            if grid[i][j] == 0:
                # store column values
                col_vals = {grid[row][j] for row in range(9)} 
                
                # store subgrid values
                subgrid_vals = {
                    grid[i // 3 * 3 + r][j // 3 * 3 + c]
                    for r in range(3)
                    for c in range(3)
                }  
                
                count = sum(
                    1 for num in range(1, 10)
                    if num not in row_vals and num not in col_vals and num not in subgrid_vals
                )
                remaining_options[i][j] = count

    return remaining_options

def find_empty_cell(grid, remaining_options):
    '''Finds the next empty cell to be filled in'''
    min_options = float('inf')
    cell = (-1, -1)

    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0 and remaining_options[i][j] < min_options:
                min_options = remaining_options[i][j]
                cell = (i, j)
                
                # if only one option remains, return immediately
                if min_options == 1:  
                    return cell
    
    return cell

def update_options(grid, remaining_options, row, col, num, increment=True):
    '''Updates the number of remaining options for cells in the grid after placing a number'''
    increment_value = 1 if increment else -1

    # update options in the row and column
    for i in range(9):
        if grid[row][i] == 0:
            remaining_options[row][i] += increment_value

        if grid[i][col] == 0:
            remaining_options[i][col] += increment_value

    # update options in the subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == 0:
                remaining_options[i][j] += increment_value
