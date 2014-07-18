# -*- coding: utf-8 -*-
from collections import defaultdict

'''
document to json data
'''


def get_basic_chunk(knp):
    for knp_line in knp:
        if knp_line.startswith("+ "):
            yield knp_line


def get_eid(knp):
    bpos_to_eid_map = defaultdict(lambda: [])
    count = 0
    for knp_line in knp:
        if knp_line.startswith("+ "):
            data = knp_line.split(" ")[2][1:-1].split("><")
            for d in data:
                if u"EID:" in d:
                    bpos_to_eid_map[int(d.split(":")[1])].append(count)
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
            rel, typ = t[0], t[1]
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
        new_pas[pred_pos] = {
            'suf': p['pred'], 'words': e_map[pred_pos]['words']
        }
        for n in n_pas.split(";"):
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
            cands = [int(b_pos)]
            deps = [a for a, v in enumerate(e_map)
                    if v["dep"] == cands[0] and a != pred_pos]
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
    convert_knp_to_pas: KNPからSimple文を作る．
      KNP は たまに失敗？して格解析結果が表示されないので，
      そのときは述語項構造からsimpleな文を作る
    '''
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


def parse_nn(data):
    '''
    「表現タイプ, 表現, 文中での開始位置, 終了位置, 単位, 数量(時間)の下限, 数量(時間)の上限, オプション」
    '''
    dd = data.split("*")
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


def add_zunded(zunda_text):
    dd = zunda_text.rstrip("\n").split("\n")
    zunda = [z.split("\t") for z in dd if z.startswith("#EVENT")]
    zunda_tmp = {z[0]: "\t".join(z[1:]) for z in zunda}
    zunda = {int(z[1]): z[0] for z in zunda}
    knp = dd[len(zunda):]
    word_count, knp_tmp = 0, []
    for knp_line in knp:
        knp_line = knp_line.rstrip("\n")
        if not (knp_line.startswith("* ") or
                knp_line.startswith("+ ") or knp_line.startswith("# ")):
            if word_count in zunda:
                knp_line = knp_line + "\t" + zunda[word_count]
            word_count += 1
        knp_tmp.append(knp_line)
    return "\n".join(knp_tmp), zunda_tmp


def add_nn(knp, nn):
    knp = knp.split("\n")
    start, end, c_count = 0, 0, 0
    pos_dict = {}
    for knp_line in knp:
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


def convert_nn(nn_text):
    nn_text = nn_text.rstrip("\n")
    if nn_text != "END":
        return [parse_nn(n) for n in nn_text.split("\n")[:-1]]
    else:
        return []


def convert_json(raw_text, zunda_text, nn_text):
    dumped_json = {}
    dumped_json["raw_text"] = raw_text
    dumped_json["nn"] = convert_nn(nn_text)
    k, z = add_zunded(zunda_text)
    dumped_json["knp"] = k
    dumped_json["zunda"] = z
    dumped_json["knp"] = add_nn(k, dumped_json["nn"])
    e, k = convert_knp_to_pas(dumped_json["knp"])
    dumped_json["simple"] = k
    dumped_json["chunks"] = e
    return dumped_json


if __name__ == '__main__':
    pass
