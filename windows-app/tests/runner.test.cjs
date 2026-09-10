const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs/promises'),os=require('node:os'),path=require('node:path');
const {LetterRunner}=require('../app/runner.cjs');
const java=process.env.FIM_TEST_JAVA;
const jar=path.resolve(__dirname,'../../bin/Fimpp.jar');
function run(text,options={}){return new Promise((resolve,reject)=>{let output='';const runner=new LetterRunner({java,jar,...options,onOutput:s=>output+=s,onEnd:r=>resolve({...r,output,runner})});runner.start(text).catch(reject);});}
const letter=body=>`Dear Princess Celestia: Regression.\nToday I learned:\n${body}\nYour faithful student, Twilight Sparkle.\n`;
test('output cap stops a runaway program and cleans its snapshot',{skip:!java},async()=>{const result=await run(letter('I did this while 1 is equal to 1: I said "abcdefghijk". That\'s what I did.'),{maxBytes:1024});assert.equal(result.status,'Output limit reached');assert(result.output.length<1500);await assert.rejects(fs.access(result.runner.temp));});
test('UTF-8 program output survives stream decoding',{skip:!java},async()=>{const result=await run(letter('I said "Hello 🦄 — 日本語".'));assert.equal(result.status,'Finished');assert(result.output.includes('Hello 🦄 — 日本語'));});
test('missing Java returns an actionable error and cleans temporary files',async()=>{const result=await new Promise(resolve=>{const runner=new LetterRunner({java:path.join(os.tmpdir(),'missing-fim-java'),jar,onOutput:()=>{},onEnd:r=>resolve({...r,runner})});runner.start(letter('I said "hi".')).catch(()=>{});});assert.match(result.status,/ENOENT/);await assert.rejects(fs.access(result.runner.temp));});
