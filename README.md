#TODO
treeとかの中身  
operationの実装  
searchの実装  
featureの計算  
tree同士の類似度を計算できるようにしたい．(サーチの時のスコアに使ったり，tとhが一致してるか調べたりに使える)  
独自の何か  
複数文を統合して得られる情報を扱えないのでどうにかしたい

#ファイルの説明
##BIUTEE/config.ini
設定用ファイル．  
各人の環境に合わせて書き換えてください.(下の感じ)  
[path]  
CHAPAS_PATH : /home/miura/chapas-0.742/  
LivSVM_PATH : /home/miura/libsvm-3.17/python/a

##t_h.py
###self.t
text(treeのリスト)

###self.hs
hypothesis(treeのリスト)のリスト．リスト内の要素が変形の過程を記録している．

###self.proof
operationのリスト．  
[ [operation, args], [operation, args], ・・・]  
argsはoperationにおいて必要になる情報を記録した辞書．
挿入する単語とかその場所なんかの情報．あとで細かく考える.

###self.feature
プロパティ.  
self.proofをもとにしたfeatureを保持．

###self.search(w, b, k)
ビームサーチ．最適なoperationの組み合わせを探してself.proofに記録する.  
w, b : 学習されたパラメータ  
k : ビーム幅  
ありとあらゆるoperationとそのargsを試してhをtに変形させる．  
サーチのためにhの変形を色々試す必要があるが，T_H自体のhを変形させるのでなくそのコピーを変形させてスコアを計算していく
(T_Hに対しての操作は最終的に得られたproofでのみ．)  
あるoperationとargsにおけるスコアはoperation.getvalue()で得られる．(予定)  
最後にself.__featureにproofからえられるfeatureを記録する．  
ここの計算量が大きいと思うので，場合によってはマルチスレッド化したりとかするといいかも

###self.translate()
self.proofをもとにself.hsを変更する

###self.__getFeature()
featureを計算．  
次元数とかどう揃えるのかよく分からない．だれかやって.

##operations/operation.py
抽象クラス．今後これを継承した操作のクラス(論文のtable3)を実装していく．  
treeの操作はそのクラスを通して行う．

###self.getValue(t, h, args)
tとhとargsをもとにスコアを計算して返す．

###self.translateTree(h, args)
h(treeのリスト)を変形させる

###self.translateT_H(t_h, args)
t_h.hsを変形させる

##operations/flipPos.py
operation.pyの実体．
今後こういう操作クラスを実装していく

