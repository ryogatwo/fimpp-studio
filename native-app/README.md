# FiM++ Studio 1.2.0

Created by: RyogaTwo

A standalone, universal macOS document editor for the latest modified FiM++ compiler.
Targets macOS 12 or later. Native AppKit editor and menus; WebKit displays the bundled offline coding guide. Both Intel and Apple Silicon Java runtimes are inside the app.

## Use

Open **FiM++ Studio.app**, or drag it into Applications first. No Java, Python, Scala, browser, or Rosetta installation is needed for native use.

- Launch and New Letter start with a blank document. Examples use four-space block indentation.
- New / Open / Save / Save As: Command-N, Command-O, Command-S, Shift-Command-S.
- Run: Command-R. Stop: Command-period.
- Find/replace: Command-F. Undo/redo: Command-Z / Shift-Command-Z.
- Reference: toolbar button or Help → FiM++ Coding Reference. Search works offline.
- View → Appearance: Follow System, Light, or Dark; remembered between launches.
- Examples: all 20 bundled examples are available in both the menu and guide. Opens an editable copy. Includes console input, books, postscript comments, algorithm examples, and Swing programs.
- Program input sends a line to standard input; End input sends EOF.
- Run uses a snapshot of the current editor text, including unsaved changes. Save separately to keep edits.
- Relative program paths resolve from the saved file's folder, or a temporary folder for an unsaved letter.

The guide covers this compiler's supported original dialect. It explicitly documents the remaining Sparkle 1.0 gaps. This app does not add a new Sparkle language mode.

## Version 1.2.0

All 20 bundled examples are available in the Examples menu and offline guide. The interpreter example is displayed as `Brainf*** interpreter`. View → Appearance provides persistent Follow System, Light, and Dark modes for the editor, console, and guide. Blank new letters and the RyogaTwo credit are retained.

## Build from source

Requires Xcode command-line tools and Python 3 on the build machine only. From the compiler project root:

```sh
python3 native-app/fetch_runtimes.py
python3 native-app/build_app.py
python3 native-app/validate_app.py
```

The input compiler is `bin/Fimpp.jar` from the latest regression-tested build. To rebuild the Scala compiler itself, follow the parent project's README (JDK 8 and the bundled Scala compiler libraries).

`build_app.py` creates `native-app/build/FiM++ Studio.app`. `fetch_runtimes.py` downloads the exact official runtimes pinned in `vendor/*.json`, verifies their SHA-256 digests, then extracts them. There are no runtime downloads by the app.

## Signing

Configure your own Developer ID Application certificate with `FIM_MAC_SIGNING_IDENTITY` and use your own local notarization keychain profile. `sign_release.py` signs each embedded native runtime component, then the universal app. The Java executable receives the JIT/library-loading entitlements it needs. The native editor runs with hardened runtime enabled.

Credentials and private keys are not included in source or artifacts. Rebuilders can use a local ad-hoc build or substitute their own certificate for a distributable release.

## Validation

- The app executable contains `arm64` and `x86_64` slices.
- Both embedded Java runtimes execute all 322 supported-dialect reference tests.
- Both slices pass the standalone app self-test; console input and bundled example probes pass.
- All 17 original examples retain identical output after formatting on both runtimes (Swing comparison uses headless mode).
- Version 1.1.0 UI checks confirm blank launch/New Letter, indented Fibonacci execution, and the updated name, version, and credits.
- Intel execution was tested under Rosetta on this Apple Silicon Mac, not on a separate physical Intel Mac.
- Native UI QA covers new/edit/save/reopen, undo/redo, running, stopping an infinite loop, console input, error-line navigation, unsaved-document prompts, guide search, and reference-pane toggling.
- See `release-validation.json` and `runtime-validation.json` in the release folder for final signing/runtime evidence.

The console stops programs that exceed 1 MB of output. Source files are UTF-8. Programs execute as the signed-in user and can use Java APIs; this is a local development tool, not an isolation boundary for untrusted code.

## Licenses

FiM++ is copyright Karol Stasiak and contributors, GPLv3 or later. This distribution's editor source is supplied under GPLv3 or later as part of the same project; see the parent LICENSE.

The bundled Eclipse Temurin OpenJDK runtimes include their legal notices and are distributed under GPLv2 with the Classpath Exception. Official build provenance, version, and release download links are in `vendor/*.json` and the app's `Contents/Resources/Licenses/runtime-provenance.json`. Scala runtime licenses are retained in the compiler JAR. Apple system frameworks are not redistributed.
