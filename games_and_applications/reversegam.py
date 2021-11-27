import random, sys 
WIDTH = 8 
HEIGHT = 8 

def draw_board(board):
	print('  12345678')
	print(' +--------+')
	for y in range(HEIGHT):
		print('%s|' %(y+1), end='')
		for x in range(WIDTH):
			print(board[x][y], end='')
		print('|%s' %(y+1))
	print(' +--------+')
	print('  12345678')


def get_new_board():
	board = []
	for i in range(WIDTH):
		board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
	return board


def is_valid_move(board, tile, xstart, ystart):
	if board[xstart][ystart] != ' ' or not is_on_board(xstart, ystart):
		return False
	if tile == 'X':
		otherTile = 'O'
	else:
		otherTile = 'X'

	tiles_to_flip = []
	for xdirection, ydirection in [[0,1], [1,1], [1,0], [1,-1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		x, y = xstart, ystart
		x += xdirection
		y += ydirection
		while is_on_board(x, y) and board[x][y] == otherTile:
			x += xdirection
			y += ydirection
			if is_on_board(x, y) and board[x][y] == tile:
				while True:
					x -= xdirection
					y -= ydirection
					if x == xstart and y == ystart:
						break
					tiles_to_flip.append([x, y])

	if len(tiles_to_flip) == 0:
		return False
	return tiles_to_flip



def is_on_board(x, y):
	return x>= 0 and x <= WIDTH -1 and y >= 0 and y <= HEIGHT -1


def get_board_with_valid_moves(board, tile):
	board_copy = get_board_copy(board)
	for x, y in get_valid_moves(board_copy, tile):
		board_copy[x][y] = '.'
	return board_copy


def get_valid_moves(board, tile):
	valid_moves = []
	for x in range(WIDTH):
		for y in range(HEIGHT):
			if is_valid_move(board, tile, x, y) != False:
				valid_moves.append([x, y])
	return valid_moves


def get_score_of_the_board(board):
	Xscore = 0
	Oscore = 0
	for x in range(WIDTH):
		for y in range(HEIGHT):
			if board[x][y] == 'X':
				Xscore += 1
			if board[x][y] == 'O':
				Oscore += 1
	return {'X':Xscore, 'O':Oscore}


def enter_player_tile():
	tile = ''
	while not (tile == 'X' or tile == 'O'):
		print('Do you want to be X or O')
		tile = input().upper()
	if tile == 'X':
		return ['X', 'O']
	else:
		return ['O', 'X']

def who_goes_first():
	if random.randint(0,1) == 0:
		return 'computer'
	else:
		return 'player'


def make_move(board, tile, xstart, ystart):
	tiles_to_flip = is_valid_move(board, tile, xstart, ystart)
	if tiles_to_flip == False:
		return False

		board[xstart][ystart] = tile
		for x, y in tiles_to_flip:
			board[x][y] = tile
		return True


def get_board_copy(board):
	board_copy = get_new_board()
	for x in range(WIDTH):
		for y in range(HEIGHT):
			board_copy[x][y] = board[x][y]
	return board_copy


def is_on_corner(x, y):
	return (x == 0 or x == WIDTH -1) and (y == 0 or y == HEIGHT -1)


def get_player_move(board, player_tile):
	move_digits = '1 2 3 4 5 6 7 8'.split()
	while True:
		print('Enter your move, "q" to end the game, or "h" to toggle hints.')
		move = input().lower()
		if move == 'q' or move == 'h':
			return move
		if len(move) == 2 and move[0] in move_digits and move[1] in move_digits:
			x = int(move[0]) - 1
			y = int(move[1]) - 1
			if is_valid_move(board, player_tile, x, y) == False:
				continue
			else:
				break
		else:
			print('Invalid Input. Enter the colum(1-8) and then the row(1-8).')
			print('For example, 23 will present the second row and the third column.')

	return [x,y]

def get_computer_move(board, computer_tile):
	possible_moves = get_valid_moves(board, computer_tile)
	random.shuffle(possible_moves)

	for x, y in possible_moves:
		if is_on_board(x, y):
			return [x, y]

	best_score = -1
	for x, y in possible_moves:
		board_copy = get_board_copy(board)
		make_move(board, computer_tile, x, y)
		score  = get_score_of_the_board(board_copy)[computer_tile]
		if score > best_score:
			best_move = [x, y]
			best_score = score
	return best_move


def print_score(board, player_tile, computer_tile):
	scores = get_score_of_the_board(board)
	print('You: %s points.\nComputer: %s points.'%(scores[player_tile], scores[computer_tile]))


def play_game(player_tile, computer_tile):
	show_hints = False
	turn = who_goes_first()
	print(f"The {turn} will go first.")

	board = get_new_board()
	board[3][3] = 'X'
	board[3][4] = 'O'
	board[4][3] = 'O'
	board[4][4] = 'X'

	while True:
		player_valid_moves = get_valid_moves(board, player_tile)
		computer_valid_moves = get_valid_moves(board, computer_tile)

		if player_valid_moves == [] and computer_valid_moves == []:
			return board

		elif turn == 'player':
			if player_valid_moves != []:
				if show_hints:
					valid_move_board = get_board_with_valid_moves(board, player_tile)
					draw_board(valid_move_board)
				else:
					draw_board(board)
				print_score(board, player_tile, computer_tile)

				move = get_player_move(board, player_tile)
				if move == 'q':
					print('Thanks for playing.')
					sys.exit()
				elif move == 'h':
					show_hints = True
					continue
				else:
					make_move(board, player_tile, move[0], move[1])
			turn = 'computer'
		elif turn == 'computer':
			if computer_valid_moves != []:
				draw_board(board)
				print_score(board, player_tile, computer_tile)

				input('Press Enter to see the computer move.')
				move = get_computer_move(board, computer_tile)
				make_move(board, computer_tile, move[0], move[1])
			return 'player'

print('WELCOME TO REVERSEGAM!')

player_tile, computer_tile = enter_player_tile()

while True:
	final_board = play_game(player_tile, computer_tile)
	draw_board(final_board)
	scores = get_score_of_the_board(final_board)
	print('X scored %s points. O socred %s points.' %(scores['X'], scores['O']))
	if scores[player_tile] > scores['computer_tile']:
		print("You beat the computer by %s points! Congrats!" %(socres[player_tile] - scores[computer_tile]))
	elif scores[player_tile] < scores[computer_tile]:
		print("The computer beat you by %s points!" %(scores[computer_tile] - scores[player_tile]))
	else:
		print("The game was a draw!")

	print('Do you want to play again? (yes/no)')
	if not input().lower().startswith('y'):
		break























