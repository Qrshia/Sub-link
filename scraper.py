import requests
import re
import urllib.parse

def fetch_and_filter():
    url = 'https://t.me/s/ConfigsHUB2'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"Error fetching telegram page: {e}")
        return

    # پیدا کردن تمام پروتکل‌ها با Regex
    pattern = r'(vless|vmess|ss|trojan|tuic|hysteria2|hy2)://[^\s<"\']+'
    configs = re.findall(pattern, html, re.IGNORECASE)
    
    # وارونه کردن لیست برای اینکه جدیدترین‌ها اول بیایند
    configs.reverse()

    filtered_ss_tr_443 = []
    all_configs = []

    for c in configs:
        # تمیز کردن کاراکترهای خاص HTML
        c_clean = c.replace('&amp;', '&')
        all_configs.append(c_clean)

        # دیکود کردن لینک برای بررسی نام کشور در بخش کامنت/ریمپ کانفیگ
        decoded = urllib.parse.unquote(c_clean).upper()

        # شروط فیلتر شما: Shadowsocks + ترکیه + پورت 443
        is_ss = c_clean.lower().startswith('ss://')
        is_tr = 'TR' in decoded or 'TURKEY' in decoded or '🇹🇷' in decoded
        is_443 = ':443' in c_clean or '%3A443' in c_clean

        if is_ss and is_tr and is_443:
            filtered_ss_tr_443.append(c_clean)

    # اعمال محدودیت تعداد (مثلاً ۱۰۰ عدد اخیر)
    filtered_ss_tr_443 = filtered_ss_tr_443[:100]
    all_configs = all_configs[:100]

    # ذخیره فایل فیلتر شده اختصاصی شما
    with open('ss_turkey_443.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(filtered_ss_tr_443))

    # ذخیره فایل همه کانفیگ‌های اخیر (اختیاری - برای استفاده‌های دیگر)
    with open('all_configs.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_configs))

    print(f"بروزرسانی موفقیت‌آمیز بود. تعداد {len(filtered_ss_tr_443)} کانفیگ مطابق با فیلتر شما یافت شد.")

if __name__ == '__main__':
    fetch_and_filter()
