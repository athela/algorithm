#!/usr/bin/python
# Filename: sweeping_mine.py
# use row and line, not x, y in traditional coordinate
import random
MINE_VALUE = -1




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
		placeholder_wid = len(str(self.grid_row))
		for i in range(self.grid_row+1):
			for j in range(self.grid_column+1):
				if i == 0:
					if j == 0:
						print ' '*(placeholder_wid+2),
					else:
						if j == self.grid_column:
							print j
						else:
							print j,					
				else:
					if j == 0:
						j_wid = len(str(i))
						print '\n',' '*(placeholder_wid-j_wid),'%d ' % i,
					else:
						index = self.get_index(i-1, j-1)
						value = self.grid[index]
						if check_mark and self.grid_mark[index] == 0:
							print '#',
						else:
							if value == MINE_VALUE:
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

	def get_around_positions(self, i, j, check_mine_value=False):
		'''get position around coordinate (i,j)
		contain eight possible position: topleft top topright left right bottomleft bottom bottomright	
		return valid positions and a int value of mine numbers when check_mine_value is true
		'''
		valid_positions = []
		mine_num = 0

		for row in range(i-1, i+2):
			for column in range(j-1, j+2):
				index = self.get_index(row, column)
				if index == -1 or (row == i and column == j):				
					continue
				if check_mine_value and self.grid[index] == MINE_VALUE:
					valid_positions.append(index)
					mine_num += 1
				else:
					valid_positions.append(index)		

		return valid_positions,mine_num


	def produce_grid_system(self):
		'''give the grid which width is grid_row, height is grid_column, mines is the index of mine 
		in the	grid
		'''	
		mines = self.random_number()
		if len(mines) != self.mine_num:
			print 'Mine number is invalid!'
			raise InitGridSystemError()

		for i in mines:
			self.grid[i] = MINE_VALUE		
		
		for i in range(0, self.grid_row):
			for j in range(0, self.grid_column):
				#Calculate a summary number of mines around the grid[i, j]								
				index = self.get_index(i, j)
				if self.grid[index] == MINE_VALUE:
					continue
				
				_, grid_value = self.get_around_positions(i, j, True)	
				self.grid[index] = grid_value

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
			a,b = raw_input('Input a row at [1, %d] and a column at [1, %d] in the coordinate system, \
use space separate them: ' % (self.grid_row, self.grid_column)).strip().split(' ');
			try:
				i = int(a)
				j = int(b)
			except:
				print 'Input is invalid, once again'
				continue

			index = self.get_index(i-1, j-1)			
			if -1 == index:
				print 'Input is invalid, once again.'
				continue
			if self.grid[index] == MINE_VALUE:
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

					around_positions, _ = self.get_around_positions(zero_index/self.grid_column, zero_index%self.grid_column)	
					for pos in around_positions:
						self.grid_mark[pos] = 1
						if self.grid[pos] == 0:
							zeros.append(pos)
					
					searched_zeros.append(zero_index)
				self.print_grid()

			#check if all grid has shown
			if self.grid_mark.count(0) == self.mine_num:
				print 'Congratulations, You win the game! '
				self.print_grid(False)
				break

class InitGridSystemError(Exception):
	''' exception when produce grid system failed
	'''
	def __init__(self):
		Exception.__init__(self)
		print 'Produce grid system failed, please check input paremters for grid system.'



if __name__ == '__main__':
	while True:
		chose = raw_input('Choose difficulty of Sweep mine game:  \n\
	           mine  row  column\n\
		[1]  10   9   9 \n\
		[2]  40   16  16 \n\
		[3]  99   16  30 \n')
		try:
			chose_number = int(chose)
		except:
			print 'Give a choice of list number above.'
			continue
		else:
			row = 0
			column = 0
			mine_num = 0
			if chose_number == 1:				
				row = 9
				column = 9
				mine_num = 10
			if chose_number == 2:
				row = 16
				column = 16
				mine_num = 40
			if chose_number == 3:
				row = 16
				column = 30
				mine_num = 99

			game = SweepMineGame(row, column, mine_num)
			game.produce_grid_system()
			game.play_game()
			break	





