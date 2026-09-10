#!/usr/bin/env python3
"""Offline source build of the 2019 FiM++ interpreter; Python 3.6+."""
import hashlib
import json
import os
import plistlib
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def java_for_build():
    home = os.environ.get('FIMPP_JAVA_HOME') or os.environ.get('JAVA_HOME')
    if not home and sys.platform == 'darwin':
        # java_home -v 1.8 may choose the browser-plugin JRE, which has no javac.
        installed = plistlib.loads(subprocess.check_output(['/usr/libexec/java_home', '-X']))
        home = next((j['JVMHomePath'] for j in installed
                     if j['JVMVersion'].startswith('1.8') and
                     (Path(j['JVMHomePath']) / 'bin/javac').exists()), None)
        if not home:
            raise RuntimeError('Install JDK 8 or set FIMPP_JAVA_HOME to its directory.')
    java = str(Path(home) / 'bin/java') if home else shutil.which('java')
    if not java:
        raise RuntimeError('Install JDK 8 or set FIMPP_JAVA_HOME to its directory.')
    return java


def verify_dependencies():
    expected = json.loads((ROOT / 'dependencies.json').read_text())
    for name, digest in expected.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Dependency checksum mismatch: ' + name)


def build():
    verify_dependencies()
    classes = ROOT / 'build/classes'
    if classes.exists():
        shutil.rmtree(str(classes))
    classes.mkdir(parents=True)
    libs = sorted((ROOT / 'lib').glob('*.jar'))
    cp = os.pathsep.join(str(p) for p in sorted((ROOT / 'tools').glob('*.jar')) + libs)
    subprocess.check_call([java_for_build(), '-Dscala.usejavacp=true', '-cp', cp,
                           'scala.tools.nsc.Main', '-encoding', 'UTF-8', '-d', str(classes)]
                          + [str(p) for p in sorted((ROOT / 'src').rglob('*.scala'))])
    entries = {}
    for lib in libs:
        with zipfile.ZipFile(str(lib)) as jar:
            for name in jar.namelist():
                if name.endswith('/') or name.upper().startswith('META-INF/'):
                    continue
                entries[name] = jar.read(name)
    for file in classes.rglob('*.class'):
        entries[file.relative_to(classes).as_posix()] = file.read_bytes()
    entries['META-INF/MANIFEST.MF'] = (
        b'Manifest-Version: 1.0\r\nMain-Class: stasiak.karol.fimpp.Main\r\n\r\n')
    # Preserve bundled dependency notices alongside the project GPL license.
    for lib in libs:
        with zipfile.ZipFile(str(lib)) as jar:
            for name in jar.namelist():
                if not name.endswith('/') and any(x in name.upper() for x in ('LICENSE', 'NOTICE', 'COPYING')):
                    entries['META-INF/licenses/' + lib.stem + '/' + name] = jar.read(name)
    output = ROOT / 'bin/Fimpp.jar'
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(output), 'w', zipfile.ZIP_DEFLATED) as jar:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, (2019, 12, 26, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            jar.writestr(info, entries[name])
    print('Built ' + str(output))


if __name__ == '__main__':
    build()
