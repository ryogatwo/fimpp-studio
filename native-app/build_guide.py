from pathlib import Path
import html,re,json
from format_examples import indent_letter
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent/'Resources/Guide'
OUT.mkdir(parents=True,exist_ok=True)

def render(text):
    lines=text.expandtabs(4).splitlines(); result=[]; i=0; code=[]; paragraph=[]
    def flush():
        if paragraph:
            s=html.escape(' '.join(paragraph));s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
            result.append('<p>'+s+'</p>');paragraph.clear()
        if code:
            result.append('<pre><code>'+html.escape('\n'.join(code).rstrip())+'</code></pre>');code.clear()
    while i<len(lines):
        line=lines[i]
        if i+1<len(lines) and re.match(r'^[=\-]{3,}\s*$',lines[i+1]):
            flush();result.append('<h3>'+html.escape(line)+'</h3>');i+=2;continue
        if line.startswith('    '):
            if paragraph:flush()
            code.append(line[4:])
        elif not line.strip():
            if code and next((x for x in lines[i+1:] if x.strip()),'').startswith('    '):code.append('')
            else:flush()
        else:
            if code:flush()
            if line.startswith('#'):
                flush();result.append('<h3>'+html.escape(line.lstrip('# '))+'</h3>')
            elif line.startswith(('* ','- ')):
                flush();result.append('<p class="bullet">• '+html.escape(line[2:])+'</p>')
            else:paragraph.append(line)
        i+=1
    flush();return '\n'.join(result)

intro='''# Your first letter
Create a letter, write your code, and choose Run (⌘R). You can run before saving. The editor sends the current text to the interpreter; a running program keeps its snapshot while you continue editing.

    Dear Princess Celestia: My first letter.

    Today I learned about greetings:
        I said "Hello, Equestria!".

    Your faithful student, Twilight Sparkle.
    P.S. A note to the reader, not part of the program.

# Create, open, and save
Launch and New Letter (⌘N) create a blank document. Choose an example from the Examples menu if you want a starting point. Open (⌘O) opens a .fimpp or .fpp UTF-8 text file. Save (⌘S) writes it; Save As (⇧⌘S) writes a new copy. Each letter has its own window, undo history, and console. Standard macOS document autosave and unsaved-change prompts apply.
Use Edit → Find (⌘F) to find or replace text. Use the Font − / + buttons in the EDITOR header or View → Larger Text / Smaller Text to resize the editor (10–40 points). Your chosen size is remembered for new letters and the next launch. Straight quotes are preserved; macOS smart-quote substitution is disabled for code.
View → Appearance offers Follow System, Light, and Dark. Your choice applies to the editor, console, and reference guide and is remembered after quitting.
The Examples menu includes all 20 bundled letters and opens an editable copy, so you can experiment without modifying the bundled examples.

# Run and stop
Run (⌘R) executes the editor text and shows output below it. Stop (⌘.) ends that run and its program windows. Run again after editing to use your changes. Each document can run independently.
The working folder is the saved letter's folder. An unsaved letter runs in a temporary folder. Relative file operations in Java interop use that working folder.
The console caps output at 1 MB and stops a program that exceeds it. Input sends a line to programs that read standard input. End input sends EOF. Sparkle's direct I heard/read/asked input commands are not part of this dialect; see Java interoperability for an input example.

# Errors
Check output means the compiler reported a syntax/runtime error or the process failed. A parser location such as [7.12] means line 7, column 12. Go to error selects that line. The program's own console text can also contain words like error; always read the details.
Common mistakes: missing final punctuation, curly quotes, a function's ending name not matching its starting name, and using Sparkle-only commands. Strings use straight double quotes. To embed a variable inside a string, use paired apostrophes, as described in Types.

# What language does this app support?
FiM++ Studio includes the customized original FiM++ interpreter, with the postscript and regression fixes. This is not a complete Sparkle 1.0 implementation. The guide's command sections describe the supported dialect. Compatibility explains the differences.
Everything needed to edit, run, and read this guide is bundled. Internet access and a separate Java installation are not required. Programs you write may use Java APIs, including file or network access, when you ask them to.
'''
notes='''# Postscript comments
    PS A note until the end of this line.
    PSS Another note.
    P.S.No space is required after a dotted marker.
    P.P.S.Standard repeated-P spelling.
    P.S.S.This spelling is also accepted.

Markers are case-insensitive. Each comment ends at a newline or end of file. Each new comment line needs its own marker. Postscripts may follow the signature or appear between statements. Markers inside strings remain text.

# Parenthesized comments
    (A standalone comment, no extra punctuation needed)
    I said "Hello". (A note after the statement)

    Dear Princess Celestia( and friends): A letter.

Parentheses comments may span lines and end at the first closing parenthesis. They do not nest. Parentheses inside quoted strings remain literal text.

# Existing comment forms
    By the way, this is a standalone comment.
    I said "Hello", because this is a comment.

The old By the way and because forms end at the required sentence punctuation. Prefer parentheses for comments containing multiple sentences.
'''
compat='''# Use the original dialect
The saved syntax documents and the Sparkle 1.0 specification describe different languages. The bundled compiler preserves the original dialect, with bug fixes. Its complete command-family regression suite passes 322 tests; the original compatibility checks and 69 postscript checks also pass.

# Important differences
- Numbers are signed 64-bit integers at runtime; literals are nonnegative integers. Division uses integer division. Words zero through twelve work. Use difference to produce negative values.
- Names are case-insensitive ASCII words. Articles a/an/the are removed. Hyphens and interior apostrophes work; numeric and general Unicode variable names do not.
- Booleans are harmony and chaos. Use the conditional-expression forms in this guide.
- Functions use with for parameters, and That's about ... with ... for the return variable.
- Arrays are one-based books; use On ... page ... to read or write.
- Use sum, difference, product, quotient, and remainder through function-call assignment, rather than Sparkle's infix arithmetic.

# Sparkle-only features are not supported
The separate Sparkle probes pass 3 of 95 checks. Typed declarations, constants, decimal and character literals, class inheritance/interfaces, multiple main methods, direct input/prompt commands, infix arithmetic, switch, do-while, counting for, and foreach syntax are not implemented here. Neither are Sparkle's case-sensitive identifiers and Unicode naming rules.
The PDF's Hello World, 100 Mississipis, sum example, and Jugs of Cider use unsupported syntax. Use the examples shipped in this app instead. A .fpp filename is accepted as text, but its extension does not select a different dialect.

# Fixes in this build
Parentheses comments no longer consume the next statement. Tuple calls accept of each without the second of. Quantified comparisons include not less than and not more than. Quoted Java field assignments, Java boolean returns, how and when method aliases, acronym/digit class lookup, and full Unicode character codepoints have been fixed.
The app uses exactly the tested latest compiler JAR. Its standalone runtime is selected natively for Intel or Apple Silicon.
'''
input_example='''# Reading a line of input through Java
Run this example, enter a line in Program input, and press Return. This uses the supported Java API rather than Sparkle input syntax.

    Dear Princess Celestia: An input example.
    Today I learned about listening:
        I enchanted Celestia with java lang system.
        I took "in" of Celestia and gave it to stream.
        I enchanted Luna with java io input stream reader.
        I woke up reader with Luna and stream.
        I enchanted Cadance with java io buffered reader.
        I woke up buffer with Cadance and reader.
        I said "What is your name?".
        I told answer I asked about buffer when they read line.
        I said "Hello, 'answer'!".
    Your faithful student, Twilight Sparkle.

# Java field names and boolean values
Field reads and writes accept identifiers or quoted field names. Returned Java booleans are harmony/chaos, so they work with an element of harmony conditions. Java library classes are available from the bundled runtime, including Swing.
Numerical Java-array field indexing is not implemented. The graphics two class-name example in the old notes is illustrative naming syntax, not a real standard Java class. Java constructors/methods still need matching supported argument types.
'''
sections=[('start','Start here',intro),('comments','Comments & postscripts',notes)]
for id,title,name in [('structure','Letter structure','Program structure.md'),('identifiers','Names & identifiers','Identifiers.md'),('types','Types & values','Type system.md'),('assignment','Variables & books','Expressions and assignment.md'),('functions','Functions & scope','Functions.md'),('conditions','Comparisons & logic','Conditional expressions.md'),('control','Branches & loops','Control statements.md'),('output','Output & other statements','Other statements.md'),('builtins','Built-in functions','Built-in functions.md'),('java','Java interoperability','Java interop.md')]:
    text=(ROOT/'syntax'/name).read_text()
    if id=='output':text=text.split('Comment in parenthesis')[0]
    if id=='java':text=text.replace('Note: untested. Might not work yet.','Quoted and identifier field writes are regression-tested in this build.')
    sections.append((id,title,text))
sections.extend([('input','Program input',input_example),('compatibility','Compatibility & limits',compat)])
examples=ROOT/'native-app/Resources/Examples';examples.mkdir(parents=True,exist_ok=True)
for p in (ROOT/'examples').glob('*.fimpp'):(examples/p.name).write_bytes(p.read_bytes())
(examples/'postscripts.fimpp').write_bytes((ROOT/'test/postscripts/hello.fimpp').read_bytes())
(examples/'books.fimpp').write_text('''Dear Princess Celestia: A book of friends.
Today I learned about books:
    I found a book named friends.
    On first page of friends I wrote "Twilight".
    On second page of friends I wrote "Rainbow Dash".
    On second page of friends I read about pony.
    I said "A friend: 'pony'".
Your faithful student, Spike.
''')
code=input_example.split('    Dear')[1].split('\n\n#')[0]
(examples/'input.fimpp').write_text('Dear'+code.replace('\n    ','\n')+'\n')
for example in examples.glob('*.fimpp'):
    example.write_text(indent_letter(example.read_text()))
catalog=json.loads((ROOT/'native-app/example_catalog.json').read_text())
assert {e['file'] for e in catalog} == {p.stem for p in examples.glob('*.fimpp')}
(examples/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
all_examples=''
for entry in catalog:
    name=entry['file']
    all_examples+='# '+entry['title']+'\n\n'+'\n'.join('    '+line for line in (examples/(name+'.fimpp')).read_text().splitlines())+'\n\n'
sections.append(('examples','Example letters',all_examples))
sections.append(('credits','About & licenses','''# FiM++ Studio
Created by: RyogaTwo

Native AppKit editor and offline WebKit reference. Includes the modified FiM++ interpreter by Karol Stasiak and contributors, distributed under GPLv3 or later. The source and license are supplied with the app package.
Eclipse Temurin 17 runtimes are bundled for arm64 and x86_64. Their legal notices are included within each runtime. Temurin is OpenJDK under GPLv2 with the Classpath Exception. Scala libraries retain their bundled licenses.
No account, separate runtime installation, or internet connection is needed for the editor or guide.
'''))
nav=''.join('<button data-target="'+id+'" onclick="show(\''+id+'\')">'+html.escape(title)+'</button>' for id,title,text in sections)
content=''.join('<section id="'+id+'"><div class="eyebrow">FiM++ coding reference</div><h1>'+html.escape(title)+'</h1>'+render(text)+'</section>' for id,title,text in sections)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FiM++ Coding Reference</title><style>
:root{color-scheme:light dark;--bg:#faf9fc;--text:#252330;--muted:#767080;--line:#e4dfea;--code:#f0edf5;--accent:#7450a5}*{box-sizing:border-box}body{margin:0;font:15px/1.65 -apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text)}header{padding:20px 22px 14px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:2}.brand{font-weight:700;letter-spacing:.03em;color:var(--accent);margin-bottom:12px}input{width:100%;padding:9px 11px;border:1px solid var(--line);border-radius:8px;background:var(--code);color:var(--text);font:inherit}nav{display:flex;gap:6px;flex-wrap:wrap;padding:14px 22px;border-bottom:1px solid var(--line)}nav button{border:1px solid var(--line);border-radius:6px;background:transparent;color:var(--text);font:12px -apple-system,sans-serif;padding:5px 8px;cursor:pointer}nav button.active{background:var(--accent);border-color:var(--accent);color:white}main{padding:24px 22px 50px;max-width:920px;margin:auto}section{display:none}section.visible{display:block}h1{font-size:25px;line-height:1.2;font-weight:650;letter-spacing:-.5px;margin:6px 0 24px}h3{font-size:17px;line-height:1.35;margin:24px 0 10px}p{margin:8px 0 12px}.eyebrow{text-transform:uppercase;letter-spacing:1.4px;font-size:9px;color:var(--muted)}pre{position:relative;background:var(--code);border:1px solid var(--line);padding:14px;border-radius:9px;font:13px/1.7 ui-monospace,Menlo,monospace;white-space:pre;overflow:auto}code{font-family:ui-monospace,Menlo,monospace;font-size:.93em}p code{padding:2px 4px;background:var(--code);border-radius:3px}.bullet{padding-left:10px}.none{display:none;color:var(--muted)}.copy{float:right;border:0;background:var(--accent);color:white;border-radius:4px;font-size:10px;padding:3px 6px;cursor:pointer}section+section{margin-top:35px}footer{font-size:10px;color:var(--muted);border-top:1px solid var(--line);padding-top:18px;margin-top:30px}@media(prefers-color-scheme:dark){:root{--bg:#242229;--text:#e7e2ed;--muted:#a49aaa;--line:#403a48;--code:#302c37;--accent:#b99bdd}}
:root[data-theme="light"]{color-scheme:light;--bg:#faf9fc;--text:#252330;--muted:#767080;--line:#e4dfea;--code:#f0edf5;--accent:#7450a5}
:root[data-theme="dark"]{color-scheme:dark;--bg:#242229;--text:#e7e2ed;--muted:#a49aaa;--line:#403a48;--code:#302c37;--accent:#b99bdd}
</style><header><div class="brand">✦  THE LETTER WRITER’S GUIDE</div><input id="search" type="search" aria-label="Search reference" placeholder="Search commands, examples, or topics…" oninput="searchGuide(this.value)"></header><nav>'''+nav+'''</nav><main><p class="none" id="no-results">No matching topic. Try “book”, “sum”, “function”, or “comment”.</p>'''+content+'''<footer>Included with FiM++ Studio • Available offline • Original FiM++ dialect</footer></main><script>
function show(id){document.getElementById('search').value='';document.querySelectorAll('section').forEach(s=>s.classList.toggle('visible',s.id===id));document.querySelectorAll('nav button').forEach(b=>{b.hidden=false;b.classList.toggle('active',b.dataset.target===id)});document.getElementById('no-results').style.display='none';window.scrollTo(0,0)}
function searchGuide(q){q=q.trim().toLowerCase();if(!q){show('start');return}let n=0;document.querySelectorAll('section').forEach(s=>{let hit=s.innerText.toLowerCase().includes(q)||s.textContent.toLowerCase().includes(q);s.classList.toggle('visible',hit);if(hit)n++;let b=document.querySelector('[data-target="'+s.id+'"]');b.hidden=!hit;b.classList.remove('active')});document.getElementById('no-results').style.display=n?'none':'block'}
document.querySelectorAll('pre').forEach(p=>{let b=document.createElement('button');b.textContent='Copy';b.className='copy';b.onclick=()=>{let t=document.createElement('textarea');t.value=p.querySelector('code').textContent;document.body.append(t);t.select();document.execCommand('copy');t.remove();b.textContent='Copied';setTimeout(()=>b.textContent='Copy',1000)};p.prepend(b)});show('start');
</script></html>'''
(OUT/'index.html').write_text(page)
print('Built offline guide:',len(sections),'sections')
