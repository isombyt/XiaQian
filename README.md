虾签-XiaQian
=======

虾签-虾米每日签到

#1.项目简介
虾签是一个用于自动化完成虾米每日签到的简单解决方案

此项目的目的是将人们从每日虾米签到的地狱中解放出来，一定程度上避免漏签带来的严重后果。

不依赖于任何PaaS服务，亦不针对任何PaaS服务特化。可运行于兼容的Python环境中。

#2.环境配置
*   XiaQian需要的运行环境为Python >=2.6 <3.0或PyPy2.0+
*   直接依赖的第三方Python库包括Gevent>=1.0,Web.py>=0.37,lxml>=3.2.4
*   依赖的官方库包括sqlite3,urllib,urllib2(非嵌入式版本的Python可无视）

#3.安装方式
    git clone https://github.com/isombyt/XiaQian.git

#4.运行方式
    python WebManager.py

*或者

    nohup python WebManager.py &

#5.使用说明
*   访问本机8888端口(可在WebManager.py中指定端口)
*   如  http://127.0.0.1:8888
*   填写帐号信息，提交即可

*   访问    http://127.0.0.1:8888/Ctrl
*   可查看当前登记的所有帐号以及签到情况

#6.TODO
*   添加邮件通知功能
*   添加每日任务支持