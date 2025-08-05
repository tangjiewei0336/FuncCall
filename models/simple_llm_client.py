"""
简单LLM客户端模块
不使用原生tool功能，直接调用模型
"""

import os
import random
from typing import List, Dict, Any
from dashscope import Generation


class SimpleLLMClient:
    """简单LLM客户端类"""
    
    def __init__(self, api_key: str = None, model: str = "qwen-plus"):
        """
        初始化简单LLM客户端
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            model: 模型名称
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("API密钥未设置，请设置DASHSCOPE_API_KEY环境变量或传入api_key参数")
    
    def call(self, prompt: str) -> str:
        """
        调用大语言模型
        
        Args:
            prompt: 完整的提示词
            
        Returns:
            模型响应文本
        """
        try:
            response = Generation.call(
                api_key=self.api_key,
                model=self.model,
                prompt=prompt,
                seed=random.randint(1, 10000),
                result_format="text",  # 使用文本格式而不是message格式
            )
            
            # 提取响应文本
            if hasattr(response, 'output') and hasattr(response.output, 'text'):
                return response.output.text
            else:
                return str(response)
                
        except Exception as e:
            raise Exception(f"调用模型失败：{e}")
    
    def call_with_messages(self, messages: List[Dict[str, Any]]) -> str:
        """
        使用消息格式调用模型（兼容性方法）
        
        Args:
            messages: 消息列表
            
        Returns:
            模型响应文本
        """
        # 将消息转换为提示词
        prompt = self._messages_to_prompt(messages)
        return self.call(prompt)
    
    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """
        将消息列表转换为提示词
        
        Args:
            messages: 消息列表
            
        Returns:
            提示词文本
        """
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "user":
                prompt_parts.append(f"用户：{content}")
            elif role == "assistant":
                prompt_parts.append(f"助手：{content}")
            elif role == "tool":
                name = message.get("name", "")
                prompt_parts.append(f"工具({name})：{content}")
        
        return "\n\n".join(prompt_parts) 