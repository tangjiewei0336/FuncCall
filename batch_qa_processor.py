"""
批量问答处理脚本
从Excel文件读取问题列表，自动生成回复并保存结果
"""

import pandas as pd
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import time
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversation_manager import CustomConversationManager


class BatchQAProcessor:
    """批量问答处理器"""
    
    def __init__(self, api_key: str = None, model: str = "qwen-plus"):
        """
        初始化批量问答处理器
        
        Args:
            api_key: API密钥
            model: 模型名称
        """
        self.conversation_manager = CustomConversationManager(api_key, model)
        self.results = []
    
    def process_excel_file(self, input_file: str, output_file: str = None, 
                          question_column: str = "问题", batch_size: int = 10,
                          delay_between_requests: float = 1.0) -> str:
        """
        处理Excel文件中的问题
        
        Args:
            input_file: 输入Excel文件路径
            output_file: 输出Excel文件路径，如果为None则自动生成
            question_column: 问题列名
            batch_size: 批处理大小
            delay_between_requests: 请求间隔时间（秒）
            
        Returns:
            处理结果信息
        """
        try:
            # 读取Excel文件
            print(f"正在读取Excel文件: {input_file}")
            df = pd.read_excel(input_file)
            
            if question_column not in df.columns:
                available_columns = list(df.columns)
                error_msg = f"错误：未找到列 '{question_column}'。\n\n可用列：\n"
                for i, col in enumerate(available_columns, 1):
                    error_msg += f"  {i}. {col}\n"
                error_msg += f"\n请使用 -c 参数指定正确的列名，例如：\n"
                error_msg += f"  python batch_qa_processor.py {input_file} -c \"{available_columns[0]}\"\n"
                error_msg += f"\n或者使用 --list-columns 查看所有列名：\n"
                error_msg += f"  python batch_qa_processor.py {input_file} --list-columns"
                return error_msg
            
            # 获取问题列表
            questions = df[question_column].dropna().tolist()
            total_questions = len(questions)
            
            if total_questions == 0:
                return "错误：Excel文件中没有找到有效的问题"
            
            print(f"找到 {total_questions} 个问题")
            
            # 生成输出文件名
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"batch_qa_results_{timestamp}.xlsx"
            
            # 批量处理问题
            print(f"开始批量处理，批大小: {batch_size}")
            
            for i, question in enumerate(questions, 1):
                print(f"\n处理第 {i}/{total_questions} 个问题: {question[:50]}...")
                
                try:
                    # 处理单个问题
                    answer, conversation_history = self.conversation_manager.process_user_input(question)
                    
                    # 保存结果
                    result = {
                        "序号": i,
                        "问题": question,
                        "回答": answer,
                        "处理时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "状态": "成功"
                    }
                    
                    # 尝试提取参考文献
                    references = self._extract_references(answer)
                    if references:
                        result["参考文献"] = references
                    
                    self.results.append(result)
                    
                    print(f"✓ 处理成功，回答长度: {len(answer)} 字符")
                    
                except Exception as e:
                    print(f"✗ 处理失败: {e}")
                    result = {
                        "序号": i,
                        "问题": question,
                        "回答": f"处理失败: {str(e)}",
                        "处理时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "状态": "失败"
                    }
                    self.results.append(result)
                
                # 请求间隔
                if i < total_questions and delay_between_requests > 0:
                    print(f"等待 {delay_between_requests} 秒...")
                    time.sleep(delay_between_requests)
                
                # 定期保存中间结果
                if i % batch_size == 0:
                    self._save_intermediate_results(output_file)
                    print(f"已保存中间结果到: {output_file}")
            
            # 保存最终结果
            self._save_final_results(output_file)
            
            # 统计结果
            successful = len([r for r in self.results if r["状态"] == "成功"])
            failed = len([r for r in self.results if r["状态"] == "失败"])
            
            result_summary = f"""
批量处理完成！

输入文件: {input_file}
输出文件: {output_file}
总问题数: {total_questions}
成功处理: {successful}
处理失败: {failed}
成功率: {successful/total_questions*100:.1f}%
            """
            
            print(result_summary)
            return result_summary
            
        except Exception as e:
            error_msg = f"批量处理失败: {e}"
            print(error_msg)
            return error_msg
    
    def _extract_references(self, answer: str) -> str:
        """
        从回答中提取参考文献
        
        Args:
            answer: 回答内容
            
        Returns:
            提取的参考文献
        """
        try:
            # 查找参考文献部分
            if "信息来源：" in answer:
                ref_start = answer.find("信息来源：")
                references = answer[ref_start:].strip()
                return references
            elif "参考链接：" in answer:
                ref_start = answer.find("参考链接：")
                references = answer[ref_start:].strip()
                return references
            else:
                return ""
        except:
            return ""
    
    def _save_intermediate_results(self, output_file: str):
        """保存中间结果"""
        try:
            df_results = pd.DataFrame(self.results)
            df_results.to_excel(output_file, index=False)
        except Exception as e:
            print(f"保存中间结果失败: {e}")
    
    def _save_final_results(self, output_file: str):
        """保存最终结果"""
        try:
            df_results = pd.DataFrame(self.results)
            df_results.to_excel(output_file, index=False)
            print(f"最终结果已保存到: {output_file}")
        except Exception as e:
            print(f"保存最终结果失败: {e}")
    
    def get_results(self) -> List[Dict[str, Any]]:
        """获取处理结果"""
        return self.results.copy()


def create_sample_excel():
    """创建示例Excel文件"""
    sample_questions = [
        "HPV疫苗的副作用有哪些？",
        "二价疫苗和四价疫苗有什么区别？",
        "HPV疫苗的接种年龄限制是什么？",
        "接种HPV疫苗后需要注意什么？",
        "HPV疫苗的保护期是多久？"
    ]
    
    df = pd.DataFrame({
        "问题": sample_questions,
        "备注": ["示例问题1", "示例问题2", "示例问题3", "示例问题4", "示例问题5"]
    })
    
    output_file = "sample_questions.xlsx"
    df.to_excel(output_file, index=False)
    print(f"示例Excel文件已创建: {output_file}")
    return output_file


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="批量问答处理工具")
    parser.add_argument("input_file", help="输入Excel文件路径")
    parser.add_argument("-o", "--output", help="输出Excel文件路径")
    parser.add_argument("-c", "--column", default="问题", help="问题列名（默认：问题）")
    parser.add_argument("-b", "--batch", type=int, default=10, help="批处理大小（默认：10）")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="请求间隔时间（秒，默认：1.0）")
    parser.add_argument("--create-sample", action="store_true", help="创建示例Excel文件")
    parser.add_argument("--list-columns", action="store_true", help="列出Excel文件中的所有列名")
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_excel()
        return
    
    # 检查输入文件
    if not os.path.exists(args.input_file):
        print(f"错误：输入文件不存在: {args.input_file}")
        return
    
    # 如果只是列出列名
    if args.list_columns:
        try:
            df = pd.read_excel(args.input_file)
            print(f"\n文件 '{args.input_file}' 中的列名：")
            for i, col in enumerate(df.columns, 1):
                print(f"  {i}. {col}")
            print(f"\n总共有 {len(df.columns)} 列")
            return
        except Exception as e:
            print(f"读取Excel文件失败: {e}")
            return
    
    # 创建处理器
    processor = BatchQAProcessor()
    
    # 处理文件
    result = processor.process_excel_file(
        input_file=args.input_file,
        output_file=args.output,
        question_column=args.column,
        batch_size=args.batch,
        delay_between_requests=args.delay
    )
    
    print(result)


if __name__ == "__main__":
    main() 