#!/usr/bin/env python3
"""Executable, document-indexed conformance inventory. No baseline blessing."""
import base64
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from build import ROOT, java_for_build

CASES = []


def letter(body, functions=''):
    return ('Dear Princess Celestia: Regression letter.\n' + functions +
            '\nToday I learned about testing:\n' + body +
            '\nYour faithful student, Twilight Sparkle.\n')


def add(name, body, expected='', doc='', dialect='legacy', functions='', source=None,
        status='ok', mode='run', stdin=''):
    CASES.append(dict(id='case-%04d' % (len(CASES) + 1), name=name, doc=doc,
                      dialect=dialect, source=source if source is not None else letter(body, functions),
                      expected=expected, expected_status=status, mode=mode, stdin=stdin))


def inventory():
    # Every command family in syntax/*.md and grammar/bnf.tex; synonym variants
    # get independent executions with explicit expected results.
    d='syntax/Other statements.md'
    for verb in ['said','wrote','sang']:
        for quickly in ['', 'quickly ']:
            for prefix in ['', 'that ', ', ', ': ']:
                add('output '+quickly+verb+' '+prefix, 'I '+quickly+verb+' '+prefix+'"ok".',
                    'ok'+('' if quickly else '\n'),d)
    for body in ['By the way, a comment. I said "ok".',
                 'I said "ok", because this is a comment.',
                 '(This is a comment)\nI said "ok".',
                 'I said "ok". (An inline comment)',
                 '(Punctuation! And a second sentence.\nMore text?) I said "ok".']:
        add('comments '+body[:40],body,'ok\n',d)
    add('parenthetical header','', 'ok\n',d,source=letter('I said "ok".').replace('Celestia:', 'Celestia( and Luna):'))
    add('quoted comment markers','I said "(literal) P.S.literal".','(literal) P.S.literal\n',d)
    d='syntax/Identifiers.md; grammar/bnf.tex: Identifiers'
    for name in ['Twilight Sparkle',"Crackle's cousin",'The Great-and-Powerful Trixie','The Cutie Mark Crusaders']:
        read='cutie mark crusaders' if 'Crusaders' in name else name.upper()
        add('identifier '+name,'Did you know that '+name+' likes 8? I wrote '+read+'.','8\n',d)
    for name in ['The Great and Powerful Trixie','DJ-Pon3','Flim & Flam']:
        add('invalid identifier '+name,'Did you know that '+name+' likes 8?',doc=d,status='parse-error')
    d='syntax/Type system.md; grammar/bnf.tex: Literals'
    for literal,value in [('1','1'),('90','90'),('seven','7'),('the number 42','42'),
                          ('the number five','5'),('number 10','10'),('zero','0'),('twelve','12'),
                          ('"text"','text'),('1, 2, and "string"','1, 2, string'),('only 1','1'),
                          ('harmony','harmony'),('chaos','chaos')]:
        add('literal '+literal,'I said '+literal+'.',value+'\n',d)
    add('string interpolation','Did you know Spike likes 8? I said "Spike has '+"'Spike'"+' gems".', 'Spike has 8 gems\n',d)
    d='syntax/Expressions and assignment.md'
    for verb in ['is','are','likes','like']:
        for that in ['', 'that ']:
            add('assignment '+that+verb,'Did you know '+that+'Spike '+verb+' 7? I wrote Spike.','7\n',d)
    for verb in ['did','made']:
        add('call assignment '+verb,'Spike '+verb+' sum of 2 and 3. I said Spike.','5\n',d)
        for each in ['of each of','of each']:
            add('tuple call assignment '+verb+each,'Did you know Pinkie likes 2 and 3? Spike '+verb+' sum '+each+' Pinkie. I said Spike.','5\n',d)
    fn='I learned echo with Spike:\nI said Spike.\nThat\'s about echo.\n'
    for prefix in ['I','I also']:
        for verb in ['did','made','caused']:
            for expr in ['of 7','of each of Pinkie','of each Pinkie']:
                add('discard result '+prefix+verb+expr,'Did you know Pinkie likes only 7? '+prefix+' '+verb+' echo '+expr+'.','7\n',d,functions=fn)
    for amount in ['one','3']:
        for direction,delta in [('more',1),('less',-1),('fewer',-1)]:
            add('increment '+amount+direction,'Did you know Spike likes 5? Spike got '+amount+' '+direction+'. I wrote Spike.',str(5+(1 if amount=='one' else 3)*delta)+'\n',d)
    for today in ['', 'Today ']:
        for named in ['named','titled']:
            for ending in ['', ' today']:
                add('book creation '+today+named+ending,today+'I found a book '+named+' Pinkie'+ending+'. On first page of Pinkie I read about Spike. I said Spike.','nothing\n',d)
    for page in ['1st page','the 2nd page','fifth page','the tenth page','page numbered by Rarity','the page numbered by Rarity']:
        for verb in ['wrote','scribbled','noted']:
            for about in ['', 'about ', 'what I knew about ']:
                body='I found a book named Pinkie. Did you know Rarity likes 4? On '+page+' of the book Pinkie I '+verb+' '+about+'7. On '+page+' of the book Pinkie I read about Spike. I said Spike.'
                add('book write/read '+page+verb+about,body,'7\n',d)
    add('book grows with empty pages','I found a book named Pinkie. On tenth page of Pinkie I wrote 9. On first page of Pinkie I read about Spike. I said Spike.','nothing\n',d)
    fn='I learned change with Pinkie: On first page of Pinkie I wrote 9. That\'s about change.'
    add('array passed by reference','I found a book named Spike. I did change of Spike. On first page of Spike I read about Twilight. I said Twilight.','9\n','syntax/Type system.md',functions=fn)
    d='syntax/Functions.md'
    for result in ['', ' with answer']:
        name='echo' if not result else 'answer'
        fn='I learned about echo with Spike and Pinkie: '+name+' made sum of Spike and Pinkie. That\'s about echo'+result+'.'
        add('function return '+result,'Twilight made echo of 2 and 3. I said Twilight.','5\n',d,functions=fn)
    fn='I learned echo: Yes, I mean that Spike. Did you know Spike likes 8? That\'s about echo.'
    add('global scope','Yes, that Spike. Did you know Spike likes 2? I did echo. I said Spike.','8\n',d,functions=fn)
    add('local scope','Did you know Spike likes 2? I did echo. I said Spike.','2\n',d,functions=fn.replace('Yes, I mean that Spike.',''))
    add('mismatched function footer','',doc=d,functions="I learned echo: That's about different.",status='parse-error')
    d='syntax/Built-in functions.md'
    for name,args,value in [('sum','2, 3 and 4','9'),('product','2, 3 and 4','24'),('difference','2 and 3','-1'),('quotient','7 and 2','3'),('remainder','7 and 2','1'),('character by code','65','A'),('character by code','128512','😀')]:
        add('builtin '+name+' '+args,'Spike made '+name+' of '+args+'. I said Spike.',value+'\n',d)
    add('builtin dictionary','Did you know Pinkie likes 2 and 3? Spike made dictionary of Pinkie. On second page of Spike I read about Twilight. I said Twilight.','3\n',d)
    add('builtin letters','Spike made letters of "pony". On second page of Spike I read about Twilight. I said Twilight.','o\n',d)
    add('invalid Unicode codepoint','Spike made character by code of 1114112.',doc=d,status='runtime-error')
    for setup in ['Did you know Spike likes 2 and 3?', 'I found a book named Spike. On first page of Spike I wrote 2.']:
        add('builtin first '+setup[:20],setup+' Twilight made first of Spike. I said Twilight.','2\n',d)
    for name,value in [('new line','\n'),('tabulation','\t'),('apostrophe',"'"),('quote','"'),('harmony','harmony'),('chaos','chaos')]:
        add('builtin constant '+name,'I quickly said '+name+'.',value,d)
    d='syntax/Conditional expressions.md'
    def cond(name,expression,value=True,setup=''):
        add(name,setup+' When '+expression+': I said "yes". In the end, I did this instead: I said "no". That\'s what I did.',('yes' if value else 'no')+'\n',d)
    for verb in ['has','have','had']:
        for op in ['more than','less than','not more than','not less than']:
            cond('numeric '+verb+op,'3 '+verb+' '+op+' 2',op in ['more than','not less than'])
    for verb in ['is','are','was','were']:
        for op,value in [('equal to',True),('not equal to',False),('an element of',True),('elements of',True),('not an element of',False),('not elements of',False)]:
            cond('equality '+verb+op,'2 '+verb+' '+op+' 2',value)
        for word,value in [('nothing',True),('nopony',True),('something',False),('somepony',False)]:
            cond('null '+verb+word,'Spike '+verb+' '+word,value,'I found a book named Pinkie. On first page of Pinkie I read about Spike.')
    cond('strict comparison','2 is equal to "2"',False)
    for who in ['everything','everypony','anything','anypony']:
        for op,value in [('more than',True),('less than',False),('not less than',True),('not more than',False)]:
            cond('quantified '+who+op,who+' in Pinkie had '+op+' 1',value,'Did you know Pinkie likes 2 and 3?')
        for op,value in [('equal to',True),('not equal to',False)]:
            cond('quantified equality '+who+op,who+' in Pinkie were '+op+' 2',value,'Did you know Pinkie likes 2 and 2?')
    cond('any versus all true','anypony in Pinkie had more than 2',True,'Did you know Pinkie likes 1 and 3?')
    cond('any versus all false','everypony in Pinkie had more than 2',False,'Did you know Pinkie likes 1 and 3?')
    for expression in ['1 is equal to 1 and 2 is equal to 2','1 is equal to 2 or 2 is equal to 2',
                       'either 1 is equal to 1 or 2 is equal to 2',
                       '1 is equal to 1, 2 is equal to 2 and 3 is equal to 3',
                       '1 is equal to 2, 2 is equal to 3 or 3 is equal to 3']:
        cond('logical '+expression,expression)
    d='syntax/Control statements.md'
    for count,n in [('3 times',3),('once',1),('',1),('0 times',0)]:
        add('repeat '+count,'I did this '+count+': I said "ok". That\'s what I did.','ok\n'*n,d)
    add('while','Did you know Spike likes 0? I did this while Spike had less than 3: I said Spike. Spike got one more. That\'s what I did.','0\n1\n2\n',d)
    for start in ['I did this once', 'I did this while 1 is equal to 1']:
        add('catch and finally '+start,start+': Did you know Spike likes "text"? Spike got one more. It didn\'t work, but I knew why: I said "caught". In the end, I did this instead: I said "finally". That\'s what I did.','caught\nfinally\n',d)
    add('finally on zero iterations','I did this 0 times: I said "no". In the end, I did this instead: I said "finally". That\'s what I did.','finally\n',d)
    add('uncaught loop error still runs finally','I did this once: Did you know Spike likes "text"? Spike got one more. In the end, I did this instead: I said "finally". That\'s what I did.','finally\n',d,status='runtime-error')
    d='syntax/Java interop.md; grammar/bnf.tex: Java statements'
    setup='I enchanted Twilight with regression fixture. I woke up Spike with Twilight.'
    for clazz in ['java lang math','java util hash map','org xml sax helpers xml filter impl','javax swing j frame','regression fixture two']:
        add('Java class '+clazz,'I enchanted Twilight with '+clazz+'. I said "ok".','ok\n',d)
    for args,value in [('',3),(' and 9',9)]:
        add('constructor'+args,'I enchanted Twilight with regression fixture. I woke up Spike with Twilight'+args+'. I took count of Spike and gave it to Pinkie. I said Pinkie.',str(value)+'\n',d)
    for verb in ['took','got','stole']:
        for of in ['of','from']:
            for pronoun in ['it','them','her','him']:
                add('field read '+verb+of+pronoun,setup+' I '+verb+' "count" '+of+' Spike and I gave '+pronoun+' to Pinkie. I said Pinkie.','3\n',d)
    for field in ['count','"count"']:
        for verb in ['gave','sold']:
            add('field write '+verb+field,setup+' I '+verb+' 9 to '+field+' of Spike. I took count of Spike and gave it to Pinkie. I said Pinkie.','9\n',d)
    add('static field set/get',setup+' I gave 11 to "total" of Twilight. I took total of Twilight and gave it to Pinkie. I said Pinkie.','11\n',d)
    for word in ['so','if','what','when','how']:
        add('method invocation '+word,'I enchanted Twilight with regression fixture. I told Pinkie I asked Twilight about 5 '+word+' they twice. I said Pinkie.','10\n',d)
    add('property setter',setup+' I asked about Spike with 9 of count. I told Pinkie I asked if Spike has count. I said Pinkie.','9\n',d)
    add('boolean setter/getter',setup+' I asked about Spike made ready. I told Pinkie I asked if Spike has ready. When Pinkie was an element of harmony: I said "yes". That\'s what I did.','yes\n',d)
    add('boolean false getter',setup+' I told Pinkie I asked if Spike has ready. When Pinkie was an element of chaos: I said "no". That\'s what I did.','no\n',d)
    for word in ['what','if','when']:
        add('property getter '+word,setup+' I told Pinkie I asked '+word+' Spike has count. I said Pinkie.','3\n',d)
    add('getter arguments',setup+' I told Pinkie I asked if Spike with 4 has plus. I said Pinkie.','7\n',d)
    fn='I learned clicked: I said "clicked". That\'s about clicked.'
    add('Swing ActionListener', 'I enchanted Twilight with javax swing j button. I woke up Spike with Twilight. I asked about Spike and clicked when they add action listener. I asked about Spike when they do click.','clicked\n',d,functions=fn)
    for file in ['swing.fimpp','gui_calculator.fimpp']:
        add('GUI example parses '+file,'',doc='examples/'+file,source=(ROOT/'examples'/file).read_text(),mode='parse-only')
    add('wrapped module','',expected='ok\n',doc='syntax/Program structure.md',source="Dear Princess Celestia: Letter. Today I learned about echo: I learned about echo: I said \"ok\". That's about echo. Your faithful student, Spike.")
    sparkle_inventory()


def sparkle_inventory():
    def s(name,body,expected='',page=0,**kwargs):
        add(name,body,expected,'FiM++ 1.0 Language Specification.pdf p.'+str(page),'sparkle',**kwargs)
    s('Sparkle Hello World','', 'Hello World\n',21,source='Dear Princess Celestia: Hello World!\nToday I learned how to say Hello World!\nI said “Hello World”!\nThat’s all about how to say Hello World!\nYour faithful student, Kyli Rouge.')
    s('class inheritance and interfaces','',page=7,source='Dear Princess Luna and Shining Armor: Letter. Today I learned: Your faithful student, Spike.',mode='parse-only')
    s('interface declaration','',page=8,source='Princess Luna:\nI learned how to fly.\nYour faithful student, Spike.',mode='parse-only')
    s('case sensitive names','Did you know Spike likes 1? Did you know spike likes 2? I said Spike. I said spike.','1\n2\n',9)
    for name in ['Team Fortress 2','Somepony’s true identity','Éclair']:
        s('Unicode/numeric identifier '+name,'Did you know that '+name+' likes 7? I said '+name+'.','7\n',10)
    for literal,value in [('31.25','31.25'),("'A'",'A'),('the letter ‘T’','T'),('“Princess”','Princess'),('the word "adorable"','adorable'),('yes','true'),('true','true'),('right','true'),('correct','true'),('no','false'),('false','false'),('wrong','false'),('incorrect','false'),('nothing','nothing')]:
        s('Sparkle literal '+literal,'I said '+literal+'.',value+'\n',12)
    for typ in ['a number','a letter','a character','a word','a phrase','a sentence','a quote','a name','a logic','an argument']:
        s('typed declaration '+typ,'Did you know that Spike is '+typ+'? I said Spike.','nothing\n',11)
    s('constant reassignment','Did you know that Spike always is 1? Spike is now 2.',page=11,status='runtime-error')
    s('array declaration write read','Did you know that cake has many names? cake 1 is "chocolate". cake 2 is "apple cinnamon". I said cake 2.','apple cinnamon\n',10)
    s('initialized array','Did you know that cake has the names "chocolate" and "fruit"? I said cake 2.','fruit\n',11)
    for expr,value in [('add 2 and 3','5'),('2 plus 3','5'),('2 and 3','5'),('2 added to 3','5'),('subtract 5 and 7','-2'),('5 minus 2','3'),('5 without 2','3'),('the difference between 5 and 2','3'),('multiply 2 and 3','6'),('2 times 3','6'),('2 multiplied with 3','6'),('divide 8 and 2','4'),('divide 8 by 2','4'),('8 divided by 2','4')]:
        s('arithmetic '+expr,'I said '+expr+'.',value+'\n',13 if 'add' in expr or 'plus' in expr else 14)
    for verb in ['is now','are now','now like','now likes','become','becomes']:
        s('rewriting '+verb,'Did you know Spike likes 1? Spike '+verb+' 2. I said Spike.','2\n',14)
    s('string concatenation','Did you know Spike likes 2? I said "gems: "Spike"!".','gems: 2!\n',15)
    s('output thought','I thought "ok".','ok\n',15)
    for verb in ['heard','read','asked']:
        s('input '+verb,'Did you know Spike likes 0? I '+verb+' Spike. I said Spike.','7\n',15,stdin='7\n')
    s('prompt','Did you know Spike likes 0? I asked Spike "How many?". I said Spike.','How many?\n7\n',16,stdin='7\n')
    for op in ['is','is not','is less than','is not greater than','is greater than','is no less than']:
        s('comparison '+op,'If 2 '+op+' 2 then: I said "ok". That\'s what I would do.', 'ok\n' if op in ['is','is not greater than','is no less than'] else '',16)
    for expr,value in [('true and true',True),('false or true',True),('either true or true',False),('not false',True),("it's not the case that false",True)]:
        s('boolean '+expr,'If '+expr+': I said "yes". Otherwise: I said "no". That\'s what I would do.',('yes' if value else 'no')+'\n',18)
    for word in ['Otherwise','Or else']:
        s('else '+word,'If 1 is 2: I said "no". '+word+': I said "yes". That\'s what I would do.','yes\n',19)
    s('switch','In regards to 2: On the 1st hoof: I said "one". On the 2nd hoof: I said "two". If all else fails: I said "other". That\'s what I did.','two\n',19)
    for word in ["Here's what I did while",'As long as']:
        s('while '+word,'Did you know Spike likes 0? '+word+' Spike had less than 2: I said Spike. Spike got one more. That\'s what I did.','0\n1\n',20)
    s('do while',"Did you know Spike likes 0? Here's what I did: I said Spike. Spike got one more. I did this while Spike had less than 2.",'0\n1\n',20)
    s('counting for','For every number x from 1 to 3: I said x. That\'s what I did.','1\n2\n3\n',20)
    s('iterating for','Did you know Spike likes "AB"? For every character c in Spike: I said c. That\'s what I did.','A\nB\n',21)
    s('typed method/return/call','I remembered echo using 2.','2\n',8,functions="I learned echo using a number Spike: I said Spike. Then you get Spike. That's all about echo!")
    s('punctuation / empty statements','I said "ok"!...','ok\n',4)
    s('inline comment','I said "ok". P.S.No space needed\nP.P.S.More','ok\n',6)
    s('block comment','(Comment!) I said "ok".','ok\n',6)
    s('standalone comparison','2 is 2.',page=16)
    s('standalone arithmetic modifies target','Did you know Spike likes 1? I would add 2 to Spike. I said Spike.','3\n',13)
    s('typed return without parameters','I said echo.','2\n',8,functions="I learned echo to get a number: Then you get 2. That's all about echo!")
    s('alternate method call would','I would echo.','ok\n',9,functions="I learned echo: I said \"ok\". That's all about echo!")
    s('multiple main methods','', 'one\ntwo\n',8,source='Dear Princess Celestia: Letter. Today I learned first: I said "one". That\'s all about first! Today I learned second: I said "two". That\'s all about second! Your faithful student, Spike.')
    s('array equality','Did you know Pinkie likes 1 and 2? Did you know Spike likes 1 and 2? If Pinkie is Spike: I said "equal". That\'s what I would do.','equal\n',16)
    s('mixed type comparison','If 2 is "2": I said "equal". That\'s what I would do.','equal\n',16)
    s('boolean standalone expression','true and false.',page=18)
    s('counting character range',"For every character c from 'A' to 'C': I said c. That's what I did.",'A\nB\nC\n',20)
    add('Binder Hello World','', 'Hello, World!\n','Binder1.pdf p.3','sparkle',source='Dear Princess Celestia:Hello World!\nToday I learned how to say hello world!\nI said “Hello, World!”!\nThat\'s all about how to say hello world.\nYour faithful student, Kyli Rouge.')
    add('Binder 100 Mississipis','', ''.join(str(i)+' Mississipi(s)\n' for i in range(1,101)), 'Binder1.pdf p.2','sparkle',source='Dear Princess Celestia: 100 Mississipis\nToday I learned how to count to 100. Did you know that the number miss was 1? As long as miss was no more than 100, I said miss" Mississipi(s)". miss got one more. That\'s what I did! That\'s all about how to count to 100!\nYour faithful student, Meowflash.')
    add('Binder import directive','',doc='Binder1.pdf p.4',dialect='sparkle',source='Remember when I wrote about Applejack?\n'+letter(''),mode='parse-only')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy-only',action='store_true',help='Gate on original-dialect tests; still report Sparkle gaps')
    args=parser.parse_args()
    os.chdir(str(ROOT))
    inventory()
    output=ROOT/'test/reference'; output.mkdir(exist_ok=True)
    (output/'cases.json').write_text(json.dumps(CASES,indent=2,ensure_ascii=False)+'\n')
    for case in CASES:
        (output/(case['id']+'.fimpp')).write_text(case['source'])
    enc=lambda s:base64.b64encode(s.encode()).decode()
    (output/'input.tsv').write_text('\n'.join('\t'.join([c['id'],enc(c['source']),enc(c['stdin']),c['mode']]) for c in CASES)+'\n')
    classes=ROOT/'build/reference-tests'; classes.mkdir(parents=True,exist_ok=True)
    java=java_for_build(); javac=str(Path(java).with_name('javac'))
    subprocess.check_call([javac,'-d',str(classes),'test/Fixture.java','test/Fixture2.java'])
    cp=os.pathsep.join(str(p) for p in sorted((ROOT/'tools').glob('*.jar'))+sorted((ROOT/'lib').glob('*.jar'))+[ROOT/'bin/Fimpp.jar'])
    subprocess.check_call([java,'-Dscala.usejavacp=true','-cp',cp,'scala.tools.nsc.Main','-d',str(classes),'test/ReferenceRunner.scala'])
    p=subprocess.run([java,'-Djava.awt.headless=true','-cp',str(ROOT/'bin/Fimpp.jar')+os.pathsep+str(classes),'ReferenceRunner',str(output/'input.tsv')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
    if p.returncode: raise RuntimeError(p.stderr.decode())
    results={}
    for line in p.stdout.decode().splitlines():
        key,status,stdout,detail=line.split('\t')
        results[key]=dict(status=status,stdout=base64.b64decode(stdout).decode(),detail=base64.b64decode(detail).decode())
    assert len(results)==len(CASES), 'Missing test results'
    for case in CASES:
        result=results[case['id']];case['actual']=result
        case['passed']=result['status']==case['expected_status'] and result['stdout']==case['expected']
    (ROOT/'reference-regression.json').write_text(json.dumps(CASES,indent=2,ensure_ascii=False)+'\n')
    write_report(CASES)
    for dialect in ['legacy','sparkle']:
        cases=[c for c in CASES if c['dialect']==dialect]
        print('{}: {}/{} passed'.format(dialect,sum(c['passed'] for c in cases),len(cases)))
        for c in cases:
            if not c['passed']: print('FAIL '+c['id']+' '+c['name']+': '+str(c['actual'])[:230])
    if any(not c['passed'] for c in CASES if not args.legacy_only or c['dialect']=='legacy'): raise SystemExit(1)


def write_report(cases):
    lines=['# FiM++ reference regression report','',
           '**Full Sparkle 1.0 conformance is not achieved.** The original JAR implements a different dialect.',
           'Tests below measure explicit output or expected errors, not just successful parsing.', '',
           '## Results','', '| Reference dialect | Passed | Failed | Total |', '|---|---:|---:|---:|']
    for dialect in ['legacy','sparkle']:
        group=[c for c in cases if c['dialect']==dialect]
        n=sum(c['passed'] for c in group)
        lines.append('| {} | {} | {} | {} |'.format(dialect,n,len(group)-n,len(group)))
    lines += ['', '## Scope and limits','',
              '- Original dialect: every command family in the ten syntax documents and the saved BNF; synonyms, outputs, branches, arrays, functions, scopes, Java interop, and a headless Swing button callback.',
              '- Sparkle: executable probes indexed to pages 4–21 of the PDF, including all major command families; Binder Hello World, 100 Mississipis, and import syntax are probed separately.',
              '- The PDF specifies incompatible semantics (case-sensitive identifiers, floating-point values, typed methods, classes, interfaces). It also contains unfinished proposals. These are reported as gaps, not silently translated.',
              '- The saved Jugs of Cider and sum-of-1-to-100 examples combine multiple unsupported Sparkle features. Passing their older `.fimpp` counterparts does not establish PDF-example compatibility.',
              '- Two GUI example files are parsed only. Swing callback execution is tested headlessly; visible windows and the interactive calculator are not manually exercised.',
              '- This finite regression suite does not prove correctness for every possible program or permutation. Raw cases, expected results, actual output, and parse/runtime errors are in `reference-regression.json`.',
              '- All reference input was read from the local folder; no web version was substituted.', '',
              '## Fixed original-dialect defects','',
              '- Parenthesized comments no longer consume the following statement and now work between tokens, across lines, and after the signature.',
              '- `of each` works without the second `of`; it is parsed before an ordinary argument list.',
              '- Quantified tuple comparisons support every parsed comparison operator, including `not less than` and `not more than`.',
              '- Java field assignments accept quoted field names; returned Java booleans become FiM++ boolean values.',
              '- `how` method calls and `when` property queries accept their documented spellings.',
              '- Java class lookup retains acronym and digit variants (e.g. XMLFilterImpl and Fixture2) and removes duplicate candidates.',
              '- `character by code` supports supplementary Unicode codepoints and rejects out-of-range values.',
              '- The build selects a Java 8 JDK rather than a browser-plugin JRE on macOS.', '',
              '## Reproduce','', '```sh','python3 build.py','python3 verify.py',
              'python3 reference_tests.py --legacy-only  # original-dialect gate',
              'python3 reference_tests.py                # full gate; fails while Sparkle gaps remain','```','',
              'JAR SHA-256: `'+hashlib.sha256((ROOT/'bin/Fimpp.jar').read_bytes()).hexdigest()+'`', '',
              '## Individual checks','', '| Test | Reference | Result | Expected / actual |', '|---|---|---|---|']
    def cell(s): return str(s).replace('|','\\|').replace('\n',' / ').replace('\r','')
    for c in cases:
        outcome='PASS' if c['passed'] else 'FAIL'
        detail='parse only' if c['mode']=='parse-only' else ('expected '+repr(c['expected']))
        if not c['passed']:
            detail+='; '+c['actual']['status']+': '+(c['actual']['detail'] or repr(c['actual']['stdout']))[:230]
        lines.append('| [{}](test/reference/{}.fimpp) | {} | {} | {} |'.format(cell(c['name']),c['id'],cell(c['doc']),outcome,cell(detail)))
    (ROOT/'REFERENCE-REGRESSION.md').write_text('\n'.join(lines)+'\n')


if __name__=='__main__': main()
