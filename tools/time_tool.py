"""
时间查询工具模块
"""

from datetime import datetime


def get_current_time() -> str:
    """
    查询当前时间的工具
    
    Returns:
        格式化后的当前时间字符串
    """
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"


def get_time_tool_config():
    """
    获取时间工具的配置信息
    
    Returns:
        工具配置字典
    """
    return {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {},  # 因为获取当前时间无需输入参数，因此parameters为空字典
        },
    } 