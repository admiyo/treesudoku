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


def test_sudoku_solver():
    solver = tree_sudoku.SudokuSolver(tree_sudoku.import_csv())
    for key, solution in solver.solved_board_strings.items():
        assert solver.solved_board_strings[key] == puzzles[key]


def test_advance():
    test_board = tree_sudoku.build_board(puzzle0)
    node = tree_sudoku.Tree_Node(None, 0)
    node.write(test_board)
    assert (test_board[0][0] == '9')
    node = node.advance(test_board)
    node = node.advance(test_board)
    node.write(test_board)
    assert (test_board[0][3] == '0')
    node = node.advance(test_board)
    node.write(test_board)
    assert (test_board[0][3] == '9')
    back_node = node.retreat()
    assert (test_board[0][3] == '0')
    assert (node.value == "9")
    back_node.write(test_board)
    assert (test_board[0][2] == '3')
    assert (back_node.row == 0)
    assert (back_node.col == 2)
