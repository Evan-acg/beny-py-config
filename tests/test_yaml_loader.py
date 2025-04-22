import pytest
from pytest_mock import MockerFixture

from by_config.loader import YamlLoader


class TestYamlLoader:
    def test_load(self) -> None:
        YamlLoader()
        assert True

    @pytest.fixture
    def loader(self) -> YamlLoader:
        return YamlLoader()

    def test_load_file(self, loader: YamlLoader, mocker: MockerFixture) -> None:
        path: str = "a.yaml"
        expected: dict = {"a": "b"}
        mocker.patch("builtins.open", mocker.mock_open(read_data="a: b"))
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("os.path.isfile", return_value=True)

        assert loader.load(path) == expected

    def test_load_file_not_exists(
        self, loader: YamlLoader, mocker: MockerFixture
    ) -> None:
        path: str = "a.yaml"
        expected: dict = {}
        mocker.patch("os.path.exists", return_value=False)
        mocker.patch("builtins.open", mocker.mock_open(read_data="a: b"))

        assert loader.load(path) == expected

    def test_load_path_not_file(
        self, loader: YamlLoader, mocker: MockerFixture
    ) -> None:
        path: str = "a.yaml"
        expected: dict = {}
        mocker.patch("os.path.exists", return_value=False)
        mocker.patch("builtins.open", mocker.mock_open(read_data="a: b"))
        assert loader.load(path) == expected

    def test_load_path_not_valid(
        self, loader: YamlLoader, mocker: MockerFixture
    ) -> None:
        path: str = "a.txt"
        expected: dict = {}
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("os.path.isfile", return_value=True)
        mocker.patch("builtins.open", mocker.mock_open(read_data="a: b"))
        assert loader.load(path) == expected
