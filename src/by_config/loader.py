import os
import yaml


class YamlLoader:
    def is_valid(self, path: str) -> bool:
        return all(
            (
                os.path.exists(path),
                os.path.isfile(path),
                path.lower().endswith(".yaml") or path.lower().endswith(".yml"),
            )
        )

    def load(self, path: str) -> dict:
        if not self.is_valid(path):
            return {}
        with open(path, "r") as file:
            return yaml.safe_load(file)


class JsonLoader:
    pass
