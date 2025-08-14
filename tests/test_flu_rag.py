import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestFluRAGRetrieval(unittest.TestCase):
    def setUp(self):
        # 导入知识库查询工具
        from tools.knowledge_base_tool import query_knowledge_base
        self.query_knowledge_base = query_knowledge_base

    def test_flu_symptom_retrieval(self):
        """
        测试流感知识库RAG检索：查询流感症状相关内容
        """
        query = "流感的主要症状有哪些？"
        result = self.query_knowledge_base(
            knowledge_base="flu",
            query=query,
            top_k=3
        )
        print("检索结果：\n", result)
        self.assertIn("FLU", result)
        self.assertIn("症状", result)
        self.assertTrue("排名" in result or "摘要" in result)

    def test_flu_vaccine_retrieval(self):
        """
        测试流感知识库RAG检索：查询流感疫苗相关内容
        """
        query = "流感疫苗的接种时间"
        result = self.query_knowledge_base(
            knowledge_base="flu",
            query=query,
            top_k=3
        )
        print("检索结果：\n", result)
        self.assertIn("FLU", result)
        self.assertTrue("疫苗" in result or "接种" in result)

if __name__ == "__main__":
    unittest.main()