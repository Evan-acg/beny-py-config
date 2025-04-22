import typing as t
from pathlib import Path

T = t.TypeVar("T", covariant=True)


class LoaderProtocol(t.Protocol[T]):
    def load(self, config_path: str | Path) -> T: ...
