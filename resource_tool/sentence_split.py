# -*- coding: utf-8 -*-


def sentence_split(text, sp=u"。．\n"):
    '''
    You can change separators by changing `sp`.
    '''
    if not isinstance(text, unicode):
        text = text.decode('utf-8')
    LEN, prev_pos = len(text), 0
    sentences = []
    for pos in range(LEN):
        if pos == LEN - 1:
            sentences.append(text[prev_pos:])
        elif text[pos] in sp:
            sentences.append(text[prev_pos:pos + 1])
            prev_pos = pos + 1
    '''
    if separators continues in sentence,
    probably the separators became independent element.
    ex "太郎走る．\nそして飛ぶ" -> ["太郎走る．", "\n", "そして飛ぶ"]
    '''
    rlist = [i for i in range(len(sentences)) if sentences[i] in sp]
    return [s for i, s in enumerate(sentences) if i not in rlist]


if __name__ == '__main__':
    text = "太郎が走った．そして羽ばたいた．"
    for t in sentence_split(text):
        print(t)

