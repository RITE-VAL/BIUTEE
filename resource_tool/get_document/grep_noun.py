# -*- coding: utf-8 -*-
import json


files1 = ["RITE2_JA_testlabel_examsearch.xml.pas.json",
          "RITE2_JA_dev_examsearch.xml.pas.json"]
files2 = ["RITE2_JA_testlabel_examsearch.xml.ne.json",
          "RITE2_JA_dev_examsearch.xml.ne.json"]


def main2():
    for fi in files2:
        data = json.load(open(fi, "r"))
        dumped_json = {}
        for t_id in data:
            dumped_json[t_id] = set([])
            for d in data[t_id]["t2"]["data"]:
                dumped_json[t_id].add(d.split(":")[0])
            dumped_json[t_id] = list(dumped_json[t_id])
        ss = json.dumps(
            dumped_json, indent=4, sort_keys=True,
            ensure_ascii=False
        )
        with open(fi.replace(".ne", ".only_ne"), "w") as w:
            w.write(ss.encode("utf-8"))


def main1():
    for fi in files1:
        data = json.load(open(fi, "r"))
        dumped_json = {}
        for t_id in data:
            dumped_json[t_id] = set([])
            pas = data[t_id]["t2"]["text"]
            for l in pas.split("\n"):
                if l.startswith("* ") or l.startswith("EOS"):
                    continue
                l = l.rstrip("\n").split("\t")
                if l[1].startswith(u"名詞"):
                    dumped_json[t_id].add(l[0])
            dumped_json[t_id] = list(dumped_json[t_id])
        ss = json.dumps(
            dumped_json, indent=4, sort_keys=True,
            ensure_ascii=False
        )
        with open(fi.replace(".pas", ".only_noun"), "w") as w:
            w.write(ss.encode("utf-8"))

if __name__ == '__main__':
    main1()
    main2()
    files = ["RITE2_JA_testlabel_examsearch.xml.only_ne.json",
             "RITE2_JA_dev_examsearch.xml.only_ne.json"]
    files3 = ["RITE2_JA_testlabel_examsearch.xml.only_noun.json",
              "RITE2_JA_dev_examsearch.xml.only_noun.json"]
    s = set()
    for f in files:
        data = json.load(open(f, "r"))
        s.update([a for d, v in data.items() for a in v])
    with open("only_ne.txt", "w") as w:
        for ss in s:
            w.write("{}\n".format(ss.encode('utf-8')))
    s = set()
    for f in files3:
        data = json.load(open(f, "r"))
        s.update([a for d, v in data.items() for a in v])
    with open("only_noun.txt", "w") as w:
        for ss in s:
            w.write("{}\n".format(ss.encode('utf-8')))
