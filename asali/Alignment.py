
from copy import deepcopy

from Directions import Directions

class Alignment:
    def __init__(
        self,
        seq_1,
        seq_2,
        score,
        path=None,
        cursor=(0, 0),
        cursor_path=[(0, 0)],
        is_gap_1_open=False,
        is_gap_2_open=False
    ):
        self._seq_1 = seq_1
        self._seq_2 = seq_2
        self.score = score
        self.path = path or []
        self.cursor = cursor
        self.cursor_path = cursor_path
        self.is_gap_1_open = is_gap_1_open
        self.is_gap_2_open = is_gap_2_open
        self._str = None

    def add_direction(self, direction):

        if direction == Directions.MATCH:
            new_cursor = (self.cursor[0] + 1, self.cursor[1] + 1)
        elif direction == Directions.GAP_1:
            new_cursor = (self.cursor[0] + 1, self.cursor[1])
        elif direction == Directions.GAP_2:
            new_cursor = (self.cursor[0], self.cursor[1] + 1)

        self.cursor = new_cursor
        self.cursor_path.append(new_cursor)
        self.path.append(direction)

    @classmethod
    def copy(
        cls,
        o,
        score=None,
        path=None,
        cursor=None,
        cursor_path=None,
        is_gap_1_open=None,
        is_gap_2_open=None,
    ):
        if score is None:
            score = o.score

        if path is None:
            path = deepcopy(o.path)

        if cursor is None:
            cursor = deepcopy(o.cursor)

        if cursor_path is None:
            cursor_path = deepcopy(o.cursor_path)

        if is_gap_1_open is None:
            is_gap_1_open = o.is_gap_1_open

        if is_gap_2_open is None:
            is_gap_2_open = o.is_gap_2_open

        return cls(
            seq_1=o._seq_1,
            seq_2=o._seq_2,
            score=score,
            path=path,
            cursor=cursor,
            cursor_path=cursor_path,
            is_gap_1_open=is_gap_1_open,
            is_gap_2_open=is_gap_2_open,
        )

    def __eq__(self, o):
        if isinstance(o, (int, float)):
            if self.score == o:
                return True
            return False

        if self.score == o.score:
            return True

        return False

    def __gt__(self, o):
        if isinstance(o, (int, float)):
            if self.score > o:
                return True

            return False

        if self.score > o.score:
            return True

        return False

    def __lt__(self, o):
        if isinstance(o, (int, float)):
            if self.score < o:
                return True

            return False

        if self.score < o.score:
            return True

        return False

    def __str__(self):

        if self._str is None:
            self._construct_str()

        return self._str

    def _construct_str(self):
        
        cursor_1 = 0
        cursor_2 = 0

        alignment_1 = ""
        alignment_2 = ""

        seperator = ""
        align_counter = 0

        for direction in self.path:
            if direction == Directions.GAP_1:
                alignment_1 += "-"
                alignment_2 += self._seq_2[cursor_2]
                seperator += " "
                cursor_2 += 1
            elif direction == Directions.GAP_2:
                alignment_1 += self._seq_1[cursor_1]
                alignment_2 += "-"
                cursor_1 += 1
                seperator += " "
            else:
                alignment_1 += self._seq_1[cursor_1]
                alignment_2 += self._seq_2[cursor_2]

                if self._seq_1[cursor_1] != self._seq_2[cursor_2]:
                    seperator += " "
                else:
                    seperator += "|"
                    align_counter += 1

                cursor_1 += 1
                cursor_2 += 1

        self._str = '\n'
        self._str += alignment_1
        self._str += '\n'
        self._str += seperator
        self._str += '\n'
        self._str += alignment_2
        self._str += '\n\n'
        self._str += f"Alignment score: {float(self.score):.1f}"
        self._str += '\n'
        self._str += f"Identity value: {float(align_counter / len(seperator) * 100):.1f}%"
        self._str += '\n'