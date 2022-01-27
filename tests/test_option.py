from play_lichess.types import Color, TimeMode, Variant


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

    # Time modes
    assert TimeMode.find("Ultra-Bullet") == TimeMode.ULTRABULLET
    assert TimeMode.find("Bullet") == TimeMode.BULLET
    assert TimeMode.find("Blitz") == TimeMode.BLITZ
    assert TimeMode.find("Rapid") == TimeMode.RAPID
    assert TimeMode.find("Classical") == TimeMode.CLASSICAL
    assert TimeMode.find("Correspondence") == TimeMode.CORRESPONDENCE

    # Colors
    assert Color.find("White") == Color.WHITE
    assert Color.find("Black") == Color.BLACK
    assert Color.find("Random") == Color.RANDOM
