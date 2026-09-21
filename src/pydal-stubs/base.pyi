import logging
from contextlib import AbstractContextManager
from hashlib import _Hash
from typing import Any, Callable, Iterable, Iterator, Literal, Mapping, Self, Sequence, overload

from .helpers.classes import (
    BasicStorage,
    ExecutionHandler,
    Serializable,
    SQLCallableList,
)
from .objects import Field as Field
from .objects import Field as _Field
from .objects import Query as Query
from .objects import Row as Row
from .objects import Row as _Row
from .objects import Rows as Rows
from .objects import Rows as _Rows
from .objects import Set as Set
from .objects import Table as Table
from .objects import Table as _Table

def hashlib_md5(s: str) -> _Hash: ...

class MetaDAL(type):
    """
    Metaclass of `DAL`; it recycles instances per `db_uid`.

    Its `__call__` is intentionally left undeclared so constructing a `DAL`
    subclass still infers that subclass rather than collapsing to `Any`.
    """

class DAL(Serializable, BasicStorage, metaclass=MetaDAL):
    """
    A database connection. Defined tables are reachable as attributes, which is
    how `db.person` works at runtime.
    """

    serializers: Any
    validators: Any
    representers: dict[str, Callable[..., Any]]
    validators_method: Callable[..., Any]
    uuid: Callable[[], str]
    logger: logging.Logger

    Field: type[_Field]
    Table: type[_Table]
    Rows: type[_Rows]
    Row: type[_Row]

    record_operators: dict[str, Any]
    execution_handlers: list[type[ExecutionHandler]]

    _adapter: Any
    _uri: str | Mapping[str, Any]
    _uri_hash: str
    _db_uid: str
    _dbname: str
    _pool_size: int
    _folder: str | None
    _db_codec: str
    _lazy_tables: bool
    _migrate: bool
    _migrate_enabled: bool
    _fake_migrate: bool
    _fake_migrate_all: bool
    _timings: list[tuple[str, float]]
    _lastsql: tuple[str, float] | None
    _tables: SQLCallableList
    _common_fields: list[_Field]
    _referee_name: str
    _bigint_id: bool
    _debug: bool
    _check_reserved: Sequence[str] | None

    def __new__(cls, uri: str | Mapping[str, Any] = ..., *args: Any, **kwargs: Any) -> Self: ...
    def __init__(
        self,
        uri: str | Mapping[str, Any] = ...,
        pool_size: int = ...,
        folder: str | None = ...,
        db_codec: str = ...,
        check_reserved: Sequence[str] | None = ...,
        migrate: bool = ...,
        fake_migrate: bool = ...,
        migrate_enabled: bool = ...,
        fake_migrate_all: bool = ...,
        decode_credentials: bool = ...,
        driver_args: Mapping[str, Any] | None = ...,
        adapter_args: Mapping[str, Any] | None = ...,
        attempts: int = ...,
        auto_import: bool = ...,
        bigint_id: bool = ...,
        debug: bool = ...,
        lazy_tables: bool = ...,
        db_uid: str | None = ...,
        after_connection: Callable[[], Any] | None = ...,
        tables: Sequence[Any] | None = ...,
        ignore_field_case: bool = ...,
        entity_quoting: bool = ...,
        table_hash: str | None = ...,
    ) -> None: ...
    @staticmethod
    def set_folder(folder: str) -> None: ...
    @staticmethod
    def get_instances() -> dict[str, Any]: ...
    @staticmethod
    def distributed_transaction_begin(*instances: DAL) -> None: ...
    @staticmethod
    def distributed_transaction_commit(*instances: DAL) -> None: ...
    def single_transaction(self) -> AbstractContextManager[DAL]: ...
    @property
    def tables(self) -> SQLCallableList: ...
    def import_table_definitions(
        self,
        path: str,
        migrate: bool = ...,
        fake_migrate: bool = ...,
        tables: Sequence[Mapping[str, Any]] | None = ...,
    ) -> None: ...
    def check_reserved_keyword(self, name: str) -> None: ...
    def parse_as_rest(
        self,
        patterns: Any,
        args: Any,
        vars: Any,
        queries: Any = ...,
        nested_select: bool = ...,
    ) -> Any: ...
    def define_table(self, tablename: str, *fields: _Field | _Table | str, **kwargs: Any) -> _Table: ...
    def lazy_define_table(
        self, tablename: str, *fields: _Field | _Table | str, **kwargs: Any
    ) -> _Table: ...
    def as_dict(self, flat: bool = ..., sanitize: bool = ...) -> dict[str, Any]: ...
    def __contains__(self, tablename: str) -> bool: ...
    # pyDAL iterates the defined tables, not the mapping keys `BasicStorage` yields.
    def __iter__(self) -> Iterator[_Table]: ...  # type: ignore[override]
    # Unknown attributes are the database's tables; see also `__getitem__`.
    def __getattr__(self, key: str) -> _Table: ...
    def __getitem__(self, key: str) -> _Table: ...
    def __setattr__(self, key: str, value: Any) -> None: ...
    def smart_query(self, fields: Sequence[_Field], text: str) -> Set: ...
    def __call__(self, query: Any = ..., ignore_common_filters: bool | None = ...) -> Set: ...
    def where(self, query: Any = ..., ignore_common_filters: bool | None = ...) -> Set: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def close(self) -> None: ...
    def get_connection_from_pool_or_new(self) -> None: ...
    def recycle_connection_in_pool_or_close(self, action: str = ...) -> None: ...
    @overload
    def executesql(
        self,
        query: str,
        placeholders: Iterable[Any] | Mapping[str, Any] | None = ...,
        *,
        as_dict: Literal[True],
        fields: Iterable[Any] | None = ...,
        colnames: Iterable[str] | None = ...,
        as_ordered_dict: bool = ...,
    ) -> list[dict[str, Any]]: ...
    @overload
    def executesql(
        self,
        query: str,
        placeholders: Iterable[Any] | Mapping[str, Any] | None = ...,
        as_dict: bool = ...,
        fields: Iterable[Any] | None = ...,
        colnames: Iterable[str] | None = ...,
        as_ordered_dict: bool = ...,
    ) -> Any: ...
    def has_representer(self, name: str) -> bool: ...
    def represent(self, name: str, *args: Any, **kwargs: Any) -> Any: ...
    def export_to_csv_file(self, ofile: Any, *args: Any, **kwargs: Any) -> None: ...
    def import_from_csv_file(
        self,
        ifile: Any,
        id_map: Mapping[str, Any] | None = ...,
        null: str = ...,
        unique: str = ...,
        map_tablenames: Mapping[str, str] | None = ...,
        ignore_missing_tables: bool = ...,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...
    def can_join(self) -> bool: ...

def DAL_unpickler(db_uid: str) -> DAL: ...
def DAL_pickler(db: DAL) -> tuple[Any, ...]: ...
