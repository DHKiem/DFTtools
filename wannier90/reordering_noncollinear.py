
#author: DHKiem
#Last update: 2025-Jun-6
from datetime import datetime 
import argparse


parser = argparse.ArgumentParser(description="options")
parser.add_argument('--input', type=str, default="wannier90_hr.dat", help="Input file  (default: wannier90_hr.dat)")
parser.add_argument('--output', type=str, default="wannier90_reordered_hr.dat", help="Input file  (default: wannier90_reordered_hr.dat)")
parser.add_argument('--mode', type=int, default=1, help="(default: 1) 1 for [convert udud to uudd] | 2 for [uudd to udud] ")

args = parser.parse_args()

print("Input:", args.input)
print("Mode:", args.mode)

inputfile = args.input
outputfile = args.output #"wannier90_reordered_hr.dat"


#  Convert interleaved (orb1↑, orb1↓, orb2↑, ...) to block (orb1↑, orb2↑, ..., orb1↓, orb2↓)
def remap_index1(old_index, num_wann):
    n = (old_index - 1) // 2  # orbital index (0-based)
    s = (old_index - 1) % 2   # spin: 0 for ↑, 1 for ↓
    return s * (num_wann // 2) + n + 1  # new 1-based index

#  Convert interleaved (orb1↑, orb2↑, ..., orb1↓, orb2↓) to block (orb1↑, orb1↓, orb2↑, ...)
def remap_index2(old_index, num_wann):
    n = (old_index-1) % (num_wann//2)    # orbital index (0-based)
    s = (old_index-1) //(num_wann//2)   # spin: 0 for ↑, 1 for ↓
    return 2 * n + s+1  # new 1-based index


#part reading
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

    if args.mode == 1:
        i_new = remap_index1(i_old, num_wann)
        j_new = remap_index1(j_old, num_wann)
    elif args.mode == 2:
        i_new = remap_index2(i_old, num_wann)
        j_new = remap_index2(j_old, num_wann)
    else:
        print("Check --mode")
        exit()

    new_line = f"{R1:5d} {R2:5d} {R3:5d} {i_new:5d} {j_new:5d} {real:>18} {imag:>18}\n"
    new_data_lines.append(new_line)

# Sort by (R, i, j) to preserve structure
new_data_lines.sort(key=lambda x: tuple(map(int, x.split()[0:3] + [x.split()[4], x.split()[3]] )))

current_time = datetime.now()
current_time_format = current_time.strftime("%-d%b%Y at %H:%M:%S")
with open(outputfile, "w") as f:
    f.write("reordered "+ current_time_format+"\n")
    f.write(f"{num_wann}\n")
    f.write(f"{num_R}\n")
    f.writelines(degeneracies)
    f.writelines(new_data_lines)

print("Output:", args.output)
print("Converting normally done.")