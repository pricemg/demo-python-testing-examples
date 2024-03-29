from typing import Optional

import pytest
from _pytest.mark.structures import MarkDecorator


class Case:
    """Container for a test case, with optional test ID.

    Attributes
    ----------
        label
            Optional test ID. Will be displayed for each test when
            running `pytest -v`.
        kwargs
            Parameters used for the test cases.

    Examples
    --------
    >>> Case(label="some test name", foo=10, bar="some value")
    >>> Case(foo=99, bar="some other value")   # no name given

    See also
    --------
    source: https://github.com/ckp95/pytest-parametrize-cases

    """

    def __init__(
        self,
        label: Optional[str] = None,
        marks: Optional[MarkDecorator] = None,
        **kwargs,
    ):
        """Initialise objects."""
        self.label = label
        self.kwargs = kwargs
        self.marks = marks
        # Makes kwargs accessible with dot notation.
        self.__dict__.update(kwargs)

    def __repr__(self) -> str:
        """Return string."""
        return f"Case({self.label!r}, **{self.kwargs!r})"


def parametrize_cases(*cases: Case):
    """More user friendly parameterize cases testing.

    See: https://github.com/ckp95/pytest-parametrize-cases
    """
    all_args = set()
    for case in cases:
        if not isinstance(case, Case):
            raise TypeError(f"{case!r} is not an instance of Case")

        all_args.update(case.kwargs.keys())

    argument_string = ",".join(sorted(all_args))

    case_list = []
    ids_list = []
    for case in cases:
        case_kwargs = case.kwargs.copy()
        args = case.kwargs.keys()

        # Make sure all keys are in each case, otherwise initialise with None.
        diff = {k: None for k in set(all_args) - set(args)}
        case_kwargs.update(diff)

        case_tuple = tuple(value for key, value in sorted(case_kwargs.items()))

        # If marks are given, wrap the case tuple.
        if case.marks:
            case_tuple = pytest.param(*case_tuple, marks=case.marks)

        case_list.append(case_tuple)
        ids_list.append(case.label)

    if len(all_args) == 1:
        # otherwise it gets passed to the test function as a singleton tuple
        case_list = [i[0] for i in case_list]

    return pytest.mark.parametrize(
        argnames=argument_string, argvalues=case_list, ids=ids_list
    )
