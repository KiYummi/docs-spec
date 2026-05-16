#!/usr/bin/env python3
"""
索引更新工具骨架

功能：扫描项目中所有 @req-id 标签，重建全局索引
输入：项目文档目录
输出：index.json

注意：此为骨架实现，需根据项目实际情况完善
"""

import json
import os
import re
import sys
from pathlib import Path


def scan_req_ids(docs_dir: str) -> dict:
    """
    扫描目录中所有 @req-id 标签

    Args:
        docs_dir: 文档目录路径

    Returns:
        需求 ID 到文件的映射
    """
    req_map = {}
    pattern = r"@req-id:\s*(R\d+)"

    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith((".md", ".json", ".yaml")):
                filepath = os.path.join(root, file)
                try:
                    content = Path(filepath).read_text(encoding="utf-8")
                    for match in re.finditer(pattern, content):
                        req_id = match.group(1)
                        if req_id not in req_map:
                            req_map[req_id] = []
                        req_map[req_id].append(filepath)
                except Exception as e:
                    print(f"Warning: Failed to read {filepath}: {e}")

    return req_map


def build_index(req_map: dict) -> dict:
    """
    构建全局索引

    Args:
        req_map: 需求 ID 到文件的映射

    Returns:
        索引结构
    """
    index = {
        "version": "1.0.0",
        "requirements": {}
    }

    for req_id, files in req_map.items():
        index["requirements"][req_id] = {
            "id": req_id,
            "artifacts": [{"path": f} for f in files]
        }

    return index


def main():
    if len(sys.argv) < 3:
        print("Usage: python index-updater.py <docs_dir> <output_path>")
        sys.exit(1)

    docs_dir = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Scanning directory: {docs_dir}")
    req_map = scan_req_ids(docs_dir)
    print(f"Found {len(req_map)} unique requirement IDs")

    index = build_index(req_map)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Index saved to: {output_path}")


if __name__ == "__main__":
    main()
