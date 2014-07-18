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


def split_chunks(text):
    d = text[1:]
    tmp_lst = []
    for x in d:
        if len(tmp_lst) > 0 and (
                x.startswith("* ") or x.startswith("EOS")
        ):
            yield tmp_lst
            tmp_lst = []
        tmp_lst.append(x)
    yield tmp_lst


def convert_chunks(chunks):
    chunks_list = []
    sentence_count = 0
    for c in chunks:
        header = c[0]
        dep = int(header.split(" ")[2][:-1])
        chunks_list.append({
            "sent_pos": sentence_count,
            "dep": dep, "words": "\n".join(c[1:])
        })
        if c[-1].startswith("EOS"):
            sentence_count += 1
    return chunks_list


def parse(text):
    text = text.split("\n")
    chunks = split_chunks(chunk_pred, text)
    noun_id = make_noun_id(chunks)
    sentences = {}
    chunk_list = convert_chunks(chunks)
    for chunk_pos, chunk in enumerate(chunks):
        for word_pos, c in enumerate(chunk[1:]):
            if c.startswith("EOS"):
                continue
            pas = c.split("\t")[3]
            if pas == "":
                continue
            pas = convert_pas(pas)
            if "type" in pas and pas["type"] == "pred":
                sentences[chunk_pos] = {}
                sentences[chunk_pos]["suf"] = c.split("\t")[0]
                for case in ["ga", "o", "ni"]:
                    if case in pas:
                        c_id, p_id = noun_id[pas[case]]
                        [c_id]
                        sentences[chunk_pos][case] = {
                            "b_pos": c_id, "rel": case,
                            "words": {
                            }
                        }
    return chunk_list, sentences


def cab_zunda_iter(iterable):
    cab_zunda = {}
    for dd in iterable.split("\n\n")[:-1]:
        data = dd.split("\n%%\n")
        c_id = data[0].split("\n")[0].split(" ")[1]
        cab_zunda[c_id] = {}
        cab_zunda[c_id]["t2"] = None
        if len(data) == 2:
            d1 = data[0].split("\n")
            d2 = data[1].split("\n")
            cab_zunda[c_id]["t1"] = {
                d.split("\t")[0]: "\t".join(d.split("\t")[1:])
                for d in filter(lambda x: x.startswith("#EVENT"), d1)
            }
            cab_zunda[c_id]["t2"] = {
                d.split("\t")[0]: "\t".join(d.split("\t")[1:])
                for d in filter(lambda x: x.startswith("#EVENT"), d2)
            }
        else:
            d2 = data[0].split("\n")
            cab_zunda[c_id]["t2"] = {
                d.split("\t")[0]: "\t".join(d.split("\t")[1:])
                for d in filter(lambda x: x.startswith("#EVENT"), d2)
            }
    return cab_zunda


def add_info_to_pas(chapas, nn, zunda):
    return chapas


def main():
    for filename in glob.iglob('[FS]V/my/*.xml.pas.json'):
        data = json.load(open(filename, "r"))
        zunda = cab_zunda_iter(
            open(
                filename.replace("pas.json", "cab_zunda"), "r"
            ).read().decode('utf-8')
        )
        raw_data = json.load(
            open(filename.replace("pas", "raw"), "r")
        )
        raw_nn = json.load(
            open(filename.replace("pas", "raw.nn"), "r")
        )
        dumps_json = data.copy()
        for text_id, t in product(data, ["t1", "t2"]):
            if t not in dumps_json[text_id]:
                continue
            if "category" in raw_data:
                dumps_json[text_id]["category"] = raw_data["category"]
            # nn と zunda を 追加
            dumps_json[text_id][t]['zunda'] = zunda[text_id][t]
            dumps_json[text_id][t]["raw_text"] = raw_data[text_id][t]
            dumps_json[text_id][t]['chapas'] = data[text_id][t]['text']
            dumps_json[text_id][t]['nn'] = raw_nn[text_id][t]['nn']
            dumps_json[text_id][t]['chapas'] = add_info_to_pas(
                data[text_id][t]['text'], raw_nn[text_id][t]['nn'],
                zunda[text_id][t]
            )
            c, s = parse(data[text_id][t]['text'])
            dumps_json[text_id][t]['chunks'] = c
            dumps_json[text_id][t]['simple'] = s
            del dumps_json[text_id][t]["text"]
        ss = json.dumps(dumps_json, indent=4,
                        sort_keys=True, ensure_ascii=False)
        with open(filename.replace("pas", "chapas_simple"), "w") as w:
            w.write(ss.encode("utf-8"))


if __name__ == '__main__':
    main()
