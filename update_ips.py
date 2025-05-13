#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2025-01-16 15:27
#   Desc    :   GitHub Action 运行的脚本
import json
from typing import Any, Optional

from retry import retry
from requests_html import HTMLSession

from common import write_hosts_content


@retry(tries=3)
def get_json() -> Optional[list]:
    try:
        with open('hosts.json', 'r') as f:
            data = json.load(f)
            return data
    except Exception as ex:
        print(f"Read hosts.json error: {ex}")
        raise Exception


def main() -> None:
    print('Start script.')
    content = ""
    content_list = get_json()
    for item in content_list:
        content += item[0].ljust(30) + item[1] + "\n"
    hosts_content = write_hosts_content(content, content_list)
    print(hosts_content)
    print('End script.')


if __name__ == '__main__':
    main()
