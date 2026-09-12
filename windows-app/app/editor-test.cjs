// Exercises the actual editor DOM in Electron, including in packaged Windows builds.
const {BrowserWindow,ipcMain}=require('electron');
const path=require('node:path');
async function editorTest(){
 const sample='Dear Princess Celestia: Colors.\nToday I learned:\n    I said "P.S. (42) <hello>".\n    I did this 3 times:\n        I wrote "Hello".\n    That\'s what I did.\nYour faithful student, Twilight Sparkle.\nPSS End comment';
 const state={docs:[{id:1,name:'Syntax test',text:sample,dirty:false}],active:1,dark:false,catalog:[],guide:'about:blank'};
 const win=new BrowserWindow({show:false,width:1000,height:750,webPreferences:{preload:path.join(__dirname,'preload.cjs'),sandbox:true,contextIsolation:true,nodeIntegration:false}});
 ipcMain.handle('studio',(event,name,arg)=>{if(event.sender!==win.webContents)throw Error('Unexpected editor test caller');if(name==='init')return state;if(name==='update'){state.docs[0].text=arg.text;return true;}throw Error('Unexpected editor test action '+name);});
 try{
 await win.loadFile(path.join(__dirname,'index.html'));
 return await win.webContents.executeJavaScript(`(async()=>{
 const assert=(ok,message)=>{if(!ok)throw Error(message);};
 for(let i=0;i<100&&!document.querySelector('.source');i++)await new Promise(r=>setTimeout(r,20));
 const area=document.querySelector('.source'),paint=document.querySelector('.syntax-paint');
 assert(area&&paint,'Editor and coloring layer loaded');
 const original=area.value;
 assert(paint.textContent===original+'\\n','Coloring preserves source exactly');
 assert(paint.querySelectorAll('.syntax-keyword').length>=6,'Keywords have color spans');
 assert(paint.querySelector('.syntax-string').textContent==='"P.S. (42) <hello>"','String protects comment markers and HTML');
 assert(paint.querySelector('.syntax-comment').textContent==='PSS End comment','Postscript colored');
 for(const theme of ['light','dark']){
 document.body.dataset.theme=theme;
 const base=getComputedStyle(paint).color;
 for(const kind of ['keyword','string','comment','number'])assert(getComputedStyle(paint.querySelector('.syntax-'+kind)).color!==base,theme+' '+kind+' differs from plain text');
 assert(getComputedStyle(area).caretColor!=='rgba(0, 0, 0, 0)',theme+' caret visible');
 }
 for(const size of [10,14,24,32]){
 document.documentElement.style.setProperty('--font-size',size+'px');
 const a=getComputedStyle(area),p=getComputedStyle(paint);
 for(const prop of ['fontFamily','fontSize','lineHeight','paddingTop','paddingLeft','whiteSpace','tabSize'])assert(a[prop]===p[prop],'Matching '+prop);
 assert(area.clientWidth===paint.clientWidth&&area.clientHeight===paint.clientHeight,'Matching viewport');
 }
 area.focus();area.setSelectionRange(area.value.length,area.value.length);
 document.execCommand('insertText',false,'\\nI said 12.');
 assert(paint.textContent===area.value+'\\n','Typing refreshes colors');
 document.execCommand('undo');assert(area.value===original,'Native undo preserved');
 document.execCommand('redo');assert(area.value.endsWith('I said 12.'),'Native redo preserved');
 area.value=('I said '+ 'long '.repeat(100)+'12.\\n').repeat(100);area.dispatchEvent(new Event('input'));
 area.scrollTop=400;area.scrollLeft=300;area.dispatchEvent(new Event('scroll'));
 assert(paint.scrollTop===area.scrollTop&&paint.scrollLeft===area.scrollLeft,'Two-axis scrolling synchronized');
 area.setSelectionRange(2,17);assert(area.selectionStart===2&&area.selectionEnd===17,'Selection preserved');
 area.value='';area.dispatchEvent(new Event('input'));assert(paint.textContent==='\\n','Blank letter remains blank');
 return {themes:2,fontSizes:4,undo:true,redo:true,scroll:true,sourcePreserved:true};
 })()`);
 }finally{ipcMain.removeHandler('studio');win.destroy();}
}
module.exports={editorTest};
