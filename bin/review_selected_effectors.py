#!/usr/bin/env python

import argparse
import annotations

from pylab import *

def draw_hydropathy_plot(record_id, values, bilobed_domain, inc_type=1):
    plot(values)

    i=0
    while i<len(values):
        if values[i]<0:
            i+=1
            continue
        j = i+1
        while j<len(values) and values[j]>=0:
            j+=1
        
        if i>=bilobed_domain[0] and i<=bilobed_domain[1]:
            # found the bilobed domain, it will have a different colour
            pass
        else:
            axvspan(i, j-1, facecolor="g", alpha=0.1)
        i = j+1

    # plot the domain interval
    axvspan(bilobed_domain[0], bilobed_domain[1], facecolor="r", alpha=0.1, label="Bilobed hydrophobic domain")
    # plot([bilobed_domain[0], bilobed_domain[1]], [0, 0], color="r", linewidth=2)
    plot([annotations.N_TERMINUS_RANGE[0], annotations.N_TERMINUS_RANGE[0]], [-4, 4],
            color="g", linestyle=":", linewidth=2)
    plot([annotations.N_TERMINUS_RANGE[1], annotations.N_TERMINUS_RANGE[1]], [-4, 4],
            color="g", linestyle=":", linewidth=2)
    
    # plot the limits
    title(record_id)
    legend()
    xlabel("Residue")
    ylabel("Hydrophobicity")
    grid(True)
    show()

# This script is designed to allow user to review manually
# the putative T3 inc effectors generated by the annotation pipeline
# (specifically, the T3SS_inc_proteins_detection)
# It is not included in the base pipeline as it needs to be interactive.

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--values", required=True, type=str,
        help="file containing the hydropathy values, as generated by the annotation pipeline")

args = parser.parse_args()
val_file = open(args.values, "r")

records_to_keep = []

# parse the values file
line = val_file.readline()
while line:
    assert line[0]==">", "Wrong file format"

    # every record should have the following syntax:
    # >record_id
    # >bilobed_domain_start-bilobed_domain_end
    # val1
    # val2
    # ...
    # valN
    record_id = line[1:].rstrip()
    line = val_file.readline()

    assert line[0]==">", "Wrong file format"
    bilobed_domain_indices = [int(i) for i in line[1:].split("-")]
    line = val_file.readline()
    values = []
    while line and line[0]!=">":
        values.append(float(line))
        line = val_file.readline()

    draw_hydropathy_plot(record_id, values, bilobed_domain_indices)
    user_input = ""
    while user_input!="Y" and user_input!="N" and user_input!="R":
        user_input = input("Keep as an effector ? (Y/N/(R)echeck) : ")
        if user_input=="R":
            draw_hydropathy_plot(record_id, values, bilobed_domain_indices)
            user_input = ""

    if user_input == "Y":
        records_to_keep.append(record_id)

output_file = open(args.values + "_selected", "w")
output_file.write("Manually selectec Inc proteins\n")
output_file.write("\n".join(records_to_keep))
