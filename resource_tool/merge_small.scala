import scala.io.Source
import scala.collection.mutable.HashMap
import scala.collection.mutable.HashSet
import java.io.PrintWriter

object Merge {
  def main(args: Array[String]) = {
    var dict = HashMap[String, Int]()
    var vocab = HashSet[String]()
    val dir = args(0)
    val v = Source.fromFile(dir + "all.vocab")
    for(line <- v.getLines) {
      vocab += line.stripLineEnd
    }
    v.close
    val f = Source.fromFile(dir + "all.freq")
    for(line <- v.getLines) {
      val a = line.stripLineEnd.split("\t")
      dict(a(0)) = dict.getOrElse(a(0), 0) + a(1).toInt
    }
    f.close
    val out = new PrintWriter(dir + "all.freq", "utf8")
    for ((k, v) <- dict) 
      out.write("%s\t%d\n".format(k, v))
    out.close
    val out2 = new PrintWriter(dir + "all.vocab", "utf8")
    for (s <- vocab) 
      out2.write("%s\n".format(s))
    out2.close
  }
}
