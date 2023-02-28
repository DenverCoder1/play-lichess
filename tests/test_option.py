from play_lichess.types import Color, TimeControlType, TimeMode, Variant


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

    # Time control types
    assert TimeControlType.find("Unlimited") == TimeControlType.UNLIMITED
    assert TimeControlType.find("Clock") == TimeControlType.CLOCK


def test_option_find_by_data():
    # Variants
    assert Variant.find_by_data("standard") == Variant.STANDARD
    assert Variant.find_by_data("crazyhouse") == Variant.CRAZYHOUSE
    assert Variant.find_by_data("chess960") == Variant.CHESS960
    assert Variant.find_by_data("kingOfTheHill") == Variant.KING_OF_THE_HILL
    assert Variant.find_by_data("threeCheck") == Variant.THREE_CHECK
    assert Variant.find_by_data("antichess") == Variant.ANTICHESS
    assert Variant.find_by_data("atomic") == Variant.ATOMIC
    assert Variant.find_by_data("horde") == Variant.HORDE
    assert Variant.find_by_data("racingKings") == Variant.RACING_KINGS

    # Time modes
    assert TimeMode.find_by_data("ultraBullet") == TimeMode.ULTRABULLET
    assert TimeMode.find_by_data("bullet") == TimeMode.BULLET
    assert TimeMode.find_by_data("blitz") == TimeMode.BLITZ
    assert TimeMode.find_by_data("rapid") == TimeMode.RAPID
    assert TimeMode.find_by_data("classical") == TimeMode.CLASSICAL
    assert TimeMode.find_by_data("correspondence") == TimeMode.CORRESPONDENCE

    # Colors
    assert Color.find_by_data("white") == Color.WHITE
    assert Color.find_by_data("black") == Color.BLACK
    assert Color.find_by_data("random") == Color.RANDOM

    # Time control types
    assert TimeControlType.find_by_data("unlimited") == TimeControlType.UNLIMITED
    assert TimeControlType.find_by_data("clock") == TimeControlType.CLOCK
    assert (
        TimeControlType.find_by_data("correspondence") == TimeControlType.CORRESPONDENCE
    )
