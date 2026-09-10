import stasiak.karol.fimpp.FimppParser

object PostscriptTests {
  def main(args: Array[String]): Unit = {
    val simple = """Dear Princess Celestia: A letter.
Today I learned about greetings:
I said "Hello, Equestria".
Your faithful student, Twilight Sparkle.
"""
    val wrapped = """Dear Princess Celestia: A letter.
Today I learned about greetings:
I learned about greetings:
I said "Hello, Equestria".
That's about greetings.
Your faithful student, Twilight Sparkle.
"""
    var checks = 0
    def parse(s: String) = FimppParser.parseAll(FimppParser.module, s)
    for (letter <- List(simple, wrapped)) {
      val baseline = parse(letter)
      assert(baseline.successful, baseline.toString)
      val notes = List(
        "PS This is a note.",
        "PSS This is another note without final punctuation",
        "ps lowercase\npss more notes",
        "P.S. One note!\nP.S.S. Another note?",
        "P.S.No space after the marker\nP.P.S.Neither here",
        "P.P.P.S. Multiple P prefixes from the specification",
        "pps: Undotted additional postscript",
        "PS: Colons work.\nPSS: More notes.",
        "PS. A sentence. Another sentence! \"Unmatched quote is fine",
        "PS\nPSS",
        "PS first\n\n  PSS indented\n\tP.S.S.S. A third note\n",
        "PS I said \"This must not execute\".",
        "PS Unicode: friendship is magic — café."
      )
      for (note <- notes; newline <- List("\n", "\r\n")) {
        val parsed = parse((letter + note).replace("\n", newline))
        assert(parsed.successful, parsed.toString)
        assert(parsed.get == baseline.get, "Postscripts changed the program: " + note)
        checks += 1
      }
      for (note <- List("Unexpected trailing text.", "PS one note\nUnmarked text.",
                        "PSYCHOLOGY is not a postscript.", "PSSuffix is not a postscript.")) {
        assert(!parse(letter + note).successful, "Unexpectedly accepted: " + note)
        checks += 1
      }
    }
    for (letter <- List(simple, wrapped)) {
      val baseline = parse(letter).get
      for (withNotes <- List(
        letter.replace("I said", "P.S.An in-body comment.\nI said"),
        letter.replace("I said \"Hello, Equestria\".", "I said \"Hello, Equestria\". P.P.S.An inline note"),
        letter.trim.stripSuffix(".") + "\nPS A note after an unpunctuated signature",
        "P.S.A note before the header\n" + letter)) {
        val parsed = parse(withNotes)
        assert(parsed.successful, parsed.toString)
        assert(parsed.get == baseline, "Inline comment changed the program")
        checks += 1
      }
    }
    val quoted = parse(simple.replace("Hello, Equestria", "P.S.This is literal text; PS and PSS too"))
    assert(quoted.successful, quoted.toString)
    assert(quoted.get != parse(simple).get, "Postscript inside a string was lost")
    checks += 1
    println("PASS " + checks + " postscript parser checks")
  }
}
