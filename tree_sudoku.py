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

from typing import List

BASIS = 3
DIM = BASIS * BASIS
MAX = DIM * DIM


def import_csv() -> List[str]:
    list_of_boards: List[str] = []
    with open('sample_sudoku_board_inputs.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list_of_boards.append(str(*row))
    return list_of_boards


class Board:
    def __init__(self, board_string: str):
        rows = re.findall(r"\d{9}", board_string)
        self.board_list = []
        for row in rows:
            row_list: List[str] = []
            row_list[:0] = row
            self.board_list.append(row_list)

    def build_solution_string(self, head_node):
        return_string = ''
        curr_node = head_node
        return_string += str(curr_node.value)
        while (curr_node.next_node):
            curr_node = curr_node.next_node
            return_string += str(curr_node.value)
        return return_string

    def solve(self):
        test_board = copy.deepcopy(self.board_list)
        head_node = Tree_Node(None, 0)
        curr_node = head_node
        while True:
            curr_node.write(test_board)
            if is_value_valid(test_board, curr_node):
                if curr_node.index + 1 >= MAX:
                    break
                curr_node = curr_node.advance(test_board)
            else:
                # backtrack
                while len(curr_node.possible_values) == 0:
                    curr_node = curr_node.retreat()
                curr_node.pop()
        return self.build_solution_string(head_node)


class Tree_Node:
    def __init__(self, last_node, index):
        self.possible_values = possible_values()
        self.value = self.possible_values.pop()
        (self.row, self.col) = index_to_row_col(index)
        self.last_node = last_node
        self.next_node = None
        self.index = index
        self.old_value = None

    def advance(self, test_board):
        new_node = Tree_Node(self, self.index + 1)
        new_node.check_solved(test_board)
        self.next_node = new_node
        return new_node

    def retreat(self):
        self.board[self.row][self.col] = self.old_value
        node = self.last_node
        node.next_node = None
        return node

    def pop(self):
        self.value = self.possible_values.pop()

    def __str__(self):
        return self.value

    def write(self, board):
        self.board = board
        if self.old_value is None:
            self.old_value = board[self.row][self.col]
        board[self.row][self.col] = self.value

    def check_solved(self, board):
        if board[self.row][self.col] != '0':
            self.value = board[self.row][self.col]
            self.possible_values = []


def strings_to_board_dict(board_strings):
    return_dict = {}
    for index, board_string in enumerate(board_strings):
        return_dict[str(index)] = Board(board_string)
    return return_dict


def print_board(board: Board):
    for index1, row in enumerate(board.board_list):
        if index1 == 0 or index1 == 3 or index1 == 6:
            print('-' * 21)
        for index, char in enumerate(row):
            print(char, '', end='')
            if index == 2 or index == 5:
                print('| ', end='')
        print('')
        if index1 == 8:
            print('-' * 21)


def possible_values():
    values = []
    for index in range(1, DIM + 1):
        values.append('%d' % index)
    return values


def column_generator(row, col):
    for i in range(0, DIM):
        yield (i, col)


def row_generator(row, col):
    for i in range(0, DIM):
        yield (row, i)


def box_generator(row, col):
    row_mod = row % BASIS
    start_row = row - row_mod
    col_mod = col % BASIS
    start_col = col - col_mod
    for i in range(0, BASIS):
        for j in range(0, BASIS):
            yield (start_row + i, start_col + j)


def is_set_valid(board, row_index, column_index, generator):
    box = possible_values()
    for (row, column) in generator(row_index, column_index):
        number = board[row][column]
        if number == '0':
            continue
        if number in box:
            box.remove(number)
        else:
            return False
    return True


def is_value_valid(board, node):
    if not is_set_valid(board, node.row, node.col, column_generator):
        return False
    if not is_set_valid(board, node.row, node.col, row_generator):
        return False
    return is_set_valid(board, node.row, node.col, box_generator)


def index_to_row_col(index):
    col = int(index % DIM)
    row = int((index - col) / DIM)
    return (row, col)


def main():
    start = time.time()
    board_strings = import_csv()
    boards_dict = strings_to_board_dict(board_strings)
    solved_board_strings = dict()
    for key, value in boards_dict.items():
        return_string = value.solve()
        solved_board_strings[key] = return_string

    for key, solution in solved_board_strings.items():
        print(f"Board: {key}")
        print_board(strings_to_board_dict([solution])['0'])
    end = time.time()
    print("start time = %f" % start)
    print("end   time = %f" % end)
    print("duration = %f" % (end - start))


if __name__ == '__main__':
    main()
