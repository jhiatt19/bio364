import math
from pathlib import Path
import pandas as pd

inputs_folder = Path("./06_PseudocountProfileHMM/inputs")
outputs_folder = Path("./06_PseudocountProfileHMM/outputs")

file_contents = {}

for file in inputs_folder.iterdir():
    if file.is_file():
        try:
            content = file.read_text(encoding="utf-8")
            file_contents[file.name] = content
            print(f"Successfully loaded: {file.name}")
        except Exception as e:
            print(f"Failed to read {file.name}: {e}")

print(f"\nTotal files read into memory: {len(file_contents)}")

outfile_contents = {}

for ofile in outputs_folder.iterdir():
    if ofile.is_file():
        try:
            content = ofile.read_text(encoding="utf-8")
            outfile_contents[ofile.name] = content
            print(f"Successfully loaded: {ofile.name}")
        except Exception as e:
            print(f"Failed to read {ofile.name}: {e}")


def get_valid_targets(from_state,num_levels):
    if from_state == 'E':
        return []
    if from_state in ['S', 'I0']:
        return ['M1', 'D1', 'I0']

    state_type = from_state[0]
    k = int(from_state[1:])

    if k < num_levels:
        return [f'M{k+1}', f'D{k+1}', f'I{k}']
    else:
        return ['E', f'I{k}']

def calculate_hidden_path(content):
    sections = content.strip().split('--------')
    holder = sections[0].strip().split()
    theta = float(holder[0])
    pseudocount = float(holder[1])
    alphabet = sections[1].strip().split()
    alignments = [line.strip() for line in sections[2].strip().split("\n") if line]
    column_skeleton = ['M', 'D', 'I']
    header_column_labels = ['S', 'I0']
    gaps = []
    num_alignments = len(alignments)

    for i in range(len(alignments[0])): #sets up gaps counter
        gaps.append(0)
    for a in alignments: #determines number of gaps at that index
        gap_index = 0
        for char in a:
            if char == "-":
                gaps[gap_index] += 1
            gap_index += 1
    
    match_column = []
    insert_column = []

    
    for gap in range(len(gaps)): #changes gaps data to probability of gaps at each index
        gaps[gap] = gaps[gap] / num_alignments
        if gaps[gap] <= theta:
            match_column.append(gap)
        else:
            insert_column.append(gap)

    levels = len(match_column)

    for i in range(1,levels+1):
        for skel in column_skeleton:
            addition = skel + str(i)
            header_column_labels.append(addition)
    header_column_labels.append('E')
    
    emission_matrix = {}
    transition_matrix = {}
    print(header_column_labels)
    for header in header_column_labels: 
        emission_matrix[header] = {}
        transition_matrix[header] = {}
        valid_targets = get_valid_targets(header,levels)
        for letter in alphabet: # emission matrix
            if header in ['S','E'] or header[0] == 'D':
                emission_matrix[header][letter] = 0
            else:
                emission_matrix[header][letter] = 0
        for head in header_column_labels: #transition matrix
            if head in valid_targets:
                transition_matrix[header][head] = 0
            else:
                transition_matrix[header][head] = 0
    for a in alignments:
        index_counter = 0
        match_level = 0
        state = 'S'
        for letter in a:
            if index_counter in insert_column and letter != '-':
                if state == 'S':
                    next_state = 'I0'
                elif state[0] == 'I':
                    next_state = state
                else:
                    next_state = 'I' + str(match_level) 
            elif index_counter in insert_column and letter == '-':
                index_counter += 1
                continue
            elif index_counter in match_column and letter != '-':
                match_level = match_column.index(index_counter) + 1
                next_state = 'M' + str(match_level)
            elif index_counter in match_column and letter == '-':
                match_level = match_column.index(index_counter) + 1
                next_state = 'D' + str(match_level)
            transition_matrix[state][next_state] += 1
            if letter != '-' and (next_state[0] in ['M','I']):
                emission_matrix[next_state][letter] += 1
            state = next_state
            index_counter += 1
        transition_matrix[state]['E'] += 1
    for head1 in header_column_labels:
        valid_targets = get_valid_targets(head1,levels)
        if not valid_targets:
            continue
        row_total = sum(transition_matrix[head1][target] for target in valid_targets)
        if row_total == 0:
            prob = 1.0 / len(valid_targets)
            for target in valid_targets:
                transition_matrix[head1][target] = prob
        else:
            zero_targets = [t for t in valid_targets if transition_matrix[head1][t] == 0]
            pseudocount_mass = len(zero_targets) * pseudocount
            remaining_mass = 1 - pseudocount_mass
            for target in valid_targets:
                if transition_matrix[head1][target] == 0:
                    transition_matrix[head1][target] = pseudocount
                else:
                    raw_freq = transition_matrix[head1][target] / row_total
                    transition_matrix[head1][target] = raw_freq * remaining_mass
    for head1 in header_column_labels:
        if head1 in ['S','E'] or head1[0] == 'D':
            continue
        total_row = sum(emission_matrix[head1][symbol] for symbol in alphabet)
        if total_row == 0:
            prob = 1.0 / len(alphabet)
            for symbol in alphabet:
                emission_matrix[head1][symbol] = prob
        else:
            zero_symbols = [s for s in alphabet if emission_matrix[head1][s] == 0]
            pseudocount_mass = len(zero_symbols) * pseudocount
            remaining_mass = 1 - pseudocount_mass

            for symbol in alphabet:
                if emission_matrix[head1][symbol] == 0:
                    emission_matrix[head1][symbol] = pseudocount
                else:
                    raw_freq = emission_matrix[head1][symbol] / total_row
                    emission_matrix[head1][symbol] = raw_freq * remaining_mass
    return transition_matrix, header_column_labels, emission_matrix, alphabet
    
    

#print(outfile_contents)
i = 0
for f in file_contents:
    transition, headers, emission, alphabet = calculate_hidden_path(file_contents[f])
    output_file = "pass_off.txt"

    with open(output_file,"w",encoding="utf-8") as file_out:
        header = "\t" + "\t".join(headers)
        file_out.write(header + "\n")
        #print(header + "\n")
        for from_state in headers:
            row = [from_state]
            for to_state in headers:
                val = transition.get(from_state, {}).get(to_state,0)
                if isinstance(val,float) and val == 0.0:
                    formatted_val = "0"
                elif isinstance(val,float):
                    formatted_val = str(round(val,3))
                else:
                    formatted_val = str(val)
                row.append(formatted_val)
            file_out.write("\t".join(row)+"\n")
            #print("\t".join(row)+"\n")
        file_out.write('--------'+"\n")
        #print('--------'+"\n")
        alph = "\t" + "\t".join(alphabet)
        file_out.write(alph+"\n")
        #print(alph+"\n")
        for from_state in headers:
                row = [from_state]
                for to_state in alphabet:
                    val = emission.get(from_state, {}).get(to_state,0)
                    if isinstance(val,float) and val == 0.0:
                        formatted_val = "0"
                    elif isinstance(val,float):
                        formatted_val = str(round(val,3))
                    else:
                        formatted_val = str(val)
                    row.append(formatted_val)
                #print("\t".join(row)+"\n")
                file_out.write("\t".join(row)+"\n")
