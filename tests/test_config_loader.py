import pytest
from ByConfig import ConfigLoader
from pathlib import Path
from unittest.mock import patch
import os
import json

class TestConfigLoader:
    @pytest.fixture
    def loader(self) -> ConfigLoader:
        return ConfigLoader(env_prefix="TEST_")
        
    def test_load_yaml_file(self, loader: ConfigLoader, tmp_path: Path):
        test_file = tmp_path / "test.yml"
        test_file.write_text("key: ${TEST_ENV_VAR}")
        
        with patch.dict(os.environ, {"TEST_ENV_VAR": "mock_value"}):
            result = loader.load(test_file)
            
        assert result == {"key": "mock_value"}
        
    def test_load_json_file(self, loader: ConfigLoader, tmp_path: Path):
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps({"num": "${TEST_NUM}"}))
        
        with patch.dict(os.environ, {"TEST_NUM": "42"}):
            result = loader.load(test_file)
            
        assert result == {"num": 42}
        
    def test_missing_file_handling(self, loader: ConfigLoader):
        with pytest.raises(FileNotFoundError):
            loader.load(Path("nonexistent.yml"))
            
    def test_environment_priority(self, loader: ConfigLoader, tmp_path: Path):
        test_file = tmp_path / "test.yml"
        test_file.write_text("""
        server:
          host: ${TEST_HOST}
          port: ${TEST_PORT}
        """)
        
        with patch.dict(os.environ, {
            "TEST_HOST": "api.example.com",
            "TEST_PORT": "8080"
        }):
            result = loader.load(test_file)
            
        assert result["server"]["host"] == "api.example.com"
        assert result["server"]["port"] == 8080
