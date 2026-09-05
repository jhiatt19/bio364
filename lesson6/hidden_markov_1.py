from pathlib import Path

inputs_folder = Path("./02_ProbabilityOutcomeGivenHiddenPath/inputs")
outputs_folder = Path("./02_ProbabilityOutcomeGivenHiddenPath/outputs")

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


def calculate_path_prob(content):
    sections = content.strip().split('--------')
    string = sections[0].strip()
    alphabet = sections[1].strip().split()
    path = sections[2].strip()
    states = sections[3].strip().split()
    matrix_lines = [line.strip() for line in sections[4].strip().split("\n") if line]
    col_headers = matrix_lines[0].split()
    matrix_dict = {}

    for line in matrix_lines[1:]:
        parts = line.split()
        row_label = parts[0]
        probabilities = [float(p) for p in parts[1:]]

        matrix_dict[row_label] = dict(zip(col_headers,probabilities))
    print(matrix_dict)
    start = 1
    for a, p in zip(string,path):
        start = start * matrix_dict[p][a]

    return start
    
    

print(outfile_contents)
i = 0
for f in file_contents:
    ans = calculate_path_prob(file_contents[f])
    print(ans)
    