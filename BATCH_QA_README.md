# 批量问答处理工具使用指南

本工具可以从Excel文件读取问题列表，自动调用大模型生成回复，并保存结果到新的Excel文件。

## 功能特性

- 📊 **Excel批量处理**: 从Excel文件读取问题列表
- 🤖 **智能问答**: 自动调用大模型生成回复
- 📚 **RAG检索**: 自动使用知识库查询工具获取权威信息
- 💾 **结果保存**: 自动保存处理结果到Excel文件
- 📈 **进度跟踪**: 实时显示处理进度和统计信息
- 🔄 **断点续传**: 定期保存中间结果，支持断点续传

## 安装依赖

```bash
pip install pandas openpyxl
```

## 使用方法

### 1. 创建示例Excel文件

```bash
python batch_qa_processor.py --create-sample
```

这将创建一个`sample_questions.xlsx`文件，包含示例问题。

### 2. 准备输入Excel文件

Excel文件格式要求：
- 必须包含一个名为"问题"的列（可通过参数自定义）
- 每行一个问题
- 支持其他列作为备注信息

示例格式：
| 问题 | 备注 |
|------|------|
| HPV疫苗的副作用有哪些？ | 示例问题1 |
| 二价疫苗和四价疫苗有什么区别？ | 示例问题2 |

### 3. 运行批量处理

#### 基本用法
```bash
python batch_qa_processor.py input_questions.xlsx
```

#### 高级用法
```bash
python batch_qa_processor.py input_questions.xlsx \
    -o output_results.xlsx \
    -c "问题" \
    -b 5 \
    -d 2.0
```

#### 参数说明
- `input_file`: 输入Excel文件路径（必需）
- `-o, --output`: 输出Excel文件路径（可选，默认自动生成）
- `-c, --column`: 问题列名（默认：问题）
- `-b, --batch`: 批处理大小（默认：10）
- `-d, --delay`: 请求间隔时间（秒，默认：1.0）
- `--create-sample`: 创建示例Excel文件

### 4. 查看结果

处理完成后，会生成包含以下列的Excel文件：
- **序号**: 问题序号
- **问题**: 原始问题
- **回答**: 大模型生成的回答
- **参考文献**: 提取的参考文献信息
- **处理时间**: 处理时间戳
- **状态**: 处理状态（成功/失败）

## 使用示例

### 示例1: 基本批量处理

```bash
# 创建示例文件
python batch_qa_processor.py --create-sample

# 处理示例文件
python batch_qa_processor.py sample_questions.xlsx
```

### 示例2: 自定义参数

```bash
python batch_qa_processor.py my_questions.xlsx \
    -o my_results.xlsx \
    -c "问题内容" \
    -b 20 \
    -d 1.5
```

### 示例3: 程序化调用

```python
from batch_qa_processor import BatchQAProcessor

# 创建处理器
processor = BatchQAProcessor()

# 处理Excel文件
result = processor.process_excel_file(
    input_file="questions.xlsx",
    output_file="results.xlsx",
    question_column="问题",
    batch_size=10,
    delay_between_requests=1.0
)

print(result)
```

## 输出结果示例

### 成功处理的回答示例
```
HPV疫苗的副作用主要包括注射部位疼痛、红肿、发热等轻微反应，这些反应通常在1-2天内自行缓解。严重的过敏反应较为罕见。

信息来源：
[1] 中国疾病预防控制中心. HPV疫苗安全性监测报告
[2] 世界卫生组织. HPV疫苗立场文件
```

### Excel输出格式
| 序号 | 问题 | 回答 | 参考文献 | 处理时间 | 状态 |
|------|------|------|----------|----------|------|
| 1 | HPV疫苗的副作用有哪些？ | HPV疫苗的副作用主要包括... | 信息来源：[1] 中国疾病预防控制中心... | 2024-01-15 10:30:25 | 成功 |

## 注意事项

### 1. API限制
- 请确保设置了正确的API密钥（DASHSCOPE_API_KEY环境变量）
- 注意API调用频率限制，建议设置适当的请求间隔

### 2. 文件格式
- 输入文件必须是Excel格式（.xlsx）
- 确保问题列名正确
- 支持中文列名

### 3. 处理时间
- 每个问题的处理时间取决于大模型响应速度
- 建议设置适当的请求间隔避免API限制
- 大量问题处理可能需要较长时间

### 4. 错误处理
- 单个问题处理失败不会影响其他问题
- 失败的问题会在结果中标记为"失败"状态
- 错误信息会记录在回答列中

## 故障排除

### 常见问题

1. **文件不存在错误**
   ```
   错误：输入文件不存在: questions.xlsx
   ```
   解决：检查文件路径是否正确

2. **列名错误**
   ```
   错误：未找到列 '问题'。可用列：['问题内容', '备注']
   ```
   解决：使用 `-c "问题内容"` 指定正确的列名

3. **API密钥错误**
   ```
   调用模型失败：API密钥未设置
   ```
   解决：设置DASHSCOPE_API_KEY环境变量

4. **处理失败**
   ```
   ✗ 处理失败: 网络连接错误
   ```
   解决：检查网络连接，增加请求间隔时间

### 性能优化建议

1. **批处理大小**: 根据API限制调整批处理大小
2. **请求间隔**: 避免API频率限制，建议1-2秒间隔
3. **文件大小**: 大量问题建议分批处理
4. **内存使用**: 处理大量问题时注意内存使用

## 高级功能

### 自定义处理器

```python
class CustomBatchQAProcessor(BatchQAProcessor):
    def _extract_references(self, answer: str) -> str:
        # 自定义参考文献提取逻辑
        return super()._extract_references(answer)
    
    def process_excel_file(self, input_file: str, **kwargs):
        # 自定义处理逻辑
        return super().process_excel_file(input_file, **kwargs)
```

### 结果分析

```python
# 获取处理结果
results = processor.get_results()

# 分析成功率
successful = len([r for r in results if r["状态"] == "成功"])
total = len(results)
success_rate = successful / total * 100

print(f"成功率: {success_rate:.1f}%")
```

## 更新日志

- v1.0.0: 初始版本，支持基本批量处理功能
- v1.1.0: 添加参考文献提取功能
- v1.2.0: 支持自定义列名和参数
- v1.3.0: 添加断点续传和进度跟踪 