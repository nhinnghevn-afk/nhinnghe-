"""Cập nhật thông báo sự kiện trên toàn website từ content/announcement.json.

- Thanh thông báo đầu mọi trang (giữa <!--announce--> ... <!--/announce-->).
- Khung sự kiện trong phần đầu Trang chủ (giữa <!--home-event--> ... <!--/home-event-->).
- Trang chuyển hướng ngắn /dang-ky/ trỏ tới phần đăng ký của sự kiện.
Chạy: python3 scripts/set-announcement.py
"""
import json, re, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / 'dist'
c = json.loads((ROOT / 'content/announcement.json').read_text(encoding='utf-8'))
e = lambda s: html.escape(s, quote=True)
on = c.get('enabled')
ext = 'target="_blank" rel="noopener noreferrer"'
sr = '<span class="sr-only"> (mở phiếu đăng ký trong thẻ mới)</span>'
bar = (f'<!--announce--><aside class="announce-bar" aria-label="Thông báo sự kiện"><div class="wrap announce-inner">'
       f'<span class="announce-date">{e(c["dateShort"])}</span>'
       f'<span class="announce-text"><span class="announce-lead">{e(c["barLead"])} </span><a href="{e(c["detailPath"])}">{e(c["title"])}</a></span>'
       f'<a class="announce-cta" href="{e(c["registerUrl"])}" {ext}>Đăng ký ngay <span aria-hidden="true">→</span>{sr}</a>'
       f'</div></aside><!--/announce-->') if on else '<!--announce--><!--/announce-->'
box = (f'<!--home-event--><div class="home-next-event"><span class="mini-label">{e(c["label"])}</span>'
       f'<strong>{e(c["title"])}</strong><span>{e(c["dateLong"])} · {e(c["audience"])}</span><small>{e(c["note"])}</small>'
       f'<p class="event-cta"><a class="btn primary" href="{e(c["registerUrl"])}" {ext}>Đăng ký tham gia <span aria-hidden="true">↗</span>{sr}</a>'
       f'<a class="text-link" href="{e(c["detailPath"])}">Xem nội dung buổi</a></p></div><!--/home-event-->') if on else '<!--home-event--><!--/home-event-->'
skip_pages = {'hoat-dong/hieu-nghe/index.html', 'dang-ky/index.html'}
n = 0
for p in sorted(D.rglob('index.html')):
    rel = p.relative_to(D).as_posix()
    if rel in skip_pages: continue
    t = p.read_text(encoding='utf-8'); o = t
    if '<!--announce-->' in t:
        t = re.sub(r'<!--announce-->.*?<!--/announce-->', lambda m: bar, t, flags=re.S)
    else:
        t = t.replace('<header class="top">', bar + '<header class="top">', 1)
    if rel == 'index.html':
        if '<!--home-event-->' in t:
            t = re.sub(r'<!--home-event-->.*?<!--/home-event-->', lambda m: box, t, flags=re.S)
        else:
            t = t.replace('<p><a class="btn primary" href="#bat-dau">Chọn nơi bắt đầu</a></p></div><aside class="home-pillars">',
                          box + '<p><a class="btn" href="#bat-dau">Chọn nơi bắt đầu</a></p></div><aside class="home-pillars">', 1)
        assert '<!--home-event-->' in t, 'không tìm thấy vị trí khung Trang chủ'
    assert '<!--announce-->' in t, rel
    if t != o: p.write_text(t, encoding='utf-8'); n += 1
# đường dẫn ngắn /dang-ky/
target = '../' + c['detailPath'].strip('/') + '/#tham-gia' if on else '../hoat-dong/chia-se-nghe-nghiep/'
dk = D / 'dang-ky'; dk.mkdir(exist_ok=True)
(dk / 'index.html').write_text(f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Đăng ký buổi chia sẻ | Nhìn Nghề</title><meta http-equiv="refresh" content="0; url={e(target)}"><link rel="canonical" href="{e(target)}"></head><body><p>Đang chuyển tới trang đăng ký… <a href="{e(target)}">Bấm vào đây nếu trang không tự chuyển</a>.</p></body></html>\n', encoding='utf-8')
print(f'Đã cập nhật {n} trang; /dang-ky/ → {target}')
