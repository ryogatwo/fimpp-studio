# FiM++ Studio 1.2.3 for Windows

Created by: RyogaTwo

A standalone Windows x64 desktop edition of FiM++ Studio. It includes the same modified original-dialect compiler, all 20 indented examples, an offline guide, and a verified Eclipse Temurin 17 runtime. No Java, Node.js, browser, or development tools need to be installed by the user. The Windows app uses Electron; the macOS app continues to use AppKit.

## Run or install

- **FiMpp-Studio-Portable-1.2.3-x64.exe**: a single EXE that extracts its bundled runtime to a temporary directory and launches Studio without installation. Keep your letters in your own folder. Appearance preferences are saved in the Windows user profile.
- **FiMpp-Studio-Setup-1.2.3-x64.exe**: the installer, with destination selection, Start menu/Desktop shortcuts, `.fimpp`/`.fpp` file associations, and an uninstaller. Uninstalling preserves user settings and letters.

Official release executables are signed and timestamped with Azure Artifact Signing. The architecture is x64 for Windows 10/11; Windows on ARM can run the x64 build through Windows emulation. See the validation reports for the exact tested OS and architecture.

## Use

New letters start blank. Use the Examples menu to open an editable example copy. The menu and guide display `Brainf*** interpreter` for that example.

- Ctrl+N / Ctrl+O: new/open letter.
- Ctrl+S / Ctrl+Shift+S: save/save as.
- Ctrl+R: run current text, including unsaved edits.
- Ctrl+period: stop the program and its child windows.
- Ctrl+F: find/replace; Ctrl+Z / Ctrl+Y: undo/redo.
- Program input sends a line to the running program. End input closes standard input.
- View → Appearance: Follow System, Light, Dark. The setting is remembered.
- Reference opens the complete offline guide. The compiler uses the documented original dialect; Sparkle-only syntax remains unsupported.

Tabs keep independent text and output. Unsaved-change prompts appear when closing a letter or exiting. Save regularly; this Windows edition does not use macOS document autosave. Source files are UTF-8, limited to 10 MB. Output is capped at 1 MB per run.

## Rebuild

The build requires Node.js 24+, Python with Pillow for the icon, and the dependencies in package.json. Dependencies are build tools only. From this directory:

```
npm install
node scripts/fetch-runtime.cjs
node scripts/build.cjs
```

Set `FIM_BUILD_PYTHON` to your Python executable if needed. The build reads the sibling `native-app/Resources` guide and examples, the included Studio icon, the parent `bin/Fimpp.jar`, and parent regression fixtures. Runtime download URLs and SHA-256 values are pinned in `vendor/windows-x64.json`. Microsoft signing is disabled explicitly in the build configuration; no signing keys are needed.

For Windows package validation, run `scripts/validate-windows.cmd` (or `scripts/validate-windows.ps1` when PowerShell scripts are allowed) from Windows with the project folder available. The embedded `--self-test --report=PATH` option tests all 322 supported-dialect reference cases, runtime resource integrity, standard input, stopping, and error locations. It does not require a developer installation.

## Licenses

The editor is distributed under GPLv3 or later with this project. FiM++ is copyright Karol Stasiak and contributors. Eclipse Temurin is GPLv2 with the Classpath Exception; its legal files ship inside the runtime. Electron is MIT licensed and includes Chromium/third-party notices. The full source archive accompanies the release.

## Font size

Use A− / A+ in the toolbar or View → Smaller Text / Larger Text (10–40 pixels). The size is remembered across tabs and launches. Reference body text is now 15 pixels and code examples are 13 pixels.

## Signing

See [Windows signing setup](SIGNING.md). Official 1.2.3 builds use Azure Artifact Signing for the app, portable launcher, installer and uninstaller.

## Layout and editor actions

Run and Stop follow Clear Output in the OUTPUT header. The EDITOR header provides Undo, Redo, Copy, and Paste. The reference starts at the same width as the editor/output area. Resize the dividers to suit your work; new letters and examples retain the current layout.
