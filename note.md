# 概述
1. 项目初始化
2. Hello world

# 项目初始化
1. 安装python
2. 创建虚拟环境
```
python -m venv venv
windows:
.\venv\Script\activate

Linux and mac:
source venv/bin/activate
```
3. 项目结构
```
| BasicFlask
--venv
--test
--app
----static
----main
----templates
-------main
```
4. 安装flask
```
pip install flask
```
5. 写入requirements.txt
```
pip freeze > requirements.txt
```
6. 工厂函数
```
为什么要工厂函数？
def create_app():
    pass
    
一般一个简单的flask是是这样的：
from flask import Flask
app = Flask(__name__)
@app.route('/')
def main():
	return "Hello Wolrd"


这个时候，如果有配置要在中间写进去这么一行：
...
app.config.from_object(config)
...

但是在我们开发的时候，有多个环境的，这个时候，你的多个单元测试需要测试应用在多个环境是否正常，但是你却只能传进去一个config。这个时候动态创建app实例就分外重要，可以自动化许多的流程
```
7. 配置分离

   ```
   class Config():
       SECRET_KEY = os.environ.get('SECRET_KEY')
       
       @staticmethod
       def init_app(self):
           pass
       
   class DevConfig(Config):
       ...
   config ={
   	'dev':DevConfig,
       ...
       'default':DevConfig
   }
   ```

8. 主程序运行

   ```
   新建BasicFlask.py

   from app import create_app
   app = creat_app('default')

   export FLASK_APP = BasicFlask
   export FLASK_DEBUG=1
   flask run
   ```

   ​

9. 蓝图

   ```
   这个时候，因为app是动态运行的，你就没办法在views.py 里面直接用app去定制路由，这个时候，蓝图是很不错的一个功能，它允许你把一个应用给分割成多个部分，比如登录，注册是一个模块，主界面是一个模块，后台管理是一个模块。
   蓝图的使用：
   新建main文件夹
   __init__.py:

   from flask import BulePrint
   main = BluePrint('main',__name__)

   from . import views

   蓝图写好后，要注册到这个app上面才能用

   create_app():
   	from app.main import main as main_blueprint
   	app.register(main_blueprint)
   	
   ```

   ​

10. 编写views

    ```
    @main.route('/')
    def main():
    	return "hello world"
    ```

    ​

    ​

    ​