inputs = ['TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC']

import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your inverse_burrows_wheeler_transform function here, along with any subroutines you need
def inverse_burrows_wheeler_transform(transform: str) -> str:
    """
    Generate the inverse of the Burrows-Wheeler Transform.
    """
    first_col = list(transform)
    first_col.sort()
    last_col = list(transform)
    last_col_labeled = labeler(last_col)
    first_col_labeled = labeler(first_col)

    col_len = len(first_col)
    curr = '$1'
    inverse_string = ''
    for i in range(col_len+1):
        x = last_col_labeled.index(curr)
        curr = first_col_labeled[x]
        if i != 0:
            inverse_string += last_col[x]
    return inverse_string 

def labeler(column: list) -> list:
    a = 1
    c = 1
    g = 1
    t = 1
    labeled = []
    for col in column:
        if col == 'A':
            labeled.append(f"{col}{a}")
            a += 1
        elif col == 'C':
            labeled.append(f"{col}{c}")
            c += 1
        elif col == 'G':
            labeled.append(f"{col}{g}")
            g += 1
        elif col == 'T':
            labeled.append(f"{col}{t}")
            t += 1
        elif col == '$':
            labeled.append('$1')
    return labeled


for i in inputs:
    print(inverse_burrows_wheeler_transform(i))