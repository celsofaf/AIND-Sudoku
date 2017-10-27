assignments = []

# since we have a DIAGONAL sudoku, I just need to add two units to our setting: the diagonals
  
rows = 'ABCDEFGHI'
cols = '123456789'
def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i]+cols[i] for i in range(len(rows))],
              [rows[i]+cols[len(cols)-i-1] for i in range(len(rows))]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    double_boxes = [box for box in values if len(values[box]) == 2]  # boxes with 2 digits
    if len(double_boxes) == 0:  # no possible candidates
        return values

    sudoku = values.copy()

    for box in double_boxes:
        for unit in units[box]:
            candidates = [candbox for candbox in unit if sudoku[candbox] == sudoku[box]]
            if len(candidates) > 1:  # found naked twins
                for candbox in set(unit) - set(candidates):
                    if len(sudoku[candbox]) >= 2:
                        digits = list(sudoku[box])
                        old_value = sudoku[candbox]
                        new_value = sudoku[candbox].replace(digits[0], '').replace(digits[1],'')
                        if new_value != old_value:
                            sudoku = assign_value(sudoku, candbox, new_value)
    return sudoku
                

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81
    all_numbers = '123456789'
    sudoku = dict(zip(boxes, grid))
    for box in sudoku:
        if sudoku[box] == '.':
            sudoku[box] = all_numbers
        else:
            sudoku[box] = str(sudoku[box])  # makes sure a single digit is a string
    
    return sudoku

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    sudoku = values.copy()
    
    solved_boxes = [box for box in values if len(values[box]) == 1]
    for box in solved_boxes:
        if len(values[box]) == 1:
            digit = values[box]
            for peer in peers[box]:
                sudoku = assign_value(sudoku, peer, sudoku[peer].replace(digit, ''))  ## if digit not there, does nothing
                #sudoku[peer] = sudoku[peer].replace(digit, '')  ## if digit not there, does nothing
    
    return sudoku

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
                #values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False   # Failed earlier!
    if all(len(values[s]) == 1 for s in boxes): 
        return values  # Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    
    # possibilities is list containing the number of current possibilities for each unsolved
    # box, sorted by the number of possibilities ;-)
    possibilities = dict([[box, len(values[box])] for box in values if len(values[box]) > 1])
    possibilities = sorted(possibilities.items(), key=lambda x:x[1])
    choice = possibilities[0][0]  # chosen box
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[choice]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, choice, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    game = grid_values(grid)
    solution = search(game)
    
    return solution


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
