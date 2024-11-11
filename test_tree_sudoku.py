from treesudoku import tree_sudoku

puzzles = {
    "0": "483921657967345821251876493548132976729564138136798245372689514814253769695417382",
    "1": "245981376169273584837564219976125438513498627482736951391657842728349165654812793",
    "2": "462831957795426183381795426173984265659312748248567319926178534834259671517643892"
}
def test_sudoku_solver():
    solver = tree_sudoku.SudokuSolver(tree_sudoku.import_csv())
    for key, solution in solver.solved_board_strings.items():
        assert solver.solved_board_strings[key] == puzzles[key]
