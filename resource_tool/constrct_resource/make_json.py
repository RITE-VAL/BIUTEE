# -*- coding: utf-8 -*-
import glob
import json
import sys
import re
from get_document import add_zunded
from itertools import takewhile, dropwhile, product, groupby
from resource_getter import ZundaGetter
sys.path.append(
    "/home/mai-om/local/dist/normalizeNumexp/swig/normalizeNumexp/"
)
from normalize_numexp import NormalizeNumexp, StringVector
from convert_knp import convert_knp


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


def sp_key_val(l):
    k = l[0]
    v = ":".join(l[1:])
    return (k, v)


def analyze_header(l):
    return dict([sp_key_val(ll.split(":")) for ll in l.rstrip().split(" ")])


rr = re.compile(ur"<COREFER_ID:(\w+?)>")


def get_corr(knp_text):
    corr_data = {}
    word_end = 0
    knp = knp_text.split('\n')[1:]
    for pos, line in enumerate(knp):
        if line.startswith("# "):
            continue
        if line.startswith("* "):
            continue
        if line.startswith("+ "):
            if u"COREFER_ID" in line:
                m = rr.search(line)
                if m:
                    pp = pos + 1
                    end = word_end
                    while pp < len(knp) and not knp[pp].startswith("+ "):
                        now_word = knp[pp].split(" ")[0]
                        end += len(now_word)
                        pp += 1
                    l = "{}+{}".format(word_end, end)
                    corr_data[l] = m.groups()[0]
        else:
            word_end += len(line.split(" ")[0])
    ss = sorted(corr_data.items(), key=lambda x: x[1])
    new_corr_data = {}
    for k, v in groupby(ss, key=lambda x: x[1]):
        dd = list(v)
        for i, d in enumerate(dd):
            new_corr_data[d[0]] = [k[0] for k in dd if k != d]
    return new_corr_data


def mix_corr():
    for filename in glob.iglob('[FS]V/my/*.xml.raw.nn.zunda.json'):
        print "{} start..".format(filename)
        sys.stdout.flush()
        data = json.load(open(filename, "r"))
        knp_data = json.load(
            open(filename.replace("raw.nn.zunda", "knp"), "r"))
        dumped_json = data.copy()
        for t_id, t in product(data, ["t1", "t2"]):
            if t not in data[t_id]:
                continue
            dumped_json[t_id][t]["corr"] = get_corr(knp_data[t_id][t]['text'])
            print dumped_json[t_id][t]["corr"]
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(dumped_json, indent=4,
                        sort_keys=True, ensure_ascii=False)
        with open(filename.replace(".zunda", ".zunda.corr"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()


def get_nn(text):
    n = NormalizeNumexp("ja")
    result = StringVector(0)
    n.normalize(text.encode("utf-8"), result)
    return list(result)


def parse_nn(data):
    '''
    「表現タイプ, 表現, 文中での開始位置, 終了位置, 単位, 数量(時間)の下限, 数量(時間)の上限, オプション」
    '''
    dd = data.decode('utf-8').split("*")
    return {
        "type": dd[0],
        "expression": dd[1],
        "start": int(dd[2]),
        "end": int(dd[3]),
        "unit": dd[4],
        "lower": dd[5],
        "upper": dd[6],
        "opt": dd[7]
    }


def get_zunda(text):
    text = text.encode('utf-8')
    zunda = ZundaGetter()
    return zunda.get(text)


def sep_chunk(data):
    data = [dd.split(":") for dd in data]
    return [{
        "word": dd[0],
        "type": dd[1],
        "begin": int(dd[2]),
        "end": int(dd[3])
    } for dd in data]


def mix_ne():
    for filename in glob.iglob('[FS]V/my/*.xml.raw.nn.zunda.corr.json'):
        print "{} start..".format(filename)
        sys.stdout.flush()
        data = json.load(open(filename, "r"))
        ne_data = json.load(
            open(filename.replace("raw.nn.zunda.corr", "ne"), "r"))
        dumped_json = data.copy()
        for t_id, t in product(data, ["t1", "t2"]):
            if t not in data[t_id]:
                continue
            if t_id not in ne_data:
                ne_data[t_id] = {}
            if t not in ne_data[t_id]:
                ne_data[t_id][t] = {}
                ne_data[t_id][t]['data'] = None
            dumped_json[t_id][t]["ne"] = sep_chunk(ne_data[t_id][t]['data'])
            dumped_json[t_id][t]["chunks"] = ne_data[t_id][t]['chunks']
            print dumped_json[t_id][t]["ne"]
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(dumped_json, indent=4,
                        sort_keys=True, ensure_ascii=False)
        with open(filename.replace(".corr", ".corr.ne"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()


def mix_zunda():
    for filename in glob.iglob('[FS]V/my/*.xml.raw.nn.json'):
        print "{} start..".format(filename)
        sys.stdout.flush()
        data = json.load(open(filename, "r"))
        dumped_json = data.copy()
        for t_id, t in product(data, ["t1", "t2"]):
            if t not in data[t_id]:
                continue
            dumped_json[t_id][t]["zunda"] = get_zunda(
                data[t_id][t]['raw_text'])
            print dumped_json[t_id][t]["zunda"]
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(dumped_json, indent=4, sort_keys=True,
                        ensure_ascii=False)
        with open(filename.replace(".nn", ".nn.zunda"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()


def add_nn(knp, nn):
    knp = knp.split("\n")
    start, end, c_count = 0, 0, 0
    pos_dict = {}
    for knp_line in knp:
        knp_line = knp_line.rstrip("\n")
        if not (knp_line.startswith("* ") or
                knp_line.startswith("+ ") or knp_line.startswith("# ")):
            w = knp_line.split(" ")[0]
            end += len(w)
        elif knp_line.startswith("* "):
            for p, n in enumerate(nn):
                if start <= n["start"] and n["end"] <= end:
                    pos_dict[c_count - 1] = p
            start = end
            c_count += 1
    for p, n in enumerate(nn):
        if start <= n["start"] and n["end"] <= end:
            pos_dict[c_count - 1] = p
    c_count, knp_tmp = 0, []
    for knp_line in knp:
        if knp_line.startswith("* "):
            if c_count in pos_dict:
                knp_line = knp_line + "\t" + str(pos_dict[c_count])
            c_count += 1
        knp_tmp.append(knp_line)
    return "\n".join(knp_tmp)


def add_nn_pos_to_knp():
    for filename in glob.iglob('[FS]V/my/*.xml.zunda_knp_1.json'):
        print "{} start..".format(filename)
        sys.stdout.flush()
        data = json.load(open(filename, "r"))
        nn_data = json.load(
            open(filename.replace("zunda_knp_1", "raw.nn"), "r"))
        dumped_json = data.copy()
        for t_id, t in product(data, ["t1", "t2"]):
            if t not in data[t_id]:
                continue
            k = add_nn(dumped_json[t_id][t]["knp"], nn_data[t_id][t]["nn"])
            dumped_json[t_id][t]["knp"] = k
            dumped_json[t_id][t]["nn"] = nn_data[t_id][t]["nn"]
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(dumped_json, indent=4, sort_keys=True,
                        ensure_ascii=False)
        with open(filename.replace(".zunda_knp_1", ".zunda_knp_2"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()


def add_zunda_pos_to_knp():
    for filename in glob.iglob('[FS]V/my/*.xml.zunda_knp.json'):
        print "{} start..".format(filename)
        sys.stdout.flush()
        data = json.load(open(filename, "r"))
        dumped_json = data.copy()
        for t_id, t in product(data, ["t1", "t2"]):
            if t not in data[t_id]:
                continue
            k, z = add_zunded(dumped_json[t_id][t]["zunda"])
            dumped_json[t_id][t]["knp"] = k
            dumped_json[t_id][t]["zunda"] = z
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(dumped_json, indent=4, sort_keys=True,
                        ensure_ascii=False)
        with open(filename.replace(".zunda_knp", ".zunda_knp_1"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()


def make_zunda_knp():
    for filename in glob.iglob('[FS]V/my/*.xml.raw.json'):
        print "{} start..".format(filename)
        sys.stdout.flush()
        data = json.load(open(filename, "r"))
        dumped_json = data.copy()
        for t_id, t in product(data, ["t1", "t2"]):
            if t not in data[t_id]:
                continue
            text = data[t_id][t]
            dumped_json[t_id][t] = {}
            dumped_json[t_id][t]["raw_text"] = text
            dumped_json[t_id][t]["zunda"] = get_zunda(
                text.replace(u" ", u"　")
            ).decode('utf-8')
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(dumped_json, indent=4, sort_keys=True,
                        ensure_ascii=False)
        with open(filename.replace(".raw", ".zunda_knp"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()


def mix_nn():
    for filename in glob.iglob('[FS]V/my/*.xml.raw.json'):
        print "{} start..".format(filename)
        sys.stdout.flush()
        data = json.load(open(filename, "r"))
        dumped_json = {}
        for t_id, t in product(data, ["t1", "t2"]):
            if t not in data[t_id]:
                continue
            if t_id not in dumped_json:
                dumped_json[t_id] = {}
            dumped_json[t_id][t] = {}
            dumped_json[t_id][t]["nn"] = [
                parse_nn(d) for d in get_nn(data[t_id][t])
            ]
            print dumped_json[t_id][t]["nn"]
            dumped_json[t_id][t]["raw_text"] = data[t_id][t]
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(
            dumped_json, indent=4, sort_keys=True, ensure_ascii=False
        )
        with open(filename.replace(".raw", ".raw.nn"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()

if __name__ == '__main__':
    # 関数適当に置く
    # make_zunda_knp()
    add_zunda_pos_to_knp()
    add_nn_pos_to_knp()
    convert_knp()
    # for filename in glob.iglob('FV/my/*.xml.simple.json'):
    #     data = json.load(open(filename, "r"))
    #     for k, v in data.items():
    #         if len(v["t2"]["simple"]) == 0:
    #             print "{} {} {}".format(filename, k, "t2")
    # for filename in glob.iglob('SV/my/*.xml.simple.json'):
    #     data = json.load(open(filename, "r"))
    #     for k, v in data.items():
    #         for t in ["t1", "t2"]:
    #             if len(v[t]["simple"]) == 0:
    #                 print "{} {} {}".format(filename, k, t)
