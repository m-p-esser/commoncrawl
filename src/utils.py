"""Random Utility functions """

import functools
import time

from dotenv import dotenv_values


def timer(func):
    """Track time of a function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        """Track time"""
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Function {func.__name__!r} took {duration:.4f} seconds to complete.")
        return value

    return wrapper_timer


def load_env_variables() -> dict:
    """Load Environment variables into memory"""
    environment = dotenv_values("make/.env")
    ENV = environment["ENV"]  # dev, test or prod

    base_env_variables = dotenv_values(
        f"make/base.env"
    )  # used across enviroments (dev, test, prod)
    env_variables = dotenv_values(f"make/{ENV}.env")  # environment specific variables
    env_variables.update(base_env_variables)  # Combine both

    return env_variables
