"""
工具测试模块
"""

import unittest
from datetime import datetime
from tools.weather_tool import get_current_weather, get_weather_tool_config
from tools.time_tool import get_current_time, get_time_tool_config
from tools.tool_registry import get_tools, get_tool_function


class TestWeatherTool(unittest.TestCase):
    """天气工具测试类"""
    
    def test_get_current_weather(self):
        """测试天气查询功能"""
        result = get_current_weather("北京")
        self.assertIn("北京", result)
        self.assertIn("晴天", result)
    
    def test_get_weather_tool_config(self):
        """测试天气工具配置"""
        config = get_weather_tool_config()
        self.assertEqual(config["type"], "function")
        self.assertEqual(config["function"]["name"], "get_current_weather")
        self.assertIn("location", config["function"]["parameters"]["properties"])


class TestTimeTool(unittest.TestCase):
    """时间工具测试类"""
    
    def test_get_current_time(self):
        """测试时间查询功能"""
        result = get_current_time()
        self.assertIn("当前时间：", result)
        
        # 验证时间格式
        time_str = result.replace("当前时间：", "").replace("。", "")
        try:
            datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.fail("时间格式不正确")
    
    def test_get_time_tool_config(self):
        """测试时间工具配置"""
        config = get_time_tool_config()
        self.assertEqual(config["type"], "function")
        self.assertEqual(config["function"]["name"], "get_current_time")
        self.assertEqual(config["function"]["parameters"], {})


class TestToolRegistry(unittest.TestCase):
    """工具注册表测试类"""
    
    def test_get_tools(self):
        """测试获取工具配置列表"""
        tools = get_tools()
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)
        
        # 验证工具配置格式
        for tool in tools:
            self.assertIn("type", tool)
            self.assertIn("function", tool)
            self.assertIn("name", tool["function"])
    
    def test_get_tool_function(self):
        """测试获取工具函数"""
        # 测试获取天气工具
        weather_func = get_tool_function("get_current_weather")
        self.assertIsNotNone(weather_func)
        self.assertTrue(callable(weather_func))
        
        # 测试获取时间工具
        time_func = get_tool_function("get_current_time")
        self.assertIsNotNone(time_func)
        self.assertTrue(callable(time_func))
        
        # 测试获取不存在的工具
        non_existent_func = get_tool_function("non_existent_tool")
        self.assertIsNone(non_existent_func)


if __name__ == "__main__":
    unittest.main() 