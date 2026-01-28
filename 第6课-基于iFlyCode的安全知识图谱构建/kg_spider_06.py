# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ===== 配置参数 =====
BASE_URL = "https://attack.mitre.org"
OUTPUT_FILE = "attack_groups_fixed.csv"
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/122.0.0.0 Safari/537.36")
DELAY_SECONDS = 2.5
USE_SYSTEM_PROXY = False    # 如必须走代理再改 True，并正确配置 HTTPS 代理
VERIFY_SSL = True
TARGET_GROUPS = [
    'G0050','G0007','G0016','G0013','G0064',
    'G0067','G0087','G1002','G0098','G0012'
]

# ===== 日志 =====
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clean_text(text: str) -> str:
    if not text:
        return ""
    return ' '.join(text.split()).strip()

def build_session():
    s = requests.Session()
    s.headers.update({'User-Agent': USER_AGENT})
    s.trust_env = USE_SYSTEM_PROXY
    retries = Retry(
        total=3,
        backoff_factor=1.2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(['GET','HEAD'])
    )
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))
    return s

def fetch_page(session: requests.Session, url: str) -> str:
    try:
        resp = session.get(url, timeout=20, verify=VERIFY_SSL)
        if resp.ok:
            resp.encoding = resp.apparent_encoding or 'utf-8'
            return resp.text
        logging.error(f"请求失败 [HTTP {resp.status_code}] URL: {url}")
    except requests.RequestException as e:
        logging.error(f"请求异常 [URL]: {url} | 错误: {repr(e)}")
    return None

def extract_group_name(soup: BeautifulSoup, fallback_id: str) -> str:
    h1 = soup.select_one('h1.page-title') or soup.select_one('h1.page-header') or soup.select_one('h1')
    return clean_text(h1.get_text()) if h1 else f"[未识别名称]{fallback_id}"

def extract_description(soup: BeautifulSoup) -> str:
    """优先采集 <div class="description-body">，无则回退 #description"""
    bodies = soup.select('div.description-body')
    paras = []
    if bodies:
        for body in bodies:
            ps = body.find_all(['p', 'div'])
            if ps:
                for p in ps:
                    t = clean_text(p.get_text())
                    if t: paras.append(t)
            else:
                t = clean_text(body.get_text())
                if t: paras.append(t)
    if not paras:
        desc = soup.select_one('#description')
        if desc:
            ps = desc.find_all(['p', 'div'], recursive=False)
            if ps:
                for p in ps:
                    t = clean_text(p.get_text())
                    if t: paras.append(t)
            else:
                t = clean_text(desc.get_text())
                if t: paras.append(t)
    return "\n".join(paras) if paras else "未找到描述。"

def _expand_thead_headers(table: BeautifulSoup):
    """
    将 thead 中的 th 展开为与 tbody 列数一致的列名列表。
    针对 'ID' 可能出现的 colspan=2，展开为 ['ID-1','ID-2']。
    """
    expanded = []
    ths = table.select('thead th')
    for th in ths:
        text = clean_text(th.get_text())
        colspan = th.get('colspan')
        try:
            c = int(colspan) if colspan else 1
        except ValueError:
            c = 1
        if c <= 1:
            expanded.append(text)
        else:
            # 为兼容 “ID” 跨两列的情形
            base = text if text else "COL"
            for i in range(1, c + 1):
                expanded.append(f"{base}-{i}")
    return expanded

def extract_use_from_techniques_table(soup: BeautifulSoup) -> str:
    """
    精确抓取 #techniques-used 下 class 包含 'techniques-used' 的表格，
    解析最后一列 'Use'，并兼容 'ID' colspan=2 的情况。
    输出格式：• Name (ID...): Use
    """
    block = soup.select_one('#techniques-used')
    if not block:
        return "未找到 Use 用法信息。"

    # 优先选择 class 含 techniques-used 的表
    table = block.select_one('table.techniques-used') or block.find('table')
    if not table:
        text = clean_text(block.get_text())
        return text if text else "未找到 Use 用法信息。"

    # 展开表头
    headers = _expand_thead_headers(table)
    headers_lc = [h.lower() for h in headers]

    # 锁定列索引
    # 可能存在的列名：Domain | ID-1 | ID-2 | Name | Use
    name_idx = None
    use_idx = None
    id_indices = []

    for i, h in enumerate(headers_lc):
        if name_idx is None and h == 'name':
            name_idx = i
        if use_idx is None and h == 'use':
            use_idx = i
        if h.startswith('id'):
            id_indices.append(i)  # ID-1、ID-2...

    # 容错：若未检测到 Use 列，尝试将最后一列视为 Use
    if use_idx is None and headers:
        use_idx = len(headers) - 1

    rows_out = []
    for tr in table.select('tbody tr'):
        tds = tr.find_all('td')
        if not tds:
            continue

        def pick(idx):
            if idx is None or idx >= len(tds):
                return ""
            # 去掉脚注/上标等文本噪声
            for sup in tds[idx].find_all(['sup', 'span']):
                sup.extract()
            return clean_text(tds[idx].get_text())

        # 拼接多个 ID 列
        ids = []
        for idx in id_indices:
            val = pick(idx)
            if val:
                ids.append(val)
        tid = " / ".join(ids) if ids else ""

        tname = pick(name_idx)
        use = pick(use_idx)

        if not (tname or tid or use):
            continue

        head = f"{tname} ({tid})" if (tname and tid) else (tname or tid or "Technique")
        rows_out.append(f"• {head}: {use}" if use else f"• {head}")

    if not rows_out:
        text = clean_text(block.get_text())
        return text if text else "未找到 Use 用法信息。"
    return "\n".join(rows_out)

def parse_group_data(html: str, group_id: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    name = extract_group_name(soup, group_id)
    desc = extract_description(soup)
    use_text = extract_use_from_techniques_table(soup)
    return {
        'APT组织名称': name,
        '网址': f"{BASE_URL}/groups/{group_id}/",
        '描述': desc,
        'Use用法': use_text
    }

def main():
    session = build_session()
    urls = [f"{BASE_URL}/groups/{gid}/" for gid in TARGET_GROUPS]
    results = []

    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{len(urls)}] 抓取: {url}")
        time.sleep(DELAY_SECONDS)
        html = fetch_page(session, url)
        if not html:
            logging.error(f"抓取失败: {url}")
            results.append({
                '序号': idx,
                'APT组织名称': TARGET_GROUPS[idx-1],
                '网址': url,
                '描述': "页面获取失败（网络/代理/证书问题）",
                'Use用法': "无"
            })
            continue

        try:
            record = parse_group_data(html, TARGET_GROUPS[idx-1])
            record['序号'] = idx
            results.append(record)
        except Exception as e:
            logging.exception(f"解析异常: {url} | {repr(e)}")
            results.append({
                '序号': idx,
                'APT组织名称': TARGET_GROUPS[idx-1],
                '网址': url,
                '描述': f"解析异常：{type(e).__name__} - {str(e)}",
                'Use用法': "需人工核查"
            })

    fieldnames = ['序号', 'APT组织名称', '网址', '描述', 'Use用法']
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            w.writeheader()
            for row in results:
                for k in fieldnames:
                    row.setdefault(k, "")
                w.writerow(row)
        print(f"成功导出 {len(results)} 条记录 -> {OUTPUT_FILE}")
    except Exception as e:
        logging.critical(f"写入CSV失败: {repr(e)}")
        print("保存失败，请查看 log.txt")

if __name__ == "__main__":
    main()
