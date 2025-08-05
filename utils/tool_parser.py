"""
工具调用解析器模块
解析模型输出中的工具调用信息
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple


class ToolCallParser:
    """工具调用解析器类"""
    
    def __init__(self):
        # 工具调用标签的正则表达式
        self.tool_call_pattern = r'<tool_call>\s*(.*?)\s*</tool_call>'
        self.flags = re.DOTALL | re.IGNORECASE
    
    def parse_tool_calls(self, model_output: str) -> List[Dict[str, Any]]:
        """
        解析模型输出中的工具调用
        
        Args:
            model_output: 模型输出文本
            
        Returns:
            工具调用列表
        """
        tool_calls = []
        
        # 查找所有工具调用标签
        matches = re.findall(self.tool_call_pattern, model_output, self.flags)
        
        for match in matches:
            tool_call = self._parse_single_tool_call(match.strip())
            if tool_call:
                tool_calls.append(tool_call)
        
        return tool_calls
    
    def _parse_single_tool_call(self, tool_call_text: str) -> Optional[Dict[str, Any]]:
        """
        解析单个工具调用
        
        Args:
            tool_call_text: 工具调用文本
            
        Returns:
            工具调用信息字典
        """
        try:
            # 提取工具名称
            tool_name_match = re.search(r'工具名称[：:]\s*(\w+)', tool_call_text)
            if not tool_name_match:
                return None
            
            tool_name = tool_name_match.group(1).strip()
            
            # 提取参数
            params_match = re.search(r'参数[：:]\s*(\{.*?\})', tool_call_text, re.DOTALL)
            if params_match:
                params_text = params_match.group(1).strip()
                try:
                    # 尝试解析JSON参数
                    params = json.loads(params_text)
                except json.JSONDecodeError:
                    # 如果JSON解析失败，尝试解析简单参数
                    params = self._parse_simple_params(params_text)
            else:
                params = {}
            
            return {
                "name": tool_name,
                "arguments": params
            }
            
        except Exception as e:
            print(f"解析工具调用时出错：{e}")
            return None
    
    def _parse_simple_params(self, params_text: str) -> Dict[str, Any]:
        """
        解析简单参数格式
        
        Args:
            params_text: 参数文本
            
        Returns:
            参数字典
        """
        params = {}
        
        # 移除大括号
        params_text = params_text.strip('{}')
        
        # 分割参数
        if params_text:
            param_pairs = params_text.split(',')
            for pair in param_pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    key = key.strip().strip('"\'')
                    value = value.strip().strip('"\'')
                    
                    # 尝试转换数值类型
                    try:
                        if value.isdigit():
                            value = int(value)
                        elif value.replace('.', '').replace('-', '').isdigit():
                            value = float(value)
                    except ValueError:
                        pass
                    
                    params[key] = value
        
        return params
    
    def extract_regular_response(self, model_output: str) -> str:
        """
        提取模型输出中的常规回答部分（非工具调用部分）
        
        Args:
            model_output: 模型输出文本
            
        Returns:
            常规回答文本
        """
        # 移除所有工具调用标签及其内容
        cleaned_output = re.sub(self.tool_call_pattern, '', model_output, flags=self.flags)
        
        # 清理多余的空白字符
        cleaned_output = re.sub(r'\n\s*\n', '\n\n', cleaned_output)
        cleaned_output = cleaned_output.strip()
        
        return cleaned_output
    
    def has_tool_calls(self, model_output: str) -> bool:
        """
        检查模型输出是否包含工具调用
        
        Args:
            model_output: 模型输出文本
            
        Returns:
            是否包含工具调用
        """
        return bool(re.search(self.tool_call_pattern, model_output, self.flags))
    
    def format_tool_call_for_display(self, tool_call: Dict[str, Any]) -> str:
        """
        格式化工具调用信息用于显示
        
        Args:
            tool_call: 工具调用信息
            
        Returns:
            格式化的显示文本
        """
        name = tool_call.get("name", "")
        arguments = tool_call.get("arguments", {})
        
        if arguments:
            args_str = json.dumps(arguments, ensure_ascii=False, indent=2)
            return f"工具：{name}\n参数：{args_str}"
        else:
            return f"工具：{name}\n参数：无" 