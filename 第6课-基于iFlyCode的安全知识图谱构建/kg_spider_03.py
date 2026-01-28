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

def fetch_page(url, retries=3, backoff_factor=1):
    """带指数退避的重试型网页请求"""
    for attempt in range(retries):
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, headers=headers, timeout=10)
            # 严格检查HTTP状态码是否成功 (2xx系列)
            if response.ok:
                response.encoding = response.apparent_encoding
                return response.text
            else:
                logging.warning(f"尝试 {attempt+1}/{retries} - HTTP错误码: {response.status_code} URL: {url}")
        except Exception as e:
            logging.error(f"尝试 {attempt+1}/{retries} - 异常类型: {type(e).__name__} | 消息: {str(e)} | URL: {url}")
        # 指数退避等待（如第一次等1秒，第二次等2秒...）
        time.sleep(backoff_factor * (2 ** attempt))
    return None  # 所有重试均失败后返回None

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
    # ===== Phase 1: 获取首页链接列表并去重 =====
    index_html = fetch_page(START_PAGE, retries=5)  # 对首页给予更多重试机会
    unique_links = set()  # 用集合实现自动去重
    if index_html:
        soup = BeautifulSoup(index_html, 'html.parser')
        # 收集所有符合条件的原始链接
        raw_links = [urljoin(BASE_URL, a_tag['href']) for a_tag in soup.select('a[href^="/groups/"]')]
        # 添加到集合中自动去重，并保留顺序前10条
        for link in raw_links:
            if len(unique_links) < 10:
                unique_links.add(link)
            else:
                break  # 已达10个即停止添加
    else:
        print(" 警告：多次尝试后仍无法加载主页！将使用空列表继续执行。")

    # 转换为有序列表以便后续迭代
    links = list(unique_links)[:10]  # 确保最多10个且有序

    # ===== Phase 2: 并行/串行处理每个组织的页面 =====
    results = []
    for i, link in enumerate(links, start=1):
        print(f" 正在处理第 {i}/{len(links)} 个组织: {link}")
        time.sleep(DELAY_SECONDS)  # 遵守爬取礼仪间隔

        # 单独为每个详情页设置较低的重试次数（避免过度消耗时间）
        group_page = fetch_page(link, retries=2)
        if group_page is None:
            results.append({
                '序号': i,
                'APT组织名称': "",
                '网址': link,
                '描述': f" 无法加载页面（见日志）",
                'Use用法': ""
            })
            continue

        try:
            record = parse_group_data(group_page, link)
            record['序号'] = i
            # 确保字段完整性
            required_keys = ['序号', 'APT组织名称', '网址', '描述', 'Use用法']
            for key in required_keys:
                record.setdefault(key, "")
            results.append(record)
        except Exception as e:
            logging.exception(f"解析页面时发生未捕获异常 | URL: {link}")
            results.append({
                '序号': i,
                'APT组织名称': "",
                '网址': link,
                '描述': f" 解析失败: {str(e)}",
                'Use用法': ""
            })

    # ===== Phase 3: 结果导出阶段 =====
    if results:  # 仅当有有效数据时才写入文件
        try:
            with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[
                    '序号', 'APT组织名称', '网址', '描述', 'Use用法'
                ])
                writer.writeheader()
                writer.writerows(results)
            print(f" 成功保存 {len(results)} 条记录至 {OUTPUT_FILE}")
        except Exception as e:
            logging.error(f"写入CSV失败: {str(e)}")
            print(" 无法保存结果，请检查日志文件 log.txt")
    else:
        print("无有效数据可保存")

if __name__ == "__main__":
    main()