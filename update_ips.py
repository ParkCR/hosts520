#!/usr/bin/env python
import json
from typing import Any, Optional
from common import write_hosts_content

def get_json() -> Optional[list]:
    try:
        with open('/github/workspace/hosts.json', 'r') as f:  # 固定路径
            data = json.load(f)
            print(f"Loaded data: {data[:1]}...")  # 打印第一条数据
            return data
    except Exception as ex:
        print(f"Error reading hosts.json: {ex}")
        return None

def main() -> None:
    print('Start script.')
    content_list = get_json()
    if not content_list:
        raise ValueError("hosts.json is empty or invalid")  # 强制失败

    content = ""
    for domain, ip in content_list:  # 明确解构
        content += f"{domain.ljust(30)}{ip}\n"
    
    hosts_content = write_hosts_content(content, content_list)
    print(f"Generated hosts content:\n{hosts_content[:100]}...")  # 预览
    print('End script.')

if __name__ == '__main__':
    main()
