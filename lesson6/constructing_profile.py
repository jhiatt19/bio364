from pathlib import Path
import pandas as pd

inputs_folder = Path("./05_ConstructingProfileHMM/inputs")
outputs_folder = Path("./05_ConstructingProfileHMM/outputs")

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


def calculate_hidden_path(content):
    sections = content.strip().split('--------')
    theta = float(sections[0].strip())
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
        if gaps[gap] < theta:
            match_column.append(gap)
        else:
            insert_column.append(gap)
    for i in range(1,len(match_column)+1):
        for skel in column_skeleton:
            addition = skel + str(i)
            header_column_labels.append(addition)
    header_column_labels.append('E')
    header_column_labels.append('Total')
    alphabet.append('Total')
    emission_matrix = {}
    transition_matrix = {}
    for header in header_column_labels: 
        emission_matrix[header] = {}
        transition_matrix[header] = {}
        for letter in alphabet: # emission matrix
            emission_matrix[header][letter] = 0
        for head in header_column_labels:
            transition_matrix[header][head] = 0
    for a in alignments:
        index_counter = 0
        state_counter = 1
        prev_states = []
        state = 'S'
        prev_states.append(state)
        for letter in a:
            if index_counter in insert_column and letter != '-':
                if state == 'S':
                    next_state = 'I0'
                elif state[0] == 'I':
                    next_state = state
                else:
                    next_state = 'I' + str(state_counter) 
            elif index_counter in insert_column and letter == '-':
                if index_counter == len(a)-1:
                    next_state = 'E'
                else:
                    next_state = 'Ignore'
            elif index_counter in match_column and letter != '-':
                if state[0] == 'I' or state[0] == 'M' or state[0] == 'D':
                    state_counter += 1
                next_state = 'M' + str(state_counter)
            elif index_counter in match_column and letter == '-':
                if state[0] == 'D' or state[0] == 'M' or (state[0] == 'I' and state != 'I0'):
                    state_counter += 1
                next_state = 'D' + str(state_counter)
            if next_state != 'Ignore':
                transition_matrix[state][next_state] += 1
                transition_matrix[state]['Total'] += 1
                if letter in alphabet:
                    emission_matrix[next_state][letter] += 1
                    emission_matrix[next_state]['Total'] += 1
                state = next_state
            index_counter += 1
        if state != 'E':
            transition_matrix[state]['E'] += 1
            transition_matrix[state]['Total'] += 1
    for head1 in header_column_labels:
        for head2 in header_column_labels:
            if transition_matrix[head1]['Total'] != 0:
                transition_matrix[head1][head2] = transition_matrix[head1][head2] / transition_matrix[head1]['Total']
    for head1 in header_column_labels:
        for head2 in alphabet:
            if emission_matrix[head1]['Total'] != 0:
                emission_matrix[head1][head2] = emission_matrix[head1][head2] / emission_matrix[head1]['Total']
    return transition_matrix, header_column_labels, emission_matrix, alphabet
    
    

#print(outfile_contents)
i = 0
for f in file_contents:
    transition, headers, emission, alphabet = calculate_hidden_path(file_contents[f])
    headers.pop()
    output_file = "pass_off.txt"

    with open(output_file,"w",encoding="utf-8") as file_out:
        header = "\t" + "\t".join(headers)
        file_out.write(header + "\n")
        for from_state in headers:
            row = [from_state]
            for to_state in headers:
                val = transition.get(from_state, {}).get(to_state,0)
                if isinstance(val,float) and val == 0.0:
                    formatted_val = "0"
                elif isinstance(val,float):
                    formatted_val = str(round(val,4))
                else:
                    formatted_val = str(val)
                row.append(formatted_val)
            file_out.write("\t".join(row)+"\n")
        file_out.write('--------'+"\n")
        alphabet.pop()
        alph = "\t" + "\t".join(alphabet)
        file_out.write(alph+"\n")
        for from_state in headers:
                row = [from_state]
                for to_state in alphabet:
                    val = emission.get(from_state, {}).get(to_state,0)
                    if isinstance(val,float) and val == 0.0:
                        formatted_val = "0"
                    elif isinstance(val,float):
                        formatted_val = str(round(val,4))
                    else:
                        formatted_val = str(val)
                    row.append(formatted_val)
                file_out.write("\t".join(row)+"\n")
