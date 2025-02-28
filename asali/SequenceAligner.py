
from contextlib import suppress
from math import inf

from ScoringMatrix import ScoringMatrix
from Alignment import Alignment
from Directions import Directions


class SequenceAligner:
    def __init__(self, scoring_matrix: dict[frozenset[str], int], gap_open: int, gap_extend: int) -> None:
        """Initialize the SequenceAligner with a scoring matrix and gap penalties.
        
        Args:
            scoring_matrix: Dictionary mapping amino acid pairs to their scores
            gap_open: Penalty for opening a new gap in the alignment
            gap_extend: Penalty for extending an existing gap
        """
        self.scoring_matrix = scoring_matrix
        self.gap_open: int = gap_open
        self.gap_extend: int = gap_extend

    def align(self, seq_1: str, seq_2: str) -> list:
        """Align two sequences using dynamic programming.
        
        Args:
            seq_1: First input sequence
            seq_2: Second input sequence
            
        Returns:
            List of aligned tuples containing matched segments and their scores
        """

        width = len(seq_1) + 1
        height = len(seq_2) + 1

        score_table = [[-inf for i in range(width)] for j in range(height)]
        score_table[0][0] = 0
        alignments = [Alignment(seq_1=seq_1, seq_2=seq_2, score=0)]

        while True:
            alignments_to_remove = []
            alignments_to_append = []
            is_complete = True

            for index, alignment in enumerate(alignments):
                i, j = alignment.cursor
                if alignment < score_table[i][j]:
                    alignments_to_remove.append(index)

            while alignments_to_remove:
                index = alignments_to_remove.pop()
                alignments_to_remove = [i - 1 if i >= index else i for i in alignments_to_remove]
                alignments.pop(index)

            alignments_to_remove = []

            for index, alignment in enumerate(alignments):
                i, j = alignment.cursor
                current_score = score_table[i][j]

                with suppress(IndexError):
                    
                    # GAP_1

                    target_score = score_table[i + 1][j]
                    score_delta = (
                        self.gap_extend if alignment.is_gap_1_open else self.gap_open
                    )
                    possible_score = current_score + score_delta

                    if possible_score >= target_score:
                        score_table[i + 1][j] = possible_score
                        alignment_copy = Alignment.copy(
                            alignment,
                            score=possible_score,
                            is_gap_1_open=True,
                            is_gap_2_open=False
                        )
                        alignment_copy.add_direction(Directions.GAP_1)
                        alignments_to_append.append(alignment_copy)

                    # GAP_2
                    
                    target_score = score_table[i][j + 1]
                    score_delta = (
                        self.gap_extend if alignment.is_gap_2_open else self.gap_open
                    )
                    possible_score = current_score + score_delta

                    if possible_score >= target_score:
                        score_table[i][j + 1] = possible_score
                        alignment_copy = Alignment.copy(
                            alignment,
                            score=possible_score,
                            is_gap_1_open=False,
                            is_gap_2_open=True,
                        )
                        alignment_copy.add_direction(Directions.GAP_2)
                        alignments_to_append.append(alignment_copy)


                    # MATCH
                    target_score = score_table[i + 1][j + 1]
                    score_delta = self.scoring_matrix.score(seq_1[j], seq_2[i])
                    possible_score = current_score + score_delta

                    if possible_score >= target_score:
                        score_table[i + 1][j + 1] = possible_score
                        alignment_copy = Alignment.copy(
                            alignment,
                            score=possible_score,
                            is_gap_1_open=False,
                            is_gap_2_open=False,
                        )
                        alignment_copy.add_direction(Directions.MATCH)
                        alignments_to_append.append(alignment_copy)

                if alignment.cursor != (height - 1, width - 1):
                    alignments_to_remove.append(index)

            while alignments_to_remove:
                index = alignments_to_remove.pop()
                alignments_to_remove = [i - 1 if i >= index else i for i in alignments_to_remove]
                alignments.pop(index)

            alignments.extend(alignments_to_append)

            for alignment in alignments:
                if alignment.cursor != (height - 1, width - 1):
                    is_complete = False

            if is_complete:
                break
            
        alignments = self._prune_alignments(alignments, score_table)
        # alignments = self._remove_duplicate_alignments(alignments)

        seq_1 = "-" + seq_1
        seq_2 = "-" + seq_2

        print("[], ", end="")
        for char in seq_1:
            print(f"[{char}], ", end="")
        print()

        for i, row in enumerate(score_table):
            print(f"[{seq_2[i]}], ", end="")
            for number in row:
                number_str = str(number)
                while len(number_str) < 5:
                    number_str = " " + number_str
                print(f"[{number_str}], ", end="")
            print()

        return alignments

    def _prune_alignments(self, alignments, score_table):
        """Remove low-scoring or redundant alignments from the results.
        
        Args:
            alignments: Current list of alignments to prune
            score_table: Dictionary mapping alignment positions to scores
        """
        max_i = len(score_table) - 1
        max_j = len(score_table[0]) - 1
        cursors_to_visit = [(max_i, max_j)]

        while cursors_to_visit:

            cursor = cursors_to_visit[0]

            if cursor == (0, 0):
                cursors_to_visit.pop(0)
                continue

            max_alignments_idxs = []
            max_alignment_prev_score = None
            alignments_to_remove = []

            for idx, alignment in enumerate(alignments):

                try:
                    alignment_cursor_idx = alignment.cursor_path.index(cursor)
                except ValueError:
                    continue

                alignment_prev_cursor = alignment.cursor_path[alignment_cursor_idx - 1]
                alignment_prev_score = score_table[alignment_prev_cursor[0]][alignment_prev_cursor[1]]

                if not max_alignments_idxs or alignment_prev_score > max_alignment_prev_score:
                    
                    for max_alignments_idx in max_alignments_idxs:
                        alignments_to_remove.append(max_alignments_idx)

                    max_alignments_idxs = [idx]
                    max_alignment_prev_score = alignment_prev_score

                elif alignment_prev_score == max_alignment_prev_score:
                    max_alignments_idxs.append(idx)

                else:
                    alignments_to_remove.append(idx)
            
            while alignments_to_remove:
                index = alignments_to_remove.pop()
                alignments_to_remove = [i - 1 if i >= index else i for i in alignments_to_remove]
                max_alignments_idxs = [i - 1 if i >= index else i for i in max_alignments_idxs]
                alignments.pop(index)

            for idx in alignments_to_remove:
                alignments.remove(alignment)
            
            cursors_to_add = set()

            for max_alignments_idx in max_alignments_idxs:

                try:
                    alignment_cursor_idx = alignments[max_alignments_idx].cursor_path.index(cursor)
                except ValueError:
                    continue

                alignment_prev_cursor = alignments[max_alignments_idx].cursor_path[alignment_cursor_idx - 1]

                cursors_to_add.add(alignment_prev_cursor)
            
            cursors_to_visit.extend(list(cursors_to_add))
            cursors_to_visit.pop(0)

        return alignments

    def _remove_duplicate_alignments(self, alignments):
        """Eliminate duplicate alignments from the results.
        
        Args:
            alignments: List of potential duplicate alignments
        """

        idx = 0

        while idx < len(alignments) - 1:
            
            reference_alignment = alignments[idx]
            alignments_to_remove = []

            for alignment in alignments[idx + 1:]:
                if alignment.cursor_path == reference_alignment.cursor_path:
                    alignments_to_remove.append(alignment)
            
            for alignment in alignments_to_remove:
                alignments.remove(alignment)

            idx += 1

        return alignments

    @classmethod
    def from_file(cls, file_path: str, gap_open: int, gap_extend: int) -> "SequenceAligner":
        """Create an instance from a scoring matrix file.
        
        Args:
            file_path: Path to the scoring matrix text file
            gap_open: Penalty for opening gaps
            gap_extend: Penalty for extending gaps
            
        Returns:
            SequenceAligner instance loaded with the provided parameters
        """
        scoring_matrix = ScoringMatrix.from_file(file_path)
        return cls(scoring_matrix, gap_open, gap_extend)

    @staticmethod
    def print_alignments(alignments: list) -> None:
        """Print formatted alignment results to standard output.
        
        Args:
            alignments: List of Alignment objects to print
        """
        print()
        print(f"Found {len(alignments)} possible alignments:")

        for i, alignment in enumerate(alignments):

            print(str(alignment))

            if i != (len(alignments) - 1):
                print(20 * '-')
