from helpers import Position


def test_addition():
    pos1, pos2 = Position(-1, 0), Position(1, 1)
    pos = pos1 + pos2
    if pos != [0, 1]: raise Exception()
test_addition()