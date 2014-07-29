# -*- coding: utf-8 -*-
import solr
import json
import glob
import sys
from itertools import combinations
from resource_getter import zunda, chapas


tokyo = solr.SolrConnection('http://pine12.naist.jp:8983/solr/dic_tokyo')
yamakawa = solr.SolrConnection('http://pine12.naist.jp:8983/solr/dic_yamakawa')


def clean_data(data, ne_data):
    data = [d for d in data if u"(" not in d and u")" not in d]
    if len(ne_data) == 0:
        return data
    tmp_data = []
    for d in data:
        flag = False
        for n in ne_data:
            if d in n:
                tmp_data.append(n)
                flag = True
                break
        if not flag:
            tmp_data.append(d)
    return set(tmp_data)


def get_result(query):
    tokyo_results = tokyo.query(query).results
    yamakawa_results = yamakawa.query(query).results
    if len(tokyo_results) > 0 or len(yamakawa_results) > 0:
        if len(tokyo_results) == 0:
            return yamakawa_results[0]
        elif len(yamakawa_results) == 0:
            return tokyo_results[0]
        else:
            return max([yamakawa_results[0], tokyo_results[0]],
                       key=lambda x: x['score'])
    return None


def add_zunded(zunda_text):
    dd = zunda_text.rstrip("\n").split("\n")
    zunda = [z.split("\t") for z in dd if z.startswith("#EVENT")]
    zunda_tmp = {z[0]: "\t".join(z[1:]) for z in zunda}
    zunda = {int(z[1]): z[0] for z in zunda}
    chapas = dd[len(zunda):]
    word_count, chapas_tmp = 0, []
    for line in chapas:
        line = line.rstrip("\n")
        if not (line.startswith("* ")):
            if word_count in zunda:
                line = line + "\t" + zunda[word_count]
            word_count += 1
        chapas_tmp.append(line)
    return "\n".join(chapas_tmp), zunda_tmp


def fix_text(text):
    return text.replace(u"。", u"。\n").replace(u"\n\n", u"\n")


def doc_to_chapas():
    for filename in glob.iglob('json/*.xml.doc_text.json'):
        done_list = {}
        data = json.load(open(filename))
        dumped_json = data.copy()
        for t_id in data:
            if dumped_json[t_id]["dic_id"] in done_list:
                a_id = done_list[dumped_json[t_id]["dic_id"]]
                dumped_json[t_id]["chapas"] = dumped_json[a_id]["chapas"]
                dumped_json[t_id]["zunda"] = dumped_json[a_id]["zunda"]
                dumped_json[t_id][
                    "fixed_text"
                ] = dumped_json[a_id]["fixed_text"]
            else:
                text = fix_text(data[t_id]["text"]).encode('utf-8')
                k, z = add_zunded(
                    zunda(chapas(text)).decode('utf-8')
                )
                dumped_json[t_id]["chapas"] = k
                dumped_json[t_id]["zunda"] = z
                dumped_json[t_id]["fixed_text"] = text.decode("utf-8")
                done_list[dumped_json[t_id]["dic_id"]] = t_id
            print "{}:{}:{} done.".format(
                filename, t_id, dumped_json[t_id]["dic_id"]
            )
            sys.stdout.flush()
        ss = json.dumps(
            dumped_json, indent=4, sort_keys=True,
            ensure_ascii=False
        )
        outfile = filename.replace(".doc_text", ".doc_text_chapa_zunda")
        with open(outfile, "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} done.".format(filename)
        sys.stdout.flush()


def ne_to_chapas():
    done_buf_list = {}
    for filename in glob.iglob('json/*.xml.doc_*_ne.json'):
        data = json.load(open(filename))
        dumped_json = data.copy()
        for t_id in data:
            target_dic = dumped_json[t_id]["t1"]["dic_id"]
            if target_dic in done_buf_list:
                dumped_json[t_id]["t1"]["doc"] = done_buf_list[target_dic]
            else:
                done_buf_list[target_dic] = []
                length = len(data[t_id]["t1"]["doc"])
                for pos, text in enumerate(data[t_id]["t1"]["doc"]):
                    k, z = add_zunded(
                        zunda(chapas(text.encode("utf-8"))).decode('utf-8')
                    )
                    dumped_json[t_id]["t1"]["doc"][pos] = {
                        "chapas": k, "zunda": z, "text": text
                    }
                    print "{}:{}/{} parsed.".format(target_dic, pos, length)
                done_buf_list[target_dic] = dumped_json[t_id]["t1"]["doc"][:]
                sys.stdout.flush()
            print "{}:{}:{} done.".format(
                filename, t_id, dumped_json[t_id]["t1"]["dic_id"]
            )
            sys.stdout.flush()
        ss = json.dumps(
            dumped_json, indent=4, sort_keys=True,
            ensure_ascii=False
        )
        outfile = filename.replace(".json", "") + "_chapa_zunda.json"
        with open(outfile, "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} done.".format(filename)
        sys.stdout.flush()


def sep_noun():
    fi = glob.glob('json/*.xml.doc_text.json')
    attr = "doc_text"
    for filename in fi:
        data = json.load(open(filename))
        ne_data = json.load(open(filename.replace(attr, 'only_ne')))
        raw_data = json.load(open(filename.replace(attr, 'ne')))
        pas_data = json.load(open(filename.replace(attr, 'pas.zunda')))
        dumped_json = {}
        for t_id in data:
            dumped_json[t_id] = {}
            dumped_json[t_id]["ans"] = raw_data[t_id]["ans"]
            dumped_json[t_id]["t1"] = data[t_id]
            dumped_json[t_id]["t2"] = pas_data[t_id]["t2"]
            dumped_json[t_id]["t2"]["ne"] = raw_data[t_id]["t2"]["data"]
            dumped_json[t_id]["t2"]["except_ne"] = data[t_id]["word"][:]
            dumped_json[t_id]["t2"]["word"] = data[t_id]["word"][:]
            for w in data[t_id]["word"]:
                if w in ne_data[t_id]:
                    dumped_json[t_id]["t2"]["except_ne"].remove(w)
            del dumped_json[t_id]["t1"]["word"]
            dumped_json[t_id]["t1"]["doc"] = fix_text(
                dumped_json[t_id]["t1"]["text"]
            ).split("\n")
            del dumped_json[t_id]["t1"]["text"]
            print "{}:{} done.".format(filename, t_id)
            sys.stdout.flush()
        ss = json.dumps(
            dumped_json, indent=4, sort_keys=True,
            ensure_ascii=False
        )
        with open(filename.replace(attr, attr + "_ne"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} done.".format(filename)
        sys.stdout.flush()


def make_query(nouns, t):
    return " OR ".join([
        "{}:{}".format(
            t, noun.encode('utf-8')
        )
        for noun in nouns
    ]).replace(
        "(", " OR {}:".format(t)
    ).replace(")", " OR {}:".format(t))


def noun_to_doc(rrr, t):
    for filename in glob.iglob('json/*.xml.only_noun.json'):
        data = json.load(open(filename))
        ne_data = json.load(open(filename.replace('noun', 'ne')))
        dumped_json = {}
        for t_id in data:
            dumped_json[t_id] = {}
            noun_list = clean_data(data[t_id], ne_data[t_id])
            noun_length = len(noun_list)
            print noun_length,
            for n in range(noun_length):
                result_tmp = []
                print n,
                sys.stdout.flush()
                for nouns in combinations(noun_list, noun_length - n):
                    query = make_query(nouns, t)
                    res = get_result(query)
                    if res is not None:
                        result_tmp.append(res)
                if len(result_tmp) > 0:
                    dumped_json[t_id] = max(
                        result_tmp, key=lambda x: x['score']
                    )
                    dumped_json[t_id]["word"] = nouns
                    break
            print "{}:{} done.".format(filename, t_id)
            sys.stdout.flush()
        ss = json.dumps(
            dumped_json, indent=4, sort_keys=True,
            ensure_ascii=False
        )
        with open(filename.replace(".only_noun", rrr), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} done.".format(filename)
        sys.stdout.flush()


def main():
    for filename in glob.iglob('json/*.xml.doc_text_chapa_zunda.json.2'):
        data = json.load(open(filename))
        org_data = json.load(open(filename.replace(
            "chapa_zunda.json.2", "ne.json"))
        )
        dumped_json = data.copy()
        for t_id in data:
            if "doc" in data[t_id]:
                dumped_json[t_id]["t1"] = {}
                dumped_json[t_id]["t1"]["doc"] = data[t_id]["doc"]
                dumped_json[t_id]["t1"]["id"] = org_data[t_id]["t1"]["id"]
                dumped_json[t_id]["t1"]["score"] = org_data[t_id]["t1"][
                    "score"]
                dumped_json[t_id]["t1"]["title"] = org_data[t_id]["t1"][
                    "title"]
                dumped_json[t_id]["t1"]["title_exact"] = org_data[t_id][
                    "t1"]["title_exact"]
                dumped_json[t_id]["t1"]["topic"] = org_data[t_id]["t1"][
                    "topic"]
                del dumped_json[t_id]["doc"]
        ss = json.dumps(
            dumped_json, indent=4, sort_keys=True,
            ensure_ascii=False
        )
        with open(filename.replace(".json.2", ".json"), "w") as w:
            w.write(ss.encode("utf-8"))
        print "{} done.".format(filename)
        sys.stdout.flush()


if __name__ == '__main__':
    ne_to_chapas()
