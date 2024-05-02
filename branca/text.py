"""
Text
----

An abstraction to automatically escape characters.
"""

import re
import warnings
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import List


class _BaseOperations(ABC):
    """An interface for all operations on the `Text` object."""

    def __init__(self):
        pass


class _BaseEscapeOperation(_BaseOperations):
    """Interface for all operations that escape characters in the `Text` object."""

    def __init__(self):
        pass

    @property
    @abstractmethod
    def pattern(self) -> re.Pattern:
        """Pattern used to match the escapable characters."""
        raise NotImplementedError(
            "This is an abstract class. Implement this property in a child class.",
        )

    def check_compliance(self, text_str: str) -> bool:
        """Check whether the provided `text_str` is compliant with the pattern.

        A text string is said to be compliant with an operation when there's no match
        for the provided pattern. Implementing classes can add more conditions to check
        for compliance.

        Implementations of this base class often don't require any special compliance
        check. This default implementation only checks if there's a matching sub-string
        for the provided pattern. If there's a match, it means that `text_str` is not
        yet compliant and `escape()` operation has not yet been applied.

        Parameters
        ----------
        text_str: str
            The string to escape characters from.

        Returns
        -------
        is_compliant: bool
            Returns `True` if the provided `text_str` is already compliant with the
            provided escape operation. Returns `False` is some sub-string
            can be escaped.
        """
        return re.match(self._pattern, text_str) is None

    @abstractmethod
    def escape(self, text_str: str) -> str:
        """Escape the characters matching with the pattern.

        Parameters
        ----------
        text_str: str
            The string to escaped characters from.

        Returns
        -------
        escaped_text: str
            The escaped string.
        """
        raise NotImplementedError(
            "This is an abstract class. Implement this property in a child class.",
        )


class EscapeBackticks(_BaseEscapeOperation):
    """Escape Backticks if they don't come directly after a backslash."""

    def __init__(self):
        self._pattern = re.compile(r"(?<!\\)`")

    @property
    def pattern(self) -> re.Pattern:
        return self._pattern

    def escape(self, text_str: str) -> str:
        return re.sub(self._pattern, r"\`", text_str)


class EscapeDoubleQuotes(_BaseEscapeOperation):
    """Escape Double-quotes from the provided string."""

    def __init__(self):
        self._pattern = re.compile('"')

    @property
    def pattern(self) -> re.Pattern:
        return self._pattern

    def escape(self, text_str: str) -> str:
        return re.sub(self._pattern, r"\"", text_str)


class EscapeBackslashes(_BaseEscapeOperation):
    """Escape backslashes from the provided string.

    A string is said to be backslashed-complaint if it doesn't contain
    and odd number of backslashes. This is not a sufficient condition since an
    even number of backslashes might also require escaping. However, this is a
    necessary condition, failing to which ensures that the string is yet to be
    escaped.
    """

    def __init__(self):
        self._pattern = re.compile(r"\\")

    @property
    def pattern(self) -> re.Pattern:
        return self._pattern

    def check_compliance(self, text_str: str) -> bool:
        return not self._has_odd_backslashes(text_str)

    def escape(self, text_str: str) -> str:
        """TODO: complete docstring"""
        return re.sub(self._pattern, r"\\\\", text_str)

    @staticmethod
    def _has_odd_backslashes(text_str: str) -> bool:
        backslashes = re.findall(r"\\+", text_str)
        for seq in backslashes:
            if len(seq) % 2 == 1:
                return True
        return False


@dataclass
class Operations:
    """Allowed Operations with their string representation."""

    backslash = EscapeBackslashes
    backtick = EscapeBackticks
    double_quote = EscapeDoubleQuotes


class Text:
    """An implementation to custom str objects, with automatic escaping capabilities.

    TODO: Explain further with examples.

    Parameters
    ----------
    text_str: str
        The string representation, with or without escaped characters.
    parse: bool (default=True)
        Whether parsing (escaping) operations should take place.
    strict: bool (default=False)
        Should dubious cases raise an Error.
    exclude_ops: set[str] (default={})
        A set of operations to exclude during parsing. The accepted values are:
        `"backslash"`, `"backtick"` and `"double_quote"`.
    """

    def __init__(
        self,
        text_str: str,
        parse: bool = True,
        strict: bool = False,
        exclude_ops: set[str] = {},
    ):
        self.parse = parse
        self.strict = strict
        self.ops = self._get_ops(exclude_ops)

        compliant = self._check_for_compliance(text_str=text_str, ops=self.ops)

        if not compliant and not parse:
            if self.strict:
                raise ValueError(
                    "Detected unescaped characters but `parse` was set to `False`. "
                    "Either enable automatically escaping it by setting "
                    "`parse=True`, or pass `strict=False` to disable this Error.",
                )
            else:
                warnings.warn(
                    "Detected unescaped characters, pass `parse=True` "
                    "to enable escaping them automatically.",
                )

        if compliant and parse:
            if self.strict:
                raise ValueError(
                    f"The passed string: {text_str} was found to be already compliant "
                    "in terms of escaping characters but `parse` was set to `True` "
                    "which might lead to over-escaping characters. Either set `parse` "
                    "to `False` or pass `strict=False` to parse the string regardless.",
                )
            else:
                warnings.warn(
                    f"The passed string: {text_str} was found to be already compliant "
                    "in terms of escapting characters but `parse` was set to `True`. "
                    "To avoid over-escaping the strings, pass `parse=False`. Ignore "
                    "the warning if you are sure that the escaping string is still "
                    "required.",
                )

        self._text = text_str if not self.parse else self._clean(text_str, self.ops)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text_str: str):
        if self.parse:
            self._text = self._clean(text_str, self.ops)
        else:
            self._check_for_compliance(
                text_str=text_str,
                ops=self.ops,
                strict=self.strict,
            )
            self._text = text_str

    @classmethod
    def from_str(
        cls,
        text_str: str,
        parse: bool = True,
        strict: bool = False,
        no_ops: set[str] = {},
    ) -> "Text":
        """Create a Text Object from a string.

        Parameters
        ----------
        text_str: str
            The string representation, with or without escaped characters.
        parse: bool (default=True)
            Whether parsing (escaping) operations should take place.
        strict: bool (default=False)
            Should dubious cases raise an Error.
        exclude_ops: set[str] (default={})
            A set of operations to exclude during parsing. The accepted values are:
            `"backslash"`, `"backtick"` and `"double_quote"`.
        """
        return Text(text=text_str, parse=parse, strict=strict, exclude_ops=no_ops)

    def __repr__(self) -> str:
        return self.text

    @staticmethod
    def _check_for_compliance(text_str: str, ops: List[_BaseEscapeOperation]) -> bool:
        """Check whether the text is already compliant with the provided ops.

        Parameters
        ----------
        text_str: str
            The string representation to check the compliance for.
        ops: List[_BaseEscapeOperation]
            The list of operations to run compliance check with.
        """
        for op in ops:
            if not op.check_compliance(text_str):
                return False
        return True

    @staticmethod
    def _clean(text_str: str, ops: List[_BaseEscapeOperation]) -> str:
        """Clean the text using the provided ops.

        Parameters
        ----------
        text_str: str
            The string representation to clean (escape).
        ops: List[_BaseEscapeOperation]
            The list of operations to run cleaning with.
        """
        for op in ops:
            text_str = op.escape(text_str)

        return text_str

    @staticmethod
    def _get_ops(exclude_ops: set[str]) -> List[_BaseEscapeOperation]:
        """Get a list of operations to use for compliance check and cleaning.

        Parameters
        ----------
        exclude_ops: set[str]
            Set of string representation of the `Operations` object to exclude.

        Raises
        ------
        ValueError: If the provided operation string is not present in the `Operations`
        object.

        Returns
        -------
        ops: List[_BaseEscapeOperation]
            A list of instantiated operations.
        """
        ops = asdict(Operations())

        for op in exclude_ops:
            if op not in ops:
                raise ValueError("TODO")
            ops.popitem(op)

        return [op() for op in ops.values()]
