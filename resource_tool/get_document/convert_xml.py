# -*- coding: utf-8 -*-
import json
import sys
from ET import xml_iter
from resource_getter import zunda, chapas


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


def dump_json(dumped_json, filename):
    ss = json.dumps(
        dumped_json, indent=4, sort_keys=True,
        ensure_ascii=False
    )
    with open(filename, "w") as w:
        w.write(ss.encode("utf-8"))
    sys.stderr.write("{} done.\n".format(filename))


def convert_xml_to_pas_zunda(filename):
    dumped_json = {}
    for pair in xml_iter(filename):
        n_id = pair.attrib['id']
        ans = pair.attrib['label']
        t1, t2 = pair.find('t1'), pair.find('t2')
        k1, z1 = add_zunded(
            zunda(chapas(t1.text.encode('utf-8'))).decode('utf-8')
        )
        k2, z2 = add_zunded(
            zunda(chapas(t2.text.encode('utf-8'))).decode('utf-8')
        )
        dumped_json[n_id] = {
            'ans': ans,
            't1': {'text': t1.text, 'chapas': k1, 'zunda': z1},
            't2': {'text': t2.text, 'chapas': k2, 'zunda': z2}
        }
        sys.stderr.write("{}:{} done.\n".format(n_id, filename))
    return dumped_json


def add_pas_zunda_to_ne(filename):
    pass

if __name__ == '__main__':
    import glob
    filelist = "RITEVAL_JA_training/json/RITE1*.txt.json"
    for filename in glob.iglob(filelist):
        dump_json(
            add_pas_zunda_to_ne(filename),
            filename.replace('.txt', '.pas.zunda')
        )
