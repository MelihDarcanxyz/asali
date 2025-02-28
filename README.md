# asali
A Simple sequence ALIgner

## Overview

asali is a Python package for aligning biological sequences using dynamic programming. It supports gap penalties and customizable scoring matrices. The tool provides flexibility in defining custom scoring matrices through either file-based or dictionary-based configurations.

## Features

- Sequence alignment with support for gap penalties
- Customizable scoring matrices
- File-based configuration for scoring matrices (see [Scoring Matrix Format](#scoring-matrix-format))
- Dynamic programming approach for optimal alignments

## Installation

To install the package and its dependencies, use poetry:

```bash
poetry install asali
```

## Usage

### Initializing SequenceAligner

You can initialize `SequenceAligner` with either a scoring matrix file or dictionary. Here are two examples:

#### From File:
```python
from asali.SequenceAligner import SequenceAligner

aligner = SequenceAligner.from_file(
    "scoring_matrix.txt", 
    gap_open=-5,  # Penalty for opening gaps
    gap_extend=-1  # Penalty for extending gaps
)
```

#### From Dictionary:
```python
scoring_matrix = {
    frozenset({'A', 'G'}): 1,
    frozenset({'A', 'T'}): -3,
    # ... other scores
}

aligner = SequenceAligner(scoring_matrix, gap_open=5, gap_extend=1)
```

### Performing Alignment

```python
alignment_results = aligner.align("ATGC", "AGCT")
```

### Getting Best Alignment

```python
best_alignment = max(alignment_results, key=lambda a: a.score)
print(best_alignment.alignment)  # e.g., 'ATG-C' and 'A-GCT'
```

### CLI Usage

```bash
python asali/main.py "AGGCT" "AGCT" examples/matrices/BLOSUM62 -5 -1

[], [-], [A], [G], [G], [C], [T], 
[-], [    0], [   -5], [   -6], [   -7], [   -8], [   -9], 
[A], [   -5], [    4], [   -1], [   -2], [   -3], [   -4], 
[G], [   -6], [   -1], [   10], [    5], [    4], [    3], 
[C], [   -7], [   -2], [    5], [    7], [   14], [    9], 
[T], [   -8], [   -3], [    4], [    3], [    9], [   19], 

Found 1 possible alignments:

AGGCT
|| ||
AG-CT

Alignment score: 19.0
Identity value: 80.0%
```

## Scoring Matrix Format

The scoring matrix file should be formatted with words on the first line followed by scores in subsequent lines. Each word represents a sequence element (e.g., DNA nucleotides or protein amino acids), and each value represents the score for that pair.

### Example:
```
   A  G  C  T
A  1 -3  2  0
G -3  5  7 -2
C  2  7  8  6
T  0 -2  6  4
```

### Notes:
- The matrix is symmetric, so the value for `frozenset({'A', 'G'})` will be the same as `frozenset({'G', 'A'})`.
- Only include scores on subsequent lines corresponding to the words listed in the header.
