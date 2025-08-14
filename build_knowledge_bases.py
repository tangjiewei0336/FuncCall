"""
知识库构建管理脚本
用于构建HPV、FLU、HIV三个知识库
"""

import json
import sys
from pathlib import Path
from tools.knowledge_base_tool import get_kb_manager, KnowledgeBaseType


def build_all_knowledge_bases():
    """构建所有知识库"""
    print("开始构建知识库...")
    
    # Excel配置示例
    excel_configs = {
        "hpv": {
            "content_column": "内容",
            "source_column": "来源",
            "link_column": "链接",
            "sheet_name": "Sheet1"
        },
        "flu": {
            "content_column": "内容",
            "source_column": "来源", 
            "link_column": "链接",
            "sheet_name": "Sheet1"
        },
        "hiv": {
            "content_column": "内容",
            "source_column": "来源",
            "link_column": "链接", 
            "sheet_name": "Sheet1"
        }
    }
    
    manager = get_kb_manager()
    
    for kb_type in KnowledgeBaseType:
        print(f"\n=== 构建 {kb_type.value.upper()} 知识库 ===")
        
        # 检查是否有Excel配置文件
        config_file = Path(f"input/{kb_type.value}/excel_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    excel_config = json.load(f)
                print(f"使用配置文件: {config_file}")
            except Exception as e:
                print(f"读取配置文件失败: {e}")
                excel_config = excel_configs.get(kb_type.value)
        else:
            excel_config = excel_configs.get(kb_type.value)
            print(f"使用默认配置，如需自定义请创建: {config_file}")
        
        # 构建知识库
        result = manager.build_knowledge_base(kb_type, excel_config)
        print(f"构建结果: {result}")
    
    print("\n知识库构建完成！")


def build_specific_knowledge_base(kb_name: str):
    """构建指定的知识库"""
    kb_type_map = {
        "hpv": KnowledgeBaseType.HPV,
        "flu": KnowledgeBaseType.FLU,
        "hiv": KnowledgeBaseType.HIV
    }
    
    if kb_name.lower() not in kb_type_map:
        print(f"错误：不支持的知识库类型 '{kb_name}'")
        print(f"支持的类型：{list(kb_type_map.keys())}")
        return
    
    kb_type = kb_type_map[kb_name.lower()]
    manager = get_kb_manager()
    
    # 检查配置文件
    config_file = Path(f"input/{kb_name}/excel_config.json")
    excel_config = None
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                excel_config = json.load(f)
            print(f"使用配置文件: {config_file}")
        except Exception as e:
            print(f"读取配置文件失败: {e}")
    else:
        print(f"未找到配置文件: {config_file}")
        print("将使用默认配置或仅处理PDF文件")
    
    print(f"\n=== 构建 {kb_name.upper()} 知识库 ===")
    result = manager.build_knowledge_base(kb_type, excel_config)
    print(f"构建结果: {result}")


def show_help():
    """显示帮助信息"""
    print("知识库构建工具")
    print("用法:")
    print("  python build_knowledge_bases.py [知识库名称]")
    print("")
    print("参数:")
    print("  知识库名称: hpv, flu, hiv (可选，不指定则构建所有知识库)")
    print("")
    print("示例:")
    print("  python build_knowledge_bases.py          # 构建所有知识库")
    print("  python build_knowledge_bases.py hpv      # 只构建HPV知识库")
    print("  python build_knowledge_bases.py flu      # 只构建FLU知识库")
    print("  python build_knowledge_bases.py hiv      # 只构建HIV知识库")
    print("")
    print("目录结构:")
    print("  input/")
    print("  ├── hpv/")
    print("  │   ├── pdf/          # PDF文件")
    print("  │   ├── excel/        # Excel文件")
    print("  │   └── excel_config.json  # Excel配置（可选）")
    print("  ├── flu/")
    print("  │   ├── pdf/")
    print("  │   ├── excel/")
    print("  │   └── excel_config.json")
    print("  └── hiv/")
    print("      ├── pdf/")
    print("      ├── excel/")
    print("      └── excel_config.json")
    print("")
    print("Excel配置文件格式:")
    print("  {")
    print('    "content_column": "内容列名",')
    print('    "source_column": "来源列名",')
    print('    "link_column": "链接列名",')
    print('    "sheet_name": "工作表名"')
    print("  }")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help", "help"]:
            show_help()
            return
        
        # 构建指定知识库
        build_specific_knowledge_base(sys.argv[1])
    else:
        # 构建所有知识库
        build_all_knowledge_bases()


if __name__ == "__main__":
    main() 