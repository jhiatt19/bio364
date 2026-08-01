import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your better_bw_matching function here, along with any subroutines you need
def better_bw_matching(bwt: str, patterns: List[str]) -> List[int]:
    first_col = list(bwt)
    first_col.sort()
    last_col = list(bwt)
    last_col_labeled = labeler(last_col)
    first_col_labeled = labeler(first_col)

    substring_matches = []
    count_array = [['A','C','G','T']]
    for i in count_array:
        pass
    pass

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

print(better_bw_matching('GGCGCCGC$TAGTCACACACGCCGTA',['ACC', 'CCG', 'CAG']))