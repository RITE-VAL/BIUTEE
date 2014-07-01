# -*- coding: utf-8 -*-
import json
import glob
from itertools import takewhile, dropwhile, product


def chunk_pred(x):
    return not x.startswith("* ") and x != "EOS"


def convert_pas(x):
    itm = x.split(" ")[:-1]
    return dict([(it.split("=")[0], it.split("=")[1][1:-1]) for it in itm])


def takewhile_repeat(pred, iterable):
    tmp_lst, lst = list(iterable)[0:1], list(iterable)[1:]
    while True:
        yield tmp_lst + list(takewhile(pred, lst))
        lst = list(dropwhile(pred, lst))
        if len(lst) == 0:
            break
        tmp_lst, lst = lst[0:1], lst[1:]


def make_noun_id(chunks):
    noun_id = {}
    for chunk_pos, chunk in enumerate(chunks):
        if chunk[0] == u"EOS":
            continue
        for word_pos, word in enumerate(chunk[1:]):
            inf = word.split("\t")
            if inf[3] != "":
                pas_info = convert_pas(inf[3])
                if "ID" in pas_info:
                    noun_id[pas_info["ID"]] = (chunk_pos, word_pos)
    return noun_id


def parse(text):
    text = text.encode("utf-8").split("\n")
    chunks = list(takewhile_repeat(chunk_pred, text))
    noun_id = make_noun_id(chunks)
    sentences = []
    tmp_sent = []
    chunk_list = []
    dep_list = []
    for chunk_pos, chunk in enumerate(chunks):
        if chunk[0] == u"EOS":
            if len(tmp_sent) > 0:
                sentences.append({"pas": None, "words": tmp_sent})
            continue
        tmp_sent.append(["\t".join(c.split("\t")[:2]) for c in chunk[1:]])
        chunk_list.append(["\t".join(c.split("\t")[:2]) for c in chunk[1:]])
        dep_list.append([chunk[0]])
        for word_pos, word in enumerate(chunk[1:]):
            inf = word.split("\t")
            if inf[3] != "":
                pas_info = convert_pas(inf[3])
                if "type" in pas_info and pas_info["type"] == "pred":
                    for c in ["ga", "o", "ni"]:
                        if c in pas_info:
                            pas_info[c] = noun_id[pas_info[c]]
                    sentences.append({"pas": pas_info, "words": tmp_sent})
                    tmp_sent = []
    return {"chunks": chunk_list, "short_sentences": sentences}


def main():
    for filename in glob.iglob('[FS]V/my/*.xml.pas.json'):
        data = json.load(open(filename, "r"))
        raw_data = json.load(open(filename.replace("pas", "raw"), "r"))
        dumps_json = {}
        for text_id, t in product(data, ["t1", "t2"]):
            if t not in data[text_id]:
                continue
            if text_id not in dumps_json:
                dumps_json[text_id] = {"ans": data[text_id]["ans"]}
                if "category" in raw_data[text_id]:
                    dumps_json[text_id]["category"] = raw_data[
                        text_id]["category"].encode("utf-8")
            dumps_json[text_id][t] = parse(data[text_id][t]['text'])
            dumps_json[text_id][t]["raw_text"] = raw_data[text_id][t].encode(
                "utf-8"
            )
        json.dump(dumps_json, open(filename.replace("pas", "short"), "w"),
                  indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    main()
