# -*- coding: utf-8 -*-
import glob
import json
import sys
import re
from itertools import takewhile, dropwhile, product, groupby
from resource_getter import ZundaGetter
sys.path.append(
    "/home/mai-om/local/dist/normalizeNumexp/swig/normalizeNumexp/"
)
from normalize_numexp import NormalizeNumexp, StringVector


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
            dumped_json[t_id][t]["nn"] = [parse_nn(d) for d in get_nn(data[t_id][t])]
            print dumped_json[t_id][t]["nn"]
            dumped_json[t_id][t]["raw_text"] = data[t_id][t]
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(dumped_json, indent=4, sort_keys=True, ensure_ascii=False)
        with open(filename.replace(".raw", ".raw.nn"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()


def convert_raw():
    for filename in glob.iglob('[FS]V/my/*.xml.raw'):
        jfilename = filename + ".json"
        dumped_dict = {}
        with open(filename, 'r') as r:
            for line in r:
                line = line.rstrip("\n").split("\t")
                if len(line) == 5:
                    t_id, t1, t2, ans, cate = line
                    dumped_dict[t_id] = {
                        "t1": t1, "t2": t2, "ans": ans, "category": cate
                    }
                elif len(line) == 4:
                    t_id, t1, t2, ans = line
                    dumped_dict[t_id] = {
                        "t1": t1, "t2": t2, "ans": ans
                    }
                else:
                    t_id, t2, ans = line
                    dumped_dict[t_id] = {
                        "t2": t2, "ans": ans
                    }
        json.dump(dumped_dict, open(jfilename, 'w'),
                  sort_keys=True, indent=4, ensure_ascii=False)


def convert_ne():
    for filename in glob.iglob('[FS]V/my/*.xml.ne'):
        jfilename = filename + ".json"
        dumped_dict = {}
        with open(filename, 'r') as r:
            t1_flag = False
            for line in r:
                line = line.rstrip("\n").split("\t")
                if len(line) == 6:
                    t_pos, d_pos, c, w_pos = 3, 4, line[2], 5
                else:
                    t_pos, d_pos, c, w_pos = 2, 3, None, 4
                if line[t_pos] == "t2":
                    if not t1_flag:
                        dumped_dict[line[0]] = {}
                        dumped_dict[line[0]]["ans"] = line[1]
                        if c:
                            dumped_dict[line[0]]["category"] = line[2]
                    t1_flag = False
                    dumped_dict[line[0]]["t2"] = {}
                    dumped_dict[line[0]]["t2"]["data"] = line[d_pos].split(" ")
                    if dumped_dict[line[0]]["t2"]["data"][0] == "":
                        dumped_dict[line[0]]["t2"]["data"] = []
                    dumped_dict[line[0]]["t2"]["chunks"] = line[w_pos].split(
                        " "
                    )
                else:
                    dumped_dict[line[0]] = {}
                    dumped_dict[line[0]]["ans"] = line[1]
                    if c:
                        dumped_dict[line[0]]["category"] = line[2]
                    t1_flag = True
                    dumped_dict[line[0]]["t1"] = {}
                    dumped_dict[line[0]]["t1"]["data"] = line[d_pos].split(" ")
                    if dumped_dict[line[0]]["t1"]["data"][0] == "":
                        dumped_dict[line[0]]["t1"]["data"] = []
                    dumped_dict[line[0]]["t1"]["chunks"] = line[w_pos].split(
                        " "
                    )
        json.dump(dumped_dict, open(jfilename, 'w'),
                  sort_keys=True, indent=4, ensure_ascii=False)


def convert_knp():
    for filename in glob.iglob('[FS]V/my/*.xml.knp'):
        jfilename = filename + ".json"
        dumped_dict = {}
        with open(filename, 'r') as r:
            data = r.read().replace("EOS\n% ID:", "EOS\n\n% ID:")
        data = data.split('\n\n')
        for d in data:
            d_dic = {}
            dd = d.split("\n")
            dic = analyze_header(dd[0])
            data_id, ans = dic['ID'], dic['ans']
            cate = dic.get('c', None)
            ts = "\n".join(dd[1:]).replace("EOS\n%", "EOS\n\n%").split("\n\n")
            d_dic['t2'] = {}
            if len(ts) == 2:
                d_dic['t1'] = {}
            for t in ts:
                tt = t.split("\n")
                d_dic[tt[0].split(" ")[1]]['data'] = "\n".join(tt[1:])
            dumped_dict[data_id] = {}
            dumped_dict[data_id]['ans'] = ans
            dumped_dict[data_id]['t2'] = d_dic['t2']
            if len(ts) == 2:
                dumped_dict[data_id]['t1'] = d_dic['t1']
            if cate is not None:
                dumped_dict['category'] = cate
        json.dump(dumped_dict, open(jfilename, 'w'),
                  sort_keys=True, indent=4, ensure_ascii=False)


def convert_chapas():
    for filename in glob.iglob('[FS]V/my/*.xml.pas'):
        jfilename = filename + ".json"
        dumped_dict = {}
        with open(filename, 'r') as r:
            data = r.read()
        data = data.split('\n\n')[:-1]
        for d in data:
            d_dic = {}
            ts = d.replace("EOS\n#", "EOS\n\n#").split("\n\n")
            d_dic['t2'], data_id, ans, cate = {}, None, None, None
            if len(ts) == 2:
                d_dic['t1'] = {}
            for t in ts:
                tt = t.split("\n")
                dic = analyze_header(tt[0])
                data_id, ans = dic['id'], dic['label']
                d_dic[dic['tag']]['text'] = "\n".join(tt[1:])
                if 'category' in dic:
                    cate = dic['category']
            dumped_dict[data_id] = {}
            dumped_dict[data_id]['ans'] = ans
            dumped_dict[data_id]['t2'] = d_dic['t2']
            if len(ts) == 2:
                dumped_dict[data_id]['t1'] = d_dic['t1']
            if cate is not None:
                dumped_dict['category'] = cate
        json.dump(dumped_dict, open(jfilename, 'w'),
                  sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # 関数適当に置く
    convert_ne()
    mix_ne()
