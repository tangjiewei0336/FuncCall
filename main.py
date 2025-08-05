"""
主程序入口
使用提示词拼接和输出解析的方式实现工具调用
"""

from conversation_manager import CustomConversationManager


def main():
    """主函数"""
    try:
        # 创建自定义对话管理器
        conversation_manager = CustomConversationManager()
        
        # 开始对话
        conversation_manager.start_conversation()
        
    except Exception as e:
        print(f"程序启动失败：{e}")
        print("请确保已设置 DASHSCOPE_API_KEY 环境变量")


if __name__ == "__main__":
    main() 