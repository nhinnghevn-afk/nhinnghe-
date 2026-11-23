"""Render six approved homepage blocks and common navigation/footer/privacy.

Run build-activities.py afterwards to render shared event cards. All source copy
is selected public material; never place full books or private records in dist.
"""
from pathlib import Path
from html import escape as esc
import json,re
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
site=json.loads((ROOT/'content/site.json').read_text());brand=site['brand'];nav=site['navigation']
articles=json.loads((D/'career-articles.json').read_text())['articles']
programs=json.loads((D/'student-programs.json').read_text())['programs']
assert all(not p['accepting']for p in programs)
def a(t,p,c='text-link'):return f'<a class="{c}" href="{esc(p,quote=True)}">{esc(t)}</a>'
parts=re.findall(r'<section\b[^>]*>.*?</section>',(ROOT/'content/home.html').read_text(),re.S)
assert len(parts)==6
home=[]
for i,b in enumerate(parts):
    b=re.sub(r'<p class="meta">.*?</p>','',b,flags=re.S)
    b=b.replace('<section ',f'<section class="home-section home-block-{i+1}" ',1)
    b=b.replace('><h2>','><div class="wrap"><h2>',1).replace('</section>','</div></section>')
    if i==0:
        b=b.replace(' id="noi-dung"','').replace('<h2>','<h1>').replace('</h2>','</h1>')
        b=b.replace('<a href="#bat-dau">','<a class="btn primary" href="#bat-dau">')
        b=b.replace('<div class="wrap">','<div class="wrap home-hero-layout"><div>',1)
        b=b.replace('</div></section>','</div><aside class="home-pillars"><span class="mini-label">BẮT ĐẦU TỪ ĐIỀU BẠN ĐANG CẦN</span><p><strong>Hiểu nghề</strong><span>Nhìn vào công việc thực tế</span></p><p><strong>Xây lộ trình</strong><span>Chọn bước tiếp theo có căn cứ</span></p><p><strong>Phát triển năng lực</strong><span>Thử làm, nhận góp ý và tiến bộ</span></p><small>Bạn có thể bắt đầu ở nơi phù hợp, không cần đi lần lượt.</small></aside></div></section>')
    if i in [1,3]:
        b=re.sub(r'(<h3>.*?</h3><p>.*?</p><p class="related">.*?</p>)',r'<article class="home-card">\1</article>',b,flags=re.S)
        first=b.index('<article');last=b.rindex('</article>')+len('</article>')
        b=b[:first]+'<div class="home-grid">'+b[first:last]+'</div>'+b[last:]
    if i==1:
        for title,id in [('Tôi là học sinh','hoc-sinh'),('Tôi là phụ huynh','phu-huynh'),('Tôi là sinh viên','sinh-vien')]:b=b.replace(f'<h3>{title}</h3>',f'<h3 id="{id}">{title}</h3>')
    if i==2:
        b=b.replace('<h2>','<span id="ve-du-an" class="home-anchor"></span><span class="section-index">NỀN TẢNG CHUYÊN MÔN</span><h2>',1)
    if i==3:
        b=re.sub(r'<p>Đồng hành lộ trình đang hoàn thiện\..*?</p>','<div class="home-availability">'+''.join(f'<p data-program-id="{p["id"]}"><strong>{esc(p["title"])}</strong><span>{esc(p["label"])}</span></p>'for p in programs)+'<p>DA là mô-đun đầu tiên đang chuẩn bị thí điểm. Bản đồ 25 nhóm nghề không đồng nghĩa có 25 mô-đun đang mở.</p></div>',b,flags=re.S)
    if i==4:
        b=re.sub(r'<div class="note">.*?</div>','',b,flags=re.S)
        marker='<p class="related"><a href="/hoat-dong/'
        pos=b.index(marker);b=b[:pos]+'<div class="event-pair"><article></article></div>'+b[pos:]
        pos=b.index('<h3>Bài viết để tự bắt đầu</h3>')
        b=b[:pos]+'<div class="home-reading" id="goc-nghe-nghiep"><h3>Bài viết để tự bắt đầu</h3><div class="home-grid home-articles">'+''.join(f'<article class="home-card" data-article-id="{ar["id"]}"><span class="mini-label">{esc(ar["theme"])}</span><h4>{a(ar["title"],ar["path"],"home-title-link")}</h4><p>{esc(ar["teaser"])}</p><p class="related">{a("Đọc bài →",ar["path"])}</p></article>'for ar in articles)+'</div><p class="related">'+a('Xem Góc nghề nghiệp','/goc-nghe-nghiep/')+'</p></div></div></section>'
        b=b.replace('<h3>Các buổi chia sẻ','<h3 class="home-events-title">Các buổi chia sẻ',1)
        b=b.replace('<div class="event-pair">','<div class="event-pair">',1)
        b=b.replace('<p class="related"><a href="/hoat-dong/','<p class="related">'+a('Xem Hoạt động','/hoat-dong/')+'<a href="/hoat-dong/',1)
    if i==5:
        b=b.replace('<h2>','<span id="ket-noi" class="home-anchor"></span><h2>',1)
        b=b.replace('<p><a href="mailto:','<p class="home-contact-links"><a href="mailto:',1)
    home.append(b)
target=D/'index.html';old=target.read_text()
target.write_text(re.sub(r'<main\b[^>]*>.*?</main>','<main id="noi-dung" class="home-page" tabindex="-1">'+''.join(home)+'</main>',old,flags=re.S))

privacy=(ROOT/'content/privacy.html').read_text().replace('<h3>','<h2>').replace('</h3>','</h2>')
shell=old.split('</head>',1)[0]
shell=re.sub(r'<title>.*?</title>','<title>Quyền riêng tư và dữ liệu bạn chủ động cung cấp | Nhìn Nghề</title>',shell)
shell=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="Thông tin về danh sách lưu trên thiết bị, liên hệ và đăng ký tại Nhìn Nghề.">',shell)
(D/'quyen-rieng-tu').mkdir(exist_ok=True)
(D/'quyen-rieng-tu/index.html').write_text(shell+'</head><body><main id="noi-dung" class="privacy-page" tabindex="-1"><div class="wrap privacy-width"><nav class="activity-crumb" aria-label="Đường dẫn">'+a('Trang chủ','/')+' / <span aria-current="page">Quyền riêng tư</span></nav><span class="eyebrow">THÔNG TIN DÙNG WEBSITE</span><h1>Quyền riêng tư và dữ liệu bạn chủ động cung cấp</h1><p class="privacy-intro">Nội dung dưới đây giải thích các chức năng hiện có của Nhìn Nghề và những thông tin bạn chủ động cung cấp khi liên hệ.</p>'+privacy+'</div></main></body></html>')
def navlinks(path):
    result=''
    for title,url in nav:
        current=' aria-current="page"'if path==url else ' aria-current="location"'if path.startswith(url)else ''
        result+=f'<a href="{url}"{current}>{esc(title)}</a>'
    return result
def header(path):
    logo='<a class="brand" href="/" aria-label="Nhìn Nghề — Trang chủ"><img src="/assets/logo.svg" width="222" height="52" alt="Nhìn Nghề"></a>'
    return '<header class="top"><div class="wrap bar">'+logo+'<nav class="desktop" aria-label="Điều hướng chính">'+navlinks(path)+'</nav><details class="mobile"><summary><span class="menu-label">Mở menu</span> <span aria-hidden="true">☰</span></summary><nav aria-label="Điều hướng trên điện thoại">'+navlinks(path)+'</nav></details></div></header>'
footer='<footer><div class="wrap footer-grid"><div class="footer-brand">'+a('Nhìn Nghề','/','footer-name')+f'<p>{esc(brand["tagline"])}</p><p>Định hướng và phát triển nghề nghiệp, trước hết trong lĩnh vực kinh tế và kinh doanh.</p><div class="brand-contact">'+''.join(a(e,'mailto:'+e,'footer-contact')for e in brand['emails'])+f'<a href="{esc(brand["facebook"],quote=True)}" target="_blank" rel="noopener noreferrer">Fanpage Nhìn Nghề <span aria-hidden="true">↗</span><span class="sr-only"> (mở thẻ mới)</span></a></div></div><div><span class="mini-label">KHÁM PHÁ</span>'+''.join(a(t,p,'footer-item')for t,p in nav)+'</div><div><span class="mini-label">HOẠT ĐỘNG VÀ ĐỒNG HÀNH</span>'+''.join(a(t,p,'footer-item')for t,p in [('Hoạt động','/hoat-dong/'),('Chia sẻ & Khám phá nghề','/hoat-dong/chia-se-nghe-nghiep/'),('Xây dựng lộ trình nghề nghiệp','/sinh-vien/lo-trinh/'),('Phát triển năng lực nghề nghiệp','/sinh-vien/phat-trien-nang-luc/')])+'</div></div><div class="wrap footer-bottom"><span>© 2026 Nhìn Nghề<br>Nền tảng nội dung: Career Playbook · TS Nguyễn Thị Hoa.</span>'+a('Quyền riêng tư và dữ liệu bạn chủ động cung cấp','/quyen-rieng-tu/','footer-privacy')+'</div></footer>'
notice=''
for page in D.rglob('index.html'):
    text=page.read_text()
    if 'http-equiv="refresh"'in text:continue
    path='/'+str(page.parent.relative_to(D)).strip('.')+'/'
    if path=='//':path='/'
    text=re.sub(r'<header class="top">.*?</header>','',text,flags=re.S)
    text=re.sub(r'<aside class="review-bar".*?</aside>|<div class="review-bar">.*?</div>','',text,flags=re.S)
    text=re.sub(r'<a class="skip".*?</a>','',text,flags=re.S)
    text=re.sub(r'<body([^>]*)>',lambda m:'<body'+m[1]+'>'+notice+'<a class="skip" href="#noi-dung">Đến nội dung chính</a>'+header(path),text,count=1)
    if '<footer>'in text:text=re.sub(r'<footer>.*?</footer>',lambda m:footer,text,flags=re.S)
    else:text=text.replace('</main>','</main>'+footer,1)
    text=re.sub(r'<dialog\b.*?</dialog>','',text,flags=re.S)
    if not re.search(r'<main[^>]*tabindex=',text):text=text.replace('<main ','<main tabindex="-1" ',1)
    text=re.sub(r'<link rel="stylesheet" href="/(?:site-common|home-refined)\.css">','',text)
    text=text.replace('</head>','<link rel="stylesheet" href="/site-common.css">'+('<link rel="stylesheet" href="/home-refined.css">'if path=='/'else '')+'</head>')
    if '/app.js'not in text:text=text.replace('</body>','<script src="/app.js"></script></body>')
    page.write_text(text)
(D/'site-public.json').write_text(json.dumps(site,ensure_ascii=False,indent=2)+'\n')
print('Rendered six homepage blocks, 5-item menu, common footer/notice and privacy page.')
