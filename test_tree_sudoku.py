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
def test_sudoku_solver():
    solver = tree_sudoku.SudokuSolver(tree_sudoku.import_csv())
    for key, solution in solver.solved_board_strings.items():
        assert solver.solved_board_strings[key] == puzzles[key]
