from treesudoku import tree_sudoku

puzzles = {
    "0": ("483921657" +
          "967345821" +
          "251876493" +
          "548132976" +
          "729564138" +
          "136798245" +
          "372689514" +
          "814253769" +
          "695417382"),
    "1": ("245981376" +
          "169273584" +
          "837564219" +
          "976125438" +
          "513498627" +
          "482736951" +
          "391657842" +
          "728349165" +
          "654812793"),
    "2": ("462831957" +
          "795426183" +
          "381795426" +
          "173984265" +
          "659312748" +
          "248567319" +
          "926178534" +
          "834259671" +
          "517643892")
}

puzzle0 = ("003020600" +
           "900305001" +
           "001806400" +
           "008102900" +
           "700000008" +
           "006708200" +
           "002609500" +
           "800203009" +
           "005010300")


def test_index_to_row_col():
    (row, col) = tree_sudoku.index_to_row_col(0)
    assert (row == 0)
    assert (col == 0)

    (row, col) = tree_sudoku.index_to_row_col(80)
    assert (row == 8)
    assert (col == 8)


def test_sudoku_solver():

    board_strings = tree_sudoku.import_csv()
    boards_dict = tree_sudoku.strings_to_board_dict(board_strings)
    solved_board_strings = dict()
    for key, value in boards_dict.items():
        return_string = value.solve()
        solved_board_strings[key] = return_string

    for key, solution in solved_board_strings.items():
        assert solved_board_strings[key] == puzzles[key]


def test_advance():
    test_board = tree_sudoku.Solver(puzzle0).board_list
    cell = tree_sudoku.Cell(test_board, None, 0)
    cell.write()
    assert (test_board[0][0] == '9')
    cell = cell.advance()
    cell = cell.advance()
    cell.write()
    assert (test_board[0][3] == '0')
    cell = cell.advance()
    cell.write()
    assert (test_board[0][3] == '9')
    back_cell = cell.retreat()
    assert (test_board[0][3] == '0')
    assert (cell.value == "9")
    back_cell.write()
    assert (test_board[0][2] == '3')
    assert (back_cell.row == 0)
    assert (back_cell.col == 2)
