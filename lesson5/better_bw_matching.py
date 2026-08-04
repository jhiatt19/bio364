import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your better_bw_matching function here, along with any subroutines you need
def better_bw_matching(bwt: str, patterns: List[str]) -> List[int]:
    first_col = list(bwt)
    first_col.sort()
    last_col = list(bwt)
    first_occurance = {}
    dna = ['$','A','C','G','T']
    for nucleotide in dna:
        first_occurance[nucleotide] = (first_col.index(nucleotide))
    count_array = [[0,0,0,0,0]]
    dolla = 0
    a = 0
    c = 0
    g = 0
    t = 0
    for nuke in bwt:
        if nuke == '$':
            dolla += 1
        elif nuke == 'A':
            a += 1
        elif nuke == 'C':
            c += 1
        elif nuke == 'G':
            g += 1
        elif nuke == 'T':
            t += 1
        count_array.append([dolla,a,c,g,t])
    substring_matches = []
    for pattern in patterns:
        substring_matches.append(better_pattern_matching(first_occurance, last_col, pattern, count_array))
    return substring_matches

def better_pattern_matching(first_occurance, last_column, pattern, count):
    top = 0
    bottom = len(last_column) - 1
    while top <= bottom:
        x = len(pattern)
        if x > 0:
            target = pattern[-1]
            pattern = pattern[0:x-1]
            indices = [j for j, k in enumerate(last_column[top:bottom+1]) if k == target]
            if len(indices) > 0:
                top = first_occurance[target] + count_algorithm(count,target,top) 
                bottom = first_occurance[target] + count_algorithm(count,target,bottom + 1) - 1
            else:
                return 0
        else:
            return bottom - top + 1

def count_algorithm(count, symbol, index):
        if symbol == '$':
            symbol_index = 0
        elif symbol == 'A':
            symbol_index = 1
        elif symbol == 'C':
            symbol_index = 2
        elif symbol == 'G':
            symbol_index = 3
        elif symbol == 'T':
            symbol_index = 4
        else:
            return 'Error'
        return count[index][symbol_index]

print(better_bw_matching('GGCGCCGC$TAGTCACACACGCCGTA',['ACC', 'CCG', 'CAG']))