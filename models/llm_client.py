"""
大语言模型客户端模块
"""

import os
import random
from typing import List, Dict, Any
from dashscope import Generation


class LLMClient:
    """大语言模型客户端类"""
    
    def __init__(self, api_key: str = None, model: str = "qwen-plus"):
        """
        初始化LLM客户端
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            model: 模型名称
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("API密钥未设置，请设置DASHSCOPE_API_KEY环境变量或传入api_key参数")
    
    def call(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = None) -> Any:
        """
        调用大语言模型
        
        Args:
            messages: 消息列表
            tools: 工具列表
            
        Returns:
            模型响应
        """
        response = Generation.call(
            api_key=self.api_key,
            model=self.model,
            messages=messages,
            tools=tools,
            seed=random.randint(1, 10000),
            result_format="message",
        )
        return response
    
    def get_response_content(self, response: Any) -> str:
        """
        从响应中提取内容
        
        Args:
            response: 模型响应
            
        Returns:
            响应内容
        """
        return response.output.choices[0].message.get('content', '')
    
    def get_tool_calls(self, response: Any) -> List[Dict[str, Any]]:
        """
        从响应中提取工具调用信息
        
        Args:
            response: 模型响应
            
        Returns:
            工具调用列表
        """
        message = response.output.choices[0].message
        return message.get('tool_calls', [])
    
    def has_tool_calls(self, response: Any) -> bool:
        """
        检查响应是否包含工具调用
        
        Args:
            response: 模型响应
            
        Returns:
            是否包含工具调用
        """
        return len(self.get_tool_calls(response)) > 0 