#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2025-01-16 15:27
#   Desc    :   GitHub Action 运行的脚本
import json
import os
from typing import Any, Optional, List

from retry import retry
from requests_html import HTMLSession

from common import write_hosts_content, write_json_file, GITHUB_URLS  # 确保导入这些


@retry(tries=3)
def get_json() -> List[Any]:
    """获取hosts数据，如果文件不存在则返回空列表"""
    try:
        filepath = os.path.join(os.getcwd(), 'hosts.json')
        if not os.path.exists(filepath):
            return []
            
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as ex:
        print(f"Read hosts.json error: {ex}")
        return []  # 文件不存在或读取失败时返回空列表


def generate_new_content() -> str:
    """生成新的hosts内容（示例，需替换为你的实际逻辑）"""
    # 这里应该是你获取最新IP的逻辑
    # 示例：返回硬编码内容用于测试
    return "\n".join([f"{ip.ljust(30)}{domain}" 
                     for domain in GITHUB_URLS 
                     for ip in ["127.0.0.1"]])  # 替换为真实IP获取逻辑


def main() -> None:
    print('Start script.')
    
    # 1. 获取现有内容
    existing_content = ""
    content_list = get_json()
    
    # 2. 生成新内容（这里需要替换为你的实际IP获取逻辑）
    new_content = generate_new_content()
    
    # 3. 合并内容（或完全使用新内容）
    final_content = new_content  # 这里简单使用新内容，可根据需求调整
    
    # 4. 更新文件（强制写入）
    hosts_content = write_hosts_content(final_content, content_list)
    
    # 调试输出
    print("=== Generated Content ===")
    print(hosts_content[:500] + "...")  # 打印部分内容避免日志过长
    print('End script.')


if __name__ == '__main__':
    main()
