# Either

A Python implementation of the `Either` type, inspired by functional programming paradigms. The `Either` type represents a value that can be one of two possible types (a disjoint union). An instance of `Either` is either an `Ok` (representing success) or an `Err` (representing failure).

## Features

- **Type Safety**: Ensures that an `Either` instance is always in a valid state.
- **Pattern Matching**: Provides a `match` method to handle both `Ok` and `Err` cases.
- **Immutability**: Uses `dataclasses` with `frozen=True` to ensure instances are immutable.

## Installation

To install the dependencies, use [Poetry](https://python-poetry.org/):

```sh
poetry install
```

Sure, here is the updated usage block for the README file:

## Usage

### Creating Instances

You can create instances of `Either` using the `Either.Ok` and `Either.Err` class methods.

```python
from either import Either

# Creating an Ok instance
result = Either.Ok(42)
print(result.is_ok)  # True
print(result.ok)     # 42
print(result.err)    # None

# Creating an Err instance
error = Either.Err("An error occurred")
print(error.is_ok)   # False
print(error.ok)      # None
print(error.err)     # 'An error occurred'
```

### Pattern Matching

You can handle both `Ok` and `Err` cases using the `match` method.

```python
result = Either.Ok(42)
message = result.match(
    left=lambda ok: f"Success: {ok}",
    right=lambda err: f"Error: {err}"
)
print(message)  # 'Success: 42'

error = Either.Err("An error occurred")
message = error.match(
    left=lambda ok: f"Success: {ok}",
    right=lambda err: f"Error: {err}"
)
print(message)  # 'Error: An error occurred'
```

### Wrapping Functions

You can wrap functions to return an `Either` instance using the `as_either` decorator.

```python
from either import as_either

@as_either
def divide(a: int, b: int) -> float:
    return a / b

result = divide(4, 2)
print(result.is_ok)  # True
print(result.ok)     # 2.0
print(result.err)    # None

error = divide(4, 0)
print(error.is_ok)   # False
print(isinstance(error.err, ZeroDivisionError))  # True
```

### Wrapping Async Functions

You can wrap async functions to return an `Either` instance using the `as_async_either` decorator.

```python
import asyncio
from either import as_async_either

@as_async_either
async def async_divide(a: int, b: int) -> float:
    return a / b

result = asyncio.run(async_divide(4, 2))
print(result.is_ok)  # True
print(result.ok)     # 2.0
print(result.err)    # None

error = asyncio.run(async_divide(4, 0))
print(error.is_ok)   # False
print(isinstance(error.err, ZeroDivisionError))  # True
```

## Running Tests

To run the tests, use [pytest](https://pytest.org/):

```sh
poetry run pytest
```

## Project Structure

```
README.md
poetry.lock
pyproject.toml
either
    __init__.py
    either.py
tests
    __init__.py
    test_either.py
```

## License

This project is licensed under the MIT License.
