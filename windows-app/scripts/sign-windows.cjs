// Signs via the existing Windows Azure CLI login; never exports a private key.
const {execFileSync}=require('node:child_process');
const path=require('node:path'),fs=require('node:fs'),crypto=require('node:crypto');
const vm=process.env.FIM_SIGNING_VM;
const quote=s=>"'"+s.replaceAll("'","''")+"'";
function windowsPath(p){p=path.resolve(p);if(process.platform==='win32')return p;if(!p.startsWith('/Users/'))throw Error('Signing input must be accessible through the Parallels AllFiles share');return '\\\\Mac\\AllFiles'+p.replaceAll('/','\\');}
function run(command){const args=['-NoProfile','-Command',command];return execFileSync(process.platform==='win32'?'powershell.exe':'prlctl',process.platform==='win32'?args:['exec',vm,'--current-user','powershell.exe',...args],{encoding:'utf8',timeout:180000,maxBuffer:4*1024*1024});}
async function sign(configuration){
 const file=path.resolve(configuration.path),metadata=process.env.FIM_SIGNING_METADATA;
 if(!metadata)throw Error('Set FIM_SIGNING_METADATA to your private signing metadata file');
 if(process.platform!=='win32'&&!vm)throw Error('Set FIM_SIGNING_VM to your Windows VM identifier');
 const stage='C:\\ArtifactSigning\\work\\fimpp-'+crypto.randomUUID();
 const command=`$ErrorActionPreference='Stop';
 az account show --output none; if($LASTEXITCODE -ne 0){throw 'Run az login in Windows first'};
 $roots=@('C:\\ArtifactSigning\\packages', (Join-Path \${env:ProgramFiles(x86)} 'Microsoft\\ArtifactSigningClientTools'), (Join-Path \${env:ProgramFiles(x86)} 'Windows Kits\\10'));
 $files=$roots | Where-Object {Test-Path $_} | ForEach-Object {Get-ChildItem $_ -Recurse -File};
 $tool=$files | Where-Object {$_.Name -eq 'signtool.exe' -and $_.FullName -match '\\\\x64\\\\'} | Select-Object -ExpandProperty FullName -First 1;
 $dll=$files | Where-Object {$_.Name -eq 'Azure.CodeSigning.Dlib.dll' -and $_.FullName -match '\\\\x64\\\\'} | Select-Object -ExpandProperty FullName -First 1;
 if(!$tool -or !$dll){throw 'Install Microsoft Artifact Signing client tools and Windows SDK x64 SignTool'};
 New-Item -ItemType Directory -Force -Path ${quote(stage)} | Out-Null;
 $target=Join-Path ${quote(stage)} 'artifact.exe';$meta=Join-Path ${quote(stage)} 'metadata.json';
 Copy-Item -LiteralPath ${quote(windowsPath(file))} -Destination $target;
 Copy-Item -LiteralPath ${quote(windowsPath(metadata))} -Destination $meta;
 Push-Location 'C:\\ArtifactSigning';
 try { & $tool sign /fd SHA256 /tr http://timestamp.acs.microsoft.com /td SHA256 /dlib $dll /dmdf $meta $target;
 if($LASTEXITCODE -ne 0){throw 'Artifact signing failed'};
 & $tool verify /pa /all $target; if($LASTEXITCODE -ne 0){throw 'Signature verification failed'};
 $sig=Get-AuthenticodeSignature -LiteralPath $target;
 if($sig.Status -ne 'Valid' -or !$sig.TimeStamperCertificate){throw 'Valid timestamped signature required'};
 Copy-Item -LiteralPath $target -Destination ${quote(windowsPath(file))} -Force;
 Write-Output ('SIGNED: '+$sig.SignerCertificate.Subject);
 } finally {Pop-Location};
 Remove-Item -LiteralPath ${quote(stage)} -Recurse -Force;`;
 console.log(run(command));
 fs.writeFileSync(file+'.signing.json',JSON.stringify({sha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),file:path.basename(file),timestamped:true},null,2)+'\n');
}
module.exports=sign;
if(require.main===module)sign({path:process.argv[2]}).catch(e=>{console.error(e.message);process.exit(1);});
