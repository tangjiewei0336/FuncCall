"""
工具注册表模块
用于管理和注册所有可用的工具
"""

from .weather_tool import get_weather_tool_config
from .time_tool import get_time_tool_config
from .calculator_tool import get_calculator_tool_config
from .knowledge_base_tool import get_knowledge_base_tool_config


class ToolRegistry:
    """工具注册表类"""
    
    def __init__(self):
        self._tools = {}
        self._tool_configs = []
        self._register_default_tools()
    
    def _register_default_tools(self):
        """注册默认工具"""
        # 注册天气工具
        self.register_tool(
            name="get_current_weather",
            function=self._get_weather_function,
            config=get_weather_tool_config()
        )
        
        # 注册时间工具
        self.register_tool(
            name="get_current_time",
            function=self._get_time_function,
            config=get_time_tool_config()
        )
        
        # 注册计算器工具
        self.register_tool(
            name="calculate",
            function=self._get_calculator_function,
            config=get_calculator_tool_config()
        )

        # 注册知识库查询工具
        self.register_tool(
            name="query_knowledge_base",
            function=self._get_knowledge_base_function,
            config=get_knowledge_base_tool_config()
        )
    
    def _get_weather_function(self, **kwargs):
        """获取天气工具函数"""
        from .weather_tool import get_current_weather
        return get_current_weather(**kwargs)
    
    def _get_time_function(self, **kwargs):
        """获取时间工具函数"""
        from .time_tool import get_current_time
        return get_current_time(**kwargs)
    
    def _get_calculator_function(self, **kwargs):
        """获取计算器工具函数"""
        from .calculator_tool import calculate
        return calculate(**kwargs)

    
    def _get_knowledge_base_function(self, **kwargs):
        """获取知识库查询工具函数"""
        from .knowledge_base_tool import query_knowledge_base
        return query_knowledge_base(**kwargs)
    
    def register_tool(self, name: str, function, config: dict):
        """
        注册新工具
        
        Args:
            name: 工具名称
            function: 工具函数
            config: 工具配置
        """
        self._tools[name] = function
        self._tool_configs.append(config)
    
    def get_tool(self, name: str):
        """
        获取工具函数
        
        Args:
            name: 工具名称
            
        Returns:
            工具函数
        """
        return self._tools.get(name)
    
    def get_tool_configs(self):
        """
        获取所有工具配置
        
        Returns:
            工具配置列表
        """
        return self._tool_configs.copy()
    
    def list_tools(self):
        """
        列出所有可用工具
        
        Returns:
            工具名称列表
        """
        return list(self._tools.keys())


# 全局工具注册表实例
_tool_registry = ToolRegistry()


def get_tools():
    """
    获取所有工具配置
    
    Returns:
        工具配置列表
    """
    return _tool_registry.get_tool_configs()


def get_tool_function(name: str):
    """
    获取指定工具的函数
    
    Args:
        name: 工具名称
        
    Returns:
        工具函数
    """
    return _tool_registry.get_tool(name)


def register_tool(name: str, function, config: dict):
    """
    注册新工具
    
    Args:
        name: 工具名称
        function: 工具函数
        config: 工具配置
    """
    _tool_registry.register_tool(name, function, config) 