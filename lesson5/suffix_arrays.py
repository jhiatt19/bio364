inputs = ["AACGATAGCGGTAGA$", "AATCAATC$", "ATCG$", "AAACA$", "ABCFED$"]


import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.

# Insert your suffix_array function here, along with any subroutines you need
def suffix_array(text: str) -> List[int]:
    array = []
    for t in range(len(text)):
            array.append(text[t:])
    array.sort()

    suffix = []
    for suf in array:
         suffix.append(text.find(suf))
        
    return suffix



for i in inputs:
    print(suffix_array(i))