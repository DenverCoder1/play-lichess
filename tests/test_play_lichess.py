__import__("sys").path.append(".")
import pytest

from play_lichess import CorrespondenceMatch, Match, RealTimeMatch, UnlimitedMatch
from play_lichess.exceptions import BadArgumentError, HttpError
from play_lichess.types import Color, TimeControlType, TimeMode, Variant


@pytest.mark.asyncio
async def test_real_time():
    match = await RealTimeMatch.create(
        clock_limit=6 * 60,
        clock_increment=0,
        variant=Variant.ANTICHESS,
    )

    assert match.status == "created"
    assert match.challenger is None
    assert match.dest_user is None
    assert match.variant == Variant.ANTICHESS
    assert match.rated is False
    assert match.speed == TimeMode.BLITZ
    assert match.time_control is not None
    assert match.time_control.type == TimeControlType.CLOCK
    assert match.time_control.limit == 6 * 60
    assert match.time_control.increment == 0
    assert match.time_control.show == "6+0"
    assert match.color == Color.RANDOM


@pytest.mark.asyncio
async def test_create_unlimited():
    match = await UnlimitedMatch.create(
        variant=Variant.STANDARD,
        name="Test",
    )

    assert match.status == "created"
    assert match.challenger is None
    assert match.dest_user is None
    assert match.variant == Variant.STANDARD
    assert match.rated is False
    assert match.speed == TimeMode.CORRESPONDENCE
    assert match.time_control is not None
    assert match.time_control.type == TimeControlType.UNLIMITED
    assert match.time_control.limit is None
    assert match.time_control.increment is None
    assert match.time_control.show is None
    assert match.color == Color.RANDOM
    assert match.name == "Test"


@pytest.mark.asyncio
async def test_create_correspondence():
    match = await CorrespondenceMatch.create(
        variant=Variant.STANDARD,
        rated=False,
        name="Test",
    )

    assert match.status == "created"
    assert match.challenger is None
    assert match.dest_user is None
    assert match.variant == Variant.STANDARD
    assert match.rated is False
    assert match.speed == TimeMode.CORRESPONDENCE
    assert match.time_control is not None
    assert match.time_control.type == TimeControlType.CORRESPONDENCE
    assert match.time_control.days_per_turn == 1
    assert match.time_control.limit is None
    assert match.time_control.increment is None
    assert match.time_control.show is None
    assert match.color == Color.RANDOM
    assert match.name == "Test"


@pytest.mark.asyncio
async def test_create_rated():
    match = await RealTimeMatch.create(
        clock_limit=10 * 60,
        clock_increment=5,
        variant=Variant.STANDARD,
        rated=True,
    )

    assert match.status == "created"
    assert match.challenger is None
    assert match.dest_user is None
    assert match.variant == Variant.STANDARD
    assert match.rated is True
    assert match.speed == TimeMode.RAPID
    assert match.time_control is not None
    assert match.time_control.type == TimeControlType.CLOCK
    assert match.time_control.limit == 10 * 60
    assert match.time_control.increment == 5
    assert match.time_control.show == "10+5"
    assert match.color == Color.RANDOM


@pytest.mark.asyncio
async def test_real_time_lower_bound_minutes():
    with pytest.raises(HttpError):
        await RealTimeMatch.create(
            clock_limit=0,
            clock_increment=0,
        )


@pytest.mark.asyncio
async def test_real_time_upper_bound_minutes():
    with pytest.raises(HttpError):
        await RealTimeMatch.create(
            clock_limit=10801,
            clock_increment=0,
            variant=Variant.STANDARD,
        )


@pytest.mark.asyncio
async def test_real_time_lower_bound_increment():
    with pytest.raises(HttpError):
        await RealTimeMatch.create(
            clock_limit=6 * 60,
            clock_increment=-1,
            variant=Variant.STANDARD,
        )


@pytest.mark.asyncio
async def test_real_time_upper_bound_increment():
    with pytest.raises(HttpError):
        await RealTimeMatch.create(
            clock_limit=6 * 60,
            clock_increment=181,
            variant=Variant.STANDARD,
        )


@pytest.mark.asyncio
async def test_days_and_limit_or_increment():
    with pytest.raises(BadArgumentError):
        await Match.create(
            days=1,
            clock_limit=6 * 60,
            clock_increment=0,
        )


@pytest.mark.asyncio
async def test_missing_increment():
    with pytest.raises(BadArgumentError):
        await Match.create(
            clock_limit=6 * 60,
            clock_increment=None,
        )


@pytest.mark.asyncio
async def test_missing_limit():
    with pytest.raises(BadArgumentError):
        await Match.create(
            clock_limit=None,
            clock_increment=5,
        )
