import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your bw_matching function here, along with any subroutines you need
def bw_matching(bwt: str, patterns: List[str]) -> List[int]:
    """
    Perform Burrows-Wheeler Matching for a set of patterns against the Burrows-Wheeler Transform of a text.
    """
    first_col = list(bwt)
    first_col.sort()
    last_col = list(bwt)
    last_col_labeled = labeler(last_col)
    first_col_labeled = labeler(first_col)

    substring_matches = []
    for pattern in patterns:
        substring_matches.append(pattern_matching(last_col, pattern, first_col_labeled, last_col_labeled))

    return substring_matches

        
            

def pattern_matching(last_col, pattern, first_col_labeled, last_col_labeled):
    top = 0
    bottom = len(last_col) - 1
    while top <= bottom:
        x = len(pattern)
        if x != 0:
            target = pattern[-1]
            pattern = pattern[0:x-1]
            indices_first = [j for j, k in enumerate(last_col_labeled) if k[0] == target]
            indices = []
            for index in indices_first:
                if index < top or index > bottom:
                    pass
                else:
                    indices.append(index)    
            if len(indices) != 0:
                topIndex = last_col_labeled[indices[0]]
                bottomIndex = last_col_labeled[indices[-1]]
                top = first_col_labeled.index(topIndex)
                bottom = first_col_labeled.index(bottomIndex)
            else:
                return 0
        else:
            return bottom - top + 1


    

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

print(bw_matching('TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC',['CCT', 'CAC', 'GAG', 'CAG', 'ATC']))