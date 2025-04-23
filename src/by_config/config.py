import os
import typing as t
import threading

from by_config.loader import YamlLoader


class Config:
    _initialized: bool = False
    _instance: "Config" = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self.loaders = [YamlLoader()]
        self.payload: dict = {}
        self.filters = [self.is_use]
        self._initialized = True

    def _merge_deep(self, a: dict, b: dict) -> None:
        for key, value in b.items():
            if isinstance(value, dict) and key in a:
                self._merge_deep(a[key], value)
            else:
                a[key] = value

    def empty(self) -> t.Self:
        self.payload = {}
        return self

    def is_use(self, item: dict) -> bool:
        return item.pop("use", False)

    def load(self, *paths: str, verbose: bool = False) -> None:
        paths = [path for path in paths if os.path.isfile(path)] + [
            os.path.join(root, file)
            for path in paths
            if os.path.isdir(path)
            for root, _, files in os.walk(path)
            for file in files
        ]

        raw_items = [
            loader.load(path, verbose) for path in paths for loader in self.loaders
        ]

        for f in self.filters:
            raw_items = [item for item in raw_items if f(item)]

        raw_items = sorted(raw_items, key=lambda x: x.pop("priority", -1))

        for item in raw_items:
            self._merge_deep(self.payload, item)

    def get(self, path: str | list[str], default=None) -> t.Any:
        keys = path.split(".") if isinstance(path, str) else path
        ret: t.Any = self.payload
        for key in keys:
            if key not in ret:
                return default
            ret = ret[key]
        return ret if ret else default
