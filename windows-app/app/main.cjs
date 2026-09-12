const {app,BrowserWindow,Menu,dialog,ipcMain,nativeTheme,shell}=require('electron');
const fs=require('node:fs/promises'),path=require('node:path');
const {fileURLToPath,pathToFileURL}=require('node:url');
const {LetterRunner}=require('./runner.cjs');
const resourceRoot=process.env.FIM_STUDIO_RESOURCES||path.join(process.resourcesPath,'StudioResources');
const java=process.env.FIM_STUDIO_JAVA||path.join(resourceRoot,'runtime','bin','java.exe');
const jar=path.join(resourceRoot,'Fimpp.jar');
let win,docs=[],nextId=0,active=null,allowClose=false,theme='system',fontSize=14,catalog=[],settingsPath,quitting=false,settingsWrite=Promise.resolve();
const send=(channel,value)=>{if(win&&!win.isDestroyed())win.webContents.send(channel,value);};
const snapshot=()=>({docs:docs.map(d=>({id:d.id,name:d.file?path.basename(d.file):d.name,file:d.file,text:d.text,dirty:d.text!==d.saved,running:!!d.runner})),active,theme,fontSize,dark:nativeTheme.shouldUseDarkColors});
function changed(){send('state',snapshot());if(win)win.setTitle((docs.find(d=>d.id===active)?.name||'Letter')+' — FiM++ Studio');}
function newLetter(text='',name){const doc={id:++nextId,name:name||'Untitled '+nextId,file:null,text,saved:text?'':text,runner:null};docs.push(doc);active=doc.id;changed();return doc;}
const getDoc=id=>{const d=docs.find(d=>d.id===id);if(!d)throw Error('Letter not found');return d;};
async function openFile(file){const existing=docs.find(d=>d.file===file);if(existing){active=existing.id;changed();return;}
 const bytes=await fs.readFile(file);const text=new TextDecoder('utf-8',{fatal:true}).decode(bytes);const doc=newLetter(text,path.basename(file));doc.file=file;doc.saved=text;changed();}
async function saveDoc(doc,saveAs=false){let file=doc.file;if(saveAs||!file){const pick=await dialog.showSaveDialog(win,{title:'Save letter',defaultPath:file||doc.name+'.fimpp',filters:[{name:'FiM++ letters',extensions:['fimpp','fpp']}]});if(pick.canceled)return false;file=pick.filePath;}
 const text=doc.text;await fs.writeFile(file,text,'utf8');doc.file=file;doc.name=path.basename(file);doc.saved=text;changed();return true;}
async function confirmClose(doc){if(doc.text===doc.saved)return true;const {response}=await dialog.showMessageBox(win,{type:'question',message:'Save changes to '+(doc.file?path.basename(doc.file):doc.name)+'?',buttons:['Save','Discard','Cancel'],defaultId:0,cancelId:2});return response===0?saveDoc(doc):response===1;}
async function closeDoc(id){const doc=getDoc(id);if(!await confirmClose(doc))return;doc.runner?.stop();docs=docs.filter(d=>d!==doc);if(active===id)active=docs.at(-1)?.id||null;if(!docs.length)newLetter();else changed();}
async function closeAll(){if(quitting)return;quitting=true;try{for(const doc of docs)if(!await confirmClose(doc))return;for(const d of docs)d.runner?.stop();await settingsWrite;allowClose=true;win.close();}finally{quitting=false;}}
function setTheme(value){if(!['system','light','dark'].includes(value))throw Error('Unknown appearance');theme=value;nativeTheme.themeSource=value;const data=JSON.stringify({theme,fontSize})+'\n';settingsWrite=settingsWrite.then(()=>fs.writeFile(settingsPath,data)).catch(e=>showError(e));buildMenu();changed();}
const showError=e=>dialog.showErrorBox('FiM++ Studio',e.message||String(e));
const action=name=>send('command',name);
function buildMenu(){Menu.setApplicationMenu(Menu.buildFromTemplate([
 {label:'File',submenu:[{label:'New Letter',accelerator:'CmdOrCtrl+N',click:()=>action('new')},{label:'Open…',accelerator:'CmdOrCtrl+O',click:()=>action('open')},{label:'Save',accelerator:'CmdOrCtrl+S',click:()=>action('save')},{label:'Save As…',accelerator:'CmdOrCtrl+Shift+S',click:()=>action('saveAs')},{label:'Close Letter',accelerator:'CmdOrCtrl+W',click:()=>action('close')},{type:'separator'},{label:'Exit',click:()=>win.close()}]},
 {label:'Edit',submenu:[{role:'undo'},{role:'redo'},{type:'separator'},{role:'cut'},{role:'copy'},{role:'paste'},{role:'selectAll'},{type:'separator'},{label:'Find / Replace',accelerator:'CmdOrCtrl+F',click:()=>action('find')}]},
 {label:'Program',submenu:[{label:'Run Letter',accelerator:'CmdOrCtrl+R',click:()=>action('run')},{label:'Stop',accelerator:'CmdOrCtrl+.',click:()=>action('stop')},{label:'Go to Error',click:()=>action('error')}]},
 {label:'Examples',submenu:catalog.map(e=>({label:e.title,click:()=>action('example:'+e.file)}))},
 {label:'View',submenu:[{label:'Reference Guide',accelerator:'CmdOrCtrl+Shift+R',click:()=>action('guide')},{label:'Larger Text',accelerator:'CmdOrCtrl+Plus',click:()=>action('larger')},{label:'Smaller Text',accelerator:'CmdOrCtrl+-',click:()=>action('smaller')},{label:'Appearance',submenu:[['system','Follow System'],['light','Light'],['dark','Dark']].map(([value,label])=>({label,type:'radio',checked:theme===value,click:()=>setTheme(value)}))},{role:'togglefullscreen'}]},
 {label:'Help',submenu:[{label:'FiM++ Coding Reference',click:()=>action('guideShow')},{label:'About FiM++ Studio',click:()=>dialog.showMessageBox(win,{title:'About FiM++ Studio',message:'FiM++ Studio '+app.getVersion(),detail:'Created by: RyogaTwo\n\nStandalone Windows letter editor and offline reference.\nFiM++ © Karol Stasiak and contributors · GPLv3+\nEclipse Temurin · GPLv2 with Classpath Exception\nElectron · MIT',buttons:['OK']})}]}]));}
async function command(name,arg){switch(name){
 case 'init':return {...snapshot(),catalog,guide:pathToFileURL(path.join(resourceRoot,'Guide','index.html')).href,version:app.getVersion()};
 case 'update':{const d=getDoc(arg.id);if(typeof arg.text!=='string'||arg.text.length>10000000)throw Error('Letter exceeds 10 MB limit.');d.text=arg.text;return true;}
 case 'activate':active=getDoc(arg).id;changed();return;
 case 'new':newLetter();return;
 case 'open':{const pick=await dialog.showOpenDialog(win,{properties:['openFile','multiSelections'],filters:[{name:'FiM++ letters',extensions:['fimpp','fpp']},{name:'Text files',extensions:['txt']}]});for(const p of pick.filePaths)await openFile(p);return;}
 case 'save':return saveDoc(getDoc(arg));case 'saveAs':return saveDoc(getDoc(arg),true);case 'close':return closeDoc(arg);
 case 'example':{const e=catalog.find(e=>e.file===arg);if(!e)throw Error('Unknown example');newLetter(await fs.readFile(path.join(resourceRoot,'Examples',e.file+'.fimpp'),'utf8'),e.title);return;}
 case 'run':{const d=getDoc(arg);if(d.runner)return;const runner=new LetterRunner({java,jar,onOutput:text=>send('output',{id:d.id,text}),onEnd:result=>{d.runner=null;send('ended',{id:d.id,...result});changed();}});d.runner=runner;send('started',{id:d.id});changed();await runner.start(d.text,d.file?path.dirname(d.file):undefined);return;}
 case 'stop':getDoc(arg).runner?.stop();return;case 'input':getDoc(arg.id).runner?.input(arg.text);return;case 'eof':getDoc(arg).runner?.eof();return;
 case 'fontSize':if(!Number.isInteger(arg)||arg<10||arg>40)throw Error('Invalid font size');fontSize=arg;settingsWrite=settingsWrite.then(()=>fs.writeFile(settingsPath,JSON.stringify({theme,fontSize})+'\n'));await settingsWrite;return;
 case 'theme':setTheme(arg);return;
 default:throw Error('Unknown command');}}
app.setName('FiM++ Studio');
if(!process.argv.includes('--self-test')&&!app.requestSingleInstanceLock())app.quit();else{
 app.on('second-instance',(_e,args)=>{const file=args.find(a=>/\.(fimpp|fpp)$/i.test(a));if(file)openFile(path.resolve(file)).catch(showError);if(win){if(win.isMinimized())win.restore();win.focus();}});
 app.whenReady().then(async()=>{
  if(process.argv.includes('--self-test')){const {selfTest}=require('./self-test.cjs');try{await selfTest({resourceRoot,java,jar,args:process.argv});app.exit(0);}catch(e){console.error(e);app.exit(1);}return;}
  settingsPath=path.join(app.getPath('userData'),'settings.json');await fs.mkdir(path.dirname(settingsPath),{recursive:true});try{const saved=JSON.parse(await fs.readFile(settingsPath,'utf8'));theme=saved.theme;if(Number.isInteger(saved.fontSize)&&saved.fontSize>=10&&saved.fontSize<=40)fontSize=saved.fontSize;}catch{}if(!['system','light','dark'].includes(theme))theme='system';nativeTheme.themeSource=theme;
  catalog=JSON.parse(await fs.readFile(path.join(resourceRoot,'Examples/catalog.json'),'utf8'));
  win=new BrowserWindow({width:1280,height:860,minWidth:850,minHeight:620,title:'FiM++ Studio',backgroundColor:nativeTheme.shouldUseDarkColors?'#242229':'#faf9fc',webPreferences:{preload:path.join(__dirname,'preload.cjs'),contextIsolation:true,nodeIntegration:false,sandbox:true}});
  win.webContents.setWindowOpenHandler(()=>({action:'deny'}));win.webContents.on('will-navigate',e=>e.preventDefault());win.webContents.session.setPermissionRequestHandler((_wc,_permission,callback)=>callback(false));
  ipcMain.handle('studio',async(event,name,arg)=>{if(event.sender!==win.webContents||event.senderFrame!==win.webContents.mainFrame)throw Error('Untrusted caller');return command(name,arg);});
  win.on('close',event=>{if(!allowClose){event.preventDefault();closeAll().catch(showError);}});
  nativeTheme.on('updated',()=>changed());buildMenu();newLetter();await win.loadFile(path.join(__dirname,'index.html'));
  const file=process.argv.find(a=>/\.(fimpp|fpp)$/i.test(a));if(file){docs=[];await openFile(path.resolve(file));}
 }).catch(e=>{showError(e);app.exit(1);});
 app.on('window-all-closed',()=>{if(!process.argv.includes('--self-test'))app.quit();});
}
