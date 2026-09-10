# Recreated FiM++ compiler / interpreter

This rebuild is based on your customized December 2019 FiM++ implementation,
with postscript support and fixes found by reference-driven regression tests.
The initial reconstruction matched every original class byte. This version
intentionally changes parser and interpreter behavior where documented commands
were broken; bundled Scala runtime dependencies remain byte-identical.

## Regression results and supported dialect

See [REFERENCE-REGRESSION.md](REFERENCE-REGRESSION.md) for a command-by-command
report, linked executable cases, known gaps, and reproduction steps.

The original interpreter's `syntax/` documents and the Sparkle 1.0 PDF describe
different dialects. This build preserves the original dialect. **It does not
implement all commands in the Sparkle 1.0 PDF.** Typed methods, floating-point
arithmetic, case-sensitive names, class inheritance/interfaces, and several
Sparkle control and input commands remain unsupported. The report includes
explicit failing probes for these features rather than marking them as passed.

Regression fixes cover parentheses comments, tuple calls using `of each`,
quantified comparisons, quoted Java field names, Java boolean returns, method
aliases, acronym/digit class lookup, and full Unicode character codepoints.

## Postscript comments

```text
Your faithful student, Twilight Sparkle.
PS This is a comment.
PSS This is another comment.
P.S.No space is required after the dotted marker.
P.P.S.This is the additional-postscript spelling from the specification.
```

Comments run to the next newline (or end of file) and do not execute. Markers
are case-insensitive. `P.S.S.`, `P.P.P.S.`, and undotted `PPS` also work.
They can appear between statements or after a statement on the same line.
Markers inside quoted strings remain literal text. Each new comment line
needs its own marker; unmarked trailing text is still an error.

This follows the **Comments / Inline** section on page 6 of your saved
`FiM++ 1.0 Language Specification.pdf`, with undotted aliases added for convenience.
The saved `Binder1.pdf` also shows a postscript after the signature.
The broader language features in those documents are not all implemented by
this older interpreter; this change specifically adds postscript comments.

FiM++ parses and runs `.fimpp` letters directly; it does not translate each
letter into a separate executable. The included source build compiles the
interpreter itself into a standalone `bin/Fimpp.jar`.

## Run a letter

Open Terminal in this folder, then run:

```sh
./bin/fimpp examples/hello.fimpp
./bin/fimpp "/path/to/your letter.fimpp"
```

Or use Java directly:

```sh
java -jar bin/Fimpp.jar examples/hello.fimpp
```

The macOS launcher prefers installed Java 8 to match the original environment.
Override it with `FIMPP_JAVA_HOME`. Windows users can use `bin\fimpp.bat`.
Java GUI examples are included in `examples/`.

## Rebuild from source

Requires **JDK 8** and **Python 3.6 or later**. All Scala dependencies are included;
the build needs no internet, IntelliJ, sbt, or globally installed Scala.

```sh
python3 build.py
python3 verify.py
python3 reference_tests.py --legacy-only
```

`build.py` checks dependency SHA-256 hashes, compiles every Scala source file,
and packages the result with its runtime libraries. It never uses the
reference JAR as a build input. On macOS it locates JDK 8 automatically.
On other systems set `JAVA_HOME` or `FIMPP_JAVA_HOME` to JDK 8.

`verify.py` checks bundled runtime class bytes against the reference and compares stdout,
stderr, and exit status for the console examples, error cases, CLI argument
handling, a filename containing spaces, Java method invocation, and the original
parser unit tests. It also runs postscript parser regression checks and executes
a letter with postscripts to ensure comment text is not executed.
GUI examples are excluded from automated execution because
they open interactive windows. See `verification.json` for the actual results.
The original parser emits one non-exhaustive-match compiler warning; its source
still has that warning. `reference_tests.py` also reports Sparkle conformance
gaps. Without `--legacy-only`, it exits unsuccessfully while any reference test
fails, making it suitable as a strict full-conformance gate.

## Contents and provenance

- `src/`: recovered Scala source, updated with the documented fixes above.
- `bin/Fimpp.jar`: freshly compiled standalone interpreter.
- `reference/Fimpp.jar`: untouched selected JAR from `bk fim++ setup/runtime`.
- `lib/`: Scala 2.11.1 library and reflection library, plus parser combinators 1.0.2.
- `tools/`: Scala 2.11.1 compiler.
- `dependencies.json`: SHA-256 hashes of the bundled build dependencies.
- `examples/`, `syntax/`, `grammar/`: recovered language examples and documentation.
- `test/`: recovered tests and additional compatibility probes.
- `reference-regression.json`: expected and actual outcomes for each reference test.
- `reference-regression-before.json`: the initial reference-test run before regression fixes.
- `README-upstream.md`, `LICENSE`: original project documentation and GPLv3 license.

The Scala compiler, library, and reflection JARs came from Maven Central's
`org/scala-lang` artifacts at version 2.11.1. Parser combinators came from your
Desktop backup. Runtime class bytes were checked against the original JAR.
The old `.ok` snapshots predate your custom changes; validation uses your
selected JAR as the behavioral reference rather than those older snapshots.

Reference JAR SHA-256:
`184fe2f4509eed326cfd7aaa39e9c5d4d0fc40c0c8fbe3e391b3e8d7a5839160`

Original project copyright: Karol Stasiak and other contributors.
Distributed under GPLv3 or later; see `LICENSE`.
