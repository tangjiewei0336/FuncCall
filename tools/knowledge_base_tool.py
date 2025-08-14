"""
知识库查询工具模块
支持HPV、FLU、HIV三个知识库的FAISS向量搜索
"""

import os
import pathlib
from typing import Dict, List, Any, Optional
import json
import pickle
from dataclasses import dataclass
from enum import Enum

# FAISS相关导入
try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("警告：FAISS或sentence-transformers未安装，知识库功能将不可用")

# 内容处理相关导入
try:
    import pandas as pd
    import pymupdf4llm
    from langchain.docstore.document import Document as LangchainDocument
    from langchain_text_splitters import CharacterTextSplitter
    CONTENT_PROCESSING_AVAILABLE = True
except ImportError:
    CONTENT_PROCESSING_AVAILABLE = False
    print("警告：pandas或pymupdf4llm未安装，内容处理功能将不可用")

from models.simple_llm_client import SimpleLLMClient


class KnowledgeBaseType(Enum):
    """知识库类型枚举"""
    HPV = "hpv"
    FLU = "flu"
    HIV = "hiv"


@dataclass
class KnowledgeDocument:
    """知识库文档数据类"""
    id: str
    title: str
    content: str
    summary: str
    source: str
    file_type: str  # "pdf" 或 "excel"
    metadata: Optional[Dict[str, Any]] = None


class KnowledgeBaseManager:
    """知识库管理器"""
    
    def __init__(self, base_dir: str = "input"):
        self.base_dir = pathlib.Path(base_dir)
        self.embedding_model = None
        self.indices = {}
        self.documents = {}
        self.llm_client = None
        
        if FAISS_AVAILABLE:
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        try:
            self.llm_client = SimpleLLMClient()
        except Exception as e:
            print(f"警告：大模型摘要生成不可用，将使用截断摘要。原因：{e}")
        
        # 初始化三个知识库
        for kb_type in KnowledgeBaseType:
            self._init_knowledge_base(kb_type)
    
    def _init_knowledge_base(self, kb_type: KnowledgeBaseType):
        """初始化知识库"""
        kb_dir = self.base_dir / kb_type.value
        index_file = kb_dir / f"{kb_type.value}_index.faiss"
        docs_file = kb_dir / f"{kb_type.value}_documents.pkl"
        
        # 创建目录
        kb_dir.mkdir(parents=True, exist_ok=True)
        
        # 尝试加载现有索引
        if FAISS_AVAILABLE and index_file.exists() and docs_file.exists():
            try:
                self.indices[kb_type] = faiss.read_index(str(index_file))
                with open(docs_file, 'rb') as f:
                    self.documents[kb_type] = pickle.load(f)
                print(f"已加载 {kb_type.value} 知识库索引")
            except Exception as e:
                print(f"加载 {kb_type.value} 知识库失败: {e}")
                self.indices[kb_type] = None
                self.documents[kb_type] = []
        else:
            self.indices[kb_type] = None
            self.documents[kb_type] = []
    
    def build_knowledge_base(self, kb_type: KnowledgeBaseType, 
                           excel_config: Optional[Dict] = None):
        """
        构建知识库
        
        Args:
            kb_type: 知识库类型
            excel_config: Excel配置，格式为 {
                "content_column": "内容列名",
                "source_column": "来源列名",
                "link_column": "链接列名",
                "sheet_name": "工作表名"
            }
        """
        if not FAISS_AVAILABLE or not CONTENT_PROCESSING_AVAILABLE:
            return "错误：缺少必要的依赖包，无法构建知识库"
        
        kb_dir = self.base_dir / kb_type.value
        documents = []
        
        # 处理PDF文件
        pdf_dir = kb_dir / "pdf"
        if pdf_dir.exists():
            for pdf_file in pdf_dir.glob("*.pdf"):
                try:
                    pdf_docs = self._process_pdf_file(pdf_file, kb_type)
                    documents.extend(pdf_docs)
                    print(f"处理PDF文件: {pdf_file.name}")
                except Exception as e:
                    print(f"处理PDF文件 {pdf_file.name} 失败: {e}")
        
        # 处理Excel文件
        excel_dir = kb_dir / "excel"
        if excel_dir.exists() and excel_config:
            for excel_file in excel_dir.glob("*.xlsx"):
                try:
                    excel_docs = self._process_excel_file(excel_file, kb_type, excel_config)
                    documents.extend(excel_docs)
                    print(f"处理Excel文件: {excel_file.name}")
                except Exception as e:
                    print(f"处理Excel文件 {excel_file.name} 失败: {e}")
        
        if not documents:
            return f"错误：在 {kb_type.value} 知识库中没有找到可处理的文档"
        
        # 创建FAISS索引
        try:
            # 提取摘要进行embedding
            summaries = [doc.summary for doc in documents]
            embeddings = self.embedding_model.encode(summaries, show_progress_bar=True)
            
            # 创建索引
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings.astype('float32'))
            
            # 保存索引和文档
            self.indices[kb_type] = index
            self.documents[kb_type] = documents
            
            # 保存到文件
            index_file = kb_dir / f"{kb_type.value}_index.faiss"
            docs_file = kb_dir / f"{kb_type.value}_documents.pkl"
            
            faiss.write_index(index, str(index_file))
            with open(docs_file, 'wb') as f:
                pickle.dump(documents, f)
            
            return f"成功构建 {kb_type.value} 知识库，包含 {len(documents)} 个文档"
            
        except Exception as e:
            return f"构建知识库失败: {e}"
    
    def _generate_summary(self, content: str) -> list:
        """用大模型生成1-3个相关问题，失败时降级为1个问题"""
        if self.llm_client:
            try:
                prompt = (
                    "请根据下面这段内容，生成1到3个用户可能会问的简明问题（每个10~30字，中文，直接输出问题本身，不要加前缀，问题之间用换行分隔）：\n\n"
                    f"{content}\n\n问题："
                )
                questions = self.llm_client.call(prompt)
                # 处理大模型输出，按换行或分号分割，去除空行
                qlist = [q.strip().replace('问题：','').replace('问题:','') for q in questions.replace(';','\n').split('\n') if q.strip()]
                qlist = [q for q in qlist if 5 < len(q) < 40]
                if qlist:
                    return qlist[:3]
            except Exception as e:
                print(f"大模型生成问题失败，降级为内容片段：{e}")
        # 降级方案
        base = content[:30].replace('\n', '')
        return [base + "……相关问题？"] if base else ["这段内容的相关问题？"]

    def _process_pdf_file(self, pdf_file: pathlib.Path, kb_type: KnowledgeBaseType) -> List[KnowledgeDocument]:
        """处理PDF文件"""
        documents = []
        
        # 使用pymupdf4llm处理PDF
        md_text = pymupdf4llm.to_markdown(str(pdf_file))
        
        # 文本分割
        splitter = CharacterTextSplitter(chunk_size=1000, separator="\n", chunk_overlap=20)
        chunks = splitter.split_text(md_text)
        
        for i, chunk in enumerate(chunks):
            # 生成摘要（这里简单使用前100个字符作为摘要）
            summary = self._generate_summary(chunk)
            
            doc = KnowledgeDocument(
                id=f"{kb_type.value}_pdf_{pdf_file.stem}_{i}",
                title=f"{pdf_file.stem} - 第{i+1}段",
                content=chunk,
                summary=summary,
                source=str(pdf_file),
                file_type="pdf",
                metadata={"file_name": pdf_file.name, "chunk_index": i}
            )
            documents.append(doc)
        
        return documents
    
    def _process_excel_file(self, excel_file: pathlib.Path, kb_type: KnowledgeBaseType, 
                           config: Dict) -> List[KnowledgeDocument]:
        """处理Excel文件"""
        documents = []
        
        try:
            df = pd.read_excel(excel_file, sheet_name=config.get("sheet_name", "Sheet1"))
            content_column = config["content_column"]
            source_column = config.get("source_column", "")
            link_column = config.get("link_column", "")
            
            for idx, row in df.iterrows():
                content = str(row[content_column])
                if len(content) < 5:  # 跳过内容太少的行
                    continue
                
                # 构建完整内容
                full_content = content
                if source_column and source_column in row:
                    full_content += f"\n来源: {row[source_column]}"
                if link_column and link_column in row:
                    full_content += f"\n链接: {row[link_column]}"
                
                # 生成摘要
                summary = self._generate_summary(content)
                
                doc = KnowledgeDocument(
                    id=f"{kb_type.value}_excel_{excel_file.stem}_{idx}",
                    title=f"{excel_file.stem} - 第{idx+1}行",
                    content=full_content,
                    summary=summary,
                    source=str(excel_file),
                    file_type="excel",
                    metadata={
                        "file_name": excel_file.name,
                        "row_index": idx,
                        "source": row.get(source_column, "") if source_column else "",
                        "link": row.get(link_column, "") if link_column else ""
                    }
                )
                documents.append(doc)
                
        except Exception as e:
            print(f"处理Excel文件 {excel_file.name} 时出错: {e}")
        
        return documents
    
    def search_knowledge_base(self, kb_type: KnowledgeBaseType, query: str, 
                            k: int = 5) -> List[Dict[str, Any]]:
        """
        搜索知识库
        
        Args:
            kb_type: 知识库类型
            query: 查询文本
            k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        if not FAISS_AVAILABLE:
            return [{"error": "FAISS未安装，无法进行向量搜索"}]
        
        if kb_type not in self.indices or self.indices[kb_type] is None:
            return [{"error": f"{kb_type.value} 知识库未初始化"}]
        
        try:
            # 对查询进行embedding
            query_embedding = self.embedding_model.encode([query])
            
            # 搜索相似向量
            distances, indices = self.indices[kb_type].search(
                query_embedding.astype('float32'), k
            )
            
            # 处理结果
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.documents[kb_type]):
                    doc = self.documents[kb_type][idx]
                    result = {
                        'rank': i + 1,
                        'title': doc.title,
                        'content': doc.content,
                        'summary': doc.summary,
                        'source': doc.source,
                        'file_type': doc.file_type,
                        'similarity_score': 1.0 / (1.0 + distance),
                        'distance': float(distance),
                        'metadata': doc.metadata
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            return [{"error": f"搜索失败: {e}"}]


# 全局知识库管理器实例
_kb_manager = None


def get_kb_manager() -> KnowledgeBaseManager:
    """获取知识库管理器实例"""
    global _kb_manager
    if _kb_manager is None:
        _kb_manager = KnowledgeBaseManager()
    return _kb_manager


def query_knowledge_base(knowledge_base: str, query: str, top_k: int = 5) -> str:
    """
    查询知识库
    
    Args:
        knowledge_base: 知识库名称 (hpv, flu, hiv)
        query: 查询文本
        top_k: 返回结果数量
        
    Returns:
        查询结果字符串
    """
    try:
        # 验证知识库类型
        kb_type_map = {
            "hpv": KnowledgeBaseType.HPV,
            "flu": KnowledgeBaseType.FLU,
            "hiv": KnowledgeBaseType.HIV
        }
        
        if knowledge_base.lower() not in kb_type_map:
            return f"错误：不支持的知识库类型 '{knowledge_base}'。支持的类型：{list(kb_type_map.keys())}"
        
        kb_type = kb_type_map[knowledge_base.lower()]
        manager = get_kb_manager()
        
        # 执行搜索
        results = manager.search_knowledge_base(kb_type, query, top_k)
        
        if not results:
            return f"在 {knowledge_base} 知识库中没有找到相关结果"
        
        if "error" in results[0]:
            return f"搜索错误：{results[0]['error']}"
        
        # 格式化结果
        result_text = f"在 {knowledge_base.upper()} 知识库中搜索 '{query}' 的结果：\n"
        result_text += "=" * 60 + "\n\n"
        
        for result in results:
            result_text += f"排名 {result['rank']}:\n"
            result_text += f"标题: {result['title']}\n"
            # 展示所有相关问题
            if isinstance(result['summary'], list):
                for idx, q in enumerate(result['summary'], 1):
                    result_text += f"可能的问题{idx}: {q}\n"
            else:
                result_text += f"可能的问题: {result['summary']}\n"
            result_text += f"原文内容: {result['content']}\n"
            result_text += f"来源: {result['source']}\n"
            result_text += f"文件类型: {result['file_type']}\n"
            result_text += f"相似度: {result['similarity_score']:.4f}\n"
            result_text += "-" * 40 + "\n\n"
        
        return result_text
        
    except Exception as e:
        return f"查询知识库时发生错误: {str(e)}"


def build_knowledge_base(knowledge_base: str, excel_config: str = None) -> str:
    """
    构建知识库
    
    Args:
        knowledge_base: 知识库名称 (hpv, flu, hiv)
        excel_config: Excel配置的JSON字符串
        
    Returns:
        构建结果字符串
    """
    try:
        # 验证知识库类型
        kb_type_map = {
            "hpv": KnowledgeBaseType.HPV,
            "flu": KnowledgeBaseType.FLU,
            "hiv": KnowledgeBaseType.HIV
        }
        
        if knowledge_base.lower() not in kb_type_map:
            return f"错误：不支持的知识库类型 '{knowledge_base}'。支持的类型：{list(kb_type_map.keys())}"
        
        kb_type = kb_type_map[knowledge_base.lower()]
        manager = get_kb_manager()
        
        # 解析Excel配置
        excel_config_dict = None
        if excel_config:
            try:
                excel_config_dict = json.loads(excel_config)
            except json.JSONDecodeError:
                return "错误：Excel配置格式不正确，应为JSON格式"
        
        # 构建知识库
        result = manager.build_knowledge_base(kb_type, excel_config_dict)
        return result
        
    except Exception as e:
        return f"构建知识库时发生错误: {str(e)}"


def get_knowledge_base_tool_config():
    """
    获取知识库查询工具的配置信息
    
    Returns:
        工具配置字典
    """
    return {
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
                        "description": "查询文本，请用问题的方式进行查询，例如：“什么是流感？”。"
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


def get_build_knowledge_base_tool_config():
    """
    获取构建知识库工具的配置信息（仅用于管理，不提供给大模型）
    
    Returns:
        工具配置字典
    """
    return {
        "type": "function",
        "function": {
            "name": "build_knowledge_base",
            "description": "构建HPV、FLU、HIV知识库，处理PDF和Excel文件（管理工具）",
            "parameters": {
                "type": "object",
                "properties": {
                    "knowledge_base": {
                        "type": "string",
                        "enum": ["hpv", "flu", "hiv"],
                        "description": "要构建的知识库类型"
                    },
                    "excel_config": {
                        "type": "string",
                        "description": "Excel文件配置的JSON字符串，格式：{\"content_column\": \"内容列名\", \"source_column\": \"来源列名\", \"link_column\": \"链接列名\", \"sheet_name\": \"工作表名\"}"
                    }
                },
                "required": ["knowledge_base"]
            }
        }
    } 