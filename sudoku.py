import copy

test = ((0,0,2,7,8,0,1,0,5),
		(0,3,6,1,0,0,0,0,8),
		(7,0,0,0,6,0,0,4,0),
		(0,0,0,0,0,7,5,0,0),
		(0,0,1,0,2,0,8,3,0),
		(2,4,7,5,3,0,0,1,0),
		(0,0,5,0,7,0,0,0,3),
		(0,0,0,0,0,6,7,9,0),
		(8,7,9,3,4,0,6,0,0))

def find_blanks(grid):
	grid = list(grid)
	blanks = []

	r = 0
	for row in grid:
		c = 0
		for cell in row:
			if (cell == 0):
				blanks.append((c, r))
			c += 1
		r += 1
	return blanks

def find_blank(grid):
	grid = list(grid)
	blanks = find_blanks(grid);
	return blanks[0];

def get_block_coor(coor):
	y = (coor[1] / 3)
	x = (coor[0] / 3)

	return (x, y)

def get_block(coor, grid):
	grid = list(grid)
	block = []

	y = (coor[1] / 3) * 3
	x = (coor[0] / 3) * 3

	for yi in range(0, 3):
		row = grid[y + yi]
		for xi in range(0, 3):
			cell = row[x + xi]
			block.append(cell)

	return block


def find_options(blank, grid):
	grid = list(grid)
	available = range(1,10)
	
	row = grid[blank[1]]
	for cell in row:
		if (cell in available):
			available.remove(cell)

	for row in grid:
		cell = row[blank[0]]
		if (cell in available):
			available.remove(cell)

	block = get_block(blank, grid)
	for cell in block:
		if (cell in available):
			available.remove(cell)

	return available

def fill(coor, val, grid):
	nrow = list(grid[coor[1]])
	nrow[coor[0]] = val

	ng = list(grid)
	ng[coor[1]] = tuple(nrow)

	return tuple(ng)

def parsolve(grid):
	blanks = find_blanks(grid)

	if (len(blanks) == 0):
		return grid

	# Fill in places with only a single option
	for blank in blanks:
		options = find_options(blank, grid)
		if (len(options) == 1):
			grid = fill(blank, options[0], grid)

	# Now branch out for all the other blanks
	blanks = find_blanks(grid)
	for blank in blanks:
		options = find_options(blank, grid)
		if (len(options) == 0):
			return False
		for option in options:
			ng = fill(blank, option, grid)
			sol = parsolve(ng)
			if (sol):
				return sol
	return False

def calc(grid):
	blanks = find_blanks(grid)
	total = 0

	for blank in blanks:
		# print find_options(blank, grid)
		total += len(find_options(blank, grid))

	return total

def check_vals(vals):
	if (len(set(vals)) != len(vals)):
		return False
	if (len(vals) < 9):
		return False
	return True

def check(grid):
	columns = [[] for x in range(0,9)]
	blocks = [[[] for x in range(0, 3)] for x in range(0, 3)]

	r = 0
	for row in grid:
		if (not check_vals(row)):
			return False
		
		c = 0
		for cell in row:
			columns[c].append(cell)

			block = get_block_coor((c, r))
			blocks[block[1]][block[0]].append(cell)
			
			c += 1

		r += 1

	for column in columns:
		if (not check_vals(column)):
			return False

	for br in blocks:
		for block in br:
			if (not check_vals(column)):
				return False

	return True

def print_grid(grid):
	for row in grid:
		print row


s = parsolve(test)
print(check(s))
print_grid(s)