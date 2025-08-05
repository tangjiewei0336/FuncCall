"""
多轮工具调用演示脚本
展示工具之间的依赖关系和复杂任务处理
"""

from conversation_manager import ConversationManager


def demo_simple_multi_tool():
    """演示简单的多轮工具调用"""
    print("=== 演示1：简单的多轮工具调用 ===")
    
    # 创建对话管理器，设置最大5轮工具调用
    manager = ConversationManager(max_tool_calls=5)
    
    # 示例：查询技术部员工的平均工资
    # 这可能需要：1. 查询技术部员工 2. 计算平均工资
    user_input = "请帮我计算技术部员工的平均工资"
    
    print(f"用户输入：{user_input}")
    result = manager.process_user_input(user_input)
    print(f"\n最终结果：{result}")


def demo_complex_analysis():
    """演示复杂的数据分析任务"""
    print("\n=== 演示2：复杂的数据分析任务 ===")
    
    manager = ConversationManager(max_tool_calls=8)
    
    # 示例：分析销售数据
    user_input = "请分析一下我们的销售情况，包括总销售额、平均订单金额，并计算利润率（假设成本是销售额的70%）"
    
    print(f"用户输入：{user_input}")
    result = manager.process_user_input(user_input)
    print(f"\n最终结果：{result}")


def demo_error_handling():
    """演示错误处理"""
    print("\n=== 演示3：错误处理 ===")
    
    manager = ConversationManager(max_tool_calls=5)
    
    # 示例：包含错误的查询
    user_input = "请查询不存在的表，然后计算2+3"
    
    print(f"用户输入：{user_input}")
    result = manager.process_user_input(user_input)
    print(f"\n最终结果：{result}")


def demo_conversation_history():
    """演示对话历史功能"""
    print("\n=== 演示4：对话历史功能 ===")
    
    manager = ConversationManager(max_tool_calls=5)
    
    # 模拟多轮对话
    conversations = [
        "请查询技术部的员工信息",
        "这些员工的平均年龄是多少？",
        "他们的总工资支出是多少？"
    ]
    
    conversation_history = []
    
    for i, user_input in enumerate(conversations, 1):
        print(f"\n--- 第{i}轮对话 ---")
        print(f"用户输入：{user_input}")
        
        answer, conversation_history = manager.process_user_input_with_history(
            user_input, conversation_history
        )
        
        print(f"助手回答：{answer}")
        print(f"对话历史长度：{len(conversation_history)} 条消息")


def main():
    """主函数"""
    print("多轮工具调用演示")
    print("=" * 50)
    
    try:
        # 运行各种演示
        demo_simple_multi_tool()
        demo_complex_analysis()
        demo_error_handling()
        demo_conversation_history()
        
        print("\n" + "=" * 50)
        print("演示完成！")
        
    except Exception as e:
        print(f"演示过程中发生错误：{e}")
        print("请确保已设置 DASHSCOPE_API_KEY 环境变量")


if __name__ == "__main__":
    main() 