import stasiak.karol.fimpp.FimppParser
import java.io.{ByteArrayInputStream, ByteArrayOutputStream, PrintStream}
import java.util.Base64
import scala.io.Source
import scala.util.control.NonFatal

object ReferenceRunner {
  def decode(s: String) = new String(Base64.getDecoder.decode(s), "UTF-8")
  def encode(s: String) = Base64.getEncoder.encodeToString(s.getBytes("UTF-8"))
  def main(args: Array[String]): Unit = {
    val lines = Source.fromFile(args(0), "UTF-8")
    try for (line <- lines.getLines()) {
      val fields = line.split("\t", -1)
      val output = new ByteArrayOutputStream
      var status = "ok"
      var detail = ""
      try {
        val parsed = FimppParser.parseAll(FimppParser.module, decode(fields(1)))
        if (!parsed.successful) { status = "parse-error"; detail = parsed.toString }
        else if (fields(3) != "parse-only") {
          Console.withIn(new ByteArrayInputStream(decode(fields(2)).getBytes("UTF-8"))) {
            Console.withOut(new PrintStream(output, true, "UTF-8")) { parsed.get.run() }
          }
        }
      } catch { case NonFatal(e) => status = "runtime-error"; detail = e.toString }
      println(fields(0) + "\t" + status + "\t" + encode(output.toString("UTF-8")) + "\t" + encode(detail))
    } finally lines.close()
  }
}
