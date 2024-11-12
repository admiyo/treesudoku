#!/usr/bin/python

# turn each csv row into a board
# find what values can go into what spot
# create a tree trying to put in each value
# if value can not be possible, end stem, go back up the tree
# return the branch when tree is 81 layers deep, the board is filled
import csv
import re
import copy
import time


BASIS = 3
DIM = BASIS * BASIS
MAX = DIM * DIM


def import_csv():
    list_of_boards = []
    with open('sample_sudoku_board_inputs.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list_of_boards.append(str(*row))
    return list_of_boards


class SudokuSolver:
    def __init__(self, board_strings):
        self.board_strings = board_strings
        self.boards_dict = self.strings_to_board_dict(self.board_strings)
        self.box_index = BoxIndex()
        self.solved_board_strings = dict()
        for key, value in self.boards_dict.items():
            return_string = self.tree_to_solution_string(value)
            self.solved_board_strings[key] = return_string

    def tree_to_solution_string(self, original_board):
        def advance(node, test_board, index):
            new_node = Tree_Node(board_index.table[index], node)
            new_node.check_solved(test_board)
            node.next_node = new_node
            return new_node

        index = 0
        head_node = Tree_Node(board_index.table[index])
        curr_node = head_node
        while index < MAX:
            curr_board_filling_node = head_node
            test_board = copy.deepcopy(original_board)
            curr_board_filling_node.write(test_board)
            while curr_board_filling_node.next_node:
                curr_board_filling_node = curr_board_filling_node.next_node
                curr_board_filling_node.write(test_board)
            curr_row = int(curr_board_filling_node.board_spot[0])
            curr_col = int(curr_board_filling_node.board_spot[1])
            test_board[curr_row][curr_col] = curr_board_filling_node.value
            if self.box_index.is_value_valid(test_board, curr_node):
                index += 1
                if index >= MAX:
                    continue
                curr_node = advance(curr_node, test_board, index)
                curr_node.check_solved(test_board)
            else:
                if len(curr_node.possible_values) == 0:
                    # backtrack
                    while len(curr_node.possible_values) == 0:
                        curr_node = curr_node.last_node
                        curr_node.next_node = None
                        index -= 1
                curr_node.next()
        return self.build_solution_string(head_node)

    def build_solution_string(self, head_node):
        return_string = ''
        curr_node = head_node
        return_string += str(curr_node.value)
        while (curr_node.next_node):
            curr_node = curr_node.next_node
            return_string += str(curr_node.value)
        return return_string

    def strings_to_board_dict(self, board_strings):
        return_dict = {}
        for index, board in enumerate(board_strings):
            return_dict[str(index)] = build_board(board)
        return return_dict


def print_board(board):
    for index1, row in enumerate(board):
        if index1 == 0 or index1 == 3 or index1 == 6:
            print('-' * 21)
        for index, char in enumerate(row):
            print(char, '', end='')
            if index == 2 or index == 5:
                print('| ', end='')
        print('')
        if index1 == 8:
            print('-' * 21)


def build_board(board):
    rows = re.findall(r"\d{9}", board)
    board_list = []
    for row in rows:
        row_list = []
        row_list[:0] = row
        board_list.append(row_list)
    return board_list


class BoxIndex:
    def __init__(self):
        self.table = self.fill_box_index_table()

    def is_value_valid(self, board, node):
        row = int(node.board_spot[0])
        col = int(node.board_spot[1])
        return self.value_valid(board, row, col)

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
        box_indexes = self.table[
            self.find_box_of_index(
                str(row_index) + str(column_index))]
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
        for each_box in self.table:
            if index in self.table[each_box]:
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
                    box_list.append(str(box_center[0] + i) +
                                    str(box_center[1] - 1))
                    box_list.append(str(box_center[0] + i) +
                                    str(box_center[1]))
                    box_list.append(str(box_center[0] + i) +
                                    str(box_center[1] + 1))
                boxes[box_number] = box_list
                box_number += 1
                box_center[1] += BASIS
            box_center[0] += BASIS
            box_center[1] -= DIM
        return boxes


class BoardIndexTable:
    def __init__(self):
        self.table = self.fill_board_index_table()

    def fill_board_index_table(self):
        return_list = []
        for row in range(DIM):
            for column in range(DIM):
                return_list.append(str(row) + str(column))
        return return_list

board_index = BoardIndexTable()


class Tree_Node:
    def __init__(self, board_spot, last_node=None, next_node=None):
        self.possible_values = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.board_spot = board_spot
        self.next_node = next_node
        self.last_node = last_node
        self.value = '9'

    def next(self):
        self.value = self.possible_values.pop()

    def __str__(self):
        return self.value

    def write(self, board):
        curr_row = int(self.board_spot[0])
        curr_col = int(self.board_spot[1])
        board[curr_row][curr_col] = self.value

    def check_solved(self, board):
        row = int(self.board_spot[0])
        col = int(self.board_spot[1])
        if board[row][col] != '0':
            self.value = board[row][col]
            self.possible_values = []


start = time.time()
solver = SudokuSolver(import_csv())
for key, solution in solver.solved_board_strings.items():
    print(f"Board: {key}")
    print_board(solver.strings_to_board_dict([solution])['0'])

end = time.time()
