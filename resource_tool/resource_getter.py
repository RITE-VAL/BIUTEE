# -*- coding: utf-8 -*-
import sys
import shlex
from subprocess import Popen, PIPE
sys.path.append(
    "/home/mai-om/local/dist/normalizeNumexp/swig/normalizeNumexp/"
)
from normalize_numexp import NormalizeNumexp, StringVector


'''
resource_getter:
  各情報をテキストを基に得るワラッパー

how to use:

  from resource_getter import *
  text = テキスト
  syncha_getter = SynchaGettar()  # Synchaの場合
  result = syncha_getter.get(text)

'''


class ZundaGetter(object):

    def __init__(self):
        self.path = '/home/mai-om/local/bin/zunda'
        self.knp = '/home/mai-om/local/bin/knp'
        self.juman = '/home/mai-om/local/bin/juman'

    def _detail_parse(self, items):
        return {
            "zisei": items[3],
            "kasou": items[4],
            "taido": items[5],
            "singi": items[6],
            "kati": items[7]
        }

    def _parse(self, result):
        result = result.decode('utf-8')
        rr = [r.split("\t") for r in result.split("\n")
              if r.startswith("#EVENT")]
        return {int(r[0][6:]): self._detail_parse(r) for r in rr}

    def _getResult(self, text):
        cmd1 = Popen(shlex.split(self.juman), stdin=PIPE,
                     stdout=PIPE, stderr=PIPE)
        cmd1.stdout.close()
        cmd2 = Popen(shlex.split(self.knp), stdin=cmd1.stdout,
                     stdout=PIPE, stderr=PIPE)
        cmd2.stdout.close()
        cmd = Popen(shlex.split(self.path), stdin=cmd2.stdout,
                    stdout=PIPE, stderr=PIPE)
        cmd.stdin.write(text)
        return cmd.communicate()[0].rstrip()

    def get(self, text):
        if isinstance(text, unicode):
            text = text.encode("UTF-8")
        return self._getResult(text)


class NNGetter(object):

    def __init__(self):
        pass

    def _parse_nn(self, data):
        dd = data.split("*")
        return {
            "type": dd[0],
            "expression": dd[1],
            "start": dd[2],
            "end": dd[3],
            "unit": dd[4],
            "lower": dd[5],
            "upper": dd[6],
            "opt": dd[7]
        }

    def _getResult(self, text):
        n = NormalizeNumexp("ja")
        result = StringVector(0)
        n.normalize(text, result)
        return [self._parse_nn(d) for d in list(result)]

    def get(self, text):
        if isinstance(text, unicode):
            text = text.encode("UTF-8")
        return self._getResult(text)


class ChaPASGetter(object):

    def __init__(self):
        self.path = "/home/mai-om/local/dist/chapas-0.742"
        self.cmd = "java -jar {path}/chapas.jar -I RAW".format(path=self.path)

    def _getResult(self, sentence):
        p2 = Popen(shlex.split(self.cmd), stdin=PIPE, stdout=PIPE)
        out, err = p2.communicate(input=sentence)
        return out.rstrip()

    def get(self, text):
        if isinstance(text, unicode):
            text = text.encode("UTF-8")
        return self._getResult(text)


class SynchaGetter(object):

    def __init__(self):
        self.path = '/home/mai-om/local/dist/syncha-0.3/syncha'

    def _getResult(self, sentence):
        syncha = Popen(shlex.split(self.path), stdin=PIPE,
                       stdout=PIPE, stderr=PIPE)
        syncha.stdin.write(sentence)
        return syncha.communicate()[0].rstrip()

    def get(self, text):
        if isinstance(text, unicode):
            text = text.encode("UTF-8")
        return self._getResult(text)


if __name__ == '__main__':
    text = u"太郎が彼に殴られた"
    syn = ChaPASGetter()
    print syn.get(text)
    text = u"ペリーは蒸気船を配備した東インド艦隊を引きいて、嘉永6年6月3日（1853年7月8日）浦賀沖に来航し、6月9日（7月14日）に開国を求めるアメリカ大統領国書を提出した後、日本を離れたが、幕府では老中阿部正弘らを中心に、諸大名から庶民まで幅広く意見を求め、嘉永7年（1854年）1月にペリーが再来航し、日米和親条約を締結した。"
    nn = NNGetter()
    print nn.get(text)
    zunda = ZundaGetter()
    for i in range(10):
        print zunda.get(text)
