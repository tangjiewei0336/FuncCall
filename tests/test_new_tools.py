"""
新工具测试模块
"""

import unittest
from tools.calculator_tool import calculate, get_calculator_tool_config
from tools.data_query_tool import query_data, get_data_query_tool_config


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


class TestDataQueryTool(unittest.TestCase):
    """数据查询工具测试类"""
    
    def test_query_all_users(self):
        """测试查询所有用户"""
        result = query_data("users")
        self.assertIn("查询结果", result)
        self.assertIn("张三", result)
    
    def test_query_with_condition(self):
        """测试条件查询"""
        result = query_data("users", "age > 25")
        self.assertIn("查询结果", result)
        self.assertIn("李四", result)
    
    def test_query_with_limit(self):
        """测试限制查询结果数量"""
        result = query_data("users", limit=2)
        self.assertIn("查询结果", result)
        # 应该只返回2条记录
    
    def test_query_products(self):
        """测试查询产品"""
        result = query_data("products")
        self.assertIn("查询结果", result)
        self.assertIn("笔记本电脑", result)
    
    def test_query_orders(self):
        """测试查询订单"""
        result = query_data("orders")
        self.assertIn("查询结果", result)
    
    def test_invalid_table(self):
        """测试无效表名"""
        result = query_data("invalid_table")
        self.assertIn("不存在", result)
    
    def test_string_condition(self):
        """测试字符串条件"""
        result = query_data("users", "department = 技术部")
        self.assertIn("查询结果", result)
        self.assertIn("张三", result)
    
    def test_contains_condition(self):
        """测试包含条件"""
        result = query_data("users", "name contains 张")
        self.assertIn("查询结果", result)
        self.assertIn("张三", result)
    
    def test_data_query_tool_config(self):
        """测试数据查询工具配置"""
        config = get_data_query_tool_config()
        self.assertEqual(config["type"], "function")
        self.assertEqual(config["function"]["name"], "query_data")
        self.assertIn("table", config["function"]["parameters"]["properties"])


if __name__ == "__main__":
    unittest.main() 