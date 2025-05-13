#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2025-01-16 15:27
#   Desc    :   公共函数
import os
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime, timezone, timedelta

from retry import retry

# 常量定义
GITHUB_URLS = [
    'alive.github.com', 'api.github.com', 'api.individual.githubcopilot.com',
    'avatars.githubusercontent.com', 'avatars0.githubusercontent.com',
    'avatars1.githubusercontent.com', 'avatars2.githubusercontent.com',
    'avatars3.githubusercontent.com', 'avatars4.githubusercontent.com',
    'avatars5.githubusercontent.com', 'camo.githubusercontent.com',
    'central.github.com', 'cloud.githubusercontent.com', 'codeload.github.com',
    'collector.github.com', 'desktop.githubusercontent.com',
    'favicons.githubusercontent.com', 'gist.github.com',
    'github-cloud.s3.amazonaws.com', 'github-com.s3.amazonaws.com',
    'github-production-release-asset-2e65be.s3.amazonaws.com',
    'github-production-repository-file-5c1aeb.s3.amazonaws.com',
    'github-production-user-asset-6210df.s3.amazonaws.com', 'github.blog',
    'github.com', 'github.community', 'github.githubassets.com',
    'github.global.ssl.fastly.net', 'github.io', 'github.map.fastly.net',
    'githubstatus.com', 'live.github.com', 'media.githubusercontent.com',
    'objects.githubusercontent.com', 'pipelines.actions.githubusercontent.com',
    'raw.githubusercontent.com', 'user-images.githubusercontent.com',
    'vscode.dev', 'education.github.com', 'private-user-images.githubusercontent.com',
    'javdb.com','missav.com','www.javbus.com','pornhub.com','phncdn.com','cv-h.phncdn.com',
    'supjav.com','everia.club'
]

HOSTS_TEMPLATE = """# Hosts520 Host Start
{content}

# Update time: {update_time}
# Update url: https://raw.hellogithub.com/hosts
# Star me: https://github.com/521xueweihan/GitHub520
# Hosts520 Host End\n"""

# 类型别名
HostsEntry = Tuple[str, str]
HostsList = List[HostsEntry]

def get_absolute_path(relative_path: str) -> Path:
    """获取绝对路径"""
    return Path(__file__).parent / relative_path

@retry(tries=3, delay=1)
def get_json() -> Optional[HostsList]:
    """读取hosts.json文件"""
    try:
        json_path = get_absolute_path("hosts.json")
        if not json_path.exists():
            print("hosts.json not found, returning None")
            return None
            
        with json_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Invalid JSON format: expected list")
            return data
    except (json.JSONDecodeError, ValueError) as ex:
        print(f"JSON decode error: {ex}")
        raise
    except Exception as ex:
        print(f"Unexpected error reading hosts.json: {ex}")
        raise

def write_file(hosts_content: str, update_time: str) -> bool:
    """
    更新README.md文件
    返回bool表示是否有变更
    """
    try:
        readme_path = get_absolute_path("README.md")
        template_path = get_absolute_path("README_template.md")
        
        # 确保目录存在
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 先写入hosts文件
        write_host_file(hosts_content)
        
        # 检查README是否已存在
        if readme_path.exists():
            old_content = readme_path.read_text(encoding='utf-8')
            if old_content:
                try:
                    old_hosts = old_content.split("```bash")[1].split("```")[0].strip()
                    old_hosts = old_hosts.split("# Update time:")[0].strip()
                    new_hosts = hosts_content.split("# Update time:")[0].strip()
                    if old_hosts == new_hosts:
                        print("Hosts content unchanged")
                        return False
                except IndexError:
                    print("Failed to parse existing README, forcing update")

        # 更新README
        template = template_path.read_text(encoding='utf-8')
        updated_content = template.format(
            hosts_str=hosts_content,
            update_time=update_time
        )
        readme_path.write_text(updated_content, encoding='utf-8')
        return True
        
    except Exception as ex:
        print(f"Error updating files: {ex}")
        raise

def write_host_file(hosts_content: str) -> None:
    """写入hosts文件"""
    try:
        hosts_path = get_absolute_path("hosts")
        hosts_path.write_text(hosts_content, encoding='utf-8')
        print(f"Successfully wrote hosts file to {hosts_path}")
    except Exception as ex:
        print(f"Failed to write hosts file: {ex}")
        raise

def write_json_file(hosts_list: HostsList) -> None:
    """写入hosts.json文件"""
    try:
        json_path = get_absolute_path("hosts.json")
        with json_path.open('w', encoding='utf-8') as f:
            json.dump(hosts_list, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated hosts.json at {json_path}")
    except Exception as ex:
        print(f"Failed to write hosts.json: {ex}")
        raise

def write_hosts_content(content: str, content_list: HostsList) -> str:
    """
    生成并写入最终的hosts内容
    返回生成的完整hosts内容
    """
    if not content:
        print("Warning: empty content provided")
        return ""

    try:
        update_time = datetime.now(timezone.utc).astimezone(
            timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
        
        hosts_content = HOSTS_TEMPLATE.format(
            content=content,
            update_time=update_time
        )
        
        has_change = write_file(hosts_content, update_time)
        if has_change:
            write_json_file(content_list)
        else:
            print("No changes detected, skipping JSON update")
            
        return hosts_content
        
    except Exception as ex:
        print(f"Error in write_hosts_content: {ex}")
        raise
