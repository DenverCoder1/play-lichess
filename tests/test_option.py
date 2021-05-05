from play_lichess.constants import Color, TimeMode, Variant


def test_option_find():
    # Variants
    assert Variant.find("Standard") == Variant.STANDARD
    assert Variant.find("Crazyhouse") == Variant.CRAZYHOUSE
    assert Variant.find("Chess 960") == Variant.CHESS960
    assert Variant.find("King of the Hill") == Variant.KING_OF_THE_HILL
    assert Variant.find("Three-check") == Variant.THREE_CHECK
    assert Variant.find("Antichess") == Variant.ANTICHESS
    assert Variant.find("Atomic") == Variant.ATOMIC
    assert Variant.find("Horde") == Variant.HORDE
    assert Variant.find("Racing Kings") == Variant.RACING_KINGS
    assert Variant.find("From Position") == Variant.FROM_POSITION

    # Time modes
    assert TimeMode.find("Real-time") == TimeMode.REALTIME
    assert TimeMode.find("Correspondence") == TimeMode.CORRESPONDENCE
    assert TimeMode.find("Unlimited") == TimeMode.UNLIMITED

    # Colors
    assert Color.find("White") == Color.WHITE
    assert Color.find("Black") == Color.BLACK
    assert Color.find("Random") == Color.RANDOM
