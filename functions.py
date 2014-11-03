
#Cross product of elements in A and elements in B
def cross(A, B):
    return [a+b for a in A for b in B]



'''Finding units and peers correspond to each square in Sudoku puzzle
for this purpose the rows and column are given alphabetical and numerical labels
in order to provide a key (an later a value) to each square of the table'''

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])

units = dict((s, [u for u in unitlist if s in u])
             for s in squares)

peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)



#Convert the input grid into a dict of {square: char} with '0' or '.' for empties.
def grid_values(grid):

    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


"""Convert grid to a dict of possible values, {square: digits}, or
return False if a contradiction is detected."""
def parse_grid(grid):
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)

    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    return values


"""Eliminate all the other values (except d) from values[s] and propagate.
Return values, except return False if a contradiction is detected."""
def assign(values, s, d):

    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        #if all(len(values[s]) == 1 for s in squares):
        return values
    else:
        return False



def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d, '')

    if len(values[s]) == 0:
        return False

    #  If a square s is reduced to one value d2, then eliminate d2 from the peers.
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False

    # If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [i for i in u if d in values[i]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


"Using depth-first search and propagation, try all possible values."
def search(values):
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))for d in values[s])


#Return some element of seq that is true.
def some(seq):
    for e in seq:
        if e:
            return e
    return False


#Read the values of solved Sudoku puzzle from the first to the last square
def display(values):
    out = ''
    for r in rows:
        out = out + ( ''.join(values[r+c] for c in cols))
    return out
