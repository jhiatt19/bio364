from pathlib import Path

inputs_folder = Path("./04_OutcomeLikelihood/inputs")
outputs_folder = Path("./04_OutcomeLikelihood/outputs")

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

    hidden_path_matrix = {}
    
    for i in range(len(string)):
        hidden_path_matrix[i] = {}
        total_prob = 0
        for j in states:
            if i == 0:
                start = 1 / len(states)
                total_prob = start * emission_matrix_dict[j][string[i]]
            else:
                total_prob = 0
                for k in states:
                    total_prob += hidden_path_matrix[i-1][k] * emission_matrix_dict[j][string[i]] * transition_matrix_dict[k][j]
            hidden_path_matrix[i][j] = (total_prob)
    final_prob = 0
    for state in states:
        final_prob += hidden_path_matrix[len(string) - 1][state]

    return final_prob
    
    

#print(outfile_contents)
i = 0
for f in file_contents:
    ans = calculate_hidden_path(file_contents[f])
    print(ans)
    