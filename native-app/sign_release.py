from pathlib import Path
import subprocess,concurrent.futures,sys,os
HERE=Path(__file__).resolve().parent
APP=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE/'build/FiM++ Studio.app'
IDENTITY=os.environ.get('FIM_MAC_SIGNING_IDENTITY')
if not IDENTITY:sys.exit('Set FIM_MAC_SIGNING_IDENTITY to your local signing identity')
magic={b'\xcf\xfa\xed\xfe',b'\xce\xfa\xed\xfe',b'\xfe\xed\xfa\xcf',b'\xfe\xed\xfa\xce',b'\xca\xfe\xba\xbe',b'\xbe\xba\xfe\xca'}
paths=[]
for p in (APP/'Contents/Resources/runtimes').rglob('*'):
 if p.is_file() and not p.is_symlink():
  with p.open('rb') as f:header=f.read(4)
  if header in magic:paths.append(p)
def sign(p):
 args=['codesign','--force','--options','runtime','--timestamp','--sign',IDENTITY]
 if p.name=='java':args+=['--entitlements',str(HERE/'java.entitlements')]
 subprocess.run(args+[str(p)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for p in pool.map(sign,paths): print('Signed',p.relative_to(APP),flush=True)
subprocess.check_call(['codesign','--force','--options','runtime','--timestamp','--sign',IDENTITY,str(APP)])
subprocess.check_call(['codesign','--verify','--deep','--strict','--verbose=2',str(APP)])
print('Developer ID signatures verified')
