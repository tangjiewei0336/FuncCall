"""
提示词构建器模块
将工具信息拼接到提示词末尾，用于自定义工具调用
"""

from typing import List, Dict, Any
from tools import get_tools


class PromptBuilder:
    """提示词构建器类"""
    
    def __init__(self):
        self.tools = get_tools()
    
    def build_prompt_with_tools(self, user_input: str, conversation_history: List[Dict[str, Any]] = None) -> str:
        """
        构建包含工具信息的完整提示词
        
        Args:
            user_input: 用户输入
            conversation_history: 对话历史
            
        Returns:
            完整的提示词
        """
        # 构建基础提示词
        base_prompt = self._build_base_prompt(user_input, conversation_history)
        
        # 添加工具信息
        tools_prompt = self._build_tools_prompt()
        
        # 添加工具调用格式说明
        format_prompt = self._build_format_prompt()
        
        # 组合完整提示词
        full_prompt = f"{base_prompt}\n\n{tools_prompt}\n\n{format_prompt}"
        
        return full_prompt
    
    def _build_base_prompt(self, user_input: str, conversation_history: List[Dict[str, Any]] = None) -> str:
        """
        构建基础提示词
        
        Args:
            user_input: 用户输入
            conversation_history: 对话历史
            
        Returns:
            基础提示词
        """
        prompt = "你是一个智能助手，可以帮助用户完成各种任务。"
        
        # 添加对话历史
        if conversation_history:
            prompt += "\n\n对话历史：\n"
            for message in conversation_history[-6:]:  # 只保留最近6条消息
                role = message.get("role", "")
                content = message.get("content", "")
                if role == "user":
                    prompt += f"用户：{content}\n"
                elif role == "assistant":
                    prompt += f"助手：{content}\n"
                elif role == "tool":
                    name = message.get("name", "")
                    prompt += f"工具({name})：{content}\n"
        
        # 添加当前用户输入
        prompt += f"\n当前用户输入：{user_input}\n"
        
        return prompt
    
    def _build_tools_prompt(self) -> str:
        """
        构建工具信息提示词
        
        Returns:
            工具信息提示词
        """
        prompt = "可用的工具：\n"
        
        for i, tool in enumerate(self.tools, 1):
            function_info = tool["function"]
            name = function_info["name"]
            description = function_info["description"]
            parameters = function_info.get("parameters", {})
            
            prompt += f"{i}. {name}：{description}\n"
            
            # 添加参数信息
            if parameters and "properties" in parameters:
                props = parameters["properties"]
                required = parameters.get("required", [])
                
                prompt += "   参数：\n"
                for param_name, param_info in props.items():
                    param_desc = param_info.get("description", "")
                    is_required = param_name in required
                    required_mark = "（必需）" if is_required else "（可选）"
                    prompt += f"   - {param_name}：{param_desc} {required_mark}\n"
            
            prompt += "\n"
        
        return prompt
    
    def _build_format_prompt(self) -> str:
        """
        构建工具调用格式说明
        
        Returns:
            格式说明提示词
        """
        prompt = """工具调用格式说明：

如果你需要使用工具，请按照以下格式输出：

<tool_call>
工具名称：get_current_time
参数：{}
</tool_call>

<tool_call>
工具名称：get_current_weather
参数：{"location": "北京"}
</tool_call>

如果你需要调用多个工具，可以连续使用多个<tool_call>标签。

如果不需要使用工具，直接回答用户问题即可。

请根据用户的需求，选择合适的工具进行调用，或者直接回答问题。"""
        
        return prompt
    
    def get_available_tools(self) -> List[str]:
        """
        获取可用工具名称列表
        
        Returns:
            工具名称列表
        """
        return [tool["function"]["name"] for tool in self.tools] 