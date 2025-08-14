"""
知识库查询功能测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_knowledge_base_query():
    """测试知识库查询功能"""
    print("=== 测试知识库查询功能 ===")
    
    try:
        from tools.knowledge_base_tool import query_knowledge_base
        
        # 测试查询（假设知识库已构建）
        test_queries = [
            ("flu", "流感症状"),
            ("hpv", "HPV疫苗"),
            ("hiv", "HIV检测")
        ]
        
        for kb_type, query in test_queries:
            print(f"\n查询 {kb_type.upper()} 知识库: '{query}'")
            result = query_knowledge_base(kb_type, query, top_k=3)
            print(f"结果: {result[:200]}..." if len(result) > 200 else f"结果: {result}")
        
        print("✓ 知识库查询测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 知识库查询测试失败: {e}")
        return False


def test_knowledge_base_manager():
    """测试知识库管理器"""
    print("\n=== 测试知识库管理器 ===")
    
    try:
        from tools.knowledge_base_tool import get_kb_manager, KnowledgeBaseType
        
        manager = get_kb_manager()
        
        # 检查知识库状态
        for kb_type in KnowledgeBaseType:
            kb_dir = manager.base_dir / kb_type.value
            index_file = kb_dir / f"{kb_type.value}_index.faiss"
            docs_file = kb_dir / f"{kb_type.value}_documents.pkl"
            
            print(f"{kb_type.value.upper()} 知识库:")
            print(f"  目录: {kb_dir}")
            print(f"  索引文件: {'存在' if index_file.exists() else '不存在'}")
            print(f"  文档文件: {'存在' if docs_file.exists() else '不存在'}")
            
            if kb_type in manager.indices and manager.indices[kb_type] is not None:
                print(f"  文档数量: {len(manager.documents.get(kb_type, []))}")
            else:
                print("  状态: 未初始化")
            print()
        
        print("✓ 知识库管理器测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 知识库管理器测试失败: {e}")
        return False


def test_tool_registration():
    """测试工具注册"""
    print("\n=== 测试工具注册 ===")
    
    try:
        from tools.tool_registry import get_tools, get_tool_function
        
        # 获取所有工具配置
        tools = get_tools()
        tool_names = [tool["function"]["name"] for tool in tools]
        
        print("已注册的工具:")
        for name in tool_names:
            print(f"  - {name}")
        
        # 检查知识库查询工具是否已注册
        if "query_knowledge_base" in tool_names:
            print("✓ 知识库查询工具已注册")
            
            # 测试工具函数
            tool_func = get_tool_function("query_knowledge_base")
            if tool_func:
                print("✓ 知识库查询工具函数可用")
            else:
                print("✗ 知识库查询工具函数不可用")
        else:
            print("✗ 知识库查询工具未注册")
            return False
        
        print("✓ 工具注册测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 工具注册测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("开始知识库功能测试...\n")
    
    tests = [
        test_knowledge_base_manager,
        test_tool_registration,
        test_knowledge_base_query
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！")
        print("\n使用说明:")
        print("1. 将PDF文件放入 input/{kb_type}/pdf/ 目录")
        print("2. 将Excel文件放入 input/{kb_type}/excel/ 目录")
        print("3. 运行 python build_knowledge_bases.py 构建知识库")
        print("4. 使用 query_knowledge_base 工具查询知识库")
    else:
        print("⚠️  部分测试失败，请检查依赖安装和代码实现。")
    
    return passed == total


if __name__ == "__main__":
    main() 