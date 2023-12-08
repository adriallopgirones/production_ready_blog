"""
Some decorators used across the project
"""
import logging
from functools import wraps

import redis

logger = logging.getLogger(__name__)


def catch_redis_down(cache_decorator):
    """
    If we decorate a view the cache_page decorator and redis is down, the view will return a 500 error
    because it can't connect to redis, this decorator will catch the exception and return the view
    without caching
    inspiration: https://stackoverflow.com/questions/73272716/wrap-python-decorator-in-try-except
    """

    def decorator(view_func):
        cache_decorated_view_func = cache_decorator(view_func)

        @wraps(view_func)
        def wrapper(*args, **kwargs):
            try:
                return cache_decorated_view_func(*args, **kwargs)
            except redis.ConnectionError:
                logger.error(
                    f"Redis is down, returning view without caching in: {view_func.__name__}"
                )
                return view_func(*args, **kwargs)

        return wrapper

    return decorator
