#!/usr/bin/python
# Filename: sweeping_mine.py
# use row and line, not x, y in traditional coordinate
import random

class SweepMineGame:
	''' Play sweeping mine game
	'''
	def __init__(self, grid_row, grid_column, mine_num):
		'''Initialize the SweepMineGame's name
		'''
		self.grid_row = grid_row
		self.grid_column = grid_column
		self.mine_num = mine_num
		grid_num = grid_row*grid_column
		self.grid = [0]*grid_num
		self.grid_mark = [0]*grid_num

	def print_grid(self, check_mark=True):
		''' print grid system, if check_mark is true, when grid is marked will show, otherwise will not show 
		'''		
		for i in range(self.grid_row+1):
			for j in range(self.grid_column+1):
				if i == 0:
					if j == 0:
						print '  ',
					else:
						if j == 9:
							print j
						else:
							print j,					
				else:
					if j == 0:
						print '\n%d ' % i,
					else:
						value = self.grid[(i-1)*self.grid_column+j-1]
						if check_mark and self.grid_mark[(i-1)*self.grid_column+j-1] == 0:
							print '#',
						else:
							if value == -1:
								print '*',
							else:
								print value,

		print '\n'


	def random_number(self):
		''' produce target_num random int number among [1, range_num]
		'''
		grid_num = self.grid_row*self.grid_column
		if self.mine_num > grid_num:
			print 'Warning: the number of mines is more than grid numbers.'
			return []
		numbers = range(0, grid_num)
		random.shuffle(numbers)	
		return numbers[:self.mine_num]		

	def get_around_positions(self, i, j):
		'''get position around coordinate (i,j)
		contain eight possible position: topleft top topright left right bottomleft bottom bottomright	
		'''
		position_around = []
		top = i-1 >= 0 and i-1 < self.grid_row
		bottom = i+1 >= 0 and i+1 < self.grid_row
		left = j-1 >= 0 and j-1 < self.grid_column
		right = j+1 >= 0 and j+1 < self.grid_column
		if top:
			position_around.append((i-1)*self.grid_column+j)
			if left:
				position_around.append((i-1)*self.grid_column+j-1)
			if right:
				position_around.append((i-1)*self.grid_column+j+1)
		if bottom:
			position_around.append((i+1)*self.grid_column+j)
			if left:
				position_around.append((i+1)*self.grid_column+j-1)
			if right:
				position_around.append((i+1)*self.grid_column+j+1)
		if left:
			position_around.append(i*self.grid_column+j-1)
		if right:
			position_around.append(i*self.grid_column+j+1)		
		return position_around



	def produce_grid_system(self):
		'''give the grid which width is grid_row, height is grid_column, mines is the index of mine 
		in the	grid
		'''	
		mines = self.random_number()		

		for i in mines:
			self.grid[i] = -1		
		
		for i in range(0, self.grid_row):
			for j in range(0, self.grid_column):
				#Calculate a summary number of mines around the grid[i, j]								
				
				if self.grid[i*self.grid_column+j] == -1:
					continue
				
				position_around = self.get_around_positions(i, j)	

				grid_value = 0
				for index in position_around:
					if -1 == self.grid[index]:
						grid_value += 1		
				self.grid[i*self.grid_column+j] = grid_value

		self.print_grid()
		

	
	def get_index(self, cur_row, cur_column):
		'''get index of cur_row cur_column in grid system
		'''
		if cur_row >=0 and cur_row < self.grid_row and cur_column >=0 and cur_column < self.grid_column:
			return cur_row*self.grid_column+cur_column
		return -1


	def play_game(self):
		''' play sweep mine game
		'''
		while True:
			a,b = raw_input('Input the a row at [1, %d] and a column at [1, %d] in the coordinate system, \
use space separate them: ' % (self.grid_row, self.grid_column)).strip().split(' ');
			i = int(a)
			j = int(b)
			index = self.get_index(i-1, j-1)			
			if -1 == index:
				print 'Input is invalid, once again.'
				continue
			if self.grid[index] == -1:
				print 'You have steped on a mine, game failed!'
				self.print_grid(False)
				break
			if self.grid[index] != 0:
				self.grid_mark[index] = 1
				self.print_grid()				
			else:
				zeros = [index]
				searched_zeros = []
				while len(zeros) != 0:
					zero_index = zeros.pop()
					if zero_index in searched_zeros:
						continue

					self.grid_mark[zero_index] = 1

					around_positions = self.get_around_positions(zero_index/self.grid_column, zero_index%self.grid_column)	
					for around_index in around_positions:
						self.grid_mark[around_index] = 1
						if self.grid[around_index] == 0:
							zeros.append(around_index)
					
					searched_zeros.append(zero_index)
				self.print_grid()

			#check if all grid has shown
			if self.grid_mark.count(0) == self.mine_num:
				print 'Congratulations, You win the game! '
				self.print_grid(False)
				break


game = SweepMineGame(9, 9, 10)
game.produce_grid_system()
game.play_game()


