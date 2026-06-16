import requests
import re
import urllib.parse

def fetch_and_filter():
    url = 'https://t.me/s/ConfigsHUB2'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        html = response.text
    except Exception as e:
        print(f"Error: {e}")
        return

    pattern = r'(vless|vmess|ss|trojan|tuic|hysteria2|hy2)://[^\s<"\']+'
    configs = re.findall(pattern, html, re.IGNORECASE)
    configs.reverse()

    # تعریف سبدهای مختلف برای تفکیک کانفیگ‌ها
    ss_tr_443 = []
    all_ss = []
    all_vless = []

    for c in configs:
        c_clean = c.replace('&amp;', '&')
        decoded = urllib.parse.unquote(c_clean).upper()
        
        is_tr = 'TR' in decoded or 'TURKEY' in decoded or '🇹🇷' in decoded
        is_443 = ':443' in c_clean or '%3A443' in c_clean

        # ۱. سبد شادوساکس ترکیه ۴۴۳
        if c_clean.lower().startswith('ss://') and is_tr and is_443:
            ss_tr_443.append(c_clean)
        
        # ۲. سبد تمام شادوساکس‌ها
        if c_clean.lower().startswith('ss://'):
            all_ss.append(c_clean)
            
        # ۳. سبد تمام Vless‌ها
        if c_clean.lower().startswith('vless://'):
            all_vless.append(c_clean)

    # ذخیره فایل‌ها (محدود به ۱۰۰ عدد اخیر)
    with open('ss_turkey_443.txt', 'w', encoding='utf-8') as f: f.write('\n'.join(ss_tr_443[:100]))
    with open('all_shadowsocks.txt', 'w', encoding='utf-8') as f: f.write('\n'.join(all_ss[:100]))
    with open('all_vless.txt', 'w', encoding='utf-8') as f: f.write('\n'.join(all_vless[:100]))

if __name__ == '__main__':
    fetch_and_filter()
