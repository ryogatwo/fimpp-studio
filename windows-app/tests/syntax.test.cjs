const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {execFileSync}=require('node:child_process');
const syntax=require('../app/syntax.js');
const cases=[
 ['I said "P.S. (hello) by the way 42".', ['keyword','string']],
 ['(I said "hello" 42) I wrote 12.', ['comment','keyword','number']],
 ['P.S.no space\r\nP.P.S. "hi"\nPS last\npss: last', ['comment','comment','comment','comment']],
 ['I wrote 4, because I said "why"!\nBy the way 42. I sang "yes".', ['keyword','number','comment','comment','keyword','string']],
 ['"unterminated (PS', ['string']],
 ['(unterminated "hi"', ['comment']],
 ['😀 I said "🌈".\r\nI did this two times:\n    I wrote 1st.\nThat\'s what I did.', ['keyword','string','keyword','number','keyword','number','keyword']],
 ['psst pepper appleps ps-name', []],
 ['I\tquickly\tsang "hello".', ['keyword','string']],
 ['"<script>&" ("quoted")', ['string','comment']],
 ['', []],
];
for(const [text,kinds] of cases)test('lexical precedence '+JSON.stringify(text),()=>{
 const tokens=syntax.tokens(text);assert.deepEqual(tokens.map(t=>t.kind),kinds);
 let end=0;for(const t of tokens){assert.ok(t.start>=end);assert.ok(t.length>0);end=t.start+t.length;assert.ok(end<=text.length);}
});
test('HTML source is escaped and round trips without markup injection',()=>{
 assert.equal(syntax.html('"<script>&"'),'<span class="syntax-string">"&lt;script&gt;&amp;"</span>\n');
});
test('Mac and Windows return identical UTF-16 spans for fixtures and all examples', {skip:process.platform!=='darwin'},()=>{
 const root=path.resolve(__dirname,'../..'),temp=fs.mkdtempSync(path.join(os.tmpdir(),'fim-syntax-'));
 try{
 const texts=cases.map(c=>c[0]);for(const name of fs.readdirSync(path.join(root,'native-app/Resources/Examples')))if(name.endsWith('.fimpp'))texts.push(fs.readFileSync(path.join(root,'native-app/Resources/Examples',name),'utf8'));
 fs.writeFileSync(path.join(temp,'main.swift'),`import Foundation
let input = try! JSONSerialization.jsonObject(with: FileHandle.standardInput.readDataToEndOfFile()) as! [String]
let kinds = ["string", "comment", "keyword", "number"]
let result = input.map { text in FiMSyntax.tokens(text).map { t in ["start": t.range.location, "length": t.range.length, "kind": kinds[t.kind]] as [String: Any] } }
FileHandle.standardOutput.write(try! JSONSerialization.data(withJSONObject: result))
`);
 execFileSync('xcrun',['swiftc','-module-cache-path',path.join(temp,'cache'),path.join(root,'native-app/Sources/FiMSyntax.swift'),path.join(temp,'main.swift'),'-o',path.join(temp,'check')]);
 const actual=JSON.parse(execFileSync(path.join(temp,'check'),{input:JSON.stringify(texts)}));assert.deepEqual(actual,texts.map(syntax.tokens));
 }finally{fs.rmSync(temp,{recursive:true,force:true});}
});
