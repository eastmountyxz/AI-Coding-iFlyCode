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
USE_SYSTEM_PROXY = False     # False: 不继承系统代理（修复HTTPS走HTTP代理问题）
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
    """
    优先采集 <div class="description-body"> 文本，
    若不存在则回退到 #description。
    """
    bodies = soup.select('div.description-body')
    paras = []
    if bodies:
        for body in bodies:
            # 只取直接文本与段落
            # 若 body 内含多段 <p>，逐段拼接
            ps = body.find_all(['p', 'div'])
            if ps:
                paras.extend([clean_text(p.get_text()) for p in ps if clean_text(p.get_text())])
            else:
                txt = clean_text(body.get_text())
                if txt:
                    paras.append(txt)
    if not paras:
        desc = soup.select_one('#description')
        if desc:
            ps = [clean_text(p.get_text()) for p in desc.find_all(['p', 'div'], recursive=False)]
            ps = [p for p in ps if p]
            if ps:
                paras = ps
            else:
                txt = clean_text(desc.get_text())
                if txt:
                    paras = [txt]
    return "\n".join(paras) if paras else "未找到描述。"

def extract_use_from_techniques_table(soup: BeautifulSoup) -> str:
    block = soup.select_one('#techniques-used')
    if not block:
        return "未找到 Use 用法信息。"
    table = block.find('table')
    if not table:
        text = clean_text(block.get_text())
        return text if text else "未找到 Use 用法信息。"

    headers = [clean_text(th.get_text()) for th in table.select('thead th')]
    id_idx = name_idx = use_idx = None
    for i, h in enumerate(headers):
        hh = h.lower()
        if id_idx is None and ('id' == hh or 'technique id' in hh):
            id_idx = i
        if name_idx is None and ('name' in hh or 'technique' == hh):
            name_idx = i
        if use_idx is None and ('use' in hh):
            use_idx = i

    rows_out = []
    for tr in table.select('tbody tr'):
        tds = tr.find_all('td')
        if not tds:
            continue

        def pick(idx):
            if idx is None or idx >= len(tds):
                return ""
            return clean_text(tds[idx].get_text())

        tid = pick(id_idx)
        tname = pick(name_idx)
        use = pick(use_idx)
        if tname or tid or use:
            head = f"{tname} ({tid})" if tid and tname else (tname or tid or "Technique")
            rows_out.append(f"• {head}: {use}" if use else f"• {head}")

    if not rows_out:
        text = clean_text(block.get_text())
        return text if text else "未找到 Use 用法信息。"
    return "\n".join(rows_out)

def parse_group_data(html: str, group_id: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    name = extract_group_name(soup, group_id)
    desc = extract_description(soup)               # ← 这里已按你的要求采集 description-body
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
