#!/usr/bin/env python3
from pathlib import Path
import subprocess,shutil,plistlib,json,hashlib,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
BUILD=HERE/'build'; BUILD.mkdir(exist_ok=True)
APP=BUILD/'FiM++ Studio.app'
if APP.exists():shutil.rmtree(str(APP))
RES=APP/'Contents/Resources';RES.mkdir(parents=True)
MAC=APP/'Contents/MacOS';MAC.mkdir()
subprocess.check_call([sys.executable,str(HERE/'build_guide.py')])
for arch in ['arm64','x86_64']:
 subprocess.check_call(['xcrun','swiftc','-O','-swift-version','5','-module-cache-path',str(BUILD/('ModuleCache-'+arch)),'-module-name','FiMStudio','-target',arch+'-apple-macosx12.0','-framework','AppKit','-framework','WebKit',str(HERE/'Sources/main.swift'),'-o',str(BUILD/('FiMStudio-'+arch))])
subprocess.check_call(['xcrun','lipo','-create',str(BUILD/'FiMStudio-arm64'),str(BUILD/'FiMStudio-x86_64'),'-output',str(MAC/'FiMStudio')])
for folder in ['Guide','Examples']:shutil.copytree(str(HERE/'Resources'/folder),str(RES/folder))
shutil.copy2(str(ROOT/'bin/Fimpp.jar'),str(RES/'Fimpp.jar'))
licenses=RES/'Licenses';licenses.mkdir()
shutil.copy2(str(ROOT/'LICENSE'),str(licenses/'FiMpp-GPLv3.txt'))
metadata={}
for arch in ['arm64','x86_64']:
 data=json.loads((HERE/'vendor'/(arch+'.json')).read_text())[0]
 assert hashlib.sha256((HERE/'vendor'/(arch+'.tar.gz')).read_bytes()).hexdigest()==data['binary']['package']['checksum']
 runtime=next((HERE/'vendor'/arch).glob('*/Contents/Home'))
 shutil.copytree(str(runtime),str(RES/'runtimes'/arch),symlinks=True)
 metadata[arch]={'version':data['version'],'package':data['binary']['package'],'release_name':data['release_name']}
(licenses/'runtime-provenance.json').write_text(json.dumps(metadata,indent=2)+'\n')
info={'CFBundleName':'FiM++ Studio','CFBundleDisplayName':'FiM++ Studio','CFBundleIdentifier':'io.github.ryogatwo.fimstudio','CFBundleExecutable':'FiMStudio','CFBundlePackageType':'APPL','CFBundleShortVersionString':'1.2.0','CFBundleVersion':'3','CFBundleIconFile':'AppIcon','LSMinimumSystemVersion':'12.0','NSHighResolutionCapable':True,'NSPrincipalClass':'NSApplication','NSHumanReadableCopyright':'FiM++ © Karol Stasiak and contributors. GPLv3+.','CFBundleDocumentTypes':[{'CFBundleTypeName':'FiM++ Letter','CFBundleTypeRole':'Editor','LSHandlerRank':'Owner','NSDocumentClass':'FiMDocument','LSItemContentTypes':['io.github.ryogatwo.fimpp-letter'],'CFBundleTypeExtensions':['fimpp','fpp']}], 'UTExportedTypeDeclarations':[{'UTTypeIdentifier':'io.github.ryogatwo.fimpp-letter','UTTypeDescription':'FiM++ Letter','UTTypeConformsTo':['public.plain-text'],'UTTypeTagSpecification':{'public.filename-extension':['fimpp','fpp'],'public.mime-type':'text/x-fimpp'}}]}
(APP/'Contents/Info.plist').write_bytes(plistlib.dumps(info))
subprocess.check_call(['xcrun','swiftc','-module-cache-path',str(BUILD/'IconModuleCache'),str(HERE/'Sources/Icon.swift'),'-o',str(BUILD/'make-icon')])
if (BUILD/'AppIcon.iconset').exists():shutil.rmtree(str(BUILD/'AppIcon.iconset'))
subprocess.check_call([str(BUILD/'make-icon'),str(BUILD/'AppIcon.iconset')])
subprocess.check_call(['iconutil','-c','icns',str(BUILD/'AppIcon.iconset'),'-o',str(RES/'AppIcon.icns')])
# Development signature only; release signing is applied after UI and runtime tests.
subprocess.check_call(['codesign','--force','--sign','-','--deep',str(APP)])
print(APP)
