# pydal-stubs

PEP 561 type stubs for [pyDAL](https://github.com/web2py/pydal).

pyDAL ships no `py.typed` marker, so type checkers fall back to `Any` (mypy) or
`Unknown` (Pyright) for everything it exports. That is contagious: anything that
subclasses `pydal.DAL` loses the benefit of its own annotations, because a base
class of unknown type swallows attribute resolution.

This package fills that gap without touching pyDAL itself.

## Installation

```bash
pip install pydal-stubs
```

Nothing needs to be imported or configured. mypy and Pyright discover a
`pydal-stubs` directory on `sys.path` automatically, per PEP 561.

The stubs are a development-time dependency only. They contain no runtime code.

Editable installs (`pip install -e .`, `uv pip install -e .`) work, but only
because the wheel target sets `dev-mode-dirs`. `pydal-stubs` is not a valid
module name, so the default editable mechanism has nothing to hook and silently
installs an empty distribution. If you vendor or fork this package, keep that
setting or install non-editable.

## Supported pyDAL version

Written against the pyDAL API as of **20251012.3** and verified against
**20260520.0**. pyDAL uses CalVer and its public surface is stable, so older and
newer releases in that range should work; a name that only exists outside this
window will simply not be described here.

This is a **partial** stub package (`py.typed` contains `partial`). Modules that
are not stubbed here fall back to pyDAL's own source, which means the runtime
package must be installed alongside the stubs. That is why `pydal>=20251012.3`
is a hard dependency rather than a suggestion.

## What you get

Dynamic attribute access is the main reason this package exists:

```python
from pydal import DAL
from pydal.objects import Field, Table

db = DAL("sqlite:memory")

table: Table = db.some_table               # DAL.__getattr__  -> Table
field: Field = db.some_table.some_field    # Table.__getattr__ -> Field
same: Field = db.some_table["some_field"]  # Table.__getitem__ -> Field
```

Queries keep their real types, so a comparison is a `Query` rather than a `bool`:

```python
rows = db(db.person.name == "Ada").select()   # Rows
count = db(db.person.age > 18).count()        # int
```

## Stubbed modules

| Module | Contents |
| --- | --- |
| `pydal` | `DAL`, `Field`, `SQLCustomType`, `QueryBuilder`, `geoLine`, `geoPoint`, `geoPolygon`, `__version__` |
| `pydal.base` | `DAL`, `MetaDAL`, `hashlib_md5`, `DAL_pickler`, `DAL_unpickler` |
| `pydal.objects` | `Row`, `Table`, `Select`, `Expression`, `Field`, `FieldVirtual`, `FieldMethod`, `Query`, `Set`, `LazySet`, `LazyReferenceGetter`, `VirtualCommand`, `BasicRows`, `Rows`, `IterRows`, `csv_reader`, `get_default_validator`, `pickle_row` |
| `pydal.helpers.classes` | `BasicStorage`, `OpRow`, `Serializable`, `Reference`, `SQLCallableList`, `SQLALL`, `SQLCustomType`, `ExecutionHandler`, `TimingHandler`, `RecordOperator`/`RecordUpdater`/`RecordDeleter`, `MethodAdder`, `FakeCursor`/`NullCursor`, `FakeDriver`/`NullDriver`, `DatabaseStoredFile`, `cachedprop` |
| `pydal.validators` | `Validator`, `ValidationError`, `validator_caller`, all 40+ `IS_*` validators, `CRYPT`, `CLEANUP`, `ANY_OF`, `UTC`, and the module-level helpers (`urlify`, `simple_hash`, ...) |
| `pydal._globals` | `DEFAULT`, `GLOBAL_LOCKER`, `THREAD_LOCAL`, `IDENTITY`, `OR`, `AND` |

## Intentionally not stubbed

These modules keep whatever the checker infers from pyDAL's own source, which
avoids hiding names behind an incomplete stub:

- `pydal.querybuilder`, `pydal.migrator`, `pydal.restapi`, `pydal.connection`,
  `pydal.drivers`, `pydal.exceptions`, `pydal.utils`, `pydal.default_validators`
- `pydal.helpers.methods`, `pydal.helpers.rest`, `pydal.helpers.serializers`,
  `pydal.helpers.regex`
- `pydal.adapters.*`, `pydal.dialects.*`, `pydal.parsers.*`,
  `pydal.representers.*`, `pydal.tools.*`, `pydal.contrib.*`

The first two groups fall back cleanly: mypy reads pyDAL's source for them and
reports no missing-import error. The subpackages in the third group are
different, because partial-stub fallback only reaches a subpackage that has a
stub directory of its own. `import pydal.adapters.base` therefore still raises
mypy's `import-untyped`, exactly as it did before installing these stubs. Add a
per-module override if you import them:

```toml
[[tool.mypy.overrides]]
module = ["pydal.adapters.*", "pydal.dialects.*", "pydal.parsers.*", "pydal.representers.*"]
ignore_missing_imports = true
```

Pyright in `strict` mode reports `reportMissingTypeStubs` for any unstubbed
module you import directly. That diagnostic is inherent to partial stubs;
silence it per-import or set `reportMissingTypeStubs = false`.

## Known limitations

- `DAL.__getattr__` returns `Table` and `Table.__getattr__` returns `Field` for
  *any* unknown name. That is what pyDAL does at runtime, but it means a typo in
  a table or field name is not caught by the type checker.
- `Table.insert()` is typed as returning `Reference`. pyDAL returns `0` instead
  when a `_before_insert` callback aborts the insert; `Reference` subclasses
  `int`, so the distinction is lost.
- `Expression.__eq__` and `__ne__` return `Query`, not `bool`. This matches
  runtime, but it is a deliberate violation of the `object` contract, so
  `Field` instances do not behave like ordinary objects in equality-based
  containers or in `assert x == y` style code.
- `_adapter` and the dialect/driver machinery behind it are typed as `Any`.
  Adapter-level APIs are out of scope for this release.
- `MetaDAL.__call__` is deliberately left undeclared. Declaring it would make
  every `DAL(...)` and subclass construction evaluate to `Any`; leaving it out
  keeps constructor inference intact at the cost of not describing the instance
  recycling that `MetaDAL` performs.
- Rows and records are not generic. `Rows` yields `Row`, and `Row` attribute
  access is `Any`; per-table row types are the job of an ORM layer such as
  [TypeDAL](https://github.com/trialandsuccess/TypeDAL).
- `**kwargs`-driven APIs (`Set.select` attributes, `define_table` options) accept
  `Any`. pyDAL validates these at runtime against its own allow-lists.
- `Table._db` is typed as `DAL`, not `DAL | None`. pyDAL never nulls it, though
  it does null a `Field`'s `db`/`_db`/`table`/`_table` (see `Field.clone`), which
  the stubs do model as optional. Code that deliberately unbinds a table to break
  reference cycles will need a suppression.
- Installing these stubs can surface new errors in code that previously relied
  on pyDAL being untyped. The common case is a downstream shim that declares
  `class Query(pydal.objects.Query)` under `TYPE_CHECKING` purely to give the
  type a name: a genuine `pydal.objects.Query` is the *supertype* of that shim,
  so it no longer satisfies parameters annotated with the shim. Widen such
  annotations to accept the real pyDAL class. The second common case is a
  subclass of `Rows`, `Select` or `Table` that re-types the container's elements
  (a typed ORM row instead of `Row`): those overrides are genuine Liskov
  violations that were simply invisible while pyDAL was untyped.

## License

BSD 3-Clause, matching pyDAL. See [LICENSE](LICENSE).
