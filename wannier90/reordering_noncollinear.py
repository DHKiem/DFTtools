from datetime import datetime 

inputfile = "wannier90_hr.dat"
outputfile = "wannier90_reordered_hr.dat"


#  Convert interleaved (orb1↑, orb1↓, orb2↑, ...) to block (orb1↑, orb2↑, ..., orb1↓, orb2↓)
def remap_index(old_index, num_wann):
    n = (old_index - 1) // 2  # orbital index (0-based)
    s = (old_index - 1) % 2   # spin: 0 for ↑, 1 for ↓
    return s * (num_wann // 2) + n + 1  # new 1-based index

with open(inputfile, "r") as f:
    lines = f.readlines()

num_wann = int(lines[1].split()[0])
num_R = int(lines[2].split()[0])
degeneracies = lines[3:(3 + (num_R + 14) // 15)]

# Start reading matrix elements
data_lines = lines[3 + len(degeneracies):]
new_data_lines = []

for line in data_lines:
    tokens = line.strip().split()
    R1, R2, R3, i_old, j_old  = map(int, tokens[:5])
    real, imag = tokens[5:7]

    i_new = remap_index(i_old, num_wann)
    j_new = remap_index(j_old, num_wann)

    new_line = f"{R1:5d} {R2:5d} {R3:5d} {i_new:5d} {j_new:5d} {real:>18} {imag:>18}\n"
    new_data_lines.append(new_line)

# Sort by (R, i, j) to preserve structure order by R, j, i
new_data_lines.sort(key=lambda x: tuple(map(int, x.split()[0:3] + [x.split()[4], x.split()[3]] )))

current_time = datetime.now()
current_time_format = current_time.strftime("%-d%b%Y at %H:%M:%S")
with open(outputfile, "w") as f:
    f.write("reordered "+ current_time_format+"\n")
    f.write(f"{num_wann}\n")
    f.write(f"{num_R}\n")
    f.writelines(degeneracies)
    f.writelines(new_data_lines)

