const {contextBridge,ipcRenderer}=require('electron');
contextBridge.exposeInMainWorld('studio',{
 call:(name,arg)=>ipcRenderer.invoke('studio',name,arg),
 on:(channel,callback)=>{if(!['state','command','output','started','ended'].includes(channel))throw Error('Unknown event');ipcRenderer.on(channel,(_event,value)=>callback(value));}
});
