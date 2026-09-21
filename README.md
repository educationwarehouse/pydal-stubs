# pydal-stubs

PEP 561 type stubs for [pyDAL](https://github.com/web2py/pydal).

pyDAL ships no `py.typed` marker, so type checkers treat everything it exports
as `Any` (mypy) or `Unknown` (Pyright). This package fills that gap without
touching pyDAL itself. One name stays deliberately untyped: `DAL` (see below).

Written against the pyDAL API as of 20251012.3, verified against 20260520.0.

## Installation

```bash
pip install pydal-stubs
```

Nothing needs to be imported or configured; mypy and Pyright discover the
`pydal-stubs` directory automatically, per PEP 561. The stubs contain no
runtime code.

## What you get

The full object model is typed: `Table`, `Field`, `Query`, `Set`, `Rows`, the
validators, and the helper classes. `Table` and `Field` attribute access keeps
its real types:

```python
from pydal.objects import Field, Query, Table

def example(table: Table) -> None:
    field: Field = table.some_field      # Table.__getattr__ -> Field
    same: Field = table["some_field"]    # Table.__getitem__ -> Field
    q: Query = table.name == "Ada"       # comparisons build queries, not bools
```

## Why `DAL` is `Any`

`pydal.DAL` is deliberately exported as a gradual `Any` alias rather than a
nominal class. Typing it as a class makes every third-party
`Callable[[DAL], ...]` annotation reject functions annotated with a DAL
*subclass*, because parameter positions are contravariant. Those annotations
were vacuous while pyDAL was untyped, so a nominal `DAL` would turn them into
hard errors across whole codebases with no fix available at either call site.

The real surface is `pydal.base.DALBase`; the public `DAL` keeps the gradual
behaviour callers already depend on. A consequence is that `db.some_table` on a
`DAL`-typed value is `Any`, not `Table`.

Frameworks that subclass pyDAL should use `DALBase`, so their subclass keeps the
whole typed API instead of inheriting from `Any`:

```python
import typing as t
import pydal

if t.TYPE_CHECKING:
    from pydal.base import DALBase as _PyDAL
else:
    _PyDAL = pydal.DAL

class MyDAL(_PyDAL): ...
```

`MyDAL().some_table` is then a `Table`, `.some_field` a `Field` and
`db(query).select()` a `Rows`, while
`Callable[[pydal.DAL], ...]` elsewhere still accepts `(db: MyDAL) -> ...`.
`DALBase` exists only for type checkers, which is why the import sits behind
`TYPE_CHECKING`.

## Stubbed modules

| Module | Contents |
| --- | --- |
| `pydal` | `DAL` (gradual alias), `Field`, `SQLCustomType`, `QueryBuilder`, geo helpers, `__version__` |
| `pydal.base` | `DALBase` (nominal surface), `DAL` (gradual alias), `MetaDAL`, ... |
| `pydal.objects` | `Row`, `Table`, `Query`, `Set`, `Rows`, `Expression`, `Field`, ... |
| `pydal.helpers.classes` | `Reference`, `SQLALL`, `RecordOperator`, `DatabaseStoredFile`, ... |
| `pydal.validators` | `Validator`, `ValidationError`, all `IS_*` validators, `CRYPT`, ... |
| `pydal._globals` | `DEFAULT`, `IDENTITY`, `OR`, `AND`, ... |

## Intentional gaps

This is a **partial** stub package (`py.typed` contains `partial`), so the
runtime `pydal` package must be installed alongside it (hence the hard
dependency on `pydal>=20251012.3`).

- **Unstubbed modules** (`pydal.migrator`, `pydal.drivers`, `pydal.adapters.*`,
  `pydal.dialects.*`, ...) fall back to pyDAL's own source. Subpackages without
  a stub directory still trigger mypy's `import-untyped` or Pyright's
  `reportMissingTypeStubs`; silence those per-module if you import them.
- **Typos are not caught**: `Table.__getattr__` returns `Field` for *any*
  name, matching runtime behavior. On `DAL`-typed values nothing is checked at
  all, since `DAL` is `Any` (see above).
- **`Expression.__eq__` returns `Query`, not `bool`**, a deliberate violation
  of the `object` contract that mirrors pyDAL.
- **Rows are not generic**: `Rows` yields `Row` and `Row` attribute access is
  `Any`. Per-table row types belong to an ORM layer such as
  [TypeDAL](https://github.com/trialandsuccess/TypeDAL).
- **Adapter internals** (`_adapter`, dialect/driver machinery) are typed as
  `Any`, and `**kwargs`-driven APIs accept `Any` (pyDAL validates them at
  runtime).
- Installing these stubs can surface new errors in code that relied on pyDAL
  being untyped, e.g. `TYPE_CHECKING`-only shims of pyDAL classes or container
  subclasses with Liskov-violating element types.

## License

BSD 3-Clause, matching pyDAL. See [LICENSE](LICENSE).
