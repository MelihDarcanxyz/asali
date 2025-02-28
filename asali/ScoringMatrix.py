
class ScoringMatrix:
    def __init__(self, matrix: dict[frozenset[str], int]) -> None:
        """Initialize a scoring matrix with a given dictionary of word pairs and scores.

        Args:
            matrix (dict[frozenset[str], int]): A dictionary where keys are frozensets of two words
                and values are the corresponding scores for those word pairs.
        """
        self._data = matrix

    def score(self, word_1: str, word_2: str) -> int:
        """Get the score between two words from the scoring matrix.
        Args:
            word_1 (str): The first word
            word_2 (str): The second word

        Returns:
            int: The score associated with the pair of words

        Examples:
            >>> matrix = ScoringMatrix.from_file("path/to/matrix.txt")
            >>> matrix.score("word1", "word2")  # returns the corresponding score
        """
        return self._data[frozenset((word_1, word_2))]

    @classmethod
    def from_file(cls, file_path: str) -> "ScoringMatrix":
        """Create a scoring matrix from a given file path.
        Args:
            file_path (str): Path to the text file containing the scoring matrix

        Returns:
            ScoringMatrix: An instance of the ScoringMatrix class loaded with data from the file

        The expected format of the file is:
        - Each line represents a row in the matrix
        - Words are separated by spaces
        - Empty lines and lines starting with '#' are ignored
        """
        with open(file_path) as f:
            matrix = cls._parse_text(f.read())
        return cls(matrix)

    @classmethod
    def _parse_text(cls, text: str | list) -> dict[frozenset[str], int]:
        """Parse text containing a scoring matrix into a dictionary format.
        Args:
            text (str | list): Input text, either as a single string or list of lines
        Returns:
            dict[frozenset[str], int]: Dictionary mapping word pairs to scores

        Notes:
            - The first line contains the words that form the headers
            - Subsequent lines contain the scores for each word pair
            - Empty lines and lines starting with '#' are ignored
        """
        if not isinstance(text, list):
            text = text.splitlines()

        matrix: dict = {}
        words: tuple = (None,)
        cursor: int = 0

        for line in text:
            if not line or line.startswith("#"):
                continue

            line_list: list = line.split()

            if cursor == 0:
                words = tuple(line_list)
                cursor += 1
                continue

            for i in range(cursor, len(words) + 1):
                word_1 = words[cursor - 1]
                word_2 = words[i - 1]
                key = frozenset((word_1, word_2))

                matrix[key] = int(line_list[i])

            cursor += 1

        return matrix
