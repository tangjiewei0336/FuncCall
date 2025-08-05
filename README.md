# FuncCall - 函数调用项目

这是一个基于阿里云通义千问的智能对话系统，使用自定义提示词拼接和输出解析的方式实现工具调用功能。

## 项目结构

```
FuncCall/
├── tools/                    # 工具模块
│   ├── __init__.py
│   ├── weather_tool.py      # 天气查询工具
│   ├── time_tool.py         # 时间查询工具
│   ├── calculator_tool.py   # 计算器工具
│   ├── data_query_tool.py   # 数据查询工具
│   └── tool_registry.py     # 工具注册表
├── models/                   # 模型模块
│   ├── __init__.py
│   └── simple_llm_client.py # 简单LLM客户端
├── utils/                    # 工具函数模块
│   ├── __init__.py
│   ├── message_handler.py   # 消息处理工具
│   ├── prompt_builder.py    # 提示词构建器
│   └── tool_parser.py       # 工具调用解析器
├── tests/                    # 测试模块
│   ├── __init__.py
│   ├── test_new_tools.py    # 新工具测试
│   └── test_tool_calls.py   # 工具调用测试
├── conversation_manager.py   # 对话管理器
├── main.py                   # 主程序入口
├── demo_tool_calls.py        # 演示脚本
└── README.md                # 项目说明
```

## 功能特性

- **自定义工具调用**: 不使用原生tool功能，通过提示词拼接和输出解析实现
- **模块化设计**: 将不同功能分离到独立模块中，便于维护和扩展
- **工具注册系统**: 支持动态注册和管理工具
- **多轮工具调用**: 支持工具之间的依赖关系，可进行多轮调用直到完成任务
- **对话历史管理**: 支持保持对话上下文，实现连续对话
- **完整的测试覆盖**: 包含单元测试，确保代码质量
- **错误处理**: 完善的异常处理机制
- **类型提示**: 使用类型提示提高代码可读性

## 安装依赖

```bash
pip install dashscope
```

## 环境配置

设置阿里云API密钥：

```bash
export DASHSCOPE_API_KEY="your-api-key-here"
```

## 使用方法

### 运行主程序

```bash
python3 main.py
```

### 运行演示

```bash
# 运行工具调用演示
python3 demo_tool_calls.py
```

### 运行测试

```bash
# 运行所有测试
python3 -m unittest discover tests

# 运行特定测试
python3 -m unittest tests.test_new_tools
python3 -m unittest tests.test_tool_calls
```

## 添加新工具

1. 在 `tools/` 目录下创建新的工具文件
2. 实现工具函数和配置函数
3. 在 `tools/tool_registry.py` 中注册新工具

示例：

```python
# tools/calculator_tool.py
def calculate(expression: str) -> str:
    """计算表达式"""
    try:
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{e}"

def get_calculator_tool_config():
    return {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 2+3*4"
                    }
                },
                "required": ["expression"]
            }
        }
    }
```

然后在 `tool_registry.py` 中注册：

```python
from .calculator_tool import get_calculator_tool_config

# 在 _register_default_tools 方法中添加
self.register_tool(
    name="calculate",
    function=self._get_calculator_function,
    config=get_calculator_tool_config()
)
```

## 自定义工具调用示例

### 工具调用格式
模型输出示例：
```
我来帮您查询时间。

<tool_call>
工具名称：get_current_time
参数：{}
</tool_call>
```

### 简单示例
用户：请帮我计算技术部员工的平均工资

系统处理流程：
1. 构建包含工具信息的提示词
2. 模型输出工具调用格式
3. 解析并执行 `query_data` 工具查询技术部员工信息
4. 解析并执行 `calculate` 工具计算平均工资
5. 模型总结结果并返回最终答案

### 复杂示例
用户：请分析一下我们的销售情况，包括总销售额、平均订单金额，并计算利润率

系统处理流程：
1. 构建包含工具信息的提示词
2. 模型输出多个工具调用
3. 依次执行：`query_data` → `calculate` → `calculate` → `calculate`
4. 模型综合分析并返回完整报告

## 项目优势

1. **可维护性**: 模块化设计使得代码易于理解和维护
2. **可扩展性**: 工具注册系统支持轻松添加新功能
3. **可测试性**: 每个模块都有独立的测试，确保代码质量
4. **可重用性**: 组件化设计使得代码可以在不同场景中重用
5. **智能性**: 支持工具间的依赖关系，能够处理复杂的多步骤任务
6. **灵活性**: 完全自定义的工具调用方式，不依赖特定的API格式

## 注意事项

- 确保已正确设置 `DASHSCOPE_API_KEY` 环境变量
- 工具函数应该是纯函数，避免副作用
- 添加新工具时需要同时更新测试用例 