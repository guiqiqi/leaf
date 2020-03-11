# Leaf 的安装与部署

## 安装

`Leaf` 目前提供三种安装方式：

1. 直接拷贝源代码
通过源代码安装只需要克隆本项目在 GitHub 上的源代码即可 - 通过这种方式安装的源代码需要拷贝到您的工作目录之中，但是它并不会添加到您的 `Python` 环境变量中：

```shell
git clone https://github.com/guiqiqi/leaf
cp leaf/leaf . -r
```

2. 通过源代码安装
通过源代码安装，步骤与上面类似，但是会添加到您的 `Python` 环境变量中：

```shell
git clone https://github.com/guiqiqi/leaf
cd leaf
python setup.py install
```

3. 通过 Pypi 自动安装（推荐）
通过 `Pypi` 的发布包安装可能会比最新的代码落后一些版本，但是十分方便，您只需要执行：
```shell
pip install wxleaf
```

## 部署

`Leaf` 的部署十分简单，只需要三个步骤：

1. 创建一个您的项目文件夹，用于保存您项目相关的文件
2. 编写配置文件 - 可以直接参考项目 `config.py` 进行修改即可
3. 编写运行文件 - 参考 `run.py` 内的注释，选择自己需要加载的模块即可

`Leaf` 基于 `Flask` 包，它的部署就如同任何一个普通的 `Flaks` 应用一样：当您只是想在本地调试代码时，可以直接启动 `run.py` 中自带的 `werkzeug` 的应用：

```Python
server.run(host="localhost", port=80)
```

当需要在生产环境中运行时，推荐使用 `Gunicorn` 部署，示例命令：

```shell
gunicorn -w 4 -b 0.0.0.0:80 run:server --daemon
```

***启动多个进程不会造成应用内的任务调度系统执行多次任务吗？***
您无需担心，我们已经在代码实现中解决了这个问题。

更多的参数配置请参考 `Gunicorn` 的[官方使用文档](https://docs.gunicorn.org/en/stable/)。

同时，我们也建议您在生产环境中使用 `Nginx` 作为代理转发，提升静态资源的访问性能。
