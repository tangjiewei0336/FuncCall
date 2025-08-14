"""
新工具测试模块
"""

import unittest
from tools.calculator_tool import calculate, get_calculator_tool_config


class TestCalculatorTool(unittest.TestCase):
    """计算器工具测试类"""
    
    def test_basic_calculation(self):
        """测试基本计算"""
        result = calculate("2+3*4")
        self.assertIn("14", result)
    
    def test_complex_calculation(self):
        """测试复杂计算"""
        result = calculate("(2+3)*4")
        self.assertIn("20", result)
    
    def test_math_functions(self):
        """测试数学函数"""
        result = calculate("sqrt(16)")
        self.assertIn("4", result)
        
        result = calculate("pow(2,3)")
        self.assertIn("8", result)
    
    def test_division_by_zero(self):
        """测试除零错误"""
        result = calculate("1/0")
        self.assertIn("除数不能为零", result)
    
    def test_invalid_expression(self):
        """测试无效表达式"""
        result = calculate("import os")
        self.assertIn("不允许的字符", result)
    
    def test_calculator_tool_config(self):
        """测试计算器工具配置"""
        config = get_calculator_tool_config()
        self.assertEqual(config["type"], "function")
        self.assertEqual(config["function"]["name"], "calculate")
        self.assertIn("expression", config["function"]["parameters"]["properties"])

if __name__ == "__main__":
    unittest.main() 