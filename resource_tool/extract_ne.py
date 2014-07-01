# -*- coding: utf-8 -*-


def extract_ne(args):
    datas = open(args.target_file).read().decode("utf-8").split('\n\n')
    f = open(args.target_file.replace('pas', 'ne'), 'w')
    for data in datas:
        lines = data.split('\n')
        nes = []
        tmp_ne, tmp_type, tmp_pos = u"", u"", 0
        header, word_pos, words = "", -1, []
        for info in lines:
            if info == u"":
                continue
            if info.startswith("EOS"):
                if tmp_ne != u"":
                    nes.append((tmp_ne, tmp_type, tmp_pos, word_pos))
                text = " ".join([
                    u"{}:{}:{}:{}".format(ne, t, p1, p2)
                    for ne, t, p1, p2 in nes
                ])
                text = header + u"\t" + text + u"\t" + u" ".join(words)
                f.write(text.encode("UTF-8"))
                f.write("\n")
                nes = []
                words = []
            elif info.startswith("#"):
                header = u"\t".join([pp.split(u':')[1]
                                     for pp in info.split(' ')[1:]])
            elif info.startswith("*"):
                continue
            else:
                dd = info.split("\t")
                words.append(dd[0])
                word_pos += 1
                if dd[2] == u"O" and tmp_ne != u"":
                    nes.append((tmp_ne, tmp_type, tmp_pos, word_pos))
                    tmp_ne = u""
                elif dd[2] == u"O":
                    continue
                elif dd[2].startswith(u"B-"):
                    if tmp_ne != u"":
                        nes.append((tmp_ne, tmp_type, tmp_pos, word_pos))
                    tmp_ne = dd[0]
                    tmp_type = dd[2][2:]
                    tmp_pos = word_pos
                else:
                    tmp_ne += dd[0]
    f.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('target_file', metavar='FILE',
                        help='result file %(default)s')
    args = parser.parse_args()
    if not ".pas" in args.target_file:
        print "Error: not contain .pas"
        exit()
    extract_ne(args)
