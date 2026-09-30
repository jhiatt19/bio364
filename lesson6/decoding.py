from pathlib import Path

inputs_folder = Path("./03_OptimalHiddenPath/inputs")
outputs_folder = Path("./03_OptimalHiddenPath/outputs")

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
    string = sections[0].strip()
    alphabet = sections[1].strip().split()
    states = sections[2].strip().split()
    transition_matrix_lines = [line.strip() for line in sections[3].strip().split("\n") if line]
    emission_matrix_lines = [line.strip() for line in sections[4].strip().split("\n") if line]
    transition_col_headers = transition_matrix_lines[0].split()
    emission_col_headers = emission_matrix_lines[0].split()
    transition_matrix_dict = {}
    emission_matrix_dict = {}

    for line in transition_matrix_lines[1:]:
        parts = line.split()
        row_label = parts[0]
        probabilities = [float(p) for p in parts[1:]]

        transition_matrix_dict[row_label] = dict(zip(transition_col_headers,probabilities))

    for line in emission_matrix_lines[1:]:
            parts = line.split()
            row_label = parts[0]
            probabilities = [float(p) for p in parts[1:]]
    
            emission_matrix_dict[row_label] = dict(zip(emission_col_headers,probabilities))

    hidden_path = []

    hidden_path_matrix = {}

    for i in range(len(string)):
        hidden_path_matrix[i] = {}
        for j in states:
            if i == 0:
                start = 1 / len(states)
                high_prob = start * emission_matrix_dict[j][string[i]]
                high_state = j
            else:
                high_prob = 0
                high_state = None
                for k in states:
                    prob = hidden_path_matrix[i-1][k][0] * emission_matrix_dict[j][string[i]] * transition_matrix_dict[k][j]
                    if prob >= high_prob:
                        high_prob = prob
                        high_state = k   
            hidden_path_matrix[i][j] = (high_prob, high_state)
    print(hidden_path_matrix)

    backtrack_state = None
    for i in range(len(string)-1,-1,-1):
        #print(i,len(string)-1)  
        if i == len(string)-1:
            highest_prob = 0
            high_state = None
            for state in states:
                prob = hidden_path_matrix[i][state][0]
                if prob >= highest_prob:
                    highest_prob = prob
                    backtrack_state = hidden_path_matrix[i][state][1]
                    high_state = state
            hidden_path.append(high_state)
        elif i < len(string) - 1:
            hidden_path.append(backtrack_state)
            #print(backtrack_state, "before")
            backtrack_state = hidden_path_matrix[i][backtrack_state][1]
            #print(backtrack_state, "after")
    hidden_path.reverse()
    final = ''
    for i in hidden_path:
        final += i
    return final
    
    

#print(outfile_contents)
i = 0
for f in file_contents:
    ans = calculate_hidden_path(file_contents[f])
    print(ans)
    