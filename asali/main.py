import argparse
from SequenceAligner import SequenceAligner

def main(args):
    """Align two amino acid sequences using the provided scoring matrix and gap penalties."""
    sa = SequenceAligner.from_file(args.scoring_matrix, args.gap_open_penalty, args.gap_extend_penalty)
    alignments = sa.align(args.sequence_1, args.sequence_2)
    SequenceAligner.print_alignments(alignments)

if __name__ == "__main__":
    """Parse command line arguments and execute the sequence alignment."""
    parser = argparse.ArgumentParser(prog="asali", description='Align amino acid sequences.')

    parser.add_argument('sequence_1', type=str, help='First sequence to align')
    parser.add_argument('sequence_2', type=str, help='Second sequence to align')
    parser.add_argument('scoring_matrix', type=str, help='Path of the scoring matrix')
    parser.add_argument('gap_open_penalty', type=int, help='Penaly to open a gap in the sequence')
    parser.add_argument('gap_extend_penalty', type=int, help='Penaly to extend a gap in the sequence')

    args = parser.parse_args()

    main(args)