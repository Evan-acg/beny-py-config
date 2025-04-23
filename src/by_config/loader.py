import logging
import os
import yaml


logger = logging.getLogger("ConfigLoader")


class YamlLoader:
    def is_valid(self, path: str) -> bool:
        return all(
            (
                os.path.exists(path),
                os.path.isfile(path),
                path.lower().endswith(".yaml") or path.lower().endswith(".yml"),
            )
        )

    def load(self, path: str, verbose: bool = False) -> dict:
        path = os.path.abspath(path)
        if not self.is_valid(path):
            return {}

        if verbose:
            logger.info(f"Loading YAML file: {path}")

        with open(path, "r") as file:
            return yaml.safe_load(file)


class JsonLoader:
    pass
