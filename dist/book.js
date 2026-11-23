const careerBlocks=[...document.querySelectorAll('.career-block')];
document.getElementById('expand-groups').addEventListener('click',()=>careerBlocks.forEach(block=>block.open=true));
document.getElementById('collapse-groups').addEventListener('click',()=>careerBlocks.forEach(block=>block.open=false));
