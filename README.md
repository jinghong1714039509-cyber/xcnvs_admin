## xcnvs_admin

### 介绍
* xcnvs_admin是集群管理平台的后台管理模块，基于Python开发

## 依赖环境

| 程序         | 版本               |
| ---------- |------------------|
| python     | 3.8+             |
| 依赖库      | requirements.txt |


### 运行说明
- 首先安装Python和依赖库环境，推荐通过虚拟环境安装，可以参考下面的安装方法
- 环境安装完成后，启动服务： python manage.py runserver 0.0.0.0:9824
- 访问服务：在浏览器输入 http://127.0.0.1:9824 就可以开始了，默认账号 admin admin888



## windows 创建虚拟环境
~~~
//创建虚拟环境
python -m venv venv

//切换到虚拟环境
venv\Scripts\activate

//更新pip
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

//安装requirements
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

~~~


## linux 创建虚拟环境
~~~

//创建虚拟环境
python -m venv venv

//切换到虚拟环境
source venv/bin/activate

//更新pip
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

//安装requirements
python -m pip install -r requirements-linux.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

~~~

## 🤖 AI开发助手提示词

当使用AI工具协助开发时，可使用以下提示词：

```
你好，我先介绍下整个项目吧。这是基于Django 开发的集群管家后台管理系统。
注意事项
- Windows激活虚拟环境 venv\Scripts\activate 或 Linux激活虚拟环境 source venv/bin/activate
- Windows环境依赖使用 requirements.txt
- Linux环境依赖使用 requirements-linux.txt
- 开发服务器默认端口：9824
请基于以上信息协助我进行开发。

```