# FiM++ Studio

**Created by: RyogaTwo**

A standalone editor and runner for FiM++ letters, with an offline coding guide. Create, edit, save, and run letters without installing Java or other runtimes separately.

## Download version 1.2.4

| Platform | Download |
| --- | --- |
| macOS 12 or later — Intel and Apple Silicon | [Universal Mac app ZIP](https://github.com/ryogatwo/fimpp-studio/releases/download/v1.2.4/FiM++-Studio-1.2.4-macOS-Universal.zip) |
| Windows x64 — run without installation | [Portable EXE](https://github.com/ryogatwo/fimpp-studio/releases/download/v1.2.4/FiMpp-Studio-Portable-1.2.4-x64.exe) |
| Windows x64 — install with shortcuts and file associations | [Windows installer](https://github.com/ryogatwo/fimpp-studio/releases/download/v1.2.4/FiMpp-Studio-Setup-1.2.4-x64.exe) |
| Complete compiler, Mac, and Windows source snapshot | [Source ZIP](https://github.com/ryogatwo/fimpp-studio/releases/download/v1.2.4/FiMpp-Studio-1.2.4-Complete-Source.zip) |

All eight files from the Desktop output folder are available on the [release page](https://github.com/ryogatwo/fimpp-studio/releases/tag/v1.2.4), including the original README files and [SHA256SUMS.txt](https://github.com/ryogatwo/fimpp-studio/releases/download/v1.2.4/SHA256SUMS.txt).

The Mac app is Developer ID signed, Apple notarized, and verified by Gatekeeper. The Windows app, portable EXE, installer and uninstaller are signed and timestamped with Azure Artifact Signing. Both platforms include their own Java runtime. The Windows application uses Electron; the Mac application uses native AppKit.

## Features

- Blank letters on launch and New Letter.
- Editor action toolbar, output controls, equal starting panes, and preserved tab layout.
- A− / A+ editor font controls with remembered size, plus a larger reference guide.
- Syntax colors for keywords, strings, numbers, and comments in both light and dark modes.
- Edit multiple letters and save UTF-8 `.fimpp` and `.fpp` files.
- Run current text, view output, provide input, stop programs, and locate compiler errors.
- Twenty bundled, indented examples, including loops, functions, arrays, input, and Swing programs.
- A complete offline guide for the supported original FiM++ dialect.
- Persistent **View → Appearance → Follow System / Light / Dark** controls.
- PS, PSS, dotted postscript forms, and parenthesized comments.

Use Command shortcuts on Mac and Control shortcuts on Windows: N for New, O for Open, S for Save, and R for Run. See [Mac instructions](native-app/README.md), [Windows instructions](windows-app/README.md), and the bundled reference for details.

## Language compatibility and validation

This project preserves the original FiM++ dialect with documented compiler fixes. It does not implement the separate Sparkle 1.0 language in full. See [compiler details](README-compiler.md) and [reference regression results](REFERENCE-REGRESSION.md) for supported features and known differences.

The supported-dialect regression suite passes **322 reference cases**. The Mac release was tested with both bundled architectures; Intel execution was tested through Rosetta on Apple Silicon. Both the portable Windows EXE and the installed Windows app passed all 322 cases on Windows 11, plus bundled-resource, program-input, process-stop, and error-location checks. Shared Windows UI testing also covered opening examples, running, saving, and Dark mode on macOS.

## Source and building

- `src/`, `syntax/`, `examples/`, and `test/`: compiler source, syntax references, examples, and regression fixtures.
- `native-app/`: AppKit Mac application and build/signing scripts.
- `windows-app/`: Electron Windows application and unsigned EXE/installer build scripts.
- `bin/Fimpp.jar`: the compiler used in the packaged release.

See each platform's README for build requirements. End users need no developer tools. Runtime download URLs and checksums are pinned in the platform source folders. Signing scripts read publisher configuration from local environment variables; no personal signing configuration or credentials are included. Other builders should use their own signing identity or create unsigned builds.

## License and acknowledgments

Studio and the modified FiM++ compiler are distributed under [GNU GPLv3 or later](LICENSE). The original FiM++ compiler is by Karol Stasiak and contributors. See [the upstream README](README-upstream.md).

Bundled Eclipse Temurin/OpenJDK runtimes use GPLv2 with the Classpath Exception. Electron uses the MIT license and includes Chromium and third-party notices. Scala libraries retain their included licenses. Runtime legal notices are included in the packaged apps.
