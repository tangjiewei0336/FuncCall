"""
处理100个评估问题的示例脚本
专门用于处理 batch_inference_input/100个评估问题选择 （分级）.xlsx 文件
"""

import os
import sys
from batch_qa_processor import BatchQAProcessor

def main():
    """处理100个评估问题"""
    
    # 输入文件路径
    input_file = "batch_inference_input/100个评估问题选择 （分级）.xlsx"
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：文件不存在: {input_file}")
        print("请确保文件路径正确")
        return
    
    print("=== 100个评估问题批量处理 ===")
    print(f"输入文件: {input_file}")
    
    # 首先列出文件中的列名
    print("\n1. 查看文件列名...")
    os.system(f"python batch_qa_processor.py \"{input_file}\" --list-columns")
    
    # 询问用户选择问题列名
    print("\n2. 请根据上面的列名，选择包含问题的列名：")
    print("常见的问题列名可能是：")
    print("  - 问题")
    print("  - 题目")
    print("  - 内容")
    print("  - 评估问题")
    print("  - 问题内容")
    
    # 这里可以根据实际文件结构预设列名
    # 如果知道确切的列名，可以直接使用
    question_column = input("请输入问题列名（或按回车使用默认值'问题'）: ").strip()
    if not question_column:
        question_column = "问题"
    
    # 设置输出文件名
    output_file = f"100个评估问题结果_{os.path.basename(input_file).replace('.xlsx', '')}.xlsx"
    
    print(f"\n3. 开始处理...")
    print(f"问题列名: {question_column}")
    print(f"输出文件: {output_file}")
    
    # 创建处理器
    processor = BatchQAProcessor()
    
    # 处理文件（使用较小的批处理大小和较长的延迟，避免API限制）
    result = processor.process_excel_file(
        input_file=input_file,
        output_file=output_file,
        question_column=question_column,
        batch_size=5,  # 较小的批处理大小
        delay_between_requests=2.0  # 较长的延迟
    )
    
    print(f"\n4. 处理完成！")
    print(result)
    print(f"\n结果已保存到: {output_file}")

if __name__ == "__main__":
    main() 