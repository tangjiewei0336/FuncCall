"""
天气查询工具模块
"""

def get_current_weather(location: str) -> str:
    """
    模拟天气查询工具
    
    Args:
        location: 城市或县区名称
        
    Returns:
        天气信息字符串
    """
    return f"{location}今天是晴天。"


def get_weather_tool_config():
    """
    获取天气工具的配置信息
    
    Returns:
        工具配置字典
    """
    return {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    } 