import threading
from typing import Any, Callable, TypeVar

_T = TypeVar("_T")

GLOBAL_LOCKER: threading.RLock
THREAD_LOCAL: threading.local

# runtime: `DEFAULT = lambda: None`, used purely as a unique sentinel.
DEFAULT: Callable[[], None]

def IDENTITY(x: _T) -> _T: ...
def OR(a: Any, b: Any) -> Any: ...
def AND(a: Any, b: Any) -> Any: ...
