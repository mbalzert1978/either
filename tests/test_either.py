import typing

import pytest

from either.either import Either, PrivateConstructorError, as_async_either, as_either

ERR = "Should not have been called."


def fail(_failure: typing.Any) -> None:
    pytest.fail(ERR)


@pytest.mark.parametrize(
    "either, ok_fn, err_fn, expected",
    [
        (Either[int, str].Ok(10), str, fail, "10"),
        (Either[int, str].Err("10"), fail, int, 10),
    ],
)
def test_match_with_incorrect_argument_types(
    either: Either,
    ok_fn,
    err_fn,
    expected,
) -> None:
    result = either.match(ok_fn, err_fn)
    assert result == expected


def test_either_cannot_be_both_ok_and_err_at_the_same() -> None:
    expected = "Use Either.Ok or Either.Err to create an instance."
    with pytest.raises(PrivateConstructorError, match=expected):
        Either[int, str](ok=10, err="10", is_ok=False)


def test_factories() -> None:
    assert Either[int, str].Ok(10) == Either.Ok(10)
    assert Either[int, str].Err("10") == Either.Err("10")


def test_as_either() -> None:
    @as_either
    def divide(a: int, b: int) -> float:
        return a / b

    result = divide(4, 2)
    assert result.is_ok
    assert result.ok == 2.0
    assert result.err is None

    error = divide(4, 0)
    assert not error.is_ok
    assert isinstance(error.err, ZeroDivisionError)


@pytest.mark.asyncio
async def test_as_async_either() -> None:
    @as_async_either
    async def async_divide(a: int, b: int) -> float:
        return a / b

    result = await async_divide(4, 2)
    assert result.is_ok
    assert result.ok == 2.0
    assert result.err is None

    error = await async_divide(4, 0)
    assert not error.is_ok
    assert isinstance(error.err, ZeroDivisionError)
