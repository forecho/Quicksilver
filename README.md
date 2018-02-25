# 爬虫计划


## 安装

安装 pip

```shell
$ curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
$ sudo python get-pip.py
$ rm get-pip.py
```

安装 podgen

```shell
$ sudo pip install podgen
$ sudo pip install requests
$ sudo pip install lxml 或者 sudo apt-get install python-lxml
$ sudo pip install beautifulsoup4
```

或者使用 virtualenv

```shell
$ sudo pip install virtualenv
$ sudo virtualenv --no-site-packages podcast --always-copy
$ pip install -r requirements.txt
$ deactivate # 退出虚拟环境
```

## 使用

单个专辑

```shell
$ python app.py 8475135
```

多个专辑，参数使用英文逗号

```shell
$ python app.py 8475135,269179
```