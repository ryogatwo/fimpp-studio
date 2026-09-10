const {spawn}=require('node:child_process');
const fs=require('node:fs/promises');
const path=require('node:path');
const os=require('node:os');
const {StringDecoder}=require('node:string_decoder');
class LetterRunner {
  constructor({java,jar,onOutput,onEnd,maxBytes=1000000}) {Object.assign(this,{java,jar,onOutput,onEnd,maxBytes});this.child=null;this.starting=false;this.cancelled=false;this.finished=false;}
  async start(text,cwd) {
    if(this.child||this.starting)throw Error('A program is already running.');
    this.starting=true; this.cancelled=false; this.finished=false; this.output='';this.bytes=0;this.reason=null;
    try {
      this.temp=await fs.mkdtemp(path.join(os.tmpdir(),'FiMStudio-'));
      const file=path.join(this.temp,'Letter.fimpp');await fs.writeFile(file,text,'utf8');
      if(this.cancelled){await this.finish(null);return;}
      const env={...process.env,JAVA_HOME:path.dirname(path.dirname(this.java))};
      for(const key of Object.keys(env))if(['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH'].includes(key.toUpperCase()))delete env[key];
      const child=spawn(this.java,['-Dfile.encoding=UTF-8','-jar',this.jar,file],{cwd:cwd||this.temp,env,windowsHide:true,detached:process.platform!=='win32',stdio:['pipe','pipe','pipe']});this.child=child;
      const decoders=[new StringDecoder('utf8'),new StringDecoder('utf8')];
      const append=(text)=>{this.output+=text;this.onOutput(text.replaceAll(file,'Letter'));};
      [child.stdout,child.stderr].forEach((stream,i)=>{
        stream.on('data',buf=>{const remaining=Math.max(0,this.maxBytes-this.bytes);this.bytes+=buf.length;append(decoders[i].write(buf.subarray(0,remaining)));if(this.bytes>this.maxBytes){this.reason='Output limit reached';this.stop();}});
        stream.on('end',()=>append(decoders[i].end()));
      });
      child.stdin.on('error',()=>{});
      child.on('error',error=>{this.reason=error.message;append(error.message+'\n');});
      child.on('close',code=>this.finish(code));
    }catch(error){this.reason=error.message;await this.finish(null);throw error;}
    finally{this.starting=false;}
  }
  input(text){if(!this.child||this.child.stdin.destroyed)throw Error('This program is not accepting input.');this.child.stdin.write(text+'\n');}
  eof(){this.child?.stdin.end();}
  stop(){this.cancelled=true;this.reason ||= 'Stopped';const child=this.child;if(!child||!child.pid)return;
    if(process.platform==='win32'){
      const killer=spawn(path.join(process.env.SystemRoot||'C:\\Windows','System32','taskkill.exe'),['/PID',String(child.pid),'/T','/F'],{windowsHide:true});killer.on('error',()=>child.kill());
    }else {try{process.kill(-child.pid,'SIGTERM');}catch{};this.killTimer=setTimeout(()=>{try{process.kill(-child.pid,'SIGKILL');}catch{}},1500);this.killTimer.unref();}
  }
  async finish(code){if(this.finished)return;this.finished=true;clearTimeout(this.killTimer);this.child=null;
    const match=this.output.match(/\[(\d+)\.(\d+)\]/);
    const status=this.reason||(code===0&&!/failure:|error:|Exception/.test(this.output)?'Finished':'Check output');
    if(this.temp)await fs.rm(this.temp,{recursive:true,force:true}).catch(()=>{});
    this.onEnd({status,exitCode:code,errorLine:match?Number(match[1]):null});
  }
}
module.exports={LetterRunner};
