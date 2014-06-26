import scala.io.Source
import scala.collection.mutable.HashMap
import scala.collection.mutable.HashSet
import java.io.PrintWriter

object MakeVocab {

  def makeCollect(): (HashMap[String, Int], HashSet[String]) = {
    var dict = HashMap[String, Int]()
    var vocab = HashSet[String]()
    for (line <- Source.stdin.getLines if line.split("\t").size == 2) {
      val s = line.split('\t')
      val origin = s(1).split(",")(6)
      dict(origin) = dict.getOrElse(origin, 0) + 1
      vocab += s(0)
    }
    return (dict, vocab)
  }

  def main(args: Array[String]) = {
    if (args.size < 1) {
      println("error: ひとつ以上の引数が必要です")
      sys.exit(1)
    }
    var (dict, vocab) = makeCollect()
    val out = new PrintWriter(args(0).replace(".cab.bz2", ".freq"), "utf8")
    for ((k, v) <- dict) 
      out.write("%s\t%d\n".format(k, v))
    out.close
    val out2 = new PrintWriter(args(0).replace(".cab.bz2", ".vocab"), "utf8")
    for (s <- vocab) 
      out2.write("%s\n".format(s))
    out2.close
  }

}
