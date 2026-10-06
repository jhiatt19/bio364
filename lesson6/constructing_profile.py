from pathlib import Path

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
    header_column_labels.append('E')
    indexes_under_theta = []
    for gap in range(len(gaps)): #changes gaps data to probability of gaps at each index
        gaps[gap] = gaps[gap] / num_alignments
        if gaps[gap] < theta:
            indexes_under_theta.append(gap)
    #print(gaps, indexes_under_theta, theta)
    emission_matrix = []
    emission_matrix.append(alphabet)

    print(emission_matrix)

    return "start"
    
    

#print(outfile_contents)
i = 0
for f in file_contents:
    ans = calculate_hidden_path(file_contents[f])
    print(ans)
    