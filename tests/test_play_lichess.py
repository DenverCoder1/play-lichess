__import__("sys").path.append(".")
from play_lichess import Match, RealTimeMatch, CorrespondenceMatch
from play_lichess.types import TimeControlType, TimeMode, Variant, Color
from play_lichess.exceptions import BadArgumentError, HttpError

import pytest


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
    assert match.time_control.type == TimeControlType.CLOCK
    assert match.time_control.limit == 6 * 60
    assert match.time_control.increment == 0
    assert match.time_control.show == "6+0"
    assert match.color == Color.RANDOM


async def test_create_unlimited():
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
    assert match.time_control.type == TimeControlType.UNLIMITED
    assert match.time_control.limit is None
    assert match.time_control.increment is None
    assert match.time_control.show is None
    assert match.color == Color.WHITE
    assert match.name == "Test"

async def test_create_rated():
    match = await RealTimeMatch.create(
        clock_limit=6 * 60,
        clock_increment=0,
        variant=Variant.STANDARD,
        rated=True,
    )

async def test_create_unlimited_rated():
    with pytest.raises(HttpError):
        match = await CorrespondenceMatch.create(
            variant=Variant.STANDARD,
            rated=False,
            name="Test",
        )



async def test_real_time_lower_bound_minutes():
    with pytest.raises(BadArgumentError):
        await RealTimeMatch.create(
            clock_limit=0,
            clock_increment=0,
            variant=Variant.STANDARD,
        )


async def test_real_time_upper_bound_minutes():
    with pytest.raises(BadArgumentError):
        await RealTimeMatch.create(
            clock_limit=10800,
            clock_increment=0,
            variant=Variant.STANDARD,
        )


async def test_real_time_lower_bound_increment():
    with pytest.raises(BadArgumentError):
        await RealTimeMatch.create(
            clock_limit=6 * 60,
            clock_increment=-1,
            variant=Variant.STANDARD,
        )


async def test_real_time_upper_bound_increment():
    with pytest.raises(BadArgumentError):
        await RealTimeMatch.create(
            clock_limit=6 * 60,
            clock_increment=60,
            variant=Variant.STANDARD,
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_real_time())
    asyncio.run(test_create_unlimited())
    asyncio.run(test_real_time_lower_bound_minutes())
    asyncio.run(test_real_time_upper_bound_minutes())
    asyncio.run(test_real_time_lower_bound_increment())
    asyncio.run(test_real_time_upper_bound_increment())
