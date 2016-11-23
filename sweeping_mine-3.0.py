#!/usr/bin/python
# coding=utf-8
# Filename: sweeping_mine.py
import random

class Grid:
	'''棋盘中的一个格子
	'''
	def __init__(self):
		'''
		value: 格点周围的雷的数量
		is_mine: 格点是否放置得有雷
		show: 是否显示
		'''
		self.value = 0
		self.is_mine = False
		self.show = False

class SweepMine:
	(input_error, has_showed, go_on, step_mine, win) = range(5)

	''' 扫雷游戏
	'''
	def __init__(self, row_num, col_num, mine_num):
		'''
		row_num: 行数
		col_num: 列数
		mine_num: 雷个数
		showed_num: 格点中已显示的格点个数
		grids：扫雷的二维格点系统
		'''
		self.row_num = row_num
		self.col_num = col_num
		self.mine_num = mine_num
		self.showed_num = 0		
		self.grids = [[Grid() for col in range(col_num)] for row in range(row_num)]
		self.init_grids()

	
	def random_number(self):
		''' 产生随机的雷的位置
		'''
		grid_num = self.row_num*self.col_num
		numbers = range(grid_num)
		return random.sample(numbers, self.mine_num)		
	
	def increase_grid_value(self, row, col):
		'''当row行col列有雷时，增加其周围的格点的雷数
		'''		
		for i in range(row-1, row+2):
			for j in range(col-1, col+2):
				if self.in_boundary(i, j) and (row != i or col != j):
					self.grids[i][j].value += 1	


	def in_boundary(self, row, col):
		'''检测i行j列是否有效
		'''
		return (row >= 0 and row < self.row_num) and (col >= 0 and col < self.col_num)

	def init_grids(self):
		'''初始化棋盘
		'''	
		mines = self.random_number()		
		for m in mines:
			i = m/self.col_num
			j = m%self.col_num
			self.grids[i][j].is_mine = True
			self.increase_grid_value(i, j)
			
	def coord2index(self, row, col):
		'''获取格点(i,j)的顺序位置
		'''	
		return row*self.col_num+col
	
	def show_grid_around(self, row, col):
		'''标记(i,j)周围的格点为show状态
		返回周围格点中value为0的格点位置集合
		'''
		empty_grids = []
		for i in range(row-1, row+2):
			for j in range(col-1, col+2):
				if self.in_boundary(i, j):
					if self.grids[i][j].show == False:
						self.grids[i][j].show = True
						self.showed_num += 1
					if self.grids[i][j].value == 0 and (row != i or col != j):
						empty_grids.append(self.coord2index(i, j))
		return empty_grids
					

	def click_grid(self, i, j):
		'''当点击i行j列
		'''
		grid_num = self.col_num*self.row_num
		if self.in_boundary(i, j) == False:
			return SweepMine.input_error

		if self.grids[i][j].is_mine == True:
			return SweepMine.step_mine

		if self.grids[i][j].show == True:
			return SweepMine.has_showed
		
		if self.grids[i][j].value != 0:
			self.grids[i][j].show = True
			self.showed_num += 1
		else:			
			empty_grids = [self.coord2index(i, j)]
			searched_empty_grids = []
			
			for xr in xrange(grid_num):
				if len(empty_grids) == 0:
					break					
				emp = empty_grids.pop()
				if emp in searched_empty_grids:
					continue

				empty_grids_around = self.show_grid_around(emp/self.col_num, emp%self.col_num)
				empty_grids.extend(empty_grids_around)
				searched_empty_grids.append(emp)

		if self.showed_num == grid_num - self.mine_num:			
			return SweepMine.win
		return SweepMine.go_on


	def print_grid(self, check_mark=True):
		''' print grid system, if check_mark is true, when grid is marked will show, otherwise will not show 
		'''		
		placeholder_wid = len(str(self.row_num))
		for i in range(self.row_num+1):
			for j in range(self.col_num+1):
				if i == 0:
					if j == 0:
						print ' '*(placeholder_wid+2),
					else:
						if j == self.col_num:
							print j-1
						else:
							print j-1,					
				else:
					if j == 0:
						j_wid = len(str(i-1))
						print '\n',' '*(placeholder_wid-j_wid),'%d ' % (i-1),
					else:						
						if check_mark and self.grids[i-1][j-1].show == False:
							print '#',
						else:
							if self.grids[i-1][j-1].is_mine == True:
								print '*',
							else:
								print self.grids[i-1][j-1].value,

		print '\n'


game_difficulty = {
	'1': [10, 9, 9],
	'2': [40, 16, 16],
	'3': [99, 16, 30]
}


def play_game():
	''' 玩扫雷游戏
	'''
	lv = raw_input('Choose difficulty of Sweep mine game:  \n\
	           mine  row  column\n\
		[1]  10   9   9 \n\
		[2]  40   16  16 \n\
		[3]  99   16  30 \n')
	if game_difficulty.has_key(lv) == False:
		print 'Choose a difficulty show on the list above.'
		return
	
	dif = game_difficulty[lv] 
	game = SweepMine(dif[1], dif[2], dif[0])
	game.print_grid()
	while True:
		row, col = raw_input('Input a row at [0, %d] and a column at [0, %d] in the coordinate system, \
use space separate them: ' % (dif[1]-1, dif[2]-1)).strip().split(' ');		
		try:
			i = int(row)
			j = int(col)
		except:
			print 'Input is invalid, once again'
			continue
		ret = game.click_grid(i, j)
		if ret == SweepMine.input_error:
			print 'Input is invalid, once again.'				
		elif ret == SweepMine.step_mine:			
			print 'You have steped on a mine, game failed!'			
			game.print_grid(False)
			return
		elif ret == SweepMine.win:
			print 'Congratulations, You win the game! '
			game.print_grid(False)
			return
		elif ret == SweepMine.go_on:
			game.print_grid()
		#elif ret == SweepMine.has_showed:		



if __name__ == '__main__':
	play_game()