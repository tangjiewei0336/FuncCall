"""
自定义工具调用演示脚本
展示使用提示词拼接和输出解析的方式实现工具调用
"""

from conversation_manager import CustomConversationManager
from utils.prompt_builder import PromptBuilder
from utils.tool_parser import ToolCallParser


def demo_prompt_building():
    """演示提示词构建功能"""
    print("=== 演示1：提示词构建功能 ===")
    
    builder = PromptBuilder()
    
    # 演示简单提示词构建
    user_input = "现在几点了？"
    prompt = builder.build_prompt_with_tools(user_input)
    
    print(f"用户输入：{user_input}")
    print(f"生成的提示词长度：{len(prompt)} 字符")
    print("提示词预览（前500字符）：")
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    
    # 演示带历史的提示词构建
    print("\n--- 带对话历史的提示词 ---")
    history = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "您好！我是智能助手，有什么可以帮助您的吗？"},
        {"role": "user", "content": "现在几点了？"},
        {"role": "assistant", "content": "我来帮您查询时间"},
        {"role": "tool", "name": "get_current_time", "content": "当前时间：2024-01-01 12:00:00"}
    ]
    
    prompt_with_history = builder.build_prompt_with_tools("北京天气如何？", history)
    print(f"带历史的提示词长度：{len(prompt_with_history)} 字符")


def demo_tool_parsing():
    """演示工具调用解析功能"""
    print("\n=== 演示2：工具调用解析功能 ===")
    
    parser = ToolCallParser()
    
    # 演示解析简单工具调用
    print("--- 解析简单工具调用 ---")
    simple_output = """
    我来帮您查询时间。
    
    <tool_call>
    工具名称：get_current_time
    参数：{}
    </tool_call>
    """
    
    tool_calls = parser.parse_tool_calls(simple_output)
    print(f"解析结果：{tool_calls}")
    
    # 演示解析带参数的工具调用
    print("\n--- 解析带参数的工具调用 ---")
    complex_output = """
    我来查询北京的天气。
    
    <tool_call>
    工具名称：get_current_weather
    参数：{"location": "北京"}
    </tool_call>
    """
    
    tool_calls = parser.parse_tool_calls(complex_output)
    print(f"解析结果：{tool_calls}")
    
    # 演示解析多个工具调用
    print("\n--- 解析多个工具调用 ---")
    multiple_output = """
    我来帮您查询时间和天气。
    
    <tool_call>
    工具名称：get_current_time
    参数：{}
    </tool_call>
    
    <tool_call>
    工具名称：get_current_weather
    参数：{"location": "北京"}
    </tool_call>
    """
    
    tool_calls = parser.parse_tool_calls(multiple_output)
    print(f"解析结果：{tool_calls}")
    
    # 演示提取常规回答
    print("\n--- 提取常规回答 ---")
    regular_response = parser.extract_regular_response(multiple_output)
    print(f"常规回答：{regular_response}")


def demo_custom_conversation():
    """演示自定义对话功能"""
    print("\n=== 演示3：自定义对话功能 ===")
    
    try:
        # 创建自定义对话管理器
        manager = CustomConversationManager(max_tool_calls=3)
        
        # 演示简单查询
        print("--- 演示时间查询 ---")
        user_input = "现在几点了？"
        print(f"用户输入：{user_input}")
        
        # 注意：这里只是演示，实际运行需要API密钥
        print("（需要API密钥才能实际运行）")
        
    except Exception as e:
        print(f"演示过程中发生错误：{e}")


def demo_tool_format():
    """演示工具格式说明"""
    print("\n=== 演示4：工具格式说明 ===")
    
    print("工具调用格式示例：")
    print()
    print("<tool_call>")
    print("工具名称：get_current_time")
    print("参数：{}")
    print("</tool_call>")
    print()
    print("<tool_call>")
    print("工具名称：get_current_weather")
    print('参数：{"location": "北京"}')
    print("</tool_call>")
    print()
    print("模型需要按照这个格式输出工具调用信息，")
    print("系统会自动解析并执行相应的工具。")


def main():
    """主函数"""
    print("自定义工具调用演示")
    print("=" * 50)
    
    try:
        # 运行各种演示
        demo_prompt_building()
        demo_tool_parsing()
        demo_custom_conversation()
        demo_tool_format()
        
        print("\n" + "=" * 50)
        print("演示完成！")
        print("\n使用方法：")
        print("1. 设置 DASHSCOPE_API_KEY 环境变量")
        print("2. 运行：python3 custom_main.py")
        
    except Exception as e:
        print(f"演示过程中发生错误：{e}")


if __name__ == "__main__":
    main() 