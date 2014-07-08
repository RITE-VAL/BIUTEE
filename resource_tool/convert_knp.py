# -*- coding: utf-8 -*-
import json
import sys
import glob
from itertools import product


def get_eid(knp):
    bpos_to_eid_map = {}
    count = 0
    for knp_line in knp:
        if knp_line.startswith("+ "):
            data = knp_line.split(" ")[2][1:-1].split("><")
            for d in data:
                if u"EID:" in d:
                    if int(d.split(":")[1]) in bpos_to_eid_map:
                        bpos_to_eid_map[int(d.split(":")[1])].append(count)
                    else:
                        bpos_to_eid_map[int(d.split(":")[1])] = [count]
            count += 1
    return bpos_to_eid_map


def get_pas_and_word_from_case(knp):
    tmp_word, words, pas, dep, count = [], [], [], None, 0
    basic_chunk_list = []
    for knp_line in knp:
        if knp_line.startswith("+ "):
            if not (dep is None):
                words.append([dep] + tmp_word)
                tmp_word = []
            data = knp_line.split(" ")[2][1:-1].split("><")
            for d in data:
                if u"格解析結果:" in d:
                    dd = d.split(":")
                    if len(dd) < 4:
                        continue
                    elif len(dd) > 4:
                        pas.append(
                            {"pred": dd[1], "case_num": dd[2],
                             "pas": ":".join(dd[3:]), "pos": count}
                        )
                    else:
                        pas.append(
                            {"pred": dd[1], "case_num": dd[2],
                             "pas": dd[3], "pos": count}
                        )
            basic_chunk_list.append(knp_line)
            dep = knp_line.split(" ")[1]
            count += 1
        elif not (knp_line.startswith("* ") or knp_line.startswith("# ")):
            tmp_word.append(knp_line)
    words.append([dep] + tmp_word[:-1])
    return words, pas, basic_chunk_list


def get_pas_from_pas(basic_chunk_list):
    pas = []
    for count, knp_line in enumerate(basic_chunk_list):
        data = knp_line.split(" ")[2][1:-1].split("><")
        for d in data:
            if u"述語項構造:" in d:
                dd = d.split(":")
                if len(dd) < 4:
                    continue
                elif len(dd) > 4:
                    pas.append(
                        {"pred": dd[1], "case_num": dd[2],
                         "pas": ":".join(dd[3:]), "pos": count}
                    )
                else:
                    pas.append(
                        {"pred": dd[1], "case_num": dd[2],
                         "pas": dd[3], "pos": count}
                    )
    return pas


def get_case_info(n, eid_map, no_case_flag):
    t = n.split('/')
    if no_case_flag:
        # 述語項: t = ガ/O/麻生太郎/1
        if len(t) == 4:
            rel, typ, suf, b_pos = t
        else:
            # ガ/O/A/B/1 のような状況
            rel = t[0]
            typ = t[1]
            suf = "/".join(t[2:-1])
            b_pos = t[-1]
        b_pos = eid_map[int(b_pos)]
        return rel, typ, suf, b_pos, None
    # 格解析: t = ガ/N/太郎/0/0/1
    if len(t) == 6:
        rel, typ, suf, b_pos, prev_sent_num = t[:-1]
    else:
        rel, typ = t[0], t[1]
        b_pos = t[-3]
        prev_sent_num = t[-2]
        suf = "/".join(t[2:-3])
    return rel, typ, suf, b_pos, prev_sent_num


def make_pas_from_case(pas, e_map, eid_map, no_case_flag):
    new_pas = {}
    for p in pas:
        pred_pos, n_pas = int(p['pos']), p['pas']
        new_pas[pred_pos] = {}
        new_pas[pred_pos]['suf'] = p['pred']
        new_pas[pred_pos]['words'] = e_map[pred_pos]['words']
        for n in n_pas.split(";"):
            print(n)
            rel, typ, suf, b_pos, prev_sent_num = get_case_info(
                n, eid_map, no_case_flag
            )
            if isinstance(b_pos, list):
                # 共参照解析関係は述語に近い方を採用
                if len(b_pos) == 1:
                    b_pos = b_pos[0]
                else:
                    b_pos = min(b_pos, key=lambda x: abs(x - pred_pos))
            if b_pos == "-":
                continue
            new_pas[pred_pos][rel] = {
                "rel": rel, "type": typ, "suf": suf,
                "b_pos": int(b_pos) if not isinstance(b_pos, int) else b_pos,
                "prev_sent": (int(prev_sent_num)
                              if prev_sent_num is not None else "NONE")
            }
            cand = int(b_pos)
            cands = [cand]
            deps = [a for a, v in enumerate(e_map)
                    if v["dep"] == cand and a != pred_pos]
            while len(deps) > 0:
                cands = deps + cands
                deps = []
                for b in deps:
                    ds = [a for a, v in enumerate(e_map)
                          if v["dep"] == b and a != pred_pos]
                    deps = ds + deps
            new_pas[pred_pos][rel]["words"] = {
                a: e_map[a]['words'] for a in cands
            }
    return new_pas


def convert_knp_to_pas(knp):
    '''
    KNP は たまに失敗？して格解析結果が表示されないので，
    そのときは述語項構造からsimpleな文を作る
    '''
    # print knp
    knp = knp.split("\n")
    words, pas, basic_chunk_list = get_pas_and_word_from_case(knp)
    no_case_flag = False
    if len(pas) == 0:
        no_case_flag = True
    eid_map = None
    if no_case_flag:
        eid_map = get_eid(knp)
        pas = get_pas_from_pas(basic_chunk_list)
    basic_chunk = []
    for w in words:
        basic_chunk.append({"dep": int(w[0][:-1]), "words": "\n".join(w[1:])})
    new_pas = make_pas_from_case(pas, basic_chunk, eid_map, no_case_flag)
    return basic_chunk, new_pas


def convert_knp():
    for filename in glob.iglob('[FS]V/my/*.xml.zunda_knp_2.json'):
        print "{} start..".format(filename)
        sys.stdout.flush()
        data = json.load(open(filename, "r"))
        dumped_json = data.copy()
        for t_id, t in product(data, ["t1", "t2"]):
            print "{}:{} start.".format(t_id, t),
            if t not in data[t_id]:
                continue
            e, k = convert_knp_to_pas(dumped_json[t_id][t]["knp"])
            dumped_json[t_id][t]["simple"] = k
            dumped_json[t_id][t]["chunks"] = e
            print "{}:{} done.".format(t_id, t)
            sys.stdout.flush()
        ss = json.dumps(dumped_json, indent=4, sort_keys=True,
                        ensure_ascii=False)
        with open(filename.replace(".zunda_knp_2", ".knp_simple"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} end..".format(filename)
        sys.stdout.flush()


if __name__ == '__main__':
    pass
