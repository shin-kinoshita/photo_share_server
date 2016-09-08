# Setting
1. mysqlのインストールし、サーバーを起動。
for mac
```
# install
$ brew update
$ brew install mysql
# run server
$ mysql.server start
```

2. 以下コマンドでデータベースを構築
```
python init_database.py
```

3. ipアドレスを調べ、main_server.pyのHOST_NAMEを書き換える。

4. 以下コマンドでmain_serverの起動
```
python main_server.py
```

pythonはversion2.7を想定しています。
