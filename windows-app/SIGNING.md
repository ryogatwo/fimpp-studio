# Signing FiM++ Studio

Signing is optional for local builds. Publisher credentials and machine-specific configuration must be supplied privately and must never be committed or included in source archives.

## Windows

1. Install Azure CLI, Microsoft Artifact Signing client tools, and Windows SDK SignTool on the signing machine.
2. Authenticate with `az login` using an account authorized to sign.
3. Copy `windows-app/artifact-signing-metadata.json` to a private file outside the repository and set your endpoint, signing account, and certificate profile.
4. Set `FIM_SIGNING_METADATA` to that private file. When signing from macOS through Parallels, also set `FIM_SIGNING_VM` to your Windows VM identifier.
5. Build with `FIM_WINDOWS_SIGN=1 node windows-app/scripts/build.cjs` using the documented build dependencies.
6. Run the Windows validation launcher. Verify app, portable launcher, installer, and uninstaller signatures with `Get-AuthenticodeSignature`, then regenerate release checksums.

Without `FIM_WINDOWS_SIGN=1`, Windows builds are unsigned. Signing failures stop signed builds.

## macOS

Use your own Developer ID Application certificate. Set `FIM_MAC_SIGNING_IDENTITY` locally before running `python3 native-app/sign_release.py`. Supply your own local keychain profile when submitting an archive with `xcrun notarytool`; staple and verify the accepted app before creating the final archive and checksums.

Code-signing certificates publicly identify their publisher. A signed application cannot conceal the identity embedded in its certificate.

[Microsoft signing documentation](https://learn.microsoft.com/en-us/azure/artifact-signing/how-to-signing-integrations)
