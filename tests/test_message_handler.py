"""
消息处理测试模块
"""

import unittest
import json
from utils.message_handler import MessageHandler


class TestMessageHandler(unittest.TestCase):
    """消息处理测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.handler = MessageHandler()
    
    def test_create_user_message(self):
        """测试创建用户消息"""
        content = "现在几点了？"
        message = self.handler.create_user_message(content)
        
        self.assertEqual(message["content"], content)
        self.assertEqual(message["role"], "user")
    
    def test_create_assistant_message(self):
        """测试创建助手消息"""
        content = "我来帮您查询时间"
        message = self.handler.create_assistant_message(content)
        
        self.assertEqual(message["content"], content)
        self.assertEqual(message["role"], "assistant")
        self.assertNotIn("tool_calls", message)
    
    def test_create_assistant_message_with_tool_calls(self):
        """测试创建带工具调用的助手消息"""
        content = "我来帮您查询时间"
        tool_calls = [
            {
                "function": {
                    "name": "get_current_time",
                    "arguments": "{}"
                }
            }
        ]
        message = self.handler.create_assistant_message(content, tool_calls)
        
        self.assertEqual(message["content"], content)
        self.assertEqual(message["role"], "assistant")
        self.assertEqual(message["tool_calls"], tool_calls)
    
    def test_create_tool_message(self):
        """测试创建工具消息"""
        name = "get_current_time"
        content = "当前时间：2024-01-01 12:00:00"
        message = self.handler.create_tool_message(name, content)
        
        self.assertEqual(message["name"], name)
        self.assertEqual(message["role"], "tool")
        self.assertEqual(message["content"], content)
    
    def test_extract_tool_call_info(self):
        """测试提取工具调用信息"""
        tool_call = {
            "function": {
                "name": "get_current_weather",
                "arguments": '{"location": "北京"}'
            }
        }
        
        info = self.handler.extract_tool_call_info(tool_call)
        
        self.assertEqual(info["name"], "get_current_weather")
        self.assertEqual(info["arguments"]["location"], "北京")
    
    def test_extract_tool_call_info_empty_args(self):
        """测试提取空参数的工具调用信息"""
        tool_call = {
            "function": {
                "name": "get_current_time",
                "arguments": "{}"
            }
        }
        
        info = self.handler.extract_tool_call_info(tool_call)
        
        self.assertEqual(info["name"], "get_current_time")
        self.assertEqual(info["arguments"], {})


if __name__ == "__main__":
    unittest.main() 