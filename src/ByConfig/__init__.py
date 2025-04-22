from typing import Protocol, TypeVar
from pathlib import Path
import yaml
import os

T = TypeVar('T', covariant=True)

class LoaderProtocol(Protocol[T]):
    def load(self, config_path: str | Path) -> T:
        ...
        
    def __call__(self, config_path: str | Path) -> T:
        ...
        
class ConfigLoader:
    """YAML/JSON配置加载器，支持环境变量解析"""
    
    def __init__(self, env_prefix: str = "BYCONFIG_"):
        self.env_prefix = env_prefix
        
    def load(self, config_path: str | Path) -> dict:
        """加载配置文件并解析环境变量"""
        with open(config_path) as f:
            config = yaml.safe_load(f)
            
        return self._resolve_env_vars(config)
        
    def _resolve_env_vars(self, config: dict) -> dict:
        """递归解析环境变量占位符，支持类型转换"""
        def process_value(value):
            if isinstance(value, dict):
                return {k: process_value(v) for k, v in value.items()}
            if isinstance(value, list):
                return [process_value(item) for item in value]
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1].strip()
                # 优先使用带前缀的环境变量
                prefixed_var = f"{self.env_prefix}{env_var}"
                env_value = os.getenv(prefixed_var) or os.getenv(env_var)
                
                if env_value is None:
                    return value
                
                # 自动类型转换
                try:
                    return int(env_value)
                except ValueError:
                    try:
                        return float(env_value)
                    except ValueError:
                        if env_value.lower() in ("true", "false"):
                            return env_value.lower() == "true"
                        return env_value
            return value
            
        return process_value(config)
        
    def __call__(self, config_path: str | Path) -> dict:
        return self.load(config_path)
        
__all__ = ['ConfigLoader', 'LoaderProtocol']
