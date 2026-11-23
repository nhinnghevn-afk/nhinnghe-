"""Render the approved preview activities from one editorial event catalogue.

Run from any directory: python scripts/build-activities.py
Dates never advance a state. Publication is restricted to planned preview events
until organisation, consent and registration requirements are confirmed.
"""
from pathlib import Path
from html import escape as esc
import json,re

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
data=json.loads((ROOT/'content/activities.json').read_text())
copy=json.loads((ROOT/'content/activities-copy.json').read_text())
events=data['events']
series=data['series']
contact='<p class="event-contact">Liên hệ chung: <a href="mailto:nhinnghe.vn@gmail.com">nhinnghe.vn@gmail.com</a>. Việc gửi câu hỏi qua email không thay cho đăng ký tham gia.</p>'

def link(label,path,cls='text-link'):
    return f'<a class="{cls}" href="{esc(path,quote=True)}">{esc(label)}</a>'

def validate(e):
    assert e['status']=='planned', 'State change requires an editorial review and matching page/registration implementation.'
    assert not e['scheduleConfirmed'] and not e['startsAt'] and not e['endsAt']
    assert not e['registration']['enabled'] and not e['registration']['url']
    assert e['publicationScope']=='preview-only' and e['fee']['amount']==0
    assert not e['speakers'] and not e['format'] and not e['venue']

for e in events:validate(e)
assert len({e['id'] for e in events})==len(events)
assert len({e['path'] for e in events})==len(events)

def cards(level=3,compact=False):
    result=[]
    for e in events:
        if compact:
            result.append(f'<article class="journey-event" data-event-id="{e["id"]}" data-event-status="{e["status"]}"><div class="event-date"><span>PÉRIODE</span><strong>{esc(e["proposedWindow"])}</strong></div><div><span class="mini-label">DỰ KIẾN · ĐĂNG KÝ SẼ THÔNG BÁO SAU</span><h3>{esc(e["title"])}</h3><p>{esc(e["audience"])} · Miễn phí</p>{link("Xem nội dung buổi chia sẻ →",e["path"])}</div></article>'.replace('PÉRIODE','THỜI GIAN DỰ KIẾN'))
        else:
            result.append(f'<article class="event-list-card" data-event-id="{e["id"]}" data-event-status="{e["status"]}"><div class="event-card-date"><span>THỜI GIAN DỰ KIẾN</span><strong>{esc(e["proposedWindow"])}</strong><span>Miễn phí</span></div><div class="event-card-body"><p class="event-audience">{esc(e["audience"])}</p><h{level}>{link(e["title"],e["path"],"event-title-link")}</h{level}><p class="event-state">Dự kiến · Đăng ký sẽ thông báo sau</p><p>{esc(e["description"])}</p>{link("Xem nội dung buổi chia sẻ →",e["path"],"event-card-link")}</div></article>')
    return ''.join(result)

def crumb(trail):
    return '<nav class="activity-crumb" aria-label="Đường dẫn">'+ ' <span aria-hidden="true">/</span> '.join(link(t,p,'crumb-link') if p else '<span aria-current="page">'+esc(t)+'</span>' for t,p in trail)+'</nav>'

def section(id,title,body,wash=False):
    return f'<section class="events-section'+(' events-wash' if wash else '')+f'" id="{id}"><div class="wrap events-width"><h2>{esc(title)}</h2>{body}</div></section>'

def jump(items):
    return '<nav class="journey-jump" aria-label="Xem nhanh nội dung"><div class="wrap"><span>Xem nhanh</span>'+''.join(link(t,'#'+id) for t,id in items)+'</div></nav>'

def hero(title,eyebrow,lead,body,trail,summary=''):
    content='<div>'+f'<span class="eyebrow">{esc(eyebrow)}</span><h1>{esc(title)}</h1><p class="events-lead">{lead}</p>'+body+'</div>'
    return '<section class="events-hero"><div class="wrap events-width">'+crumb(trail)+(f'<div class="events-hero-grid">{content}{summary}</div>' if summary else content)+'</div></section>'

def write(path,title,description,main):
    target=DIST/path.lstrip('/')/'index.html'
    old=target.read_text()
    head=old.split('</head>',1)[0]
    head=re.sub(r'<title>.*?</title>',f'<title>{esc(title)} | Nhìn Nghề</title>',head)
    head=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{esc(description,quote=True)}">',head)
    if '/events-refined.css' not in head:head+='<link rel="stylesheet" href="/events-refined.css">'
    header=re.search(r'<body>(.*?)<main',old,re.S).group(1)
    tail=old.split('</main>',1)[1]
    tail=re.sub(r'<script>.*?</script>','',tail,flags=re.S)
    target.write_text(head+'</head><body>'+header+'<main id="noi-dung" class="events-page">'+main+'</main>'+tail)

def split_copy(key):
    body=copy[key].strip()
    question=re.search(r'<p class="question">(.*?)</p>',body,re.S).group(1)
    body=re.sub(r'<p class="question">.*?</p>','',body,count=1,flags=re.S)
    intro,rest=body.split('<h3>',1)
    parts=re.split(r'<h3>(.*?)</h3>','<h3>'+rest,flags=re.S)
    return question,intro,[(parts[i],parts[i+1])for i in range(1,len(parts),2)]

q,intro,parts=split_copy('hoat-dong')
main=hero(q,'HOẠT ĐỘNG CÙNG NHÌN NGHỀ',re.sub(r'^\s*<p>|</p>\s*$','',intro.strip()),'',[('Trang chủ','/'),('Hoạt động',None)])
main+=jump([('Các buổi dự kiến','lich'),('Hoạt động đã diễn ra','da-dien-ra'),('Tự tìm hiểu thêm','ba-huong')])
for i,(title,body) in enumerate(parts):
    if i==0:
        # Keep the series link after the shared event cards.
        related=re.search(r'<p class="related">.*?</p>',body,re.S).group(0)
        body=body.replace(related,'')+'<div class="event-list">'+cards()+'</div>'+related
    main+=section(['lich','da-dien-ra','ba-huong'][i],title,body,i==1)
write('/hoat-dong/','Hoạt động cùng Nhìn Nghề','Chọn buổi chia sẻ phù hợp; xem nội dung và trạng thái của từng hoạt động.',main)

q,intro,parts=split_copy('chuoi')
main=hero(series['title'],'CHUỖI CHIA SẺ MIỄN PHÍ',q,intro,[('Trang chủ','/'),('Hoạt động','/hoat-dong/'),(series['title'],None)])
main+=jump([('Chọn buổi','lich-chia-se'),('Điều nhận được','dieu-nhan-duoc'),('Cách tham gia','cach-tham-gia'),('Câu hỏi thường gặp','cau-hoi')])
for i,(title,body) in enumerate(parts):
    if i==0:
        at=body.index('<p>Buổi dành cho các nhóm sinh viên')
        body=body[:at]+'<div class="event-list">'+cards()+'</div>'+body[at:]
    if i==3:
        matches=list(re.finditer(r'<p><strong>(.*?)</strong><br>(.*?)</p>',body,re.S))
        for m in reversed(matches):
            body=body[:m.start()]+f'<details class="events-faq"><summary>{m[1]}</summary><p>{m[2]}</p></details>'+body[m.end():]
    main+=section(['lich-chia-se','dieu-nhan-duoc','cach-tham-gia','cau-hoi'][i],title,body,i in [1,3])
write(series['path'],series['title'],'Chuỗi chia sẻ miễn phí dành cho học sinh, phụ huynh và sinh viên trong kinh tế và kinh doanh.',main)

for e in events:
    summary=f'<aside class="events-summary" aria-label="Thông tin buổi chia sẻ"><h2>Thông tin dự kiến</h2><dl><dt>Đối tượng</dt><dd>{esc(e["audience"])}</dd><dt>Thời gian dự kiến</dt><dd>{esc(e["proposedWindow"])}</dd><dt>Ngày, giờ và thời lượng</dt><dd>Sẽ thông báo</dd><dt>Hình thức và người chia sẻ</dt><dd>Sẽ thông báo</dd><dt>Phí tham gia</dt><dd>Miễn phí</dd></dl></aside>'
    status='<p class="event-state">Dự kiến · Đăng ký sẽ thông báo sau</p>'
    body=status+f'<p>Dành cho {esc(e["audience"].lower())} quan tâm lĩnh vực kinh tế và kinh doanh.</p>'+link('Xem nội dung buổi chia sẻ','#noi-dung-de-xuat','btn primary')
    trail=[('Trang chủ','/'),('Hoạt động','/hoat-dong/'),(series['title'],series['path']),(e['title'],None)]
    main=hero(e['title'],'BUỔI CHIA SẺ MIỄN PHÍ',esc(e['description']),body,trail,summary)
    main+=jump([('Nội dung chính','noi-dung-de-xuat'),('Kết quả hướng tới','ket-qua'),('Chuẩn bị trước','chuan-bi'),('Thông tin tham gia','tham-gia')])
    topics='<ol class="events-topics">'+''.join(f'<li><h3>{esc(t)}</h3><p>{esc(v)}</p></li>' for t,v in e['topics'])+'</ol>'
    main+=section('noi-dung-de-xuat','Nội dung chính',topics)
    result=f'<p>{esc(e["intendedTakeaway"])}</p><blockquote><span>Ví dụ giả định về câu hỏi hoặc việc tiếp theo</span><p>{esc(e["example"])}</p></blockquote><p class="events-caveat">Đây là định hướng nội dung, không phải kết quả đã ghi nhận từ người tham gia hoặc cam kết giúp học sinh chốt một nghề, ngành.</p>'
    main+=section('ket-qua','Kết quả hướng tới',result,True)
    main+=section('chuan-bi','Bạn có thể chuẩn bị trước',f'<p>{esc(e["preparation"])}</p>')
    main+=section('tham-gia','Thông tin tham gia','<div class="events-registration-note"><strong>Thông tin đăng ký sẽ được thông báo khi có lịch chính thức.</strong><p>Khi lịch và cách tổ chức được xác nhận, trang này sẽ nêu cách tham gia, cách nhận xác nhận và việc cần chuẩn bị. Đăng ký buổi này không tự đăng ký buổi khác.</p><p>Phụ huynh có thể tìm hiểu cùng con; cách đăng ký và hình thức tham gia sẽ được hướng dẫn cụ thể trước khi mở tiếp nhận.</p></div>',True)
    main+=section('trong-luc-cho','Trong thời gian chờ','<p class="related">'+link(e['nextRead'][1],e['nextRead'][0])+link('Xem các buổi khác trong chuỗi',series['path'])+'</p>'+contact)
    write(e['path'],e['title'],'Buổi chia sẻ miễn phí dành cho '+e['audience'].lower()+'.',main)

# Update only homepage event teasers; its full redesign remains a later step.
home=DIST/'index.html'
t=home.read_text()
t,n=re.subn(r'<div class="event-pair">.*?</article></div>',lambda m:'<div class="event-pair">'+cards(compact=True)+'</div>',t,count=1,flags=re.S)
assert n==1,'Expected the existing homepage event pair.'
t=t.replace('Lịch minh họa theo kế hoạch dự kiến. Ngày, giờ, hình thức chưa công bố; chưa mở đăng ký.','Hai đề xuất chưa xác nhận tổ chức; ngày, giờ, hình thức và người chia sẻ chưa công bố. Chưa mở đăng ký.')
home.write_text(t)

# Keep the old shared link working without publishing a third sample event.
old=DIST/'hoat-dong/hieu-nghe/index.html'
old.write_text('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=/hoat-dong/chia-se-nghe-nghiep/"><title>Chia sẻ &amp; Khám phá nghề | Nhìn Nghề</title></head><body><h1>Chia sẻ &amp; Khám phá nghề</h1><p>Nội dung hiện được quản lý tại trang chuỗi chia sẻ.</p><a href="/hoat-dong/chia-se-nghe-nghiep/">Đến trang chuỗi chia sẻ</a></body></html>')

keys=['id','path','title','audience','proposedWindow','description','topics','intendedTakeaway','preparation','example','nextRead','seriesId','status','statusLabel','scheduleConfirmed','startsAt','endsAt','timezone','format','venue','speakers','fee','registration','publicationScope','resources','recap','lastEditorialDate']
public={'edition':'activities-public-preview-v1','series':series,'events':[{k:e[k] for k in keys}for e in events]}
(DIST/'events-public.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
print('Rendered activity hub, series, 2 planned event pages, legacy redirect and shared homepage teasers. Registration remains disabled.')
