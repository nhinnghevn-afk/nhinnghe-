(()=>{
'use strict';
const root=document.getElementById('public-school');if(!root)return;
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fold=v=>String(v).toLocaleLowerCase('vi').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d');
const KEY='nhinnghe-discovery-v1',NOTE_LIMIT=300,MAX=3;
const kinds=['careers','majors','schools'],labels={careers:'Hướng nghề',majors:'Ngành học',schools:'Trường để tìm hiểu'};
const selected=Object.fromEntries(kinds.map(k=>[k,Object.create(null)]));
let data,programData,programId=null,careerId=null,majorId=null,majorLimit=8,storageOK=false;
const find=(k,id)=>data[k].find(x=>x.id===id);
const has=(k,id)=>Object.hasOwn(selected[k],id);
const count=()=>kinds.reduce((n,k)=>n+Object.keys(selected[k]).length,0);
function announce(s){$('public-status').textContent=s;$('public-shortlist-status').textContent=s;}
function jump(id,focus=false){const el=$(id);if(!el)return;if(focus)el.focus({preventScroll:true});el.scrollIntoView({behavior:'instant',block:'start'});}
function storageNotice(){
 $('public-storage-notice').textContent=storageOK?'Danh sách và ghi chú được lưu trên trình duyệt này, không gửi về Nhìn Nghề. Không đồng bộ sang thiết bị khác; có thể mất khi xóa dữ liệu trình duyệt. Dùng “Xóa danh sách” để xóa toàn bộ.':'Trình duyệt chưa cho lưu danh sách. Các mục và ghi chú chỉ giữ tạm trong phiên này; có thể mất khi tải lại hoặc rời trang. Hãy in/lưu PDF trước khi đóng.';
}
function persist(){
 if(!storageOK)return;
 try{localStorage.setItem(KEY,JSON.stringify({version:1,selected}));}
 catch{storageOK=false;storageNotice();announce('Chưa lưu được thay đổi trên thiết bị. Danh sách đang giữ tạm trong phiên này; hãy in/lưu PDF trước khi đóng.');}
}
function restore(){
 try{
  const raw=localStorage.getItem(KEY);
  localStorage.setItem(KEY+'.probe','1');localStorage.removeItem(KEY+'.probe');storageOK=true;
  if(raw){
   const saved=JSON.parse(raw);
   if(saved&&saved.version===1&&saved.selected&&typeof saved.selected==='object'){
    for(const k of kinds){const group=saved.selected[k];if(!group||typeof group!=='object'||Array.isArray(group))continue;
     for(const [id,note] of Object.entries(group)){if(Object.keys(selected[k]).length>=MAX)break;if(find(k,id)&&typeof note==='string')selected[k][id]=note.slice(0,NOTE_LIMIT);}
    }
   }
  }
 }catch(err){
  if(err instanceof SyntaxError){storageOK=true;announce('Bản lưu cũ không đọc được. Bạn có thể tạo lại danh sách.');}
  else storageOK=false;
 }
 storageNotice();
}
function saveButton(k,id){const on=has(k,id),name=find(k,id).name;return `<button type="button" class="public-save" data-save-kind="${k}" data-save-id="${id}" aria-pressed="${on}" aria-label="${on?'Bỏ khỏi danh sách':'Lưu để tìm hiểu'}: ${esc(name)}">${on?'Đã lưu ✓':'Lưu để tìm hiểu +'}</button>`;}
function renderBlocks(){
 const opened=new Set(Array.from(root.querySelectorAll('.public-block[open]')).map(x=>x.dataset.block));
 if(careerId)opened.add(String(find('careers',careerId).block));
 $('public-blocks').innerHTML=data.blocks.map(b=>`<details class="public-block" data-block="${b.id}" ${opened.has(String(b.id))?'open':''}><summary><span>${String(b.id).padStart(2,'0')}</span><b>${esc(b.name)}</b></summary><div>${data.careers.filter(c=>c.block===b.id).map(c=>`<button type="button" class="public-career-choice" data-career="${c.id}" aria-pressed="${c.id===careerId}"><span>${c.id}</span>${esc(c.name)}</button>`).join('')}</div></details>`).join('');
}
function renderCareer(){
 if(!careerId)return;
 const c=find('careers',careerId),b=data.blocks.find(x=>x.id===c.block);
 $('public-career-detail').classList.remove('school-empty');
 $('public-career-detail').innerHTML=`<span class="public-selected-label">ĐANG XEM · KHỐI ${c.block} · ${esc(b.name)}</span><p class="career-profile-label">${c.profileKind==='sample'?'Hồ sơ mẫu · có bài đọc chuyên sâu':'Hồ sơ khám phá nghề'}</p><h3>${c.id} · ${esc(c.name)}</h3><p class="public-career-summary">${esc(c.summary)}</p><h4>Kết quả tiêu biểu</h4><p>${esc(c.output)}</p><h4>Một số vị trí minh họa</h4><ul>${c.roles.map(r=>`<li>${esc(r)}</li>`).join('')}</ul><h4>Nền tảng nên tìm hiểu</h4><p>${esc(c.foundation)}</p><div class="public-try"><b>Một việc nhỏ để khám phá</b><p>${esc(c.tryTask)}</p><p class="try-output"><strong>Kết quả giữ lại:</strong> ${esc(c.tryResult)}</p><p class="try-prep"><strong>Mức chuẩn bị:</strong> ${esc(c.tryPreparation)}</p></div><h4>Có thể bắt đầu tìm hiểu những ngành nào?</h4><p class="tiny">Các ngành tiêu biểu dưới đây giúp bạn bắt đầu. Hãy đọc học phần, thực hành và chuẩn đầu ra của chương trình cụ thể để hiểu nền tảng được đào tạo.</p><div class="public-hints">${c.majorHints.map(h=>`<div><button type="button" class="public-link-button" data-major="${h.major}" data-major-origin="hint">${esc(find('majors',h.major).name)} →</button><p>${esc(h.reason)}</p></div>`).join('')}</div><div class="career-profile-next">${c.sampleUrl?`<a class="text-link" href="${esc(c.sampleUrl)}">Đọc hồ sơ mẫu chuyên sâu: công việc, ba mức nền tảng và bước chuẩn bị →</a>`:'<a class="text-link" href="/hoc-sinh/ho-so-mau/quan-ly-du-an-van-hanh/">Xem cách đọc ba mức nền tảng qua hồ sơ mẫu →</a>'}<p>Bạn đang cân nhắc giữa những ngành học này? Nhìn Nghề có thể cùng gia đình so sánh chương trình, nền tảng học tập và điều kiện thực tế để cân nhắc lựa chọn và xây bước chuẩn bị.</p><a class="text-link" href="#dong-hanh-gia-dinh">Tìm hiểu hình thức đồng hành ↓</a></div>${saveButton('careers',c.id)}<p class="public-save-note">Tối đa ba hướng nghề. Thêm lý do hoặc câu hỏi tại Danh sách của bạn; ${storageOK?'lưu trên trình duyệt này':'hiện chỉ giữ tạm trong phiên'}.</p><p class="tiny public-source">Nguồn: ${esc(c.source)}</p>`;
 root.querySelectorAll('.public-career-choice').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.career===careerId)));
}
function majorMatches(){const q=fold($('public-major-search').value.trim());return data.majors.filter(m=>!q||fold(m.name).includes(q)||m.id.includes(q));}
function schoolContext(){
 const id=majorId||programData.clusterMajor;
 $('public-school-context').textContent=id===programData.clusterMajor?'Đang hiển thị: chương trình Quản trị kinh doanh và các chương trình kinh doanh liên quan.':'Bạn đang xem ngành '+find('majors',id).name+'. Trang hiện chưa giới thiệu chương trình cụ thể cho ngành này. Bạn có thể mở cổng thông tin trường bên dưới để tìm hiểu thêm.';
 renderSchools();
}
function clearMajor(){majorId=null;$('public-major-detail').classList.add('school-empty');$('public-major-detail').innerHTML='<h3>Chọn một ngành trong kết quả tìm kiếm</h3><p>Phần chi tiết sẽ hiển thị trọng tâm và câu hỏi cần đối chiếu chương trình.</p>';schoolContext();}
function renderMajors(){
 const matches=majorMatches();
 if(majorId&&!matches.some(m=>m.id===majorId))clearMajor();
 $('public-major-results').innerHTML=`<p class="tiny">${matches.length} ngành trong danh mục chọn lọc.</p>`+matches.slice(0,majorLimit).map(m=>`<button type="button" class="public-major-choice" data-major="${m.id}" aria-pressed="${m.id===majorId}"><span>${esc(m.name)}</span><small>${m.id}</small></button>`).join('')+(matches.length>majorLimit?'<button type="button" class="public-more" data-more="majors">Xem thêm ngành ↓</button>':'')+(!matches.length?'<p>Chưa có kết quả. Thử tên ngắn hơn hoặc mã ngành.</p>':'');
}
function renderMajor(){
 if(!majorId)return;
 const m=find('majors',majorId),examples=data.careers.filter(c=>c.majorHints.some(h=>h.major===majorId));
 $('public-major-detail').classList.remove('school-empty');
 $('public-major-detail').innerHTML=`<span class="public-selected-label">ĐANG XEM · MÃ NGÀNH ${m.id}</span><h3>${esc(m.name)}</h3><p>${esc(m.overview)}</p><div class="public-try"><b>Câu hỏi khi đọc chương trình</b><p>${esc(m.programQuestion)}</p></div><h4>Gợi mở để tìm hiểu công việc</h4>${examples.length?'<p>Một số hướng được chọn để minh họa:</p><div class="public-related">'+examples.slice(0,3).map(c=>`<button type="button" class="public-link-button" data-career="${c.id}">${esc(c.name)} ↑</button>`).join('')+'</div>':'<p>Chưa có ví dụ nghề–ngành được giới thiệu cho ngành này trên trang. Không có ví dụ ở đây không có nghĩa ngành không liên quan tới một hướng nghề.</p>'}<p class="tiny">${esc(m.source)}</p><div class="public-detail-actions">${saveButton('majors',m.id)}<button type="button" class="public-link-button" data-jump="truong">Xem chương trình và cách xét tuyển ↓</button></div><p class="public-save-note">Tối đa ba ngành; ghi chú tại Danh sách của bạn. Chương trình có nguồn và năm riêng tại phần Học ở đâu; danh sách lưu vẫn giữ từng nhóm độc lập.</p>`;
 renderMajors();schoolContext();
}
function visiblePrograms(){
 const q=fold($('public-school-search').value.trim()),region=$('public-school-region').value;
 if(majorId&&majorId!==programData.clusterMajor)return [];
 return programData.programs.filter(p=>{const school=programData.schools.find(s=>s.id===p.school);return (!region||school.regions.includes(region))&&(!q||fold(school.name+' '+school.id+' '+p.name+' '+p.code).includes(q));});
}
function renderAdmission(){
 const el=$('public-admission-detail'),p=programData.programs.find(p=>p.id===programId);
 el.classList.toggle('school-empty',!p);
 if(!p){el.innerHTML='<h3>Bạn muốn xem cách xét tuyển của chương trình nào?</h3><p>Chọn “Xem cách xét tuyển” ở phần Học ở đâu để đọc phương thức, điều kiện chính và nguồn tương ứng.</p><a class="text-link" href="#truong">Chọn trường và chương trình ↑</a>';return;}
 const school=programData.schools.find(s=>s.id===p.school),policy=programData.policies[p.school];
 el.innerHTML=`<span class="public-selected-label">ĐANG XEM · ${esc(school.id)} · ${esc(p.code)}</span><h3>${esc(p.name)}</h3><p class="admission-school">${esc(school.name)}</p><p class="program-year">${esc(policy.yearLabel)}</p><p>${esc(policy.intro)}</p><ul class="admission-methods">${policy.methods.map(m=>`<li>${esc(m)}</li>`).join('')}</ul><p class="public-note">${esc(policy.check)}</p><p>${esc(p.note)}</p><div class="admission-source"><a class="public-official" href="${esc(p.source)}" target="_blank" rel="noopener noreferrer">Đọc thông tin chính thức của ${esc(school.id)} ↗<span class="sr-only"> (mở thẻ mới)</span></a><p class="tiny">${esc(policy.locator)} · Đối chiếu ngày ${esc(programData.checked)}.</p></div><p class="tiny">Thông tin cơ bản giúp tự tìm hiểu, chưa phải đánh giá phù hợp hay kết luận khả năng trúng tuyển.</p><button type="button" class="public-link-button" data-jump="program-${esc(p.id)}">Quay lại chương trình đã chọn ↑</button>`;
}
function renderSchools(){
 const list=visiblePrograms(),covered=!majorId||majorId===programData.clusterMajor;
 if(!list.some(p=>p.id===programId))programId=null;
 $('public-program-count').textContent=covered?`${list.length}/10 chương trình khớp điều kiện tìm. Bạn có thể mở cổng thông tin trường để tìm thêm lựa chọn.`:'Trang hiện chưa giới thiệu chương trình cụ thể cho ngành đang xem.';
 $('public-school-results').innerHTML=list.length?programData.schools.filter(s=>list.some(p=>p.school===s.id)).map(school=>`<article class="public-school-card program-school"><div class="public-school-meta"><span>${esc(school.label)}</span><small>${esc(school.id)}</small></div><h3>${esc(school.name)}</h3><p class="tiny">${esc(school.location)}</p><p class="program-year">${esc(programData.policies[school.id].yearLabel)}</p><div class="school-program-list">${list.filter(p=>p.school===school.id).map(p=>`<article id="program-${p.id}" class="program-choice" tabindex="-1"><span class="program-relation">${esc(p.relation)}</span><h4>${esc(p.name)}</h4><p class="program-code">Mã ${esc(p.code)}</p><button type="button" class="program-admission-button" data-program="${p.id}" aria-controls="public-admission-detail" aria-pressed="${p.id===programId}" aria-label="Xem cách xét tuyển: ${esc(p.name)}, ${esc(school.id)}, mã ${esc(p.code)}">${p.id===programId?'Đang xem xét tuyển ✓':'Xem cách xét tuyển ↓'}</button></article>`).join('')}</div>${saveButton('schools',school.id)}<p class="public-save-note">Lưu tên trường để tìm hiểu; ghi thêm mã chương trình và năm nguồn trong ghi chú.</p></article>`).join(''):covered?'<div class="public-note"><p>Không có chương trình khớp bộ lọc trong danh mục hiện có. Thử tên ngắn hơn hoặc bỏ điều kiện vùng.</p><button type="button" class="public-link-button" data-clear-program-filters>Đặt lại bộ lọc</button></div>':'<div class="public-note"><p>Bạn có thể xem các chương trình Quản trị kinh doanh và một số chương trình kinh doanh liên quan đang được giới thiệu trên trang. Các ngành khác sẽ được bổ sung tiếp.</p><button type="button" class="public-link-button" data-major="7340101" data-major-origin="hint">Xem các chương trình Quản trị kinh doanh</button></div>';
 renderAdmission();
}
function renderSchoolDirectory(){
 $('public-school-directory').innerHTML=data.schools.filter(s=>['NEU','UEH','UEL'].includes(s.id)).map(s=>`<div><h4>${esc(s.name)}</h4><a class="public-official" href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">Mở cổng thông tin ${esc(s.id)} ↗<span class="sr-only"> (mở thẻ mới)</span></a><p class="tiny">Chỉ là liên kết tra cứu thêm; không xác nhận tuyển sinh cho ngành đang xem.</p>${saveButton('schools',s.id)}</div>`).join('');
}
function updateSaveButtons(){
 root.querySelectorAll('[data-save-kind]').forEach(b=>{const k=b.dataset.saveKind,id=b.dataset.saveId,on=has(k,id);b.setAttribute('aria-pressed',String(on));b.textContent=on?'Đã lưu ✓':'Lưu để tìm hiểu +';b.setAttribute('aria-label',(on?'Bỏ khỏi danh sách: ':'Lưu để tìm hiểu: ')+find(k,id).name);});
}
function renderShortlist(){
 $('public-shortlist').innerHTML=kinds.map(k=>`<div><h3>${labels[k]} <small>${Object.keys(selected[k]).length}/3</small></h3>${Object.keys(selected[k]).length?'<ul>'+Object.entries(selected[k]).map(([id,note])=>{const x=find(k,id),noteId='note-'+k+'-'+id;return `<li><div class="shortlist-item-head"><strong>${esc(x.name)}</strong><button type="button" class="public-remove" data-remove-kind="${k}" data-remove-id="${id}" aria-label="Bỏ ${esc(x.name)}">Bỏ</button></div>${k==='schools'?`<a class="shortlist-source" href="${esc(x.url)}" target="_blank" rel="noopener noreferrer">${esc(x.url)}</a>`:k==='majors'?`<span class="shortlist-source">Mã ngành ${id}</span>`:`<span class="shortlist-source">Nhóm nghề ${id} · Career Playbook</span>`}<label class="shortlist-note-label" for="${noteId}">Lý do quan tâm hoặc câu hỏi</label><textarea id="${noteId}" class="shortlist-note" data-note-kind="${k}" data-note-id="${id}" maxlength="300" aria-label="Ghi chú: ${esc(x.name)}" placeholder="Ví dụ: Mình muốn tìm hiểu thêm điều gì?">${esc(note)}</textarea><p class="note-print" id="print-${noteId}">${esc(note||'Chưa ghi câu hỏi.')}</p></li>`;}).join('')+'</ul>':'<p class="tiny">Chưa lưu mục nào. Chọn mục quan tâm rồi dùng “Lưu để tìm hiểu”.</p>'}</div>`).join('');
 $('public-total').textContent=String(count());$('public-clear').disabled=count()===0;$('public-print').disabled=count()===0;updateSaveButtons();
}
function changeSave(k,id){
 if(has(k,id)){delete selected[k][id];announce('Đã bỏ '+find(k,id).name+' khỏi danh sách.');}
 else if(Object.keys(selected[k]).length>=MAX){announce('Bạn đã lưu ba mục trong nhóm này. Hãy bỏ một mục trong danh sách nếu muốn thay đổi.');jump('danh-sach');return;}
 else{selected[k][id]='';announce('Đã lưu '+find(k,id).name+' để tìm hiểu. Bạn có thể thêm ghi chú tại Danh sách của bạn.');}
 persist();renderShortlist();
}
function revealHash(){
 try{const id=decodeURIComponent(location.hash.slice(1));const el=id&&$(id);if(!el)return;let d=el.closest('details');while(d){d.open=true;d=d.parentElement.closest('details');}el.scrollIntoView({behavior:'instant',block:'start'});}catch{}
}
root.addEventListener('click',e=>{
 const program=e.target.closest('[data-program]');if(program&&visiblePrograms().some(p=>p.id===program.dataset.program)){programId=program.dataset.program;renderSchools();const p=programData.programs.find(p=>p.id===programId);announce('Đang xem cách xét tuyển: '+p.name+', '+p.school+', mã '+p.code+'.');jump('public-admission-detail',true);return;}
 if(e.target.closest('[data-clear-program-filters]')){$('public-school-search').value='';$('public-school-region').value='';renderSchools();announce('Đã đặt lại bộ lọc trường và chương trình.');jump('truong');return;}

 const c=e.target.closest('[data-career]');if(c&&find('careers',c.dataset.career)){careerId=c.dataset.career;renderBlocks();renderCareer();announce('Đang xem nhóm nghề '+find('careers',careerId).name+'.');jump('public-career-detail',true);return;}
 const m=e.target.closest('[data-major]');if(m&&find('majors',m.dataset.major)){majorId=m.dataset.major;programId=null;$('public-school-search').value='';$('public-school-region').value='';if(m.dataset.majorOrigin==='hint'){$('public-major-search').value=find('majors',majorId).name;majorLimit=8;}renderMajor();announce('Đang xem ngành '+find('majors',majorId).name+'.');jump('public-major-detail',true);return;}
 const save=e.target.closest('[data-save-kind]');if(save){changeSave(save.dataset.saveKind,save.dataset.saveId);return;}
 const remove=e.target.closest('[data-remove-kind]');if(remove){changeSave(remove.dataset.removeKind,remove.dataset.removeId);return;}
 if(e.target.closest('[data-more]')){majorLimit+=8;renderMajors();return;}
 const j=e.target.closest('[data-jump]');if(j)jump(j.dataset.jump,j.dataset.jump.startsWith('program-'));
});
root.addEventListener('input',e=>{
 const el=e.target;if(!el.matches('[data-note-kind]'))return;
 const k=el.dataset.noteKind,id=el.dataset.noteId;if(!has(k,id))return;
 selected[k][id]=el.value.slice(0,NOTE_LIMIT);$('print-'+el.id).textContent=selected[k][id]||'Chưa ghi câu hỏi.';persist();
});
$('public-major-search').addEventListener('input',()=>{if(!data)return;majorLimit=8;renderMajors();});
$('public-school-search').addEventListener('input',()=>{if(data)renderSchools();});
$('public-school-region').addEventListener('change',()=>{if(data)renderSchools();});
function printDate(){$('public-print-date').textContent='Nhìn Nghề · Danh sách tìm hiểu · Ngày in '+new Date().toLocaleDateString('vi-VN');}
$('public-print').addEventListener('click',()=>{printDate();window.print();});window.addEventListener('beforeprint',printDate);
$('public-clear').addEventListener('click',()=>{$('public-clear-confirm').hidden=false;$('public-keep').focus();});
$('public-keep').addEventListener('click',()=>{$('public-clear-confirm').hidden=true;$('public-clear').focus();});
$('public-confirm-clear').addEventListener('click',()=>{
 for(const k of kinds)for(const id of Object.keys(selected[k]))delete selected[k][id];
 let removed=true;try{localStorage.removeItem(KEY);}catch{removed=false;}
 $('public-clear-confirm').hidden=true;renderShortlist();jump('danh-sach',true);announce(removed?'Đã xóa toàn bộ danh sách và ghi chú trên trình duyệt này.':'Đã xóa khỏi phiên này, nhưng trình duyệt chưa cho xóa bản lưu trên thiết bị. Nếu đã có bản lưu trước đó, hãy xóa dữ liệu trang trong trình duyệt để xóa hẳn.');
});
window.addEventListener('hashchange',revealHash);
async function load(){
 try{
  const responses=await Promise.all([fetch('/school-public-data.json'),fetch('/school-programs.json')]);if(responses.some(r=>!r.ok))throw Error('load');[data,programData]=await Promise.all(responses.map(r=>r.json()));
  if(data.careers.length!==25||data.majors.length!==57)throw Error('data');
  restore();const careerParam=new URLSearchParams(location.search).get('nghe');if(careerParam&&find('careers',careerParam))careerId=careerParam;renderBlocks();if(careerId)renderCareer();renderMajors();const initial=new URLSearchParams(location.search).get('nganh');if(initial&&find('majors',initial)){majorId=initial;$('public-major-search').value=find('majors',initial).name;renderMajor();}else schoolContext();renderSchoolDirectory();renderShortlist();$('public-load-state').hidden=true;revealHash();
 }catch{$('public-load-state').hidden=false;$('public-load-state').innerHTML='Chưa tải được nội dung. <button type="button" id="public-retry">Thử lại</button>';$('public-retry').addEventListener('click',load);}
}
load();
})();
