

readmeになります。
テキストをMarkdownエディタで開いていただくと整形されます。
オンラインだと http://marxi.co/ 等があるようです。


－－－－－－－－－－－

### pip のインストール  （venv（pipの仮想環境）を使う場合）

venv を使わない場合は以下の venvの手順は不要です。
作業フォルダに移動後、

```
$ python -m venv ./my_venv1   # my_venv1 は任意の名前
$ sourse my_venv1/bin/activate  # 仮想環境を有効化。この仮想環境を有効化する際、毎回実行
             # （Windows の場合、パスがmy_venv1/Scripts/activate　）

$ deactivate  # 仮想環境を出る時
```


### pip ライブラリインストール

```
$ pip install Flask 
$ pip install orator
$ pip install python-dotenv
```

### .env について

.env にDB設定を記載しています。
（.env を利用しない場合は、settings.pyに直接記載）


### 実行

jobs/ 配下に 実行するファイルtaskNN.pyを作成し、（NNは数字）
jobs/__init__.pyに追加します。


* jobs/__init__.py

import 部分に jobs/taskNN.py の関数を追加


```
from jobs.task1 import task1_run
from jobs.task2 import task2_run
```

job.add_command() 部分に追加


```
job.add_command(task1_run)
job.add_command(task2_run)
```


その後、コマンドから実行します。


```
$ export FLASK_APP=cli.py  # flaskコマンドが参照するファイル名を指定する事前準備コマンド。一度指定されていれば毎回実行は不要
$env:FLASK_APP = "cli"
$ flask job task1  # task1.pyを実行する場合

$ flask job task2  # task2.pyを実行する場合
```


### 実行について
flask のコマンドライン機構を使って実行していますが
直接 python ファイルを実行が使いやすければその方がいいかもしれません。
（その場合は、taskNN.pyを直接実行して、 taskNN_run()関数を直接呼び出すイメージです。）


### DBについて

Orator というライブラリを使用しています。
お手軽かつ便利で非常に良いと思われます。

SQLを直接書くマニュアル
https://orator-orm.com/docs/0.9/basic_usage.html#running-a-select-query
Query Builderを使うマニュアル
https://orator-orm.com/docs/0.9/query_builder.html#retrieving-all-row-from-a-table


### コマンドリスト
リモートにプッシュ
git remote add origin https://github.com/itsu1113/serp202210.git
git push origin master

gitクローン
git clone https://github.com/itsu1113/serp.git

$env:FLASK_APP = "cli"
flask job task1


test
