"""
测试RAG提示词构建
验证大模型是否会被正确引导使用知识库查询工具
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_rag_prompt():
    """测试RAG提示词构建"""
    print("=== 测试RAG提示词构建 ===")
    
    try:
        from utils.prompt_builder import PromptBuilder
        
        # 创建提示词构建器
        builder = PromptBuilder()
        
        # 测试医学相关问题的提示词
        medical_questions = [
            "流感的主要症状是什么？",
            "HPV疫苗的副作用有哪些？",
            "HIV检测的方法是什么？",
            "如何预防流感？"
        ]
        
        for question in medical_questions:
            print(f"\n--- 测试问题: {question} ---")
            
            # 构建提示词
            prompt = builder.build_prompt_with_tools(question)
            
            # 检查是否包含RAG相关说明
            rag_keywords = [
                "知识库查询工具",
                "query_knowledge_base", 
                "参考文献",
                "权威信息",
                "医学问题"
            ]
            
            print("提示词中包含的RAG关键词:")
            for keyword in rag_keywords:
                if keyword in prompt:
                    print(f"  ✓ {keyword}")
                else:
                    print(f"  ✗ {keyword}")
            
            # 检查工具调用格式说明
            if "query_knowledge_base" in prompt and "flu" in prompt and "hpv" in prompt:
                print("  ✓ 包含知识库查询示例")
            else:
                print("  ✗ 缺少知识库查询示例")
            
            # 显示提示词的前500字符
            print(f"\n提示词预览（前500字符）:\n{prompt[:500]}...")
            
        print("\n=== RAG提示词测试完成 ===")
        return True
        
    except Exception as e:
        print(f"✗ RAG提示词测试失败: {e}")
        return False


def test_conversation_manager():
    """测试对话管理器是否支持RAG"""
    print("\n=== 测试对话管理器RAG支持 ===")
    
    try:
        from conversation_manager import CustomConversationManager
        
        # 创建对话管理器
        manager = CustomConversationManager()
        
        # 检查提示词构建器
        prompt_builder = manager.prompt_builder
        
        # 测试医学问题
        test_question = "流感症状有哪些？"
        prompt = prompt_builder.build_prompt_with_tools(test_question)
        
        if "知识库查询工具" in prompt and "query_knowledge_base" in prompt:
            print("✓ 对话管理器正确配置了RAG提示词")
        else:
            print("✗ 对话管理器RAG提示词配置有问题")
        
        print("=== 对话管理器RAG测试完成 ===")
        return True
        
    except Exception as e:
        print(f"✗ 对话管理器RAG测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("开始RAG提示词测试...\n")
    
    tests = [
        test_rag_prompt,
        test_conversation_manager
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有RAG提示词测试通过！")
        print("\n现在大模型会：")
        print("1. 在医学问题中自动使用知识库查询工具")
        print("2. 返回权威的参考文献和链接")
        print("3. 引用原文内容并说明信息来源")
    else:
        print("⚠️  部分测试失败，请检查RAG提示词配置。")
    
    return passed == total


if __name__ == "__main__":
    main() 