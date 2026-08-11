inputs = ['AATCGGGTTCAATCGGGGT', 'ATATATATAT', 'bananas', 'AAACAA', 'GAGCAT']
patterns = [['ATCG', 'GGGT'], ['GT', 'AGCT', 'TAA', 'AAT', 'AATAT'], ['ana', 'as'], ['AA'], ['GA', 'AG']]

import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your multiple_pattern_matching function here, along with any subroutines you need
def multiple_pattern_matching(text: str, patterns: List[str]) -> Dict[str, List[int]]:
    """
    Find all starting positions in text where each string from patterns appears as a substring.
    """
    text = text + '$'
    bwt = burrows_wheeler_transform(text)
    output = better_bw_matching(bwt,patterns)
    suffix = suffix_array(text)
    final_output = {}
    for out in output:
        for o in out.keys():
            if out[o][0] != None:
                end = suffix[out[o][0]:out[o][1]]
                end.sort()
                final_output[o] = end
            else:
                final_output[o] = []

    return final_output


def better_bw_matching(bwt: str, patterns: List[str]) -> List[int]:
    first_col = list(bwt)
    first_col.sort()
    last_col = list(bwt)
    first_occurance = {}
    unique_characters = set(first_col)
    zeros = []
    for char in unique_characters:
        first_occurance[char] = (first_col.index(char))
        zeros.append(0)
    count_array = [zeros]
    count_array_counter = 0
    for nuke in bwt:
        i = 0
        new_addition = []
        for char in unique_characters:
            if char == nuke:
                new_addition.append(count_array[count_array_counter][i]+1)
            else:
                new_addition.append(count_array[count_array_counter][i])
            i += 1
        count_array.append(new_addition)
        count_array_counter += 1
    substring_matches = []
    for pattern in patterns:
        substring_matches.append(better_pattern_matching(first_occurance, last_col, pattern, count_array))
    return substring_matches

def better_pattern_matching(first_occurance, last_column, pattern, count):
    beginning_pattern = pattern
    top = 0
    bottom = len(last_column) - 1
    while top <= bottom:
        x = len(pattern)
        if x > 0:
            target = pattern[-1]
            pattern = pattern[0:x-1]
            indices = [j for j, k in enumerate(last_column[top:bottom+1]) if k == target]
            if len(indices) > 0:
                top = first_occurance[target] + count_algorithm(count,target,top,list(first_occurance)) 
                bottom = first_occurance[target] + count_algorithm(count,target,bottom + 1, list(first_occurance)) - 1
            else:
                return {beginning_pattern: [None]}
        else:
            return {beginning_pattern: [top, bottom+1]}

def count_algorithm(count, symbol, index, symbols):
        symbol_index = -1
        i = 0
        for sims in symbols:
            if sims == symbol:
                symbol_index = i
            i += 1
        if symbol_index == -1:
            return 'Error'
        return count[index][symbol_index]

def burrows_wheeler_transform(text: str) -> str:
    """
    Generate the Burrows-Wheeler Transform of the given text.
    """
    array = [text]
    j = len(array)-1
    text_len = len(text)-1
    for i in range(len(text)-1):
        new_string = array[j][text_len]
        new_string += array[j][0:text_len]
        array.append(new_string)
        j += 1
    array.sort()
    last_column = ""
    for rotation in array:
        last_column += rotation[-1]
    return last_column

def suffix_array(text: str) -> List[int]:
    array = []
    for t in range(len(text)):
            array.append(text[t:])
    array.sort()

    suffix = []
    for suf in array:
         suffix.append(text.find(suf))
        
    return suffix

def inverse_burrows_wheeler_transform(transform: str, symbols) -> str:
    """
    Generate the inverse of the Burrows-Wheeler Transform.
    """
    first_col = list(transform)
    first_col.sort()
    last_col = list(transform)
    last_col_labeled = labeler(last_col,symbols)
    first_col_labeled = labeler(first_col,symbols)

    col_len = len(first_col)
    curr = '$1'
    inverse_string = ''
    for i in range(col_len+1):
        x = last_col_labeled.index(curr)
        curr = first_col_labeled[x]
        if i != 0:
            inverse_string += last_col[x]
    return inverse_string 

def labeler(column: list, symbols:list) -> list:
    symbol_counter = {}
    for symbol in symbols:
        symbol_counter[symbol] = 1
    labeled = []
    for col in column:
        for sym in symbols:
            if sym == col:
                labeled.append(f"{col}{symbol_counter[col]}")
                symbol_counter[col] += 1
    return labeled

for i in range(len(inputs)):
    print(multiple_pattern_matching(inputs[i],patterns[i]))