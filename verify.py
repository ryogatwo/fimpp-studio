#!/usr/bin/env python3
"""Compare rebuilt class bytes and console behavior with the reference JAR."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile
from build import ROOT, java_for_build


def class_files(path):
    with zipfile.ZipFile(str(path)) as jar:
        return {n: jar.read(n) for n in jar.namelist() if n.endswith('.class')}


def main():
    os.chdir(str(ROOT))
    java = java_for_build()
    original, rebuilt = ROOT / 'reference/Fimpp.jar', ROOT / 'bin/Fimpp.jar'
    old, new = class_files(original), class_files(rebuilt)
    unchanged_old = {n: b for n, b in old.items() if not n.startswith('stasiak/')}
    unchanged_new = {n: b for n, b in new.items() if not n.startswith('stasiak/')}
    assert unchanged_old == unchanged_new, 'Unexpected changes to bundled runtime dependencies'
    report = {'reference_sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
              'rebuilt_sha256': hashlib.sha256(rebuilt.read_bytes()).hexdigest(),
              'identical_application_classes': sum(n.startswith('stasiak/') and old.get(n) == b for n, b in new.items()),
              'identical_runtime_classes': sum(not n.startswith('stasiak/') and old.get(n) == b for n, b in new.items()),
              'java': subprocess.check_output([java, '-version'], stderr=subprocess.STDOUT).decode(),
              'passed': [], 'skipped': []}

    def run(jar, args, main_class=None):
        command = [java]
        if main_class:
            command += ['-cp', str(jar) + os.pathsep + str(ROOT / 'build/test-classes'), main_class]
        else:
            command += ['-jar', str(jar)]
        proc = subprocess.run(command + args, input=b'', stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=45)
        return (proc.returncode, proc.stdout, proc.stderr)

    cases = [('no arguments', []), ('multiple arguments', ['one', 'two']),
             ('missing file', ['test/does-not-exist.fimpp'])]
    for folder in ['examples', 'test/errors', 'test/compatibility']:
        for source in sorted(Path(folder).glob('*.fimpp')):
            if 'swing' in source.read_text().lower():
                report['skipped'].append(str(source) + ' (interactive GUI)')
            else:
                cases.append((str(source), [str(source)]))
    for name, args in cases:
        assert run(original, args) == run(rebuilt, args), 'Behavior differs: ' + name
        report['passed'].append(name)
        print('PASS ' + name, flush=True)
    test_classes = ROOT / 'build/test-classes'
    test_classes.mkdir(exist_ok=True)
    cp = os.pathsep.join(str(p) for p in sorted((ROOT / 'tools').glob('*.jar'))
                         + sorted((ROOT / 'lib').glob('*.jar')) + [rebuilt])
    subprocess.check_call([java, '-Dscala.usejavacp=true', '-cp', cp, 'scala.tools.nsc.Main',
                           '-d', str(test_classes), 'test/UnitTests.scala', 'test/PostscriptTests.scala'])
    assert run(original, [], 'UnitTests') == run(rebuilt, [], 'UnitTests'), 'Parser test output differs'
    report['passed'].append('upstream parser unit tests')
    result = run(rebuilt, [], 'PostscriptTests')
    assert result[0] == 0 and not result[2], result
    print(result[1].decode().strip())
    report['passed'].append(result[1].decode().strip())
    source = 'test/postscripts/hello.fimpp'
    result = run(rebuilt, [source])
    expected = ('parsing: ' + source + '\ninterpreting: ' + source + '\n\n\nHello, Equestria\n').encode()
    assert result == (0, expected, b''), result
    report['passed'].append('postscript CLI execution (comments do not execute)')
    (ROOT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: {} test groups; {} unchanged class files.'.format(len(report['passed']), len(unchanged_new)))


if __name__ == '__main__':
    main()
