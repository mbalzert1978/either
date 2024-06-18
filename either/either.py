from __future__ import annotations

import dataclasses
import functools
import typing

TOk = typing.TypeVar("TOk")
TErr = typing.TypeVar("TErr")
T = typing.TypeVar("T")
P = typing.ParamSpec("P")


class EitherError(Exception):
    """Either base exception."""


class PrivateConstructorError(EitherError):
    """Either cannot be both Ok and Err at the same time."""


class UnreachableError(EitherError):
    """Either is in an invalid state."""


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class Either(typing.Generic[TOk, TErr]):
    """
    A disjoint union type that can hold either an Ok value or an Err value.

    Attributes:
        ok (Optional[TOk]): The Ok value.
        err (Optional[TErr]): The Err value.
        is_ok (bool): A flag indicating whether the instance is Ok.

    Methods:
        Ok(ok: TOk) -> "Either[TOk, TErr]":
            Creates an instance of Either with an Ok value.

        Err(err: TErr) -> "Either[TOk, TErr]":
            Creates an instance of Either with an Err value.

        match(
            left: typing.Callable[[TOk], T],
            right: typing.Callable[[TErr], T],
        ) -> T:
            Matches on the Either instance and applies the appropriate function.
    """

    ok: typing.Optional[TOk]
    err: typing.Optional[TErr]
    is_ok: bool

    def __new__(cls, *args, **kwargs):
        """
        Prevents direct instantiation of Either.

        Raises:
            PrivateConstructorError: Always raised to prevent direct instantiation.
        """
        err = "Use Either.Ok or Either.Err to create an instance."
        raise PrivateConstructorError(err)

    @classmethod
    def Ok(cls, ok: TOk) -> "Either[TOk, TErr]":
        """
        Creates an instance of Either with an Ok value.

        Args:
            ok (TOk): The Ok value.

        Returns:
            Either[TOk, TErr]: An instance of Either with the Ok value.

        Examples:
            >>> result = Either.Ok(42)
            >>> result.is_ok
            True
            >>> result.ok
            42
            >>> result.err is None
            True
        """
        instance = object.__new__(cls)
        object.__setattr__(instance, "err", None)
        object.__setattr__(instance, "ok", ok)
        object.__setattr__(instance, "is_ok", True)
        return instance

    @classmethod
    def Err(cls, err: TErr) -> "Either[TOk, TErr]":
        """
        Creates an instance of Either with an Err value.

        Args:
            err (TErr): The Err value.

        Returns:
            Either[TOk, TErr]: An instance of Either with the Err value.

        Examples:
            >>> error = Either.Err("An error occurred")
            >>> error.is_ok
            False
            >>> error.err
            'An error occurred'
            >>> error.ok is None
            True
        """
        instance = object.__new__(cls)
        object.__setattr__(instance, "err", err)
        object.__setattr__(instance, "ok", None)
        object.__setattr__(instance, "is_ok", False)
        return instance

    def match(
        self,
        ok_fn: typing.Callable[[TOk], T],
        err_fn: typing.Callable[[TErr], T],
    ) -> T:
        """
        Matches on the Either instance and applies the appropriate function.

        Args:
            ok_fn (typing.Callable[[TOk], T]): Function to apply if the instance is Ok.
            err_fn (typing.Callable[[TErr], T]): Function to apply if the instance is Err.

        Returns:
            T: The result of applying the appropriate function.

        Raises:
            UnreachableError: If the Either instance is in an invalid state.

        Examples:
            >>> result = Either.Ok(42)
            >>> result.match(
            ...     ok_fn=lambda ok: f"Success: {ok}",
            ...     err_fn=lambda err: f"Error: {err}"
            ... )
            'Success: 42'

            >>> error = Either.Err("An error occurred")
            >>> error.match(
            ...     ok_fn=lambda ok: f"Success: {ok}",
            ...     err_fn=lambda err: f"Error: {err}"
            ... )
            'Error: An error occurred'
        """
        match (self.is_ok, self.ok, self.err):
            case (True, _ok, None) if _ok is not None:
                return ok_fn(_ok)
            case (False, None, _err) if _err is not None:
                return err_fn(_err)
            case _:
                err = "Either is in an invalid state."
                raise UnreachableError(err)


def as_either(
    fn: typing.Callable[P, T],
) -> typing.Callable[P, Either[T, Exception]]:
    """
    Wraps a function to return an Either instance.

    Args:
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Either[T, Exception]: An Either instance containing the result of the function or an exception.

    Examples:
        >>> @as_either
        ... def divide(a: int, b: int) -> float:
        ...     return a / b
        ...
        >>> result = divide(4, 2)
        >>> result.is_ok
        True
        >>> result.ok
        2.0
        >>> result.err is None
        True

        >>> error = divide(4, 0)
        >>> error.is_ok
        False
        >>> isinstance(error.err, ZeroDivisionError)
        True
    """

    @functools.wraps(fn)
    def inner(*args: P.args, **kwargs: P.kwargs) -> Either[T, Exception]:
        try:
            return Either.Ok(fn(*args, **kwargs))
        except Exception as exc:
            return Either.Err(exc)

    return inner


def as_async_either(
    fn: typing.Callable[P, typing.Awaitable[T]],
) -> typing.Callable[P, typing.Awaitable[Either[T, Exception]]]:
    """
    Wraps an async function to return an Either instance.

    Args:
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Either[T, Exception]: An Either instance containing the result of the function or an exception.

    Examples:
        >>> @as_async_either
        ... async def async_divide(a: int, b: int) -> float:
        ...     return a / b
        ...
        >>> import asyncio
        >>> result = asyncio.run(async_divide(4, 2))
        >>> result.is_ok
        True
        >>> result.ok
        2.0
        >>> result.err is None
        True

        >>> error = asyncio.run(async_divide(4, 0))
        >>> error.is_ok
        False
        >>> isinstance(error.err, ZeroDivisionError)
        True
    """

    @functools.wraps(fn)
    async def inner(*args: P.args, **kwargs: P.kwargs) -> Either[T, Exception]:
        try:
            return Either.Ok(await fn(*args, **kwargs))
        except Exception as exc:
            return Either.Err(exc)

    return inner
