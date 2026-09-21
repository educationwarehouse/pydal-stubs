import datetime
from typing import Any, Callable, Iterable, Mapping, Sequence

from .objects import Field, Table

_Message = str
_Result = tuple[Any, Any]

class ValidationError(Exception):
    message: str
    def __init__(self, message: str) -> None: ...

class Validator:
    """
    Root of every pyDAL validator.

    Calling a validator returns `(value, error)`; `validate` raises
    `ValidationError` instead and returns the coerced value.
    """

    translator: Callable[[str], str]
    error_message: str
    def formatter(self, value: Any) -> Any: ...
    @staticmethod
    def validate(value: Any, record_id: Any = ...) -> Any: ...
    def __call__(self, value: Any, record_id: Any = ...) -> _Result: ...

def validator_caller(
    func: Validator | Callable[[Any], _Result], value: Any, record_id: Any = ...
) -> Any: ...

class DefaultValidatorProxy(Validator):
    obj: Validator
    def __init__(self, obj: Validator) -> None: ...

class ANY_OF(Validator):
    def __init__(self, subs: Iterable[Validator], error_message: _Message | None = ...) -> None: ...

class CLEANUP(Validator):
    def __init__(self, regex: str | None = ...) -> None: ...

class CRYPT(Validator):
    def __init__(
        self,
        key: str | None = ...,
        digest_alg: str = ...,
        min_length: int = ...,
        error_message: _Message = ...,
        salt: bool | str = ...,
        max_length: int = ...,
    ) -> None: ...

class LazyCrypt:
    crypt: CRYPT
    password: str
    def __init__(self, crypt: CRYPT, password: str) -> None: ...
    def __str__(self) -> str: ...
    def __eq__(self, stored_password: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

class IS_MATCH(Validator):
    def __init__(
        self,
        expression: str,
        error_message: _Message = ...,
        strict: bool = ...,
        search: bool = ...,
        extract: bool = ...,
        is_unicode: bool = ...,
    ) -> None: ...

class IS_ALPHANUMERIC(IS_MATCH):
    def __init__(self, error_message: _Message = ...) -> None: ...

class IS_DATE(Validator):
    def __init__(self, format: str = ..., error_message: _Message = ...) -> None: ...

class IS_DATE_IN_RANGE(IS_DATE):
    def __init__(
        self,
        minimum: datetime.date | None = ...,
        maximum: datetime.date | None = ...,
        format: str = ...,
        error_message: _Message | None = ...,
    ) -> None: ...

class IS_DATETIME(Validator):
    def __init__(
        self, format: str = ..., error_message: _Message = ..., timezone: Any = ...
    ) -> None: ...

class IS_DATETIME_IN_RANGE(IS_DATETIME):
    def __init__(
        self,
        minimum: datetime.datetime | None = ...,
        maximum: datetime.datetime | None = ...,
        format: str = ...,
        error_message: _Message | None = ...,
        timezone: Any = ...,
    ) -> None: ...

class IS_DECIMAL_IN_RANGE(Validator):
    def __init__(
        self,
        minimum: Any = ...,
        maximum: Any = ...,
        error_message: _Message | None = ...,
        dot: str = ...,
    ) -> None: ...

class IS_EMAIL(Validator):
    def __init__(
        self,
        banned: str | None = ...,
        forced: str | None = ...,
        error_message: _Message = ...,
    ) -> None: ...

class IS_EMPTY_OR(Validator):
    other: Any
    def __init__(
        self,
        other: Validator | Sequence[Validator],
        null: Any = ...,
        empty_regex: str | None = ...,
    ) -> None: ...
    def set_self_id(self, id: Any) -> None: ...

# Kept by pyDAL for backward compatibility.
IS_NULL_OR = IS_EMPTY_OR

class IS_EQUAL_TO(Validator):
    def __init__(self, expression: Any, error_message: _Message = ...) -> None: ...

class IS_EXPR(Validator):
    def __init__(
        self,
        expression: str | Callable[[Any], Any],
        error_message: _Message = ...,
        environment: Mapping[str, Any] | None = ...,
    ) -> None: ...

class IS_FILE(Validator):
    def __init__(
        self,
        filename: str | None = ...,
        extension: str | Sequence[str] | None = ...,
        lastdot: bool = ...,
        case: int = ...,
        error_message: _Message = ...,
    ) -> None: ...

class IS_FLOAT_IN_RANGE(Validator):
    def __init__(
        self,
        minimum: float | None = ...,
        maximum: float | None = ...,
        error_message: _Message | None = ...,
        dot: str = ...,
    ) -> None: ...

class IS_GENERIC_URL(Validator):
    def __init__(
        self,
        error_message: _Message = ...,
        allowed_schemes: Sequence[str | None] | None = ...,
        prepend_scheme: str | None = ...,
    ) -> None: ...

class IS_HTTP_URL(Validator):
    def __init__(
        self,
        error_message: _Message = ...,
        allowed_schemes: Sequence[str | None] | None = ...,
        prepend_scheme: str | None = ...,
        allowed_tlds: Sequence[str] | None = ...,
    ) -> None: ...

class IS_URL(Validator):
    def __init__(
        self,
        error_message: _Message = ...,
        mode: str = ...,
        allowed_schemes: Sequence[str | None] | None = ...,
        prepend_scheme: str | None = ...,
        allowed_tlds: Sequence[str] | None = ...,
    ) -> None: ...

class IS_IMAGE(Validator):
    def __init__(
        self,
        extensions: Sequence[str] = ...,
        maxsize: tuple[int, int] = ...,
        minsize: tuple[int, int] = ...,
        aspectratio: tuple[float, float] = ...,
        error_message: _Message = ...,
    ) -> None: ...

class IS_INT_IN_RANGE(Validator):
    def __init__(
        self,
        minimum: int | None = ...,
        maximum: int | None = ...,
        error_message: _Message | None = ...,
    ) -> None: ...

class IS_IN_DB(Validator):
    def __init__(
        self,
        dbset: Any,
        field: str | Field,
        label: str | Callable[[Any], str] | None = ...,
        error_message: _Message = ...,
        orderby: Any = ...,
        groupby: Any = ...,
        distinct: Any = ...,
        cache: Any = ...,
        multiple: bool = ...,
        zero: str | None = ...,
        sort: bool = ...,
        _and: Validator | None = ...,
        left: Any = ...,
        delimiter: str | None = ...,
        auto_add: bool = ...,
    ) -> None: ...
    dbset: Any
    field: str | Field
    ktable: str
    kfield: str
    fieldnames: list[str]
    label: Any
    labels: Any
    theset: Any
    orderby: Any
    groupby: Any
    distinct: Any
    cache: Any
    multiple: bool
    zero: str | None
    sort: bool
    left: Any
    delimiter: str | None
    auto_add: bool
    def set_self_id(self, id: Any) -> None: ...
    def build_set(self) -> None: ...
    def maybe_add(self, table: Table, fieldname: str, value: Any) -> Any: ...
    def options(self, zero: bool = ...) -> list[tuple[Any, Any]]: ...

class IS_NOT_IN_DB(Validator):
    def __init__(
        self,
        dbset: Any,
        field: str | Field,
        error_message: _Message = ...,
        allowed_override: Sequence[Any] = ...,
        ignore_common_filters: bool = ...,
    ) -> None: ...
    dbset: Any
    field: str | Field
    record_id: Any
    allowed_override: Sequence[Any]
    ignore_common_filters: bool
    def set_self_id(self, id: Any) -> None: ...

class IS_IN_SET(Validator):
    def __init__(
        self,
        theset: Iterable[Any] | Mapping[Any, Any],
        labels: Sequence[Any] | None = ...,
        error_message: _Message = ...,
        multiple: bool | tuple[int, int] = ...,
        zero: str | None = ...,
        sort: bool = ...,
    ) -> None: ...
    theset: Any
    labels: Any
    multiple: bool | tuple[int, int]
    zero: str | None
    sort: bool
    def options(self, zero: bool = ...) -> list[tuple[Any, Any]]: ...

class IS_IPV4(Validator):
    def __init__(
        self,
        minip: str | Sequence[str] = ...,
        maxip: str | Sequence[str] = ...,
        invert: bool = ...,
        is_localhost: bool | None = ...,
        is_private: bool | None = ...,
        is_automatic: bool | None = ...,
        error_message: _Message = ...,
    ) -> None: ...

class IS_IPV6(Validator):
    def __init__(
        self,
        is_private: bool | None = ...,
        is_link_local: bool | None = ...,
        is_reserved: bool | None = ...,
        is_multicast: bool | None = ...,
        is_routeable: bool | None = ...,
        is_6to4: bool | None = ...,
        is_teredo: bool | None = ...,
        subnets: str | Sequence[str] | None = ...,
        error_message: _Message = ...,
    ) -> None: ...

class IS_IPADDRESS(Validator):
    def __init__(
        self,
        minip: str | Sequence[str] = ...,
        maxip: str | Sequence[str] = ...,
        invert: bool = ...,
        is_localhost: bool | None = ...,
        is_private: bool | None = ...,
        is_automatic: bool | None = ...,
        is_ipv4: bool | None = ...,
        is_link_local: bool | None = ...,
        is_reserved: bool | None = ...,
        is_multicast: bool | None = ...,
        is_routeable: bool | None = ...,
        is_6to4: bool | None = ...,
        is_teredo: bool | None = ...,
        subnets: str | Sequence[str] | None = ...,
        is_ipv6: bool | None = ...,
        error_message: _Message = ...,
    ) -> None: ...

class IS_JSON(Validator):
    def __init__(self, error_message: _Message = ..., native_json: bool = ...) -> None: ...

class IS_LENGTH(Validator):
    def __init__(
        self, maxsize: int = ..., minsize: int = ..., error_message: _Message = ...
    ) -> None: ...

class IS_LIST_OF(Validator):
    def __init__(
        self,
        other: Validator | Sequence[Validator] | None = ...,
        minimum: int | None = ...,
        maximum: int | None = ...,
        error_message: _Message | None = ...,
    ) -> None: ...

class IS_LIST_OF_STRINGS(Validator):
    def __init__(self, error_message: _Message = ...) -> None: ...

class IS_LIST_OF_EMAILS(IS_LIST_OF_STRINGS):
    def __init__(self, error_message: _Message = ...) -> None: ...

class IS_LIST_OF_INTS(IS_LIST_OF_STRINGS):
    def __init__(self, error_message: _Message = ...) -> None: ...

class IS_LOWER(Validator): ...
class IS_UPPER(Validator): ...

class IS_NOT_EMPTY(Validator):
    def __init__(
        self, error_message: _Message = ..., empty_regex: str | None = ...
    ) -> None: ...

class IS_SAFE(Validator):
    def __init__(
        self,
        sanitizer: Callable[[Any], Any] | None = ...,
        error_message: _Message = ...,
        mode: str = ...,
    ) -> None: ...

class IS_SLUG(Validator):
    def __init__(
        self,
        maxlen: int = ...,
        check: bool = ...,
        error_message: _Message = ...,
        keep_underscores: bool = ...,
    ) -> None: ...
    @staticmethod
    def urlify(value: str, maxlen: int = ..., keep_underscores: bool = ...) -> str: ...

class IS_STRONG(Validator):
    def __init__(
        self,
        min: int | None = ...,
        max: int | None = ...,
        upper: int | None = ...,
        lower: int | None = ...,
        number: int | None = ...,
        entropy: float | None = ...,
        special: int | None = ...,
        specials: str = ...,
        invalid: str = ...,
        error_message: _Message | None = ...,
        es: bool = ...,
    ) -> None: ...

class IS_TIME(Validator):
    def __init__(self, error_message: _Message = ...) -> None: ...

class IS_UPLOAD_FILENAME(Validator):
    def __init__(
        self,
        filename: str | None = ...,
        extension: str | Sequence[str] | None = ...,
        lastdot: bool = ...,
        case: int = ...,
        error_message: _Message = ...,
    ) -> None: ...

class UTC(datetime.tzinfo):
    ZERO: datetime.timedelta
    def utcoffset(self, dt: datetime.datetime | None) -> datetime.timedelta: ...
    def tzname(self, dt: datetime.datetime | None) -> str: ...
    def dst(self, dt: datetime.datetime | None) -> datetime.timedelta: ...

utc: UTC

def calc_entropy(string: str) -> float: ...
def escape_unicode(string: str) -> str: ...
def get_digest(value: str | Callable[..., Any]) -> Any: ...
def is_empty(value: Any, empty_regex: Any = ...) -> tuple[Any, bool]: ...
def options_sorter(x: tuple[Any, Any], y: tuple[Any, Any]) -> int: ...
def parse_tokens(line: str) -> Any: ...
def pbkdf2_hex(
    data: Any, salt: Any, iterations: int = ..., keylen: int = ..., hashfunc: Any = ...
) -> str: ...
def quote_token(token: str) -> str: ...
def range_error_message(
    error_message: _Message | None, what_to_enter: str, minimum: Any, maximum: Any
) -> str: ...
def simple_hash(
    text: str, key: str = ..., salt: str = ..., digest_alg: str = ...
) -> str: ...
def str2dec(number: str) -> Any: ...
def translate(text: str | None) -> str | None: ...
def unicode_to_ascii_authority(authority: str) -> str: ...
def unicode_to_ascii_url(url: str, prepend_scheme: str | None) -> str: ...
def urlify(s: str, maxlen: int = ..., keep_underscores: bool = ...) -> str: ...
