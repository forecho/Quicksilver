# 爬虫计划


## 解决了什么问题?

解决了『很多国内播客节目只上架国内播客平台（喜马拉雅、蜻蜓FM）导致无法使用通用型播客客户端收听』的问题


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
$ python app.py ximalaya 8475135 # 喜马拉雅
$ python app.py qingting 209678  # 蜻蜓fm
```

多个专辑，参数使用英文逗号

```shell
$ python app.py ximalaya 8475135,269179
$ python app.py qingting 209678,207865
```

[目前已经支持的节目单](https://github.com/forecho/Quicksilver/wiki/%E7%9B%AE%E5%89%8D%E5%B7%B2%E7%BB%8F%E6%94%AF%E6%8C%81%E7%9A%84%E8%8A%82%E7%9B%AE%E5%88%97%E8%A1%A8)，目前此脚本只支持喜马拉雅和蜻蜓fm的专辑转换为 RSS，如果需要更多节目，欢迎提交 [Issues](https://github.com/forecho/Quicksilver/issues)。


## 赞助

![微信支付](https://raw.githubusercontent.com/iiYii/getyii/master/wechat-pay.png)
![支付宝支付](https://raw.githubusercontent.com/iiYii/getyii/master/ali-pay.png)

手机微信或者支付宝扫描上方二维码可向本项目赞助，所得捐赠将用于改善网站服务器、购买开发/调试设备&工具。感谢以下这些朋友的资金支持：


捐赠人    | 金额 | 时间 | 说明
-------|------|------ | ------
   | -  | - | - | -
