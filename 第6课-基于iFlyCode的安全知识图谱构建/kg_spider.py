# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import logging
from urllib.parse import urljoin
import time

# 配置日志系统
logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://attack.mitre.org"
START_PAGE = f"{BASE_URL}/groups/"
OUTPUT_FILE = "attack_groups.csv"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
DELAY_SECONDS = 2  # 避免频繁请求被屏蔽

def clean_text(text):
    """清理文本：移除HTML标签、多余空格和换行"""
    if not text:
        return ""
    # 替换各种空白字符为单个空格
    cleaned = ' '.join(text.split())
    return cleaned.strip()

def fetch_page(url):
    """获取网页内容，失败时返回None"""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 触发HTTP错误异常
        # 自动检测编码以防乱码
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        logging.error(f"请求失败 [URL]: {url} | 错误: {str(e)}")
        return None

def parse_group_data(html_content, group_url):
    """解析单个APT组织页面的数据"""
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}

    # 1. APT组织名称（来自<title>标签）
    title_tag = soup.find('title')
    data['name'] = clean_text(title_tag.get_text()) if title_tag else ""

    # 2. URL已由参数传入，无需重复提取
    data['url'] = group_url

    # 3. 提取Description段落
    desc_section = soup.find('div', string=lambda t: 'description' in str(t).lower())
    if desc_section:  # 宽松匹配包含description的元素
        data['description'] = clean_text(desc_section.get_text())
    else:
        data['description'] = ""

    # 4. 提取Use/Techniques Used等章节内容
    use_content = ""
    # 根据常见标题关键词查找相关区域
    headings = ['use', 'techniques used', 'software/tools used', 'tactics used']
    for heading in headings:
        section = soup.find('h3', string=lambda t: heading in str(t).lower())
        if section:
            next_sibling = section.find_next_sibling('div') or section.find_next('div')
            if next_sibling:
                use_content += clean_text(next_sibling.get_text()) + "\n"
    data['use_cases'] = clean_text(use_content).strip() if use_content else ""

    return data

def main():
    # Step 1: 获取所有APT组织的链接列表
    index_page = fetch_page(START_PAGE)
    if not index_page:
        print("无法加载主页，程序终止。")
        return

    soup = BeautifulSoup(index_page, 'html.parser')
    links = []
    for a_tag in soup.select('a[href^="/groups/"]'):
        href = a_tag.get('href')
        full_link = urljoin(BASE_URL, href)
        links.append(full_link)

    results = []
    for i, link in enumerate(links, start=1):
        print(f"正在处理第 {i}/{len(links)} 个组织: {link}")
        time.sleep(DELAY_SECONDS)  # 礼貌性延迟

        html = fetch_page(link)
        if html is None:
            results.append({
                '序号': i,
                'APT组织名称': "",
                '网址': link,
                '描述': "",
                'Use用法': ""
            })
            continue

        try:
            record = parse_group_data(html, link)
            record['序号'] = i
            # 确保所有必要键都存在
            required_keys = ['序号', 'APT组织名称', '网址', '描述', 'Use用法']
            for key in required_keys:
                if key not in record:
                    record[key] = ""
            results.append(record)
        except Exception as e:
            logging.error(f"解析页面时出错 [URL]: {link} | 错误: {str(e)}")
            # 发生异常时填充默认空值
            results.append({
                '序号': i,
                'APT组织名称': "",
                '网址': link,
                '描述': "",
                'Use用法': f"解析错误: {str(e)}"
            })

    # Step 2: 写入CSV文件
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                '序号', 'APT组织名称', '网址', '描述', 'Use用法'
            ])
            writer.writeheader()
            writer.writerows(results)
        print(f"数据已成功保存至 {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"写入CSV文件失败: {str(e)}")
        print("无法保存结果，请检查日志文件 log.txt")

if __name__ == "__main__":
    main()
