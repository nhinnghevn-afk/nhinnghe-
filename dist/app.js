(()=>{
 'use strict';
 const routes={school:'/hoc-sinh/',student:'/sinh-vien/',path:'/sinh-vien/lo-trinh/',da:'/sinh-vien/phan-tich-du-lieu/',work:'/goc-nghe-nghiep/nhin-nghe-tu-cong-viec/',evidence:'/goc-nghe-nghiep/minh-chung-tien-bo/',privacy:'/quyen-rieng-tu/'};
 document.addEventListener('click',e=>{const b=e.target.closest('[data-dialog]');if(b&&routes[b.dataset.dialog])location.assign(routes[b.dataset.dialog]);});
 const menu=document.querySelector('details.mobile');
 if(menu){
  const summary=menu.querySelector('summary'),label=summary.querySelector('.menu-label');
  const update=()=>{if(label)label.textContent=menu.open?'Đóng menu':'Mở menu';};
  menu.addEventListener('toggle',update);update();
  menu.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>{menu.open=false;update();}));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.open){menu.open=false;update();summary.focus();}});
 }
})();
