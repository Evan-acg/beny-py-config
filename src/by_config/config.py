import os
import typing as t

from by_config.loader import YamlLoader


class Config:
    def __init__(self) -> None:
        self.loaders = [YamlLoader()]
        self.payload: dict = {}
        self.filters = [self.is_use]

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

    def load(self, *paths: str) -> None:
        paths = [path for path in paths if os.path.isfile(path)] + [
            os.path.join(root, file)
            for path in paths
            if os.path.isdir(path)
            for root, _, files in os.walk(path)
            for file in files
        ]

        raw_items = [loader.load(path) for path in paths for loader in self.loaders]

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
