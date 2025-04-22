import argparse
import json
import sys
from pathlib import Path

from . import ConfigLoader, __version__


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        prog="byconfig",
        description="加载并解析配置文件（支持环境变量替换）"
    )
    parser.add_argument("config", type=Path, help="配置文件路径（YAML/JSON）")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-o", "--output", choices=["json", "yaml"], default="json", 
                      help="输出格式（默认：json）")
    
    args = parser.parse_args()
    
    if not args.config.exists():
        parser.error(f"配置文件不存在：{args.config}")
    
    loader = ConfigLoader()
    config_data = loader(args.config)
    
    if args.output == "json":
        print(json.dumps(config_data, indent=2, ensure_ascii=False))
    else:
        import yaml
        yaml.safe_dump(config_data, sys.stdout, allow_unicode=True)

if __name__ == "__main__":
    main()
