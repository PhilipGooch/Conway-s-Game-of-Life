import pygame
import time
import math
pygame.init()
width = 1366
height = 768
panel = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
black = (0, 0, 0)
white = (255, 255, 255)
white_square_original = [pygame.image.load("white.png")]
white_square = [pygame.image.load("white.png")]
clock = pygame.time.Clock()
fps = 10000
zoom = 30
grid_x = 0			# the top left corner of the center square of the grid
grid_y = 0
saved_grid_x = 0		# the last position of grid_x when mouse button is released 
saved_grid_y = 0
mouse_x = 0  		# position of mouse
mouse_y = 0
mouse_pressed = (0, 0)		# position of mouse when pressed. used in calculating grid_x	
pressed = False				# boolean mouse is pressed
left_mouse_button = False
right_mouse_button = False
tick_rate = 10000
fps = 0
# 1, 2, 4, 8, 16, 32, 64, 128, 264, 512, 1024, 2048, 4096
grid_size = 2048 	# can be infinite
on = []
# glider
# tick_rate = 30
# on = [(1066, 1090), (1067, 1090), (1068, 1090), (1068, 1091), (1067, 1092)]
# square
# on = [(1079, 1055), (1080, 1055), (1079, 1056), (1079, 1056)]
# glider gun
# on =[(1031, 1033), (1031, 1034), (1032, 1033), (1032, 1034), (1041, 1033), (1041, 1034), (1041, 1035), (1042, 1036), (1042, 1032), (1043, 1031), (1044, 1031), (1043, 1037), (1044, 1037), (1045, 1034), (1046, 1032), (1047, 1033), (1048, 1034), (1047, 1034), (1047, 1035), (1046, 1036), (1051, 1033), (1051, 1032), (1052, 1032), (1052, 1033), (1051, 1031), (1052, 1031), (1053, 1030), (1053, 1034), (1055, 1030), (1055, 1029), (1055, 1034), (1055, 1035), (1065, 1031), (1065, 1032), (1066, 1032), (1066, 1031)]
# double glider gun
# on = [(1038, 1053), (1038, 1054), (1039, 1054), (1039, 1053), (1048, 1053), (1048, 1054), (1048, 1055), (1049, 1052), (1050, 1051), (1051, 1051), (1049, 1056), (1050, 1057), (1051, 1057), (1052, 1054), (1053, 1052), (1054, 1053), (1055, 1054), (1054, 1054), (1054, 1055), (1053, 1056), (1058, 1053), (1059, 1053), (1059, 1052), (1058, 1052), (1058, 1051), (1059, 1051), (1060, 1050), (1060, 1054), (1062, 1050), (1062, 1049), (1062, 1054), (1062, 1055), (1072, 1051), (1072, 1052), (1073, 1051), (1073, 1052), (1110, 1052), (1110, 1051), (1124, 1051), (1124, 1052), (1124, 1053), (1132, 1051), (1132, 1057), (1144, 1053), (1144, 1054), (1109, 1051), (1109, 1052), (1120, 1049), (1120, 1050), (1120, 1054), (1120, 1055), (1122, 1050), (1122, 1054), (1123, 1051), (1123, 1052), (1123, 1053), (1127, 1054), (1128, 1053), (1128, 1054), (1128, 1055), (1129, 1052), (1129, 1056), (1130, 1054), (1131, 1051), (1131, 1057), (1133, 1052), (1133, 1056), (1134, 1053), (1134, 1054), (1134, 1055), (1143, 1053), (1143, 1054)]
# ship
tick_rate = 50
# on = [(1040, 1056), (1040, 1057), (1040, 1058), (1039, 1055), (1039, 1058), (1038, 1058), (1037, 1058), (1036, 1057), (1036, 1055)]
game_exit = False
select_mode = True
font = pygame.font.SysFont("none", 30)
start_frame = 0
end_frame = 0
generation = 0
save_on = []
save = True
go = False
square_number = (0, 0)

def resize_square(zoom):
	white_square[0] = pygame.transform.smoothscale(white_square_original[0], (zoom, zoom))

def find_square_number(zoom):
	return (int((mouse_x - grid_x + grid_size / 2 * zoom) / zoom), int((mouse_y - grid_y + grid_size / 2 * zoom) / zoom))

def select(zoom, left_mouse_button):
	square_number = find_square_number(zoom)
	if square_number[0] >= 0 and square_number[0] < grid_size and square_number[1] >= 0 and square_number[1] < grid_size:
		if left_mouse_button:
			if square_number not in on:
				on.append(square_number)
		elif right_mouse_button:
			if square_number in on:
				on.remove(square_number)

ignor = []
def am_i_square(x, y):
	flag = False
	if (x + 1, y) in on:
		if (x, y + 1) in on and (x + 1, y + 1) in on:
			for i in range(-1, 3):
				if (x + i, y - 1) in on or (x + i, y + 2) in on:
					flag = True
					break
			for i in range(2):
				if (x - 1, y + i) in on or (x + 2, y + i) in on:
					flag = True
					break
			if not flag:
				return True, 0
		elif (x, y - 1) in on and (x + 1, y - 1) in on:
			for i in range(-1, 3):
				if (x + i, y - 2) in on or (x + i, y + 1) in on:
					flag = True
					break
			for i in range(-1, 1):
				if (x - 1, y + i) in on or (x + 2, y + i) in on:
					flag = True
					break
			if not flag:
				return True, 2
	elif (x - 1, y) in on:
		if (x, y + 1) in on and (x - 1, y + 1) in on:
			for i in range(-2, 2):
				if (x + i, y - 1) in on or (x + i, y + 2) in on:
					flag = True
					break
			for i in range(2):
				if (x - 2, y + i) in on or (x + 1, y + i) in on:
					flag = True
					break
			if not flag:
				return True, 1
		elif (x, y - 1) in on and (x - 1, y - 1) in on:
			for i in range(-2, 2):
				if (x + i, y - 2) in on or (x + i, y + 1) in on:
					flag = True
					break
			for i in range(-1, 1):
				if (x - 2, y + i) in on or (x + 1, y + i) in on:
					flag = True
					break
			if not flag:
				return True, 3
	return False, 0



def update(on):
	next_on = []
	off = []
	for cell in on:
		square = am_i_square(cell[0], cell[1])
		# print(square)
		# if not square[0]:
		#count neighbours
		count = 0
		# if cell x and cell y
		if 0 < cell[0] < grid_size - 1 and 0 < cell[1] < grid_size - 1:
			if (cell[0] - 1, cell[1] - 1) in on:
				count += 1
			elif (cell[0] + 1, cell[1] + 1):
				off.append((cell[0] - 1, cell[1] - 1))
			if (cell[0], cell[1] - 1) in on:
				count += 1
			elif (cell[0] + 1, cell[1] + 1):
				off.append((cell[0], cell[1] - 1))
			if (cell[0] + 1, cell[1] - 1) in on:
				count += 1
			elif (cell[0] + 1, cell[1] + 1):
				off.append((cell[0] + 1, cell[1] - 1))
			if (cell[0] - 1, cell[1]) in on:
				count += 1
			elif (cell[0] + 1, cell[1] + 1):
				off.append((cell[0] - 1, cell[1]))
			if (cell[0] + 1, cell[1]) in on:
				count += 1
			elif (cell[0] + 1, cell[1] + 1):
				off.append((cell[0] + 1, cell[1]))
			if (cell[0] - 1, cell[1] + 1) in on:
				count += 1
			elif (cell[0] + 1, cell[1] + 1):
				off.append((cell[0] - 1, cell[1] + 1))
			if (cell[0], cell[1] + 1) in on:
				count += 1
			elif (cell[0] + 1, cell[1] + 1):
				off.append((cell[0], cell[1] + 1))
			if (cell[0] + 1, cell[1] + 1) in on:
				count += 1
			elif (cell[0] + 1, cell[1] + 1):
				off.append((cell[0] + 1, cell[1] + 1))
		if count == 2 or count == 3:
			next_on.append(cell)
		# else:
		# 	if square[1] == 0:
		# 		next_on.append(cell)
		# 		next_on.append((cell[0] + 1, cell[1]))
		# 		next_on.append((cell[0], cell[1] + 1))
		# 		next_on.append((cell[0] + 1, cell[1] + 1))
		# 		for i in range(-1, 3):
		# 			off.append((cell[0] + i, cell[1] - 1))
		# 			off.append((cell[0] + i, cell[1] + 2))
		# 		for i in range(2):
		# 			off.append((cell[0] - 1, cell[1] + i))
		# 			off.append((cell[0] + 2, cell[1] + i))
		# 	elif square[1] == 1:
		# 		next_on.append(cell)
		# 		next_on.append((cell[0] - 1, cell[1]))
		# 		next_on.append((cell[0], cell[1] + 1))
		# 		next_on.append((cell[0] - 1, cell[1] + 1))
		# 		for i in range(-2, 2):
		# 			off.append((cell[0] + i, cell[1] - 1))
		# 			off.append((cell[0] + i, cell[1] + 2))
		# 		for i in range(2):
		# 			off.append((cell[0] + 1, cell[1] + i))
		# 			off.append((cell[0] - 2, cell[1] + i))
		# 	elif square[1] == 2:
		# 		next_on.append(cell)
		# 		next_on.append((cell[0] + 1, cell[1]))
		# 		next_on.append((cell[0], cell[1] - 1))
		# 		next_on.append((cell[0] + 1, cell[1] - 1))
		# 		for i in range(-1, 3):
		# 			off.append((cell[0] + i, cell[1] - 2))
		# 			off.append((cell[0] + i, cell[1] + 1))
		# 		for i in range(-1, 1):
		# 			off.append((cell[0] - 1, cell[1] + i))
		# 			off.append((cell[0] + 2, cell[1] + i))
		# 	elif square[1] == 3:
		# 		next_on.append(cell)
		# 		next_on.append((cell[0] - 1, cell[1]))
		# 		next_on.append((cell[0], cell[1] - 1))
		# 		next_on.append((cell[0] - 1, cell[1] - 1))
		# 		for i in range(-2, 2):
		# 			off.append((cell[0] + i, cell[1] - 2))
		# 			off.append((cell[0] + i, cell[1] + 1))
		# 		for i in range(-1, 1):
		# 			off.append((cell[0] + 1, cell[1] + i))
		# 			off.append((cell[0] - 2, cell[1] + i))
	off = list(set(off))
	next_on = list(set(next_on))
	for cell in off:
		#count neighbours
		count = 0
		# if cell x and cell y
		if 0 < cell[0] < grid_size - 1 and 0 < cell[1] < grid_size - 1:
			if (cell[0] - 1, cell[1] - 1) in on:
				count += 1
			if (cell[0], cell[1] - 1) in on:
				count += 1
			if (cell[0] + 1, cell[1] - 1) in on:
				count += 1
			if (cell[0] - 1, cell[1]) in on:
				count += 1
			if (cell[0] + 1, cell[1]) in on:
				count += 1
			if (cell[0] - 1, cell[1] + 1) in on:
				count += 1
			if (cell[0], cell[1] + 1) in on:
				count += 1
			if (cell[0] + 1, cell[1] + 1) in on:
				count += 1
		if count == 3:
			next_on.append(cell)
		next_on = list(set(next_on))
	return next_on

# the glitch starts earlier on zoom in on the squares to the end of the array. to do with size

def display(grid_size, zoom, go):
	panel.fill(black)
	# for i in range(- int(grid_size / 2) * zoom, int(grid_size / 2) * zoom + zoom, zoom):
	# 	for j in range(- int(grid_size / 2) * zoom, int(grid_size / 2) * zoom + zoom, zoom):
	# 		pygame.draw.line(panel, white, (- int(grid_size / 2) * zoom + grid_x, j + grid_y), (int(grid_size / 2) * zoom + grid_x, j + grid_y))
	# 		pygame.draw.line(panel, white, (i + grid_x, - int(grid_size / 2) * zoom + grid_y), (i + grid_x, int(grid_size / 2) * zoom + grid_y))
	for square in on:
		panel.blit(white_square[0], (grid_x - int(grid_size / 2) * zoom + square[0] * zoom, grid_y - int(grid_size / 2) * zoom + square[1] * zoom))
	panel.blit(font.render("Generation: %i" % generation, 0, white), (1150, 700))

second_count = 0
frames = 0
resize_square(zoom)
while not game_exit:
	start_time = time.time()
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				game_exit = True
			if event.key == pygame.K_SPACE:
				if not go:
					go = True
				else:
					go = False
					select_mode = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x = pygame.mouse.get_pos()[0]
			mouse_y = pygame.mouse.get_pos()[1]
			mouse_pressed = pygame.mouse.get_pos()
			if event.button == 2:
				if not select_mode:
					select_mode = True
				else:
					select_mode = False
			if event.button == 1 or event.button == 3:
				pressed = True
			if event.button == 1 and select_mode:
				left_mouse_button = True
				select(zoom, True)
			elif event.button == 3 and select_mode:
				right_mouse_button = True
				select(zoom, False)
			# zoom in
			if event.button == 5 and zoom > 1:
				find_square_number(zoom)
				square_number = find_square_number(zoom)
				zoom -= 1
				grid_x += (square_number[0] - 1 - grid_size / 2) + 1
				grid_y += (square_number[1] - 1 - grid_size / 2) + 1
				resize_square(zoom)
			# zoom out
			if event.button == 4 and zoom < 50:
				find_square_number(zoom)
				square_number = find_square_number(zoom)
				zoom += 1
				grid_x -= (square_number[0] - 1 - grid_size / 2) + 1
				grid_y -= (square_number[1] - 1 - grid_size / 2) + 1
				resize_square(zoom)
		if event.type == pygame.MOUSEMOTION and pressed:
			mouse_x = pygame.mouse.get_pos()[0]
			mouse_y = pygame.mouse.get_pos()[1]
			if select_mode:
				if left_mouse_button:
					select(zoom, True)
				elif right_mouse_button:
					select(zoom, False)
			else:
				grid_x = mouse_x - mouse_pressed[0] + saved_grid_x
				grid_y = mouse_y - mouse_pressed[1] + saved_grid_y
		if event.type == pygame.MOUSEBUTTONUP:
			pressed = False
			saved_grid_x = grid_x
			saved_grid_y = grid_y
			if event.button == 1 and select_mode:
				left_mouse_button = False
			elif event.button == 3 and select_mode:
				right_mouse_button = False
	# for cell in on:
	# 	print(cell[0], cell[1])
	# 	if am_i_square(cell[0], cell[1]):
	# 		print(True)
	# 	else:
	# 		print(False)
	
	display(grid_size, zoom, go)
	if go:
		select_mode = False
		on = update(on)
		# go = False
		generation += 1
		end_time = time.time()
		second_count += end_time - start_time
		frames += 1
		if second_count >= 1:
			second_count = 0
			fps = frames
			frames = 0
	panel.blit(font.render("fps = %s" % fps, 0, white), (1150, 730))
	pygame.display.update()
	if save:
		save = False
		save_on = on
	# if generation == 1103:
	# 	game_exit = True
	clock.tick(tick_rate)
# print(save_on)
pygame.quit()
quit()