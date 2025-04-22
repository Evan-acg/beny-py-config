import pytest
from pytest_mock import MockerFixture

from by_config.config import Config


class TestConfig:
    @pytest.fixture
    def config(self) -> Config:
        config: Config = Config()
        return config.empty()

    def test_load_empty_path(self, config: Config) -> None:
        config.load()
        assert config.payload == {}

    def test_load_specific_file_path(
        self, config: Config, mocker: MockerFixture
    ) -> None:
        expected = {"key": "value"}
        mocker.patch("os.path.isfile", return_value=True)
        mocker.patch(
            "by_config.loader.YamlLoader.load",
            return_value={"key": "value", "use": True},
        )
        config.load("path/to/file.yaml")
        assert config.payload == expected

    def test_load_multiple_file_paths(
        self, config: Config, mocker: MockerFixture
    ) -> None:
        expected = {"key1": "value1", "key2": "value2"}
        mocker.patch("os.path.isfile", return_value=True)
        mocker.patch(
            "by_config.loader.YamlLoader.load",
            side_effect=[
                {"key1": "value1", "use": True},
                {"key2": "value2", "use": True},
            ],
        )
        config.load("path/to/file1.yaml", "path/to/file2.yaml")
        assert config.payload == expected

    def test_load_dir(self, config: Config, mocker: MockerFixture) -> None:
        path: str = "dir/to/load"
        expected = {"key": "value"}
        mocker.patch("os.path.isfile", return_value=False)
        mocker.patch("os.path.isdir", return_value=True)
        mocker.patch("os.walk", return_value=[("path/to/dir", [], ["file.yaml"])])
        mocker.patch(
            "by_config.loader.YamlLoader.load",
            return_value={"key": "value", "use": True},
        )
        config.load(path)
        assert config.payload == expected

    def test_load_file_with_use(self, config: Config, mocker: MockerFixture) -> None:
        paths: list[str] = ["path/to/file1.yaml", "path/to/file2.yaml"]
        expected = {"key1": "value1"}
        mocker.patch("os.path.isfile", return_value=True)
        mocker.patch(
            "by_config.loader.YamlLoader.load",
            side_effect=[
                {"key1": "value1", "use": True},
                {"key2": "value2"},
            ],
        )
        config.load(*paths)
        assert config.payload == expected

    def test_load_file_with_priority(
        self, config: Config, mocker: MockerFixture
    ) -> None:
        paths: list[str] = ["path/to/file1.yaml", "path/to/file2.yaml"]
        expected = {"key": "value1"}
        mocker.patch("os.path.isfile", return_value=True)
        mocker.patch(
            "by_config.loader.YamlLoader.load",
            side_effect=[
                {"key": "value1", "priority": 1, "use": True},
                {"key": "value2", "use": True},
            ],
        )
        config.load(*paths)
        assert config.payload == expected
