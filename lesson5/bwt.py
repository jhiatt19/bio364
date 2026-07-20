inputs = ["GCGTGCCTGGTCA$", "AATCAATC$", "AAAAAAAAAA$", "GAGCAT$"]

import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your burrows_wheeler_transform function here, along with any subroutines you need
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

for i in inputs:
    print(burrows_wheeler_transform(i))