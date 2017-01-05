#安装python3.5.2解释器，安装时添加系统环境变量
xp可以安装3.4版本


#创建project虚拟环境
1: cd servermanager
2: pyvenv venv
3: venv\Scripts\activate


#安装工程依赖的whl包
4: cd install
5: pip install --no-index -f . -r requirements.txt


#初始化工程db和表结构
6: cd servermanager
7: python -m manager db init 
   python -m manager db migrate
   python -m manager db upgrade


#初始化工程测试数据
8: python -m manager init_static_data && python -m manager init_test_data


#在pycharm启动app
9: 将该工程下面的venv设置为该工程默认的解释器，start app