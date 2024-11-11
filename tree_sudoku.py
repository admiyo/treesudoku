#turn each csv row into a board
#find what values can go into what spot
#create a tree trying to put in each value
#if value can not be possible, end stem, go back up the tree
#retrun the branch when tree is 81 layers deep, the board is filled
import csv
import re
import copy
import time

BASIS = 3
DIM = BASIS * BASIS
MAX = DIM * DIM

class SudokuSolver:
    def __init__(self):
        self.board_strings = self.import_csv()
        self.boards_dict = self.strings_to_board_dict(self.board_strings)
        self.box_index_table = self.fill_box_index_table()
        self.board_index_table = self.fill_board_index_table()
        self.solved_board_strings = []
        for key, value in self.boards_dict.items():
            print(f"Board: {key}")
            self.solved_board_strings.append([self.tree_to_solution_string(value)])
    def tree_to_solution_string(self, original_board):
        index = 0
        head_node = Tree_Node(index, self.board_index_table[index])
        current_node = head_node
        while index < MAX:
            current_board_filling_node = head_node
            test_board = copy.deepcopy(original_board)
            test_board[int(current_board_filling_node.board_spot[0])][int(current_board_filling_node.board_spot[1])] = current_board_filling_node.value
            while current_board_filling_node.next_node:
                current_board_filling_node = current_board_filling_node.next_node
                test_board[int(current_board_filling_node.board_spot[0])][int(current_board_filling_node.board_spot[1])] = current_board_filling_node.value
            if self.value_valid(test_board, int(current_node.board_spot[0]), int(current_node.board_spot[1])):
                index += 1
                if index >= MAX:
                    continue
                new_node = Tree_Node(index, self.board_index_table[index], current_node)
                if test_board[int(new_node.board_spot[0])][int(new_node.board_spot[1])] != '0':
                    new_node.value = test_board[int(new_node.board_spot[0])][int(new_node.board_spot[1])]
                    new_node.possible_values = []
                current_node.next_node = new_node
                current_node = new_node
            else:
                if len(current_node.possible_values) == 0:
                    while len(current_node.possible_values) == 0:
                        current_node = current_node.last_node
                        current_node.next_node = None
                        index -= 1
                    current_node.next()
                else:
                    current_node.next()
 
        return_string = ''
        current_node = head_node
        return_string += str(current_node.value)
        while(current_node.next_node):
            current_node = current_node.next_node
            return_string += str(current_node.value)
        self.print_board(self.strings_to_board_dict([return_string])['0'])
        return return_string
    def import_csv(self):
        list_of_boards = []
        with open('sample_sudoku_board_inputs.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                list_of_boards.append(str(*row))
        return list_of_boards
 
    def strings_to_board_dict(self, board_strings):
        return_dict = {}
        for index, board in enumerate(board_strings):
            rows = re.findall(r"\d{9}", board)
            board_list = []
            for row in rows:
                row_list = []
                row_list[:0] = row
                board_list.append(row_list)
            return_dict[str(index)] = board_list
        return return_dict
 
    def print_board(self, board):
        for index1, row in enumerate(board):
            if index1 == 0 or index1 == 3 or index1 == 6:
                print('-' * 21)
            for index, char in enumerate(row):
                print(char, '', end='')
                if index == 2 or index == 5:
                    print('| ', end = '')
            print('')
            if index1 == 8:
                print('-' * 21)
 
    def value_valid(self, board, row_index, column_index):
        row = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        column = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        square = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for number in board[row_index]:
            if number == '0':
                continue
            if number in row:
                row.remove(number)
            else:
                return False
        for a_row in range(DIM):
            number = board[a_row][column_index]
            if number == '0':
                continue
            if number in column:
                column.remove(number)
            else:
                return False
        box_indexes = self.box_index_table[self.find_box_of_index(str(row_index) + str(column_index))]
        for index in box_indexes:
            row = int(index[0])
            column = int(index[1])
            number = board[row][column]
            if number == '0':
                continue
            if number in square:
                square.remove(number)
            else:
                return False
 
        return True
 
    def find_box_of_index(self, index):
        box = 'box not found'
        for each_box in self.box_index_table:
            if index in self.box_index_table[each_box]:
                box = each_box
                break
        return box
    def fill_box_index_table(self):
        boxes = {}
        box_center = [1, 1]
        box_number = 0
        for _row_of_boxes in range(BASIS):
            for _each_box in range(BASIS):
                box_list = []
                for i in range(-1, 2):
                    box_list.append(str(box_center[0] + i) + str(box_center[1] - 1))
                    box_list.append(str(box_center[0] + i) + str(box_center[1]))
                    box_list.append(str(box_center[0] + i) + str(box_center[1] + 1))
                boxes[box_number] = box_list
                box_number += 1
                box_center[1] += BASIS
            box_center[0] += BASIS
            box_center[1] -= DIM
        return boxes
 
    def fill_board_index_table(self):
        return_list = []
        for row in range(DIM):
            for column in range(DIM):
                return_list.append(str(row) + str(column))
        return return_list
class Tree_Node:
    def __init__(self, index, board_spot, last_node=None, next_node=None):
        self.possible_values = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.index = index
        self.board_spot = board_spot
        self.next_node = next_node
        self.last_node = last_node
        self.value = '9'
    def next(self):
        self.value = self.possible_values.pop()
 
    def __str__(self):
        return self.value
start = time.time()
x = SudokuSolver()
end = time.time()
