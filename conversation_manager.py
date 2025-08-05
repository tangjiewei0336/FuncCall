"""
对话管理器模块
整合所有组件，提供完整的对话功能
"""

from typing import List, Dict, Any, Optional
from models import LLMClient
from utils import MessageHandler
from tools import get_tools


class ConversationManager:
    """对话管理器类"""
    
    def __init__(self, api_key: str = None, model: str = "qwen-plus", max_tool_calls: int = 10):
        """
        初始化对话管理器
        
        Args:
            api_key: API密钥
            model: 模型名称
            max_tool_calls: 最大工具调用轮数，防止无限循环
        """
        self.llm_client = LLMClient(api_key, model)
        self.message_handler = MessageHandler()
        self.tools = get_tools()
        self.max_tool_calls = max_tool_calls
    
    def process_user_input(self, user_input: str) -> str:
        """
        处理用户输入，支持多轮工具调用
        
        Args:
            user_input: 用户输入内容
            
        Returns:
            最终回答
        """
        # 创建消息列表
        messages = [self.message_handler.create_user_message(user_input)]
        
        # 多轮工具调用循环
        tool_call_count = 0
        
        while tool_call_count < self.max_tool_calls:
            print(f"\n=== 第 {tool_call_count + 1} 轮调用 ===")
            
            # 调用模型
            response = self.llm_client.call(messages, self.tools)
            assistant_message = response.output.choices[0].message
            messages.append(assistant_message)
            
            print(f"大模型输出信息：{response}\n")
            
            # 检查是否需要调用工具
            if not self.llm_client.has_tool_calls(response):
                final_answer = assistant_message.get('content', '')
                print(f"最终答案：{final_answer}")
                return final_answer
            
            # 执行工具调用
            tool_calls = self.llm_client.get_tool_calls(response)
            print(f"检测到 {len(tool_calls)} 个工具调用")
            
            for i, tool_call in enumerate(tool_calls):
                try:
                    tool_result = self.message_handler.execute_tool_call(tool_call)
                    tool_name = self.message_handler.extract_tool_call_info(tool_call)["name"]
                    
                    print(f"工具 {i+1} ({tool_name}) 输出：{tool_result}")
                    
                    # 添加工具消息到对话历史
                    tool_message = self.message_handler.create_tool_message(tool_name, tool_result)
                    messages.append(tool_message)
                    
                except Exception as e:
                    error_msg = f"工具调用失败：{e}"
                    print(f"错误：{error_msg}")
                    
                    # 添加错误消息到对话历史
                    tool_name = self.message_handler.extract_tool_call_info(tool_call)["name"]
                    error_message = self.message_handler.create_tool_message(tool_name, error_msg)
                    messages.append(error_message)
            
            tool_call_count += 1
            print(f"完成第 {tool_call_count} 轮工具调用\n")
        
        # 如果达到最大轮数，返回当前结果
        print(f"警告：已达到最大工具调用轮数 ({self.max_tool_calls})")
        final_answer = self.llm_client.get_response_content(response)
        print(f"最终答案：{final_answer}")
        return final_answer
    
    def process_user_input_with_history(self, user_input: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> tuple[str, List[Dict[str, Any]]]:
        """
        处理用户输入，支持对话历史
        
        Args:
            user_input: 用户输入内容
            conversation_history: 对话历史记录
            
        Returns:
            (最终回答, 更新后的对话历史)
        """
        # 初始化或使用现有对话历史
        if conversation_history is None:
            messages = []
        else:
            messages = conversation_history.copy()
        
        # 添加用户输入
        messages.append(self.message_handler.create_user_message(user_input))
        
        # 多轮工具调用循环
        tool_call_count = 0
        
        while tool_call_count < self.max_tool_calls:
            print(f"\n=== 第 {tool_call_count + 1} 轮调用 ===")
            
            # 调用模型
            response = self.llm_client.call(messages, self.tools)
            assistant_message = response.output.choices[0].message
            messages.append(assistant_message)
            
            print(f"大模型输出信息：{response}\n")
            
            # 检查是否需要调用工具
            if not self.llm_client.has_tool_calls(response):
                final_answer = assistant_message.get('content', '')
                print(f"最终答案：{final_answer}")
                return final_answer, messages
            
            # 执行工具调用
            tool_calls = self.llm_client.get_tool_calls(response)
            print(f"检测到 {len(tool_calls)} 个工具调用")
            
            for i, tool_call in enumerate(tool_calls):
                try:
                    tool_result = self.message_handler.execute_tool_call(tool_call)
                    tool_name = self.message_handler.extract_tool_call_info(tool_call)["name"]
                    
                    print(f"工具 {i+1} ({tool_name}) 输出：{tool_result}")
                    
                    # 添加工具消息到对话历史
                    tool_message = self.message_handler.create_tool_message(tool_name, tool_result)
                    messages.append(tool_message)
                    
                except Exception as e:
                    error_msg = f"工具调用失败：{e}"
                    print(f"错误：{error_msg}")
                    
                    # 添加错误消息到对话历史
                    tool_name = self.message_handler.extract_tool_call_info(tool_call)["name"]
                    error_message = self.message_handler.create_tool_message(tool_name, error_msg)
                    messages.append(error_message)
            
            tool_call_count += 1
            print(f"完成第 {tool_call_count} 轮工具调用\n")
        
        # 如果达到最大轮数，返回当前结果
        print(f"警告：已达到最大工具调用轮数 ({self.max_tool_calls})")
        final_answer = self.llm_client.get_response_content(response)
        print(f"最终答案：{final_answer}")
        return final_answer, messages
    
    def start_conversation(self):
        """开始交互式对话"""
        print("欢迎使用智能助手！输入 'quit' 或 'exit' 退出对话。")
        print(f"支持最多 {self.max_tool_calls} 轮工具调用")
        
        conversation_history = []
        
        while True:
            try:
                user_input = input("\n请输入：").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("再见！")
                    break
                
                if not user_input:
                    continue
                
                # 使用带历史记录的处理方法
                answer, conversation_history = self.process_user_input_with_history(user_input, conversation_history)
                
            except KeyboardInterrupt:
                print("\n\n再见！")
                break
            except Exception as e:
                print(f"发生错误：{e}")
                continue 