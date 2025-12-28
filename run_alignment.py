#!/usr/bin/env python3
"""
Multiple sequence alignment script for phylogenetic analysis.
Uses MAFFT to align FASTA files in the data/ directory.
"""

import os
import sys
from Bio.Align.Applications import MafftCommandline
from Bio import SeqIO

def main():
    # Input directory containing FASTA files
    data_dir = "data"
    if not os.path.isdir(data_dir):
        sys.stderr.write(f"Error: directory '{data_dir}' not found.\n")
        sys.exit(1)
    
    # Collect all FASTA files
    fasta_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir)
                   if f.endswith(('.fasta', '.fa', '.fna'))]
    if not fasta_files:
        sys.stderr.write("Error: no FASTA files found in data/.\n")
        sys.exit(1)
    
    # Create a temporary concatenated input file for MAFFT
    combined_input = "combined_input.fasta"
    with open(combined_input, 'w') as out_handle:
        for fasta in fasta_files:
            for record in SeqIO.parse(fasta, "fasta"):
                # Shorten IDs to avoid MAFFT issues
                record.id = record.id.split('|')[0][:30]
                SeqIO.write(record, out_handle, "fasta")
    
    # Run MAFFT alignment
    # Assuming MAFFT is installed and accessible in PATH
    mafft_cline = MafftCommandline(input=combined_input)
    print(f"Running MAFFT command: {mafft_cline}")
    
    # Execute MAFFT, capture stdout as alignment
    stdout, stderr = mafft_cline()
    
    # Write alignment output
    with open("alignment.aln", "w") as aln_handle:
        aln_handle.write(stdout)
    
    # Clean up temporary file
    os.remove(combined_input)
    
    print("Alignment completed and saved as 'alignment.aln'.")
    return 0

if __name__ == "__main__":
    sys.exit(main())