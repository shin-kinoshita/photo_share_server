# Setting
- mysqlのインストールし、サーバーを起動。
for mac
```
# install
$ brew update
$ brew install mysql

# run server
$ mysql.server start
```

- mysqlのpython用APIのインストール
```
pip install MySQL-python
pip install mysql-connector-python-rf
```

- 以下コマンドでデータベースを構築
(注)以下コマンド実行前にphoto_share_serverによるデータベースが構築するされている場合、保存されているデータば全て削除される。
 ```
python init_database.py user_name password
```
user_name: mysqlの全権限が与えらているユーザー名
password: 上記ユーザのパスワード
をそれぞれ指定。
macではデフォルトでパスワードなしのrootユーザーが存在しているので、
```
python init_database.py root
 ```
でよい。

- ipアドレスを調べ、main_server.pyのHOST_NAMEを書き換える。

- 以下コマンドでmain_serverの起動
 ```
python main_server.py
 ```

pythonはversion2.7を想定しています。
