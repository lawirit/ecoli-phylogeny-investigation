#!/usr/bin/env python3
"""
Phylogenetic tree construction script.
Reads a multiple sequence alignment and builds a Neighbor-Joining tree.
"""

import sys
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Phylo import write

def main():
    alignment_file = "alignment.aln"
    try:
        alignment = AlignIO.read(alignment_file, "fasta")  # assuming fasta format
    except FileNotFoundError:
        sys.stderr.write(f"Error: alignment file '{alignment_file}' not found.\n")
        sys.exit(1)
    except ValueError as e:
        sys.stderr.write(f"Error reading alignment: {e}\n")
        sys.exit(1)
    
    print(f"Alignment loaded: {len(alignment)} sequences, length {alignment.get_alignment_length()}")
    
    # Calculate distance matrix using identity (or other model)
    calculator = DistanceCalculator('identity')
    distance_matrix = calculator.get_distance(alignment)
    
    # Construct Neighbor-Joining tree
    constructor = DistanceTreeConstructor(calculator, 'nj')
    tree = constructor.build_tree(alignment)
    
    # Save tree in Newick format
    output_file = "phylogeny.tree"
    with open(output_file, 'w') as out_handle:
        write(tree, out_handle, 'newick')
    
    print(f"Phylogenetic tree saved as '{output_file}'.")
    
    # Print a simple text representation
    print("\nTree structure (ASCII):")
    from Bio.Phylo import draw_ascii
    draw_ascii(tree)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())