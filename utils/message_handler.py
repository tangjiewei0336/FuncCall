"""
消息处理工具模块
"""

import json
from typing import List, Dict, Any
from tools import get_tool_function


class MessageHandler:
    """消息处理类"""
    
    def __init__(self):
        pass
    
    def create_user_message(self, content: str) -> Dict[str, str]:
        """
        创建用户消息
        
        Args:
            content: 消息内容
            
        Returns:
            用户消息字典
        """
        return {
            "content": content,
            "role": "user",
        }
    
    def create_assistant_message(self, content: str, tool_calls: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        创建助手消息
        
        Args:
            content: 消息内容
            tool_calls: 工具调用列表
            
        Returns:
            助手消息字典
        """
        message = {
            "content": content,
            "role": "assistant",
        }
        
        if tool_calls:
            message["tool_calls"] = tool_calls
            
        return message
    
    def create_tool_message(self, name: str, content: str) -> Dict[str, str]:
        """
        创建工具消息
        
        Args:
            name: 工具名称
            content: 工具输出内容
            
        Returns:
            工具消息字典
        """
        return {
            "name": name,
            "role": "tool",
            "content": content,
        }
    
    def extract_tool_call_info(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取工具调用信息
        
        Args:
            tool_call: 工具调用字典
            
        Returns:
            工具调用信息字典
        """
        function_info = tool_call["function"]
        return {
            "name": function_info["name"],
            "arguments": json.loads(function_info["arguments"])
        }
    
    def execute_tool_call(self, tool_call: Dict[str, Any]) -> str:
        """
        执行工具调用
        
        Args:
            tool_call: 工具调用字典
            
        Returns:
            工具执行结果
        """
        tool_info = self.extract_tool_call_info(tool_call)
        tool_name = tool_info["name"]
        arguments = tool_info["arguments"]
        
        # 获取工具函数
        tool_function = get_tool_function(tool_name)
        
        if not tool_function:
            raise ValueError(f"未找到工具: {tool_name}")
        
        # 执行工具函数
        result = tool_function(**arguments)
        return result 