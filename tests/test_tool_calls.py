"""
自定义工具调用测试模块
"""

import unittest
from utils.prompt_builder import PromptBuilder
from utils.tool_parser import ToolCallParser
from tools import get_tools


class TestPromptBuilder(unittest.TestCase):
    """提示词构建器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.builder = PromptBuilder()
    
    def test_build_prompt_with_tools(self):
        """测试构建包含工具信息的提示词"""
        user_input = "现在几点了？"
        prompt = self.builder.build_prompt_with_tools(user_input)
        
        # 检查提示词包含必要信息
        self.assertIn("智能助手", prompt)
        self.assertIn("可用的工具", prompt)
        self.assertIn("工具调用格式说明", prompt)
        self.assertIn(user_input, prompt)
    
    def test_build_prompt_with_history(self):
        """测试构建包含对话历史的提示词"""
        user_input = "北京天气如何？"
        history = [
            {"role": "user", "content": "现在几点了？"},
            {"role": "assistant", "content": "我来帮您查询时间"},
            {"role": "tool", "name": "get_current_time", "content": "当前时间：2024-01-01 12:00:00"}
        ]
        
        prompt = self.builder.build_prompt_with_tools(user_input, history)
        
        # 检查包含对话历史
        self.assertIn("对话历史", prompt)
        self.assertIn("现在几点了？", prompt)
        self.assertIn("我来帮您查询时间", prompt)
        self.assertIn("工具(get_current_time)", prompt)
    
    def test_get_available_tools(self):
        """测试获取可用工具列表"""
        tools = self.builder.get_available_tools()
        
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)
        self.assertIn("get_current_time", tools)
        self.assertIn("get_current_weather", tools)


class TestToolCallParser(unittest.TestCase):
    """工具调用解析器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.parser = ToolCallParser()
    
    def test_parse_simple_tool_call(self):
        """测试解析简单工具调用"""
        model_output = """
        我来帮您查询时间。
        
        <tool_call>
        工具名称：get_current_time
        参数：{}
        </tool_call>
        """
        
        tool_calls = self.parser.parse_tool_calls(model_output)
        
        self.assertEqual(len(tool_calls), 1)
        self.assertEqual(tool_calls[0]["name"], "get_current_time")
        self.assertEqual(tool_calls[0]["arguments"], {})
    
    def test_parse_tool_call_with_params(self):
        """测试解析带参数的工具调用"""
        model_output = """
        我来查询北京的天气。
        
        <tool_call>
        工具名称：get_current_weather
        参数：{"location": "北京"}
        </tool_call>
        """
        
        tool_calls = self.parser.parse_tool_calls(model_output)
        
        self.assertEqual(len(tool_calls), 1)
        self.assertEqual(tool_calls[0]["name"], "get_current_weather")
        self.assertEqual(tool_calls[0]["arguments"]["location"], "北京")
    
    def test_parse_multiple_tool_calls(self):
        """测试解析多个工具调用"""
        model_output = """
        我来帮您查询时间和天气。
        
        <tool_call>
        工具名称：get_current_time
        参数：{}
        </tool_call>
        
        <tool_call>
        工具名称：get_current_weather
        参数：{"location": "北京"}
        </tool_call>
        """
        
        tool_calls = self.parser.parse_tool_calls(model_output)
        
        self.assertEqual(len(tool_calls), 2)
        self.assertEqual(tool_calls[0]["name"], "get_current_time")
        self.assertEqual(tool_calls[1]["name"], "get_current_weather")
    
    def test_parse_invalid_tool_call(self):
        """测试解析无效的工具调用"""
        model_output = """
        这是一个无效的工具调用格式。
        
        <tool_call>
        无效格式
        </tool_call>
        """
        
        tool_calls = self.parser.parse_tool_calls(model_output)
        
        self.assertEqual(len(tool_calls), 0)
    
    def test_extract_regular_response(self):
        """测试提取常规回答"""
        model_output = """
        我来帮您查询时间。
        
        <tool_call>
        工具名称：get_current_time
        参数：{}
        </tool_call>
        
        这是额外的回答内容。
        """
        
        regular_response = self.parser.extract_regular_response(model_output)
        
        self.assertIn("我来帮您查询时间", regular_response)
        self.assertIn("这是额外的回答内容", regular_response)
        self.assertNotIn("<tool_call>", regular_response)
    
    def test_has_tool_calls(self):
        """测试检查是否包含工具调用"""
        # 包含工具调用的输出
        output_with_tools = """
        <tool_call>
        工具名称：get_current_time
        参数：{}
        </tool_call>
        """
        self.assertTrue(self.parser.has_tool_calls(output_with_tools))
        
        # 不包含工具调用的输出
        output_without_tools = "这是一个普通的回答，没有工具调用。"
        self.assertFalse(self.parser.has_tool_calls(output_without_tools))
    
    def test_format_tool_call_for_display(self):
        """测试格式化工具调用信息"""
        tool_call = {
            "name": "get_current_weather",
            "arguments": {"location": "北京"}
        }
        
        formatted = self.parser.format_tool_call_for_display(tool_call)
        
        self.assertIn("工具：get_current_weather", formatted)
        self.assertIn("参数", formatted)
        self.assertIn("北京", formatted)


if __name__ == "__main__":
    unittest.main() 