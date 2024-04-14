from typing import Callable
import functools


def compose(*functions):
    """Function composition with functools.reduce"""
    return functools.reduce(
        lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs), **kwargs), functions
    )


def bucket_local_vars(_locals: dict):
    """Separate callables from locals dictionary."""
    ### extract, remove keyword arguments from local scope
    _kwargs = _locals.get("kwargs")
    del _locals["kwargs"]

    ### extract, remove callables from local scope
    # TODO: consider removing ignore function from here to potentially
    # TODO: (continued) avoid attribute overhead in tidyworkflow
    _callables = {k: v for k, v in _locals.items() if isinstance(v, Callable)}
    for callable in _callables:
        del _locals[callable]

    ### return groups of objects
    return _locals, _kwargs, _callables
