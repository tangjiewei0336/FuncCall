# 知识库查询工具使用指南

本工具支持HPV、FLU、HIV三个知识库的向量化查询，基于FAISS实现高效的语义搜索。

## 功能特性

- 🎯 **多知识库支持**: HPV、FLU、HIV三个独立知识库
- 📄 **多格式支持**: PDF和Excel文件处理
- 🔍 **语义搜索**: 基于FAISS的向量相似度搜索
- 🛠️ **易于集成**: 作为AI工具集成到现有系统
- ⚡ **高效查询**: 只对摘要字段进行embedding，提高效率

## 目录结构

```
input/
├── hpv/
│   ├── pdf/              # HPV相关PDF文件
│   ├── excel/            # HPV相关Excel文件
│   └── excel_config.json # Excel配置文件
├── flu/
│   ├── pdf/              # FLU相关PDF文件
│   ├── excel/            # FLU相关Excel文件
│   └── excel_config.json # Excel配置文件
└── hiv/
    ├── pdf/              # HIV相关PDF文件
    ├── excel/            # HIV相关Excel文件
    └── excel_config.json # Excel配置文件
```

## 安装依赖

```bash
pip install -r requirements_faiss.txt
```

## 快速开始

### 1. 准备数据

将您的文档按以下方式组织：

- **PDF文件**: 放入 `input/{kb_type}/pdf/` 目录
- **Excel文件**: 放入 `input/{kb_type}/excel/` 目录
- **Excel配置**: 在 `input/{kb_type}/excel_config.json` 中指定列名

### 2. 配置Excel文件

创建 `input/{kb_type}/excel_config.json` 文件：

```json
{
    "content_column": "内容",
    "source_column": "来源",
    "link_column": "链接",
    "sheet_name": "Sheet1"
}
```

- `content_column`: 包含主要内容的列名
- `source_column`: 来源信息的列名（可选）
- `link_column`: 链接信息的列名（可选）
- `sheet_name`: Excel工作表名称

### 3. 构建知识库

```bash
# 构建所有知识库
python build_knowledge_bases.py

# 构建指定知识库
python build_knowledge_bases.py hpv
python build_knowledge_bases.py flu
python build_knowledge_bases.py hiv
```

### 4. 查询知识库

通过AI工具调用：

```python
# 查询FLU知识库
result = query_knowledge_base(
    knowledge_base="flu",
    query="流感症状有哪些？",
    top_k=5
)

# 查询HPV知识库
result = query_knowledge_base(
    knowledge_base="hpv",
    query="HPV疫苗的副作用",
    top_k=3
)
```

## 工具配置

### 查询工具配置

```json
{
    "type": "function",
    "function": {
        "name": "query_knowledge_base",
        "description": "查询HPV、FLU、HIV知识库，支持向量相似度搜索",
        "parameters": {
            "type": "object",
            "properties": {
                "knowledge_base": {
                    "type": "string",
                    "enum": ["hpv", "flu", "hiv"],
                    "description": "要查询的知识库类型"
                },
                "query": {
                    "type": "string",
                    "description": "查询文本，将基于语义相似度搜索相关文档"
                },
                "top_k": {
                    "type": "integer",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 20,
                    "description": "返回结果数量，默认为5"
                }
            },
            "required": ["knowledge_base", "query"]
        }
    }
}
```

## 使用示例

### 示例1: 查询流感症状

```python
# 用户查询
query = "流感的主要症状是什么？"

# AI工具调用
result = query_knowledge_base(
    knowledge_base="flu",
    query=query,
    top_k=5
)

# 返回结果示例
"""
在 FLU 知识库中搜索 '流感的主要症状是什么？' 的结果：
============================================================

排名 1:
标题: 流感症状指南 - 第1段
摘要: 流感的主要症状包括发热、咳嗽、喉咙痛、肌肉疼痛、头痛、疲劳等...
来源: input/flu/pdf/flu_symptoms.pdf
文件类型: pdf
相似度: 0.9234
----------------------------------------

排名 2:
标题: 流感诊断标准 - 第3段
摘要: 根据WHO标准，流感症状可分为典型症状和非典型症状...
来源: input/flu/pdf/diagnosis_guide.pdf
文件类型: pdf
相似度: 0.8765
----------------------------------------
"""
```

### 示例2: 查询HPV疫苗信息

```python
# 用户查询
query = "HPV疫苗的接种年龄"

# AI工具调用
result = query_knowledge_base(
    knowledge_base="hpv",
    query=query,
    top_k=3
)
```

### 示例3: 查询HIV检测

```python
# 用户查询
query = "HIV检测的方法和窗口期"

# AI工具调用
result = query_knowledge_base(
    knowledge_base="hiv",
    query=query,
    top_k=5
)
```

## 技术实现

### 核心特性

1. **摘要优先**: 只对文档摘要进行embedding，提高效率
2. **向量搜索**: 使用FAISS进行高效的向量相似度搜索
3. **多格式处理**: 
   - PDF: 使用pymupdf4llm转换为markdown
   - Excel: 支持自定义列配置
4. **缓存机制**: 自动保存和加载FAISS索引

### 处理流程

1. **文档处理**:
   - PDF → pymupdf4llm → markdown → 文本分割
   - Excel → pandas → 按配置提取内容
   
2. **向量化**:
   - 提取摘要 → sentence-transformers → 向量
   - 使用all-MiniLM-L6-v2模型

3. **索引构建**:
   - FAISS IndexFlatL2 → 保存索引文件

4. **查询处理**:
   - 查询文本 → 向量化 → FAISS搜索 → 结果排序

## 测试

运行测试脚本验证功能：

```bash
python test_knowledge_base.py
```

## 注意事项

1. **文件格式**: 确保PDF和Excel文件格式正确
2. **列名配置**: Excel配置文件中的列名必须与实际文件匹配
3. **内存使用**: 大文件可能需要较多内存
4. **首次构建**: 首次构建知识库需要下载embedding模型

## 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements_faiss.txt
   ```

2. **Excel列名不匹配**
   - 检查excel_config.json中的列名
   - 确保与实际Excel文件中的列名一致

3. **PDF处理失败**
   - 确保PDF文件未损坏
   - 检查pymupdf4llm是否正确安装

4. **内存不足**
   - 减少batch_size参数
   - 分批处理大文件

## 扩展功能

### 自定义embedding模型

```python
# 在knowledge_base_tool.py中修改
self.embedding_model = SentenceTransformer("your-model-name")
```

### 添加新的知识库类型

```python
# 在KnowledgeBaseType枚举中添加
class KnowledgeBaseType(Enum):
    HPV = "hpv"
    FLU = "flu"
    HIV = "hiv"
    NEW_KB = "new_kb"  # 新增
```

### 自定义搜索策略

可以修改`_get_text_for_embedding`方法来实现不同的embedding策略。 