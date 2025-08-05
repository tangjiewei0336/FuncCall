"""
数据查询工具模块
模拟数据库查询功能
"""

from typing import Dict, List, Any
import random


# 模拟数据
MOCK_DATA = {
    "users": [
        {"id": 1, "name": "张三", "age": 25, "salary": 8000, "department": "技术部"},
        {"id": 2, "name": "李四", "age": 30, "salary": 12000, "department": "销售部"},
        {"id": 3, "name": "王五", "age": 28, "salary": 10000, "department": "技术部"},
        {"id": 4, "name": "赵六", "age": 35, "salary": 15000, "department": "管理部"},
        {"id": 5, "name": "钱七", "age": 26, "salary": 9000, "department": "技术部"},
    ],
    "products": [
        {"id": 1, "name": "笔记本电脑", "price": 5999, "category": "电子产品", "stock": 50},
        {"id": 2, "name": "手机", "price": 3999, "category": "电子产品", "stock": 100},
        {"id": 3, "name": "办公椅", "price": 299, "category": "办公用品", "stock": 200},
        {"id": 4, "name": "打印机", "price": 899, "category": "办公用品", "stock": 30},
        {"id": 5, "name": "显示器", "price": 1299, "category": "电子产品", "stock": 80},
    ],
    "orders": [
        {"id": 1, "user_id": 1, "product_id": 1, "quantity": 1, "total": 5999},
        {"id": 2, "user_id": 2, "product_id": 2, "quantity": 2, "total": 7998},
        {"id": 3, "user_id": 3, "product_id": 3, "quantity": 5, "total": 1495},
        {"id": 4, "user_id": 1, "product_id": 4, "quantity": 1, "total": 899},
        {"id": 5, "user_id": 4, "product_id": 5, "quantity": 2, "total": 2598},
    ]
}


def query_data(table: str, condition: str = None, limit: int = 10) -> str:
    """
    查询数据
    
    Args:
        table: 表名 (users, products, orders)
        condition: 查询条件，如 "age > 25" 或 "department = 技术部"
        limit: 返回结果数量限制
        
    Returns:
        查询结果字符串
    """
    try:
        if table not in MOCK_DATA:
            return f"错误：表 '{table}' 不存在。可用表：{list(MOCK_DATA.keys())}"
        
        data = MOCK_DATA[table].copy()
        
        # 应用查询条件
        if condition:
            filtered_data = []
            for item in data:
                if _evaluate_condition(item, condition):
                    filtered_data.append(item)
            data = filtered_data
        
        # 应用数量限制
        if limit and limit > 0:
            data = data[:limit]
        
        if not data:
            return f"查询结果：表 '{table}' 中没有找到匹配的数据"
        
        # 格式化输出
        result = f"查询结果：表 '{table}' 找到 {len(data)} 条记录\n"
        result += "=" * 50 + "\n"
        
        for i, item in enumerate(data, 1):
            result += f"记录 {i}:\n"
            for key, value in item.items():
                result += f"  {key}: {value}\n"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"查询错误：{str(e)}"


def _evaluate_condition(item: Dict[str, Any], condition: str) -> bool:
    """
    评估查询条件
    
    Args:
        item: 数据项
        condition: 条件字符串
        
    Returns:
        是否满足条件
    """
    try:
        # 简单的条件解析
        condition = condition.strip()
        
        # 处理相等条件
        if "=" in condition:
            field, value = condition.split("=", 1)
            field = field.strip()
            value = value.strip().strip('"\'')
            return str(item.get(field, "")) == value
        
        # 处理大于条件
        elif ">" in condition:
            field, value = condition.split(">", 1)
            field = field.strip()
            value = value.strip()
            try:
                return item.get(field, 0) > float(value)
            except (ValueError, TypeError):
                return False
        
        # 处理小于条件
        elif "<" in condition:
            field, value = condition.split("<", 1)
            field = field.strip()
            value = value.strip()
            try:
                return item.get(field, 0) < float(value)
            except (ValueError, TypeError):
                return False
        
        # 处理包含条件
        elif "contains" in condition:
            # 格式：field contains value
            parts = condition.split("contains", 1)
            field = parts[0].strip()
            value = parts[1].strip().strip('"\'')
            return value in str(item.get(field, ""))
        
        return False
        
    except Exception:
        return False


def get_data_query_tool_config():
    """
    获取数据查询工具的配置信息
    
    Returns:
        工具配置字典
    """
    return {
        "type": "function",
        "function": {
            "name": "query_data",
            "description": "查询模拟数据库中的数据，支持条件筛选",
            "parameters": {
                "type": "object",
                "properties": {
                    "table": {
                        "type": "string",
                        "description": "表名：users（用户表）、products（产品表）、orders（订单表）"
                    },
                    "condition": {
                        "type": "string",
                        "description": "查询条件，如 'age > 25'、'department = 技术部'、'name contains 张'"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回结果数量限制，默认10"
                    }
                },
                "required": ["table"]
            }
        }
    } 