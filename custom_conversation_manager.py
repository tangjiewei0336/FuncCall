"""
自定义对话管理器模块
使用提示词拼接和输出解析的方式实现工具调用
"""

from typing import List, Dict, Any, Optional
from models import SimpleLLMClient
from utils import PromptBuilder, ToolCallParser, MessageHandler
from tools import get_tool_function


class CustomConversationManager:
    """自定义对话管理器类"""
    
    def __init__(self, api_key: str = None, model: str = "qwen-plus", max_tool_calls: int = 10):
        """
        初始化自定义对话管理器
        
        Args:
            api_key: API密钥
            model: 模型名称
            max_tool_calls: 最大工具调用轮数，防止无限循环
        """
        self.llm_client = SimpleLLMClient(api_key, model)
        self.prompt_builder = PromptBuilder()
        self.tool_parser = ToolCallParser()
        self.message_handler = MessageHandler()
        self.max_tool_calls = max_tool_calls
    
    def process_user_input(self, user_input: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> tuple[str, List[Dict[str, Any]]]:
        """
        处理用户输入，支持多轮工具调用和对话历史
        
        Args:
            user_input: 用户输入内容
            conversation_history: 对话历史记录
            
        Returns:
            (最终回答, 更新后的对话历史)
        """
        # 初始化或使用现有对话历史
        if conversation_history is None:
            conversation_history = []
        else:
            conversation_history = conversation_history.copy()
        
        # 添加用户输入到历史
        user_message = self.message_handler.create_user_message(user_input)
        conversation_history.append(user_message)
        
        # 多轮工具调用循环
        tool_call_count = 0
        
        while tool_call_count < self.max_tool_calls:
            print(f"\n=== 第 {tool_call_count + 1} 轮调用 ===")
            
            # 构建完整提示词
            full_prompt = self.prompt_builder.build_prompt_with_tools(user_input, conversation_history)
            
            # 调用模型
            model_response = self.llm_client.call(full_prompt)
            print(f"模型原始输出：\n{model_response}\n")
            
            # 检查是否包含工具调用
            if not self.tool_parser.has_tool_calls(model_response):
                # 没有工具调用，直接返回回答
                final_answer = self.tool_parser.extract_regular_response(model_response)
                print(f"最终答案：{final_answer}")
                
                # 添加助手回答到对话历史
                assistant_message = self.message_handler.create_assistant_message(final_answer)
                conversation_history.append(assistant_message)
                
                return final_answer, conversation_history
            
            # 解析工具调用
            tool_calls = self.tool_parser.parse_tool_calls(model_response)
            print(f"检测到 {len(tool_calls)} 个工具调用")
            
            # 提取助手的回答部分（如果有的话）
            assistant_content = self.tool_parser.extract_regular_response(model_response)
            if assistant_content.strip():
                assistant_message = self.message_handler.create_assistant_message(assistant_content)
                conversation_history.append(assistant_message)
            
            # 执行工具调用
            for i, tool_call in enumerate(tool_calls):
                try:
                    tool_name = tool_call["name"]
                    arguments = tool_call["arguments"]
                    
                    print(f"工具 {i+1} ({tool_name}) 参数：{arguments}")
                    
                    # 获取并执行工具函数
                    tool_function = get_tool_function(tool_name)
                    if tool_function:
                        tool_result = tool_function(**arguments)
                        print(f"工具 {i+1} ({tool_name}) 输出：{tool_result}")
                        
                        # 添加工具消息到对话历史
                        tool_message = self.message_handler.create_tool_message(tool_name, tool_result)
                        conversation_history.append(tool_message)
                    else:
                        error_msg = f"未找到工具：{tool_name}"
                        print(f"错误：{error_msg}")
                        
                        # 添加错误消息到对话历史
                        error_message = self.message_handler.create_tool_message(tool_name, error_msg)
                        conversation_history.append(error_message)
                        
                except Exception as e:
                    error_msg = f"工具调用失败：{e}"
                    print(f"错误：{error_msg}")
                    
                    # 添加错误消息到对话历史
                    tool_name = tool_call.get("name", "unknown")
                    error_message = self.message_handler.create_tool_message(tool_name, error_msg)
                    conversation_history.append(error_message)
            
            tool_call_count += 1
            print(f"完成第 {tool_call_count} 轮工具调用\n")
        
        # 如果达到最大轮数，返回当前结果
        print(f"警告：已达到最大工具调用轮数 ({self.max_tool_calls})")
        final_answer = self.tool_parser.extract_regular_response(model_response)
        print(f"最终答案：{final_answer}")
        
        # 添加助手回答到对话历史
        assistant_message = self.message_handler.create_assistant_message(final_answer)
        conversation_history.append(assistant_message)
        
        return final_answer, conversation_history
    
    def start_conversation(self):
        """开始交互式对话"""
        print("欢迎使用自定义工具调用智能助手！")
        print("输入 'quit' 或 'exit' 退出对话。")
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
                
                # 处理用户输入
                answer, conversation_history = self.process_user_input(user_input, conversation_history)
                
            except KeyboardInterrupt:
                print("\n\n再见！")
                break
            except Exception as e:
                print(f"发生错误：{e}")
                continue 