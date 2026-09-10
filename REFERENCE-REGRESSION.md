# FiM++ reference regression report

**Full Sparkle 1.0 conformance is not achieved.** The original JAR implements a different dialect.
Tests below measure explicit output or expected errors, not just successful parsing.

## Results

| Reference dialect | Passed | Failed | Total |
|---|---:|---:|---:|
| legacy | 322 | 0 | 322 |
| sparkle | 3 | 92 | 95 |

## Scope and limits

- Original dialect: every command family in the ten syntax documents and the saved BNF; synonyms, outputs, branches, arrays, functions, scopes, Java interop, and a headless Swing button callback.
- Sparkle: executable probes indexed to pages 4–21 of the PDF, including all major command families; Binder Hello World, 100 Mississipis, and import syntax are probed separately.
- The PDF specifies incompatible semantics (case-sensitive identifiers, floating-point values, typed methods, classes, interfaces). It also contains unfinished proposals. These are reported as gaps, not silently translated.
- The saved Jugs of Cider and sum-of-1-to-100 examples combine multiple unsupported Sparkle features. Passing their older `.fimpp` counterparts does not establish PDF-example compatibility.
- Two GUI example files are parsed only. Swing callback execution is tested headlessly; visible windows and the interactive calculator are not manually exercised.
- This finite regression suite does not prove correctness for every possible program or permutation. Raw cases, expected results, actual output, and parse/runtime errors are in `reference-regression.json`.
- All reference input was read from the local folder; no web version was substituted.

## Fixed original-dialect defects

- Parenthesized comments no longer consume the following statement and now work between tokens, across lines, and after the signature.
- `of each` works without the second `of`; it is parsed before an ordinary argument list.
- Quantified tuple comparisons support every parsed comparison operator, including `not less than` and `not more than`.
- Java field assignments accept quoted field names; returned Java booleans become FiM++ boolean values.
- `how` method calls and `when` property queries accept their documented spellings.
- Java class lookup retains acronym and digit variants (e.g. XMLFilterImpl and Fixture2) and removes duplicate candidates.
- `character by code` supports supplementary Unicode codepoints and rejects out-of-range values.
- The build selects a Java 8 JDK rather than a browser-plugin JRE on macOS.

## Reproduce

```sh
python3 build.py
python3 verify.py
python3 reference_tests.py --legacy-only  # original-dialect gate
python3 reference_tests.py                # full gate; fails while Sparkle gaps remain
```

JAR SHA-256: `d7523625397564be33d0a48ecf0c31423ba87b11c1f4af6832eae07407594e41`

## Individual checks

| Test | Reference | Result | Expected / actual |
|---|---|---|---|
| [output said ](test/reference/case-0001.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output said that ](test/reference/case-0002.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output said , ](test/reference/case-0003.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output said : ](test/reference/case-0004.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output quickly said ](test/reference/case-0005.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly said that ](test/reference/case-0006.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly said , ](test/reference/case-0007.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly said : ](test/reference/case-0008.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output wrote ](test/reference/case-0009.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output wrote that ](test/reference/case-0010.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output wrote , ](test/reference/case-0011.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output wrote : ](test/reference/case-0012.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output quickly wrote ](test/reference/case-0013.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly wrote that ](test/reference/case-0014.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly wrote , ](test/reference/case-0015.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly wrote : ](test/reference/case-0016.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output sang ](test/reference/case-0017.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output sang that ](test/reference/case-0018.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output sang , ](test/reference/case-0019.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output sang : ](test/reference/case-0020.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [output quickly sang ](test/reference/case-0021.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly sang that ](test/reference/case-0022.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly sang , ](test/reference/case-0023.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [output quickly sang : ](test/reference/case-0024.fimpp) | syntax/Other statements.md | PASS | expected 'ok' |
| [comments By the way, a comment. I said "ok".](test/reference/case-0025.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [comments I said "ok", because this is a comment.](test/reference/case-0026.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [comments (This is a comment) / I said "ok".](test/reference/case-0027.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [comments I said "ok". (An inline comment)](test/reference/case-0028.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [comments (Punctuation! And a second sentence. / Mor](test/reference/case-0029.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [parenthetical header](test/reference/case-0030.fimpp) | syntax/Other statements.md | PASS | expected 'ok\n' |
| [quoted comment markers](test/reference/case-0031.fimpp) | syntax/Other statements.md | PASS | expected '(literal) P.S.literal\n' |
| [identifier Twilight Sparkle](test/reference/case-0032.fimpp) | syntax/Identifiers.md; grammar/bnf.tex: Identifiers | PASS | expected '8\n' |
| [identifier Crackle's cousin](test/reference/case-0033.fimpp) | syntax/Identifiers.md; grammar/bnf.tex: Identifiers | PASS | expected '8\n' |
| [identifier The Great-and-Powerful Trixie](test/reference/case-0034.fimpp) | syntax/Identifiers.md; grammar/bnf.tex: Identifiers | PASS | expected '8\n' |
| [identifier The Cutie Mark Crusaders](test/reference/case-0035.fimpp) | syntax/Identifiers.md; grammar/bnf.tex: Identifiers | PASS | expected '8\n' |
| [invalid identifier The Great and Powerful Trixie](test/reference/case-0036.fimpp) | syntax/Identifiers.md; grammar/bnf.tex: Identifiers | PASS | expected '' |
| [invalid identifier DJ-Pon3](test/reference/case-0037.fimpp) | syntax/Identifiers.md; grammar/bnf.tex: Identifiers | PASS | expected '' |
| [invalid identifier Flim & Flam](test/reference/case-0038.fimpp) | syntax/Identifiers.md; grammar/bnf.tex: Identifiers | PASS | expected '' |
| [literal 1](test/reference/case-0039.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '1\n' |
| [literal 90](test/reference/case-0040.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '90\n' |
| [literal seven](test/reference/case-0041.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '7\n' |
| [literal the number 42](test/reference/case-0042.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '42\n' |
| [literal the number five](test/reference/case-0043.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '5\n' |
| [literal number 10](test/reference/case-0044.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '10\n' |
| [literal zero](test/reference/case-0045.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '0\n' |
| [literal twelve](test/reference/case-0046.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '12\n' |
| [literal "text"](test/reference/case-0047.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected 'text\n' |
| [literal 1, 2, and "string"](test/reference/case-0048.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '1, 2, string\n' |
| [literal only 1](test/reference/case-0049.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected '1\n' |
| [literal harmony](test/reference/case-0050.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected 'harmony\n' |
| [literal chaos](test/reference/case-0051.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected 'chaos\n' |
| [string interpolation](test/reference/case-0052.fimpp) | syntax/Type system.md; grammar/bnf.tex: Literals | PASS | expected 'Spike has 8 gems\n' |
| [assignment is](test/reference/case-0053.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [assignment that is](test/reference/case-0054.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [assignment are](test/reference/case-0055.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [assignment that are](test/reference/case-0056.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [assignment likes](test/reference/case-0057.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [assignment that likes](test/reference/case-0058.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [assignment like](test/reference/case-0059.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [assignment that like](test/reference/case-0060.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [call assignment did](test/reference/case-0061.fimpp) | syntax/Expressions and assignment.md | PASS | expected '5\n' |
| [tuple call assignment didof each of](test/reference/case-0062.fimpp) | syntax/Expressions and assignment.md | PASS | expected '5\n' |
| [tuple call assignment didof each](test/reference/case-0063.fimpp) | syntax/Expressions and assignment.md | PASS | expected '5\n' |
| [call assignment made](test/reference/case-0064.fimpp) | syntax/Expressions and assignment.md | PASS | expected '5\n' |
| [tuple call assignment madeof each of](test/reference/case-0065.fimpp) | syntax/Expressions and assignment.md | PASS | expected '5\n' |
| [tuple call assignment madeof each](test/reference/case-0066.fimpp) | syntax/Expressions and assignment.md | PASS | expected '5\n' |
| [discard result Ididof 7](test/reference/case-0067.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result Ididof each of Pinkie](test/reference/case-0068.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result Ididof each Pinkie](test/reference/case-0069.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result Imadeof 7](test/reference/case-0070.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result Imadeof each of Pinkie](test/reference/case-0071.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result Imadeof each Pinkie](test/reference/case-0072.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result Icausedof 7](test/reference/case-0073.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result Icausedof each of Pinkie](test/reference/case-0074.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result Icausedof each Pinkie](test/reference/case-0075.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsodidof 7](test/reference/case-0076.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsodidof each of Pinkie](test/reference/case-0077.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsodidof each Pinkie](test/reference/case-0078.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsomadeof 7](test/reference/case-0079.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsomadeof each of Pinkie](test/reference/case-0080.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsomadeof each Pinkie](test/reference/case-0081.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsocausedof 7](test/reference/case-0082.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsocausedof each of Pinkie](test/reference/case-0083.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [discard result I alsocausedof each Pinkie](test/reference/case-0084.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [increment onemore](test/reference/case-0085.fimpp) | syntax/Expressions and assignment.md | PASS | expected '6\n' |
| [increment oneless](test/reference/case-0086.fimpp) | syntax/Expressions and assignment.md | PASS | expected '4\n' |
| [increment onefewer](test/reference/case-0087.fimpp) | syntax/Expressions and assignment.md | PASS | expected '4\n' |
| [increment 3more](test/reference/case-0088.fimpp) | syntax/Expressions and assignment.md | PASS | expected '8\n' |
| [increment 3less](test/reference/case-0089.fimpp) | syntax/Expressions and assignment.md | PASS | expected '2\n' |
| [increment 3fewer](test/reference/case-0090.fimpp) | syntax/Expressions and assignment.md | PASS | expected '2\n' |
| [book creation named](test/reference/case-0091.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [book creation named today](test/reference/case-0092.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [book creation titled](test/reference/case-0093.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [book creation titled today](test/reference/case-0094.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [book creation Today named](test/reference/case-0095.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [book creation Today named today](test/reference/case-0096.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [book creation Today titled](test/reference/case-0097.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [book creation Today titled today](test/reference/case-0098.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [book write/read 1st pagewrote](test/reference/case-0099.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read 1st pagewroteabout ](test/reference/case-0100.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read 1st pagewrotewhat I knew about ](test/reference/case-0101.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read 1st pagescribbled](test/reference/case-0102.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read 1st pagescribbledabout ](test/reference/case-0103.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read 1st pagescribbledwhat I knew about ](test/reference/case-0104.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read 1st pagenoted](test/reference/case-0105.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read 1st pagenotedabout ](test/reference/case-0106.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read 1st pagenotedwhat I knew about ](test/reference/case-0107.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagewrote](test/reference/case-0108.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagewroteabout ](test/reference/case-0109.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagewrotewhat I knew about ](test/reference/case-0110.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagescribbled](test/reference/case-0111.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagescribbledabout ](test/reference/case-0112.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagescribbledwhat I knew about ](test/reference/case-0113.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagenoted](test/reference/case-0114.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagenotedabout ](test/reference/case-0115.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the 2nd pagenotedwhat I knew about ](test/reference/case-0116.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagewrote](test/reference/case-0117.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagewroteabout ](test/reference/case-0118.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagewrotewhat I knew about ](test/reference/case-0119.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagescribbled](test/reference/case-0120.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagescribbledabout ](test/reference/case-0121.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagescribbledwhat I knew about ](test/reference/case-0122.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagenoted](test/reference/case-0123.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagenotedabout ](test/reference/case-0124.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read fifth pagenotedwhat I knew about ](test/reference/case-0125.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagewrote](test/reference/case-0126.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagewroteabout ](test/reference/case-0127.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagewrotewhat I knew about ](test/reference/case-0128.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagescribbled](test/reference/case-0129.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagescribbledabout ](test/reference/case-0130.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagescribbledwhat I knew about ](test/reference/case-0131.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagenoted](test/reference/case-0132.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagenotedabout ](test/reference/case-0133.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the tenth pagenotedwhat I knew about ](test/reference/case-0134.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Raritywrote](test/reference/case-0135.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Raritywroteabout ](test/reference/case-0136.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Raritywrotewhat I knew about ](test/reference/case-0137.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Rarityscribbled](test/reference/case-0138.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Rarityscribbledabout ](test/reference/case-0139.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Rarityscribbledwhat I knew about ](test/reference/case-0140.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Raritynoted](test/reference/case-0141.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Raritynotedabout ](test/reference/case-0142.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read page numbered by Raritynotedwhat I knew about ](test/reference/case-0143.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Raritywrote](test/reference/case-0144.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Raritywroteabout ](test/reference/case-0145.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Raritywrotewhat I knew about ](test/reference/case-0146.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Rarityscribbled](test/reference/case-0147.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Rarityscribbledabout ](test/reference/case-0148.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Rarityscribbledwhat I knew about ](test/reference/case-0149.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Raritynoted](test/reference/case-0150.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Raritynotedabout ](test/reference/case-0151.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book write/read the page numbered by Raritynotedwhat I knew about ](test/reference/case-0152.fimpp) | syntax/Expressions and assignment.md | PASS | expected '7\n' |
| [book grows with empty pages](test/reference/case-0153.fimpp) | syntax/Expressions and assignment.md | PASS | expected 'nothing\n' |
| [array passed by reference](test/reference/case-0154.fimpp) | syntax/Type system.md | PASS | expected '9\n' |
| [function return ](test/reference/case-0155.fimpp) | syntax/Functions.md | PASS | expected '5\n' |
| [function return  with answer](test/reference/case-0156.fimpp) | syntax/Functions.md | PASS | expected '5\n' |
| [global scope](test/reference/case-0157.fimpp) | syntax/Functions.md | PASS | expected '8\n' |
| [local scope](test/reference/case-0158.fimpp) | syntax/Functions.md | PASS | expected '2\n' |
| [mismatched function footer](test/reference/case-0159.fimpp) | syntax/Functions.md | PASS | expected '' |
| [builtin sum 2, 3 and 4](test/reference/case-0160.fimpp) | syntax/Built-in functions.md | PASS | expected '9\n' |
| [builtin product 2, 3 and 4](test/reference/case-0161.fimpp) | syntax/Built-in functions.md | PASS | expected '24\n' |
| [builtin difference 2 and 3](test/reference/case-0162.fimpp) | syntax/Built-in functions.md | PASS | expected '-1\n' |
| [builtin quotient 7 and 2](test/reference/case-0163.fimpp) | syntax/Built-in functions.md | PASS | expected '3\n' |
| [builtin remainder 7 and 2](test/reference/case-0164.fimpp) | syntax/Built-in functions.md | PASS | expected '1\n' |
| [builtin character by code 65](test/reference/case-0165.fimpp) | syntax/Built-in functions.md | PASS | expected 'A\n' |
| [builtin character by code 128512](test/reference/case-0166.fimpp) | syntax/Built-in functions.md | PASS | expected '😀\n' |
| [builtin dictionary](test/reference/case-0167.fimpp) | syntax/Built-in functions.md | PASS | expected '3\n' |
| [builtin letters](test/reference/case-0168.fimpp) | syntax/Built-in functions.md | PASS | expected 'o\n' |
| [invalid Unicode codepoint](test/reference/case-0169.fimpp) | syntax/Built-in functions.md | PASS | expected '' |
| [builtin first Did you know Spike l](test/reference/case-0170.fimpp) | syntax/Built-in functions.md | PASS | expected '2\n' |
| [builtin first I found a book named](test/reference/case-0171.fimpp) | syntax/Built-in functions.md | PASS | expected '2\n' |
| [builtin constant new line](test/reference/case-0172.fimpp) | syntax/Built-in functions.md | PASS | expected '\n' |
| [builtin constant tabulation](test/reference/case-0173.fimpp) | syntax/Built-in functions.md | PASS | expected '\t' |
| [builtin constant apostrophe](test/reference/case-0174.fimpp) | syntax/Built-in functions.md | PASS | expected "'" |
| [builtin constant quote](test/reference/case-0175.fimpp) | syntax/Built-in functions.md | PASS | expected '"' |
| [builtin constant harmony](test/reference/case-0176.fimpp) | syntax/Built-in functions.md | PASS | expected 'harmony' |
| [builtin constant chaos](test/reference/case-0177.fimpp) | syntax/Built-in functions.md | PASS | expected 'chaos' |
| [numeric hasmore than](test/reference/case-0178.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [numeric hasless than](test/reference/case-0179.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [numeric hasnot more than](test/reference/case-0180.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [numeric hasnot less than](test/reference/case-0181.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [numeric havemore than](test/reference/case-0182.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [numeric haveless than](test/reference/case-0183.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [numeric havenot more than](test/reference/case-0184.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [numeric havenot less than](test/reference/case-0185.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [numeric hadmore than](test/reference/case-0186.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [numeric hadless than](test/reference/case-0187.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [numeric hadnot more than](test/reference/case-0188.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [numeric hadnot less than](test/reference/case-0189.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality isequal to](test/reference/case-0190.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality isnot equal to](test/reference/case-0191.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality isan element of](test/reference/case-0192.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality iselements of](test/reference/case-0193.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality isnot an element of](test/reference/case-0194.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality isnot elements of](test/reference/case-0195.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [null isnothing](test/reference/case-0196.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [null isnopony](test/reference/case-0197.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [null issomething](test/reference/case-0198.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [null issomepony](test/reference/case-0199.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality areequal to](test/reference/case-0200.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality arenot equal to](test/reference/case-0201.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality arean element of](test/reference/case-0202.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality areelements of](test/reference/case-0203.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality arenot an element of](test/reference/case-0204.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality arenot elements of](test/reference/case-0205.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [null arenothing](test/reference/case-0206.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [null arenopony](test/reference/case-0207.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [null aresomething](test/reference/case-0208.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [null aresomepony](test/reference/case-0209.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality wasequal to](test/reference/case-0210.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality wasnot equal to](test/reference/case-0211.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality wasan element of](test/reference/case-0212.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality waselements of](test/reference/case-0213.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality wasnot an element of](test/reference/case-0214.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality wasnot elements of](test/reference/case-0215.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [null wasnothing](test/reference/case-0216.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [null wasnopony](test/reference/case-0217.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [null wassomething](test/reference/case-0218.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [null wassomepony](test/reference/case-0219.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality wereequal to](test/reference/case-0220.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality werenot equal to](test/reference/case-0221.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality werean element of](test/reference/case-0222.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality wereelements of](test/reference/case-0223.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [equality werenot an element of](test/reference/case-0224.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [equality werenot elements of](test/reference/case-0225.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [null werenothing](test/reference/case-0226.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [null werenopony](test/reference/case-0227.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [null weresomething](test/reference/case-0228.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [null weresomepony](test/reference/case-0229.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [strict comparison](test/reference/case-0230.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified everythingmore than](test/reference/case-0231.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified everythingless than](test/reference/case-0232.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified everythingnot less than](test/reference/case-0233.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified everythingnot more than](test/reference/case-0234.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified equality everythingequal to](test/reference/case-0235.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified equality everythingnot equal to](test/reference/case-0236.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified everyponymore than](test/reference/case-0237.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified everyponyless than](test/reference/case-0238.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified everyponynot less than](test/reference/case-0239.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified everyponynot more than](test/reference/case-0240.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified equality everyponyequal to](test/reference/case-0241.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified equality everyponynot equal to](test/reference/case-0242.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified anythingmore than](test/reference/case-0243.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified anythingless than](test/reference/case-0244.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified anythingnot less than](test/reference/case-0245.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified anythingnot more than](test/reference/case-0246.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified equality anythingequal to](test/reference/case-0247.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified equality anythingnot equal to](test/reference/case-0248.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified anyponymore than](test/reference/case-0249.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified anyponyless than](test/reference/case-0250.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified anyponynot less than](test/reference/case-0251.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified anyponynot more than](test/reference/case-0252.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [quantified equality anyponyequal to](test/reference/case-0253.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [quantified equality anyponynot equal to](test/reference/case-0254.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [any versus all true](test/reference/case-0255.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [any versus all false](test/reference/case-0256.fimpp) | syntax/Conditional expressions.md | PASS | expected 'no\n' |
| [logical 1 is equal to 1 and 2 is equal to 2](test/reference/case-0257.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [logical 1 is equal to 2 or 2 is equal to 2](test/reference/case-0258.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [logical either 1 is equal to 1 or 2 is equal to 2](test/reference/case-0259.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [logical 1 is equal to 1, 2 is equal to 2 and 3 is equal to 3](test/reference/case-0260.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [logical 1 is equal to 2, 2 is equal to 3 or 3 is equal to 3](test/reference/case-0261.fimpp) | syntax/Conditional expressions.md | PASS | expected 'yes\n' |
| [repeat 3 times](test/reference/case-0262.fimpp) | syntax/Control statements.md | PASS | expected 'ok\nok\nok\n' |
| [repeat once](test/reference/case-0263.fimpp) | syntax/Control statements.md | PASS | expected 'ok\n' |
| [repeat ](test/reference/case-0264.fimpp) | syntax/Control statements.md | PASS | expected 'ok\n' |
| [repeat 0 times](test/reference/case-0265.fimpp) | syntax/Control statements.md | PASS | expected '' |
| [while](test/reference/case-0266.fimpp) | syntax/Control statements.md | PASS | expected '0\n1\n2\n' |
| [catch and finally I did this once](test/reference/case-0267.fimpp) | syntax/Control statements.md | PASS | expected 'caught\nfinally\n' |
| [catch and finally I did this while 1 is equal to 1](test/reference/case-0268.fimpp) | syntax/Control statements.md | PASS | expected 'caught\nfinally\n' |
| [finally on zero iterations](test/reference/case-0269.fimpp) | syntax/Control statements.md | PASS | expected 'finally\n' |
| [uncaught loop error still runs finally](test/reference/case-0270.fimpp) | syntax/Control statements.md | PASS | expected 'finally\n' |
| [Java class java lang math](test/reference/case-0271.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected 'ok\n' |
| [Java class java util hash map](test/reference/case-0272.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected 'ok\n' |
| [Java class org xml sax helpers xml filter impl](test/reference/case-0273.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected 'ok\n' |
| [Java class javax swing j frame](test/reference/case-0274.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected 'ok\n' |
| [Java class regression fixture two](test/reference/case-0275.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected 'ok\n' |
| [constructor](test/reference/case-0276.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [constructor and 9](test/reference/case-0277.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '9\n' |
| [field read tookofit](test/reference/case-0278.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read tookofthem](test/reference/case-0279.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read tookofher](test/reference/case-0280.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read tookofhim](test/reference/case-0281.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read tookfromit](test/reference/case-0282.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read tookfromthem](test/reference/case-0283.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read tookfromher](test/reference/case-0284.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read tookfromhim](test/reference/case-0285.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read gotofit](test/reference/case-0286.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read gotofthem](test/reference/case-0287.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read gotofher](test/reference/case-0288.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read gotofhim](test/reference/case-0289.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read gotfromit](test/reference/case-0290.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read gotfromthem](test/reference/case-0291.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read gotfromher](test/reference/case-0292.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read gotfromhim](test/reference/case-0293.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read stoleofit](test/reference/case-0294.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read stoleofthem](test/reference/case-0295.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read stoleofher](test/reference/case-0296.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read stoleofhim](test/reference/case-0297.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read stolefromit](test/reference/case-0298.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read stolefromthem](test/reference/case-0299.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read stolefromher](test/reference/case-0300.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field read stolefromhim](test/reference/case-0301.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [field write gavecount](test/reference/case-0302.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '9\n' |
| [field write soldcount](test/reference/case-0303.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '9\n' |
| [field write gave"count"](test/reference/case-0304.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '9\n' |
| [field write sold"count"](test/reference/case-0305.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '9\n' |
| [static field set/get](test/reference/case-0306.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '11\n' |
| [method invocation so](test/reference/case-0307.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '10\n' |
| [method invocation if](test/reference/case-0308.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '10\n' |
| [method invocation what](test/reference/case-0309.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '10\n' |
| [method invocation when](test/reference/case-0310.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '10\n' |
| [method invocation how](test/reference/case-0311.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '10\n' |
| [property setter](test/reference/case-0312.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '9\n' |
| [boolean setter/getter](test/reference/case-0313.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected 'yes\n' |
| [boolean false getter](test/reference/case-0314.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected 'no\n' |
| [property getter what](test/reference/case-0315.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [property getter if](test/reference/case-0316.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [property getter when](test/reference/case-0317.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '3\n' |
| [getter arguments](test/reference/case-0318.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected '7\n' |
| [Swing ActionListener](test/reference/case-0319.fimpp) | syntax/Java interop.md; grammar/bnf.tex: Java statements | PASS | expected 'clicked\n' |
| [GUI example parses swing.fimpp](test/reference/case-0320.fimpp) | examples/swing.fimpp | PASS | parse only |
| [GUI example parses gui_calculator.fimpp](test/reference/case-0321.fimpp) | examples/gui_calculator.fimpp | PASS | parse only |
| [wrapped module](test/reference/case-0322.fimpp) | syntax/Program structure.md | PASS | expected 'ok\n' |
| [Sparkle Hello World](test/reference/case-0323.fimpp) | FiM++ 1.0 Language Specification.pdf p.21 | FAIL | expected 'Hello World\n'; parse-error: [1.36] failure: `:' expected but `!' found /  / Dear Princess Celestia: Hello World! /  /                                    ^ |
| [class inheritance and interfaces](test/reference/case-0324.fimpp) | FiM++ 1.0 Language Specification.pdf p.7 | FAIL | parse only; parse-error: [1.15] failure: string matching regex `(?i)\b\Qcelestia\E\b' expected but `L' found /  / Dear Princess Luna and Shining Armor: Letter. Today I learned: Your faithful student, Spike. /               ^ |
| [interface declaration](test/reference/case-0325.fimpp) | FiM++ 1.0 Language Specification.pdf p.8 | FAIL | parse only; parse-error: [1.1] failure: string matching regex `(?i)\b\Qdear\E\b' expected but `P' found /  / Princess Luna: /  / ^ |
| [case sensitive names](test/reference/case-0326.fimpp) | FiM++ 1.0 Language Specification.pdf p.9 | FAIL | expected '1\n2\n'; ok: '2\n2\n' |
| [Unicode/numeric identifier Team Fortress 2](test/reference/case-0327.fimpp) | FiM++ 1.0 Language Specification.pdf p.10 | FAIL | expected '7\n'; parse-error: [4.33] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / Did you know that Team Fortress 2 likes 7? I said Team Fortress 2. /  /                                 ^ |
| [Unicode/numeric identifier Somepony’s true identity](test/reference/case-0328.fimpp) | FiM++ 1.0 Language Specification.pdf p.10 | FAIL | expected '7\n'; parse-error: [4.27] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `’' found /  / Did you know that Somepony’s true identity likes 7? I said Somepony’s true identity. /  /                           ^ |
| [Unicode/numeric identifier Éclair](test/reference/case-0329.fimpp) | FiM++ 1.0 Language Specification.pdf p.10 | FAIL | expected '7\n'; parse-error: [4.19] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `É' found /  / Did you know that Éclair likes 7? I said Éclair. /  /                   ^ |
| [Sparkle literal 31.25](test/reference/case-0330.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected '31.25\n'; parse-error: [4.11] failure: string matching regex `(?i)\b\Qyour\E\b' expected but `2' found /  / I said 31.25. /  /           ^ |
| [Sparkle literal 'A'](test/reference/case-0331.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'A\n'; parse-error: [4.8] failure: string matching regex `[A-Za-z]+(-[A-Za-z]+)*('[A-Za-z]+(-[A-Za-z]+)*)?' expected but `'' found /  / I said 'A'. /  /        ^ |
| [Sparkle literal the letter ‘T’](test/reference/case-0332.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'T\n'; parse-error: [4.19] failure: `!' expected but `‘' found /  / I said the letter ‘T’. /  /                   ^ |
| [Sparkle literal “Princess”](test/reference/case-0333.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'Princess\n'; parse-error: [4.8] failure: string matching regex `[A-Za-z]+(-[A-Za-z]+)*('[A-Za-z]+(-[A-Za-z]+)*)?' expected but `“' found /  / I said “Princess”. /  /        ^ |
| [Sparkle literal the word "adorable"](test/reference/case-0334.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'adorable\n'; parse-error: [4.17] failure: `!' expected but `"' found /  / I said the word "adorable". /  /                 ^ |
| [Sparkle literal yes](test/reference/case-0335.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'true\n'; parse-error: [4.11] failure: ‘Yes’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Yes’? /  / I said yes. /  /           ^ |
| [Sparkle literal true](test/reference/case-0336.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'true\n'; ok: 'True\n' |
| [Sparkle literal right](test/reference/case-0337.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'true\n'; ok: 'Right\n' |
| [Sparkle literal correct](test/reference/case-0338.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'true\n'; ok: 'Correct\n' |
| [Sparkle literal no](test/reference/case-0339.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'false\n'; ok: 'No\n' |
| [Sparkle literal false](test/reference/case-0340.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'false\n'; ok: 'False\n' |
| [Sparkle literal wrong](test/reference/case-0341.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'false\n'; ok: 'Wrong\n' |
| [Sparkle literal incorrect](test/reference/case-0342.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | FAIL | expected 'false\n'; ok: 'Incorrect\n' |
| [Sparkle literal nothing](test/reference/case-0343.fimpp) | FiM++ 1.0 Language Specification.pdf p.12 | PASS | expected 'nothing\n' |
| [typed declaration a number](test/reference/case-0344.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Number\n' |
| [typed declaration a letter](test/reference/case-0345.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Letter\n' |
| [typed declaration a character](test/reference/case-0346.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Character\n' |
| [typed declaration a word](test/reference/case-0347.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Word\n' |
| [typed declaration a phrase](test/reference/case-0348.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Phrase\n' |
| [typed declaration a sentence](test/reference/case-0349.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Sentence\n' |
| [typed declaration a quote](test/reference/case-0350.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: '"\n' |
| [typed declaration a name](test/reference/case-0351.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Name\n' |
| [typed declaration a logic](test/reference/case-0352.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Logic\n' |
| [typed declaration an argument](test/reference/case-0353.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'nothing\n'; ok: 'Argument\n' |
| [constant reassignment](test/reference/case-0354.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected ''; parse-error: [4.46] failure: ‘Is’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Is’? /  / Did you know that Spike always is 1? Spike is now 2. /  /                                              ^ |
| [array declaration write read](test/reference/case-0355.fimpp) | FiM++ 1.0 Language Specification.pdf p.10 | FAIL | expected 'apple cinnamon\n'; parse-error: [4.27] failure: ‘Has’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Has’? /  / Did you know that cake has many names? cake 1 is "chocolate". cake 2 is "apple cinnamon". I said cake 2. /  /                           ^ |
| [initialized array](test/reference/case-0356.fimpp) | FiM++ 1.0 Language Specification.pdf p.11 | FAIL | expected 'fruit\n'; parse-error: [4.27] failure: ‘Has’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Has’? /  / Did you know that cake has the names "chocolate" and "fruit"? I said cake 2. /  /                           ^ |
| [arithmetic add 2 and 3](test/reference/case-0357.fimpp) | FiM++ 1.0 Language Specification.pdf p.13 | FAIL | expected '5\n'; parse-error: [4.12] failure: `!' expected but `2' found /  / I said add 2 and 3. /  /            ^ |
| [arithmetic 2 plus 3](test/reference/case-0358.fimpp) | FiM++ 1.0 Language Specification.pdf p.13 | FAIL | expected '5\n'; parse-error: [4.10] failure: `!' expected but `p' found /  / I said 2 plus 3. /  /          ^ |
| [arithmetic 2 and 3](test/reference/case-0359.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '5\n'; ok: '2, 3\n' |
| [arithmetic 2 added to 3](test/reference/case-0360.fimpp) | FiM++ 1.0 Language Specification.pdf p.13 | FAIL | expected '5\n'; parse-error: [4.10] failure: `!' expected but `a' found /  / I said 2 added to 3. /  /          ^ |
| [arithmetic subtract 5 and 7](test/reference/case-0361.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '-2\n'; parse-error: [4.17] failure: `!' expected but `5' found /  / I said subtract 5 and 7. /  /                 ^ |
| [arithmetic 5 minus 2](test/reference/case-0362.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '3\n'; parse-error: [4.10] failure: `!' expected but `m' found /  / I said 5 minus 2. /  /          ^ |
| [arithmetic 5 without 2](test/reference/case-0363.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '3\n'; parse-error: [4.10] failure: `!' expected but `w' found /  / I said 5 without 2. /  /          ^ |
| [arithmetic the difference between 5 and 2](test/reference/case-0364.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '3\n'; parse-error: [4.31] failure: `!' expected but `5' found /  / I said the difference between 5 and 2. /  /                               ^ |
| [arithmetic multiply 2 and 3](test/reference/case-0365.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '6\n'; parse-error: [4.17] failure: `!' expected but `2' found /  / I said multiply 2 and 3. /  /                 ^ |
| [arithmetic 2 times 3](test/reference/case-0366.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '6\n'; parse-error: [4.10] failure: `!' expected but `t' found /  / I said 2 times 3. /  /          ^ |
| [arithmetic 2 multiplied with 3](test/reference/case-0367.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '6\n'; parse-error: [4.10] failure: `!' expected but `m' found /  / I said 2 multiplied with 3. /  /          ^ |
| [arithmetic divide 8 and 2](test/reference/case-0368.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '4\n'; parse-error: [4.15] failure: `!' expected but `8' found /  / I said divide 8 and 2. /  /               ^ |
| [arithmetic divide 8 by 2](test/reference/case-0369.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '4\n'; parse-error: [4.15] failure: `!' expected but `8' found /  / I said divide 8 by 2. /  /               ^ |
| [arithmetic 8 divided by 2](test/reference/case-0370.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '4\n'; parse-error: [4.10] failure: `!' expected but `d' found /  / I said 8 divided by 2. /  /          ^ |
| [rewriting is now](test/reference/case-0371.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '2\n'; parse-error: [4.37] failure: ‘Is’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Is’? /  / Did you know Spike likes 1? Spike is now 2. I said Spike. /  /                                     ^ |
| [rewriting are now](test/reference/case-0372.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '2\n'; parse-error: [4.38] failure: ‘Are’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Are’? /  / Did you know Spike likes 1? Spike are now 2. I said Spike. /  /                                      ^ |
| [rewriting now like](test/reference/case-0373.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '2\n'; parse-error: [4.43] failure: ‘Like’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Like’? /  / Did you know Spike likes 1? Spike now like 2. I said Spike. /  /                                           ^ |
| [rewriting now likes](test/reference/case-0374.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '2\n'; parse-error: [4.44] failure: ‘Likes’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Likes’? /  / Did you know Spike likes 1? Spike now likes 2. I said Spike. /  /                                            ^ |
| [rewriting become](test/reference/case-0375.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '2\n'; parse-error: [4.42] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / Did you know Spike likes 1? Spike become 2. I said Spike. /  /                                          ^ |
| [rewriting becomes](test/reference/case-0376.fimpp) | FiM++ 1.0 Language Specification.pdf p.14 | FAIL | expected '2\n'; parse-error: [4.43] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / Did you know Spike likes 1? Spike becomes 2. I said Spike. /  /                                           ^ |
| [string concatenation](test/reference/case-0377.fimpp) | FiM++ 1.0 Language Specification.pdf p.15 | FAIL | expected 'gems: 2!\n'; parse-error: [4.44] failure: `!' expected but `S' found /  / Did you know Spike likes 2? I said "gems: "Spike"!". /  /                                            ^ |
| [output thought](test/reference/case-0378.fimpp) | FiM++ 1.0 Language Specification.pdf p.15 | FAIL | expected 'ok\n'; parse-error: [4.3] failure: string matching regex `(?i)\b\Qsold\E\b' expected but `t' found /  / I thought "ok". /  /   ^ |
| [input heard](test/reference/case-0379.fimpp) | FiM++ 1.0 Language Specification.pdf p.15 | FAIL | expected '7\n'; parse-error: [4.31] failure: string matching regex `(?i)\b\Qsold\E\b' expected but `h' found /  / Did you know Spike likes 0? I heard Spike. I said Spike. /  /                               ^ |
| [input read](test/reference/case-0380.fimpp) | FiM++ 1.0 Language Specification.pdf p.15 | FAIL | expected '7\n'; parse-error: [4.31] failure: string matching regex `(?i)\b\Qsold\E\b' expected but `r' found /  / Did you know Spike likes 0? I read Spike. I said Spike. /  /                               ^ |
| [input asked](test/reference/case-0381.fimpp) | FiM++ 1.0 Language Specification.pdf p.15 | FAIL | expected '7\n'; parse-error: [4.42] failure: string matching regex `(?i)\b\Qwhen\E\b' expected but `.' found /  / Did you know Spike likes 0? I asked Spike. I said Spike. /  /                                          ^ |
| [prompt](test/reference/case-0382.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected 'How many?\n7\n'; parse-error: [4.43] failure: string matching regex `(?i)\b\Qwhen\E\b' expected but `"' found /  / Did you know Spike likes 0? I asked Spike "How many?". I said Spike. /  /                                           ^ |
| [comparison is](test/reference/case-0383.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected 'ok\n'; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / If 2 is 2 then: I said "ok". That's what I would do. /  /    ^ |
| [comparison is not](test/reference/case-0384.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected ''; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / If 2 is not 2 then: I said "ok". That's what I would do. /  /    ^ |
| [comparison is less than](test/reference/case-0385.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected ''; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / If 2 is less than 2 then: I said "ok". That's what I would do. /  /    ^ |
| [comparison is not greater than](test/reference/case-0386.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected 'ok\n'; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / If 2 is not greater than 2 then: I said "ok". That's what I would do. /  /    ^ |
| [comparison is greater than](test/reference/case-0387.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected ''; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / If 2 is greater than 2 then: I said "ok". That's what I would do. /  /    ^ |
| [comparison is no less than](test/reference/case-0388.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected 'ok\n'; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / If 2 is no less than 2 then: I said "ok". That's what I would do. /  /    ^ |
| [boolean true and true](test/reference/case-0389.fimpp) | FiM++ 1.0 Language Specification.pdf p.18 | FAIL | expected 'yes\n'; parse-error: [4.12] failure: ‘And’ ain't no pony I've heard of.  /    Do they have tea parties with ‘And’? /  / If true and true: I said "yes". Otherwise: I said "no". That's what I would do. /  /            ^ |
| [boolean false or true](test/reference/case-0390.fimpp) | FiM++ 1.0 Language Specification.pdf p.18 | FAIL | expected 'yes\n'; parse-error: [4.12] failure: ‘Or’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Or’? /  / If false or true: I said "yes". Otherwise: I said "no". That's what I would do. /  /            ^ |
| [boolean either true or true](test/reference/case-0391.fimpp) | FiM++ 1.0 Language Specification.pdf p.18 | FAIL | expected 'no\n'; parse-error: [4.10] failure: ‘Either’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Either’? /  / If either true or true: I said "yes". Otherwise: I said "no". That's what I would do. /  /          ^ |
| [boolean not false](test/reference/case-0392.fimpp) | FiM++ 1.0 Language Specification.pdf p.18 | FAIL | expected 'yes\n'; parse-error: [4.13] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `:' found /  / If not false: I said "yes". Otherwise: I said "no". That's what I would do. /  /             ^ |
| [boolean it's not the case that false](test/reference/case-0393.fimpp) | FiM++ 1.0 Language Specification.pdf p.18 | FAIL | expected 'yes\n'; parse-error: [4.32] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `:' found /  / If it's not the case that false: I said "yes". Otherwise: I said "no". That's what I would do. /  /                                ^ |
| [else Otherwise](test/reference/case-0394.fimpp) | FiM++ 1.0 Language Specification.pdf p.19 | FAIL | expected 'yes\n'; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `1' found /  / If 1 is 2: I said "no". Otherwise: I said "yes". That's what I would do. /  /    ^ |
| [else Or else](test/reference/case-0395.fimpp) | FiM++ 1.0 Language Specification.pdf p.19 | FAIL | expected 'yes\n'; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `1' found /  / If 1 is 2: I said "no". Or else: I said "yes". That's what I would do. /  /    ^ |
| [switch](test/reference/case-0396.fimpp) | FiM++ 1.0 Language Specification.pdf p.19 | FAIL | expected 'two\n'; parse-error: [4.15] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / In regards to 2: On the 1st hoof: I said "one". On the 2nd hoof: I said "two". If all else fails: I said "other". That's what I did. /  /               ^ |
| [while Here's what I did while](test/reference/case-0397.fimpp) | FiM++ 1.0 Language Specification.pdf p.20 | FAIL | expected '0\n1\n'; parse-error: [4.40] failure: ‘What’ ain't no pony I've heard of.  /    Do they have tea parties with ‘What’? /  / Did you know Spike likes 0? Here's what I did while Spike had less than 2: I said Spike. Spike got one more. That's what I did. /  /        |
| [while As long as](test/reference/case-0398.fimpp) | FiM++ 1.0 Language Specification.pdf p.20 | FAIL | expected '0\n1\n'; parse-error: [4.49] failure: ‘Had’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Had’? /  / Did you know Spike likes 0? As long as Spike had less than 2: I said Spike. Spike got one more. That's what I did. /  /                       |
| [do while](test/reference/case-0399.fimpp) | FiM++ 1.0 Language Specification.pdf p.20 | FAIL | expected '0\n1\n'; parse-error: [4.40] failure: ‘What’ ain't no pony I've heard of.  /    Do they have tea parties with ‘What’? /  / Did you know Spike likes 0? Here's what I did: I said Spike. Spike got one more. I did this while Spike had less than 2. /  /               |
| [counting for](test/reference/case-0400.fimpp) | FiM++ 1.0 Language Specification.pdf p.20 | FAIL | expected '1\n2\n3\n'; parse-error: [4.24] failure: ‘From’ ain't no pony I've heard of.  /    Do they have tea parties with ‘From’? /  / For every number x from 1 to 3: I said x. That's what I did. /  /                        ^ |
| [iterating for](test/reference/case-0401.fimpp) | FiM++ 1.0 Language Specification.pdf p.21 | FAIL | expected 'A\nB\n'; parse-error: [4.56] failure: ‘In’ ain't no pony I've heard of.  /    Do they have tea parties with ‘In’? /  / Did you know Spike likes "AB"? For every character c in Spike: I said c. That's what I did. /  /                                                |
| [typed method/return/call](test/reference/case-0402.fimpp) | FiM++ 1.0 Language Specification.pdf p.8 | FAIL | expected '2\n'; parse-error: [2.70] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `.' found /  / I learned echo using a number Spike: I said Spike. Then you get Spike. That's all about echo! /  /                                                         |
| [punctuation / empty statements](test/reference/case-0403.fimpp) | FiM++ 1.0 Language Specification.pdf p.4 | FAIL | expected 'ok\n'; parse-error: [4.13] failure: string matching regex `(?i)\b\Qyour\E\b' expected but `.' found /  / I said "ok"!... /  /             ^ |
| [inline comment](test/reference/case-0404.fimpp) | FiM++ 1.0 Language Specification.pdf p.6 | PASS | expected 'ok\n' |
| [block comment](test/reference/case-0405.fimpp) | FiM++ 1.0 Language Specification.pdf p.6 | PASS | expected 'ok\n' |
| [standalone comparison](test/reference/case-0406.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected ''; parse-error: [4.1] failure: string matching regex `(?i)\b\Qyour\E\b' expected but `2' found /  / 2 is 2. /  / ^ |
| [standalone arithmetic modifies target](test/reference/case-0407.fimpp) | FiM++ 1.0 Language Specification.pdf p.13 | FAIL | expected '3\n'; parse-error: [4.31] failure: string matching regex `(?i)\b\Qsold\E\b' expected but `w' found /  / Did you know Spike likes 1? I would add 2 to Spike. I said Spike. /  /                               ^ |
| [typed return without parameters](test/reference/case-0408.fimpp) | FiM++ 1.0 Language Specification.pdf p.8 | FAIL | expected '2\n'; parse-error: [2.46] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / I learned echo to get a number: Then you get 2. That's all about echo! /  /                                              ^ |
| [alternate method call would](test/reference/case-0409.fimpp) | FiM++ 1.0 Language Specification.pdf p.9 | FAIL | expected 'ok\n'; parse-error: [2.46] failure: ‘About’ ain't no pony I've heard of.  /    Do they have tea parties with ‘About’? /  / I learned echo: I said "ok". That's all about echo! /  /                                              ^ |
| [multiple main methods](test/reference/case-0410.fimpp) | FiM++ 1.0 Language Specification.pdf p.8 | FAIL | expected 'one\ntwo\n'; parse-error: [1.86] failure: ‘About’ ain't no pony I've heard of.  /    Do they have tea parties with ‘About’? /  / Dear Princess Celestia: Letter. Today I learned first: I said "one". That's all about first! Today I learned second: I said "two". Th |
| [array equality](test/reference/case-0411.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected 'equal\n'; parse-error: [4.82] failure: ‘Is’ ain't no pony I've heard of.  /    Do they have tea parties with ‘Is’? /  / Did you know Pinkie likes 1 and 2? Did you know Spike likes 1 and 2? If Pinkie is Spike: I said "equal". That's what I would do. /  /           |
| [mixed type comparison](test/reference/case-0412.fimpp) | FiM++ 1.0 Language Specification.pdf p.16 | FAIL | expected 'equal\n'; parse-error: [4.4] failure: string matching regex `(?i)\b\Qgot\E\b' expected but `2' found /  / If 2 is "2": I said "equal". That's what I would do. /  /    ^ |
| [boolean standalone expression](test/reference/case-0413.fimpp) | FiM++ 1.0 Language Specification.pdf p.18 | FAIL | expected ''; parse-error: [4.9] failure: ‘And’ ain't no pony I've heard of.  /    Do they have tea parties with ‘And’? /  / true and false. /  /         ^ |
| [counting character range](test/reference/case-0414.fimpp) | FiM++ 1.0 Language Specification.pdf p.20 | FAIL | expected 'A\nB\nC\n'; parse-error: [4.27] failure: ‘From’ ain't no pony I've heard of.  /    Do they have tea parties with ‘From’? /  / For every character c from 'A' to 'C': I said c. That's what I did. /  /                           ^ |
| [Binder Hello World](test/reference/case-0415.fimpp) | Binder1.pdf p.3 | FAIL | expected 'Hello, World!\n'; parse-error: [1.35] failure: `:' expected but `!' found /  / Dear Princess Celestia:Hello World! /  /                                   ^ |
| [Binder 100 Mississipis](test/reference/case-0416.fimpp) | Binder1.pdf p.2 | FAIL | expected '1 Mississipi(s)\n2 Mississipi(s)\n3 Mississipi(s)\n4 Mississipi(s)\n5 Mississipi(s)\n6 Mississipi(s)\n7 Mississipi(s)\n8 Mississipi(s)\n9 Mississipi(s)\n10 Mississipi(s)\n11 Mississipi(s)\n12 Mississipi(s)\n13 Mississipi(s)\n14 Mississipi(s)\n15 Mississipi(s)\n16 Mississipi(s)\n17 Mississipi(s)\n18 Mississipi(s)\n19 Mississipi(s)\n20 Mississipi(s)\n21 Mississipi(s)\n22 Mississipi(s)\n23 Mississipi(s)\n24 Mississipi(s)\n25 Mississipi(s)\n26 Mississipi(s)\n27 Mississipi(s)\n28 Mississipi(s)\n29 Mississipi(s)\n30 Mississipi(s)\n31 Mississipi(s)\n32 Mississipi(s)\n33 Mississipi(s)\n34 Mississipi(s)\n35 Mississipi(s)\n36 Mississipi(s)\n37 Mississipi(s)\n38 Mississipi(s)\n39 Mississipi(s)\n40 Mississipi(s)\n41 Mississipi(s)\n42 Mississipi(s)\n43 Mississipi(s)\n44 Mississipi(s)\n45 Mississipi(s)\n46 Mississipi(s)\n47 Mississipi(s)\n48 Mississipi(s)\n49 Mississipi(s)\n50 Mississipi(s)\n51 Mississipi(s)\n52 Mississipi(s)\n53 Mississipi(s)\n54 Mississipi(s)\n55 Mississipi(s)\n56 Mississipi(s)\n57 Mississipi(s)\n58 Mississipi(s)\n59 Mississipi(s)\n60 Mississipi(s)\n61 Mississipi(s)\n62 Mississipi(s)\n63 Mississipi(s)\n64 Mississipi(s)\n65 Mississipi(s)\n66 Mississipi(s)\n67 Mississipi(s)\n68 Mississipi(s)\n69 Mississipi(s)\n70 Mississipi(s)\n71 Mississipi(s)\n72 Mississipi(s)\n73 Mississipi(s)\n74 Mississipi(s)\n75 Mississipi(s)\n76 Mississipi(s)\n77 Mississipi(s)\n78 Mississipi(s)\n79 Mississipi(s)\n80 Mississipi(s)\n81 Mississipi(s)\n82 Mississipi(s)\n83 Mississipi(s)\n84 Mississipi(s)\n85 Mississipi(s)\n86 Mississipi(s)\n87 Mississipi(s)\n88 Mississipi(s)\n89 Mississipi(s)\n90 Mississipi(s)\n91 Mississipi(s)\n92 Mississipi(s)\n93 Mississipi(s)\n94 Mississipi(s)\n95 Mississipi(s)\n96 Mississipi(s)\n97 Mississipi(s)\n98 Mississipi(s)\n99 Mississipi(s)\n100 Mississipi(s)\n'; parse-error: [1.25] failure: string matching regex `[A-Za-z]+(-[A-Za-z]+)*('[A-Za-z]+(-[A-Za-z]+)*)?' expected but `1' found /  / Dear Princess Celestia: 100 Mississipis /  /                         ^ |
| [Binder import directive](test/reference/case-0417.fimpp) | Binder1.pdf p.4 | FAIL | parse only; parse-error: [1.1] failure: string matching regex `(?i)\b\Qdear\E\b' expected but `R' found /  / Remember when I wrote about Applejack? /  / ^ |
