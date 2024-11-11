from treesudoku import tree_sudoku

import subprocess
check_data ="""
Board:0483921657967345821251876493548132976729564138136798245372689514814253769695417382
Board:1245981376169273584837564219976125438513498627482736951391657842728349165654812793
Board:2462831957795426183381795426173984265659312748248567319926178534834259671517643892"""
def test_end_to_end():
    print ("Running Test")
    p = subprocess.run(["python3", "./tree_sudoku.py"], capture_output=True)
    output = p.stdout.decode("utf-8").split("\n")
    output = "".join(output[:-2])
    output = output.replace("-","").replace("|","")
    output = output.replace(" ","").replace("\n","")
    output = output.replace("Board","\nBoard")
    print("comparing output ")
    assert(len(check_data) == len(output))
    assert(check_data == output)
    print("OK")

test_end_to_end()
