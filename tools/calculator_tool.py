"""
计算器工具模块
支持基本数学运算
"""

import re
from typing import Union, Dict, Any


def calculate(expression: str) -> str:
    """
    计算数学表达式
    
    Args:
        expression: 数学表达式，如 "2+3*4" 或 "sqrt(16)"
        
    Returns:
        计算结果字符串
    """
    try:
        # 安全检查：只允许数字、运算符、括号、字母和基本函数
        allowed_chars = r'^[0-9+\-*/().\s,a-zA-Z]+$'
        if not re.match(allowed_chars, expression):
            return "错误：表达式包含不允许的字符"
        
        # 额外的安全检查：不允许危险的关键字
        dangerous_keywords = ['import', 'exec', 'eval', 'open', 'file', 'system', 'subprocess']
        expression_lower = expression.lower()
        for keyword in dangerous_keywords:
            if keyword in expression_lower:
                return "错误：表达式包含不允许的字符"
        
        # 替换一些常见的数学函数
        expression = expression.lower()
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('pow', 'math.pow')
        expression = expression.replace('abs', 'abs')
        
        # 添加math模块导入
        import math
        
        # 计算表达式
        result = eval(expression, {"__builtins__": {}}, {"math": math, "abs": abs})
        
        # 格式化结果
        if isinstance(result, (int, float)):
            if result == int(result):
                return f"计算结果：{int(result)}"
            else:
                return f"计算结果：{result:.4f}"
        else:
            return f"计算结果：{result}"
            
    except ZeroDivisionError:
        return "错误：除数不能为零"
    except Exception as e:
        return f"计算错误：{str(e)}"


def get_calculator_tool_config():
    """
    获取计算器工具的配置信息
    
    Returns:
        工具配置字典
    """
    return {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，支持基本运算（+、-、*、/、()）和函数（sqrt、pow、abs）",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，例如：2+3*4、sqrt(16)、pow(2,3)"
                    }
                },
                "required": ["expression"]
            }
        }
    } 