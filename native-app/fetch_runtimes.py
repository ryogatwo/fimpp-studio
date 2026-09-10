#!/usr/bin/env python3
"""Fetch pinned official runtimes for a source rebuild, with SHA-256 verification."""
from pathlib import Path
import hashlib,json,tarfile,urllib.request
HERE=Path(__file__).resolve().parent
for arch in ['arm64','x86_64']:
    vendor=HERE/'vendor'; metadata=json.loads((vendor/(arch+'.json')).read_text())[0]
    package=metadata['binary']['package']; archive=vendor/(arch+'.tar.gz')
    if not archive.exists():
        print('Downloading',package['name'],flush=True)
        urllib.request.urlretrieve(package['link'],str(archive))
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==package['checksum'], 'Runtime checksum mismatch'
    output=vendor/arch; output.mkdir(exist_ok=True)
    with tarfile.open(str(archive)) as tar:
        for member in tar.getmembers():
            if member.name.startswith('/') or '..' in Path(member.name).parts:raise ValueError('Unsafe archive path')
        tar.extractall(str(output))
    print('Verified',arch)
