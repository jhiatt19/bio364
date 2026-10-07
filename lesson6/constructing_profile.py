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
    
    match_state = []
    ignore_state = []
    for gap in range(len(gaps)): #changes gaps data to probability of gaps at each index
        gaps[gap] = gaps[gap] / num_alignments
        if gaps[gap] < theta:
            match_state.append(gap)
        else:
            ignore_state.append(gap)
    #print(gaps, match_state, theta)
    for i in range(1,len(match_state)+1):
        for skel in column_skeleton:
            addition = skel + str(i)
            header_column_labels.append(addition)
    header_column_labels.append('E')
    header_column_labels.append('Total')
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
        match_state_counter = 1
        state = 'S'
        for letter in a:
            if index_counter in ignore_state and letter != '-':
                if index_counter == 0:
                    next_state = 'I' + str(index_counter)
                if state == 'S' or state == 'I0':
                    next_state = 'I0'
                else:
                    next_state = 'I' + str(match_state_counter)
            elif index_counter in ignore_state and letter == '-':
                if index_counter == len(a)-1:
                    next_state = 'E'
                else:
                    match_state_counter += 1
                    next_state = 'M' + str(match_state_counter)
            elif index_counter in match_state and letter != '-':
                if state[0] == 'I':
                    match_state_counter += 1
                next_state = 'M' + str(match_state_counter)
            elif index_counter in match_state and letter == '-':
                if state[0] == 'D' or state[0] == 'M' and state != 'I0':
                    match_state_counter += 1
                next_state = 'D' + str(match_state_counter)
            print(state,next_state,index_counter)
            if state != next_state or (state[0] == 'I' and state == next_state):
                transition_matrix[state][next_state] += 1
                transition_matrix[state]['Total'] += 1
            state = next_state
            index_counter += 1
        if state != 'E':
            transition_matrix[state]['E'] += 1
            transition_matrix[state]['Total'] += 1
        print(state,"E")
    for head1 in header_column_labels:
        for head2 in header_column_labels:
            if transition_matrix[head1]['Total'] != 0:
                transition_matrix[head1][head2] = transition_matrix[head1][head2] / transition_matrix[head1]['Total']

    return transition_matrix, header_column_labels
    
    

#print(outfile_contents)
i = 0
for f in file_contents:
    ans, headers = calculate_hidden_path(file_contents[f])
    headers.pop()
    header = "\t" + "\t".join(headers)
    print(header)
    for from_state in headers:
        row = [from_state]
        for to_state in headers:
            val = ans.get(from_state, {}).get(to_state,0)
            if isinstance(val,float) and val == 0.0:
                formatted_val = "0"
            elif isinstance(val,float):
                formatted_val = str(round(val,4))
            else:
                formatted_val = str(val)
            row.append(formatted_val)
        print("\t".join(row))
    print('--------')