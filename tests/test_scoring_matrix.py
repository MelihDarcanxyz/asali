from asali.ScoringMatrix import ScoringMatrix

def test_scoring_matrix():
    scoring_matrix = ScoringMatrix.from_file("examples/matrices/BLOSUM62")

    assert scoring_matrix.score("A", "A") == 4
    assert scoring_matrix.score("I", "Q") == -3
    assert scoring_matrix.score("*", "F") == -4
    assert scoring_matrix.score("V", "C") == -1
    assert scoring_matrix.score("M", "K") == -1
