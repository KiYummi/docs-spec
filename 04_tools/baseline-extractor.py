#!/usr/bin/env python3
"""
原子需求提取工具骨架

功能：从 PRD 文档中提取原子需求，生成结构化基线
输入：PRD Markdown 文件
输出：原子需求清单 JSON

注意：此为骨架实现，需根据项目实际情况完善
"""

import json
import re
import sys
from pathlib import Path


def extract_requirements(prd_path: str) -> list[dict]:
    """
    从 PRD 文件中提取原子需求

    Args:
        prd_path: PRD 文件路径

    Returns:
        原子需求列表
    """
    content = Path(prd_path).read_text(encoding="utf-8")
    requirements = []

    # TODO: 实现需求提取逻辑
    # 1. 查找"原子需求提取"章节
    # 2. 解析表格中的需求
    # 3. 提取 ID、描述、语义要素、来源、优先级

    # 示例解析逻辑（伪代码）：
    # pattern = r'@req-id:\s*(R\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(P\d+)'
    # for match in re.finditer(pattern, content):
    #     requirements.append({
    #         "id": match.group(1),
    #         "description": match.group(2),
    #         "semantic_elements": match.group(3),
    #         "source": match.group(4),
    #         "priority": match.group(5)
    #     })

    return requirements


def save_requirements(requirements: list[dict], output_path: str):
    """
    保存原子需求到 JSON 文件

    Args:
        requirements: 原子需求列表
        output_path: 输出文件路径
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(requirements, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 3:
        print("Usage: python baseline-extractor.py <prd_path> <output_path>")
        sys.exit(1)

    prd_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Extracting requirements from: {prd_path}")
    requirements = extract_requirements(prd_path)
    print(f"Found {len(requirements)} requirements")

    save_requirements(requirements, output_path)
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
