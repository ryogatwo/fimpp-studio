#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,base64,hashlib,sys,os
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
APP=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'build/FiM++ Studio.app'
RES=APP/'Contents/Resources'
catalog=json.loads((RES/'Examples/catalog.json').read_text())
assert len(catalog)==20 and len({e['file'] for e in catalog})==20
assert {e['file'] for e in catalog}=={p.stem for p in (RES/'Examples').glob('*.fimpp')}
import html
guide=(RES/'Guide/index.html').read_text()
for entry in catalog:
    assert '<h3>'+html.escape(entry['title'])+'</h3>' in guide,entry
expected=json.loads((ROOT/'reference-regression.json').read_text())
report={'example_catalog_entries':len(catalog),'compiler_sha256':hashlib.sha256((RES/'Fimpp.jar').read_bytes()).hexdigest(),'architectures':{}}
assert (RES/'Fimpp.jar').read_bytes()==(ROOT/'bin/Fimpp.jar').read_bytes()
for arch,platform in [('arm64','arm64'),('x86_64','x86_64')]:
    check=subprocess.run(['/usr/bin/arch','-'+platform,str(APP/'Contents/MacOS/FiMStudio'),'--self-test'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
    assert check.returncode==0,(arch,check.stderr.decode())
    java=RES/'runtimes'/arch/'bin/java'
    cp=str(RES/'Fimpp.jar')+os.pathsep+str(ROOT/'build/reference-tests')
    test=subprocess.run([str(java),'-Djava.awt.headless=true','-Dfile.encoding=UTF-8','-cp',cp,'ReferenceRunner',str(ROOT/'test/reference/input.tsv')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
    assert test.returncode==0,test.stderr.decode()
    results={}
    for line in test.stdout.decode().splitlines():
        key,status,out,detail=line.split('\t')
        results[key]=(status,base64.b64decode(out).decode())
    passing=0
    for c in expected:
        if c['dialect']!='legacy':continue
        assert results[c['id']]==(c['expected_status'],c['expected']),(arch,c['name'],results[c['id']])
        passing+=1
    inp=subprocess.run([str(java),'-Dfile.encoding=UTF-8','-jar',str(RES/'Fimpp.jar'),str(RES/'Examples/input.fimpp')],input=b'Fluttershy\n',stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
    assert inp.returncode==0 and b'Hello, Fluttershy!' in inp.stdout,(arch,inp.stdout,inp.stderr)
    for name in ['books','postscripts']:
        p=subprocess.run([str(java),'-jar',str(RES/'Fimpp.jar'),str(RES/'Examples'/(name+'.fimpp'))],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
        assert p.returncode==0 and b'failure:' not in p.stdout and b'error:' not in p.stdout,(name,p.stdout)
    def compare_example(original):
        formatted=RES/'Examples'/original.name
        # No statements or literal content may change during indentation.
        assert [x.lstrip() for x in original.read_text().splitlines()]==[x.lstrip() for x in formatted.read_text().splitlines()],original.name
        def run(path):
            p=subprocess.run([str(java),'-Djava.awt.headless=true','-Dfile.encoding=UTF-8','-jar',str(RES/'Fimpp.jar'),str(path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
            return p.returncode,p.stdout.replace(str(path).encode(),b'<example>'),p.stderr.replace(str(path).encode(),b'<example>')
        before,after=run(original),run(formatted)
        assert before==after,(arch,original.name,'formatted output differs')
        if original.stem not in ['swing','gui_calculator']:
            assert after[0]==0 and b'failure:' not in after[1] and b'Exception' not in after[2],(original.name,after)
        return original.name
    with ThreadPoolExecutor(max_workers=4) as pool:
        compared=list(pool.map(compare_example,sorted((ROOT/'examples').glob('*.fimpp'))))
    version=subprocess.check_output([str(java),'-version'],stderr=subprocess.STDOUT).decode()
    report['architectures'][arch]={'self_test':check.stdout.decode().strip(),'reference_cases_passed':passing,'stdin_test':'passed','formatted_examples_compared':compared,'version':version,'execution':'native Apple Silicon' if arch=='arm64' else 'Intel slice and Intel JVM under Rosetta on Apple Silicon'}
    print(arch,'PASS',passing,'reference tests, stdin, examples, standalone self-test',flush=True)
for p in RES.rglob('*'):
    if p.is_symlink():assert str(p.resolve()).startswith(str(APP.resolve())),p
report['bundle_size_bytes']=sum(p.stat().st_size for p in APP.rglob('*') if p.is_file())
(HERE/'build/runtime-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS bundled runtime validation')
