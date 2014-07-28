# -*- coding: utf-8 -*-
import json
import sys
import subprocess
from itertools import product


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


def zunda(chapas_data):
    proc = subprocess.Popen(
        ['zunda', '-i', '3'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    return proc.communicate(chapas_data)[0]


def main(filename):
    data = json.load(open(filename, "r"))
    dumped_json = data.copy()
    raw_data = json.load(
        open(filename.replace("pas", "raw"), "r")
    )
    for t_id, t in product(data, ["t1", "t2"]):
        if t not in data[t_id]:
            continue
        zunda_chapas = zunda(dumped_json[t_id][t]["text"].encode("utf-8"))
        k, z = add_zunded(zunda_chapas.decode('utf-8'))
        dumped_json[t_id][t]["chapas"] = k
        dumped_json[t_id][t]["zunda"] = z
        # dumped_json[t_id][t]['nn'] = raw_nn[t_id][t]['nn']
        dumped_json[t_id][t]["text"] = raw_data[t_id][t]
        if "category" in raw_data[t_id][t]:
            dumped_json[t_id][t]["category"] = raw_data[t_id][t]["category"]
        print "{}:{} done.".format(t_id, t)
        sys.stdout.flush()
    ss = json.dumps(dumped_json, indent=4, sort_keys=True,
                    ensure_ascii=False)
    with open(filename.replace(".pas", ".pas.zunda"), "w") as w:
        w.write(ss.encode("utf-8"))
    print "{} end..".format(filename)
    sys.stdout.flush()


if __name__ == '__main__':
    import glob
    for filename in glob.iglob("[FS]V/my/*.pas.json"):
        main(filename)
