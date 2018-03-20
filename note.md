# mysql在Linux下的安装
1. yum 安装
```
wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
yum localinstall mysql57-community-release-el7-11.noarch.rpm
yum install mysql-community-server
```
2. docker 安装
```
安装docker
docker run --name mysql -p 3306:3306 -v /data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
```
# 连接
我们使用pymysql连接mysql数据库。 查看 [文档](http://flask-sqlalchemy.pocoo.org/2.3/)
key | func
----|----
SQLALCHEMY_DATABASE_URI| mysql+pymysql://username:passwd@server/db
SQLALCHEMY_TRACK_MODIFICATIONS|如果orm的对象有改变，就会有一个记录，影响性能，不需要，设置为false

# 数据库的版本控制
数据库的版本控制用到了flask-migrate,首先安装flask-migrate
```
pip install flask-migrate

加入app构造函数，完成初始化
...
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def create_app():
    db.init_app(app)

在入口的BasicFlask.py 增加
from app.models import User

写完models.py就可以
flask db init
flask db migrate -m "xxxx"
flask db upgrade

如果要回退版本
flask db downgrade
flask db downgrade 版本号，在versions里面

```
# 注册和认证
1. 要用到什么模块？
```
flask-login
flask-wtf

```
2. 有什么安全问题？比如说越权，csrf
3. 如何组织