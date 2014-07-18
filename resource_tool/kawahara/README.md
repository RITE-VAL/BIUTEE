
## expand_knp.sh

KNPで解析されたWebデータからcabochaのフォーマットに変形するスクリプト．
一旦`kawahara/knp`を別の適当な場所に保存したのち`kawahara/knp`に`expand_knp.sh`と`expand_knp_file.py`を置く．そして，

    ./expand_knp.sh

とすることで各`tsubameXX.kototoi.org/`ディレクトリ以下に`**.cab.bz2`ファイルができる．

### expand_knp_file.py

expand_knp.shのサブのスクリプト．KNPのフォーマットから元の文に復元する

    python expand_knp_file < hoge.txt

でKNPフォーマットから元の生文に復元する

