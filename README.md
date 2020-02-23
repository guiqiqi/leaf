# Leaf - 开源微信商城系统框架

![Python](https://img.shields.io/badge/Python-3.5%2B-blue) ![Pylint](https://img.shields.io/badge/Pylint-9+%2F10-brightgreen) ![TypeHints](https://img.shields.io/badge/TypeHints-support-green) ![License](https://img.shields.io/badge/license-Apache2-yellow) ![pypi](https://img.shields.io/badge/Pypi-v1.0.6-orange)

![Logo](https://github.com/guiqiqi/leaf/blob/dev/docs/logo-bar.png?raw=true)

`Leaf` 旨在实现一个对普通用户易用、对开发者友好的 *轻型* 开源 CMS 框架；`Leaf` 基于 `Python3.5+` 构建，后端使用 `Flask` 作为基础框架、`mongoengine` 进行数据库建模。

我们希望能减少普通用户搭建微信商城的成本，同时为有开发能力的朋友提供更多样化的功能。

**`Leaf` 当前的开发仍在进行当中，最新的代码变动请参考 `dev` 分支**

---

## 安装及使用

### 安装

提供两种安装方式：
- 手动安装：从本项目下载代码到您的目录，运行 `python setup.py install`
- 自动安装：运行 `pip install wxleaf`

**请注意，在正式版本发布之前，在代码分支 `dev`, `beta` 的代码都不可用于生产环境**

在正式版本的 `release` 之前，*推荐* 使用手动安装模式（自动安装的包仍会不定期更新）

---

### 使用

下面是一个简单的使用示例，在项目的 `demo` 文件夹内会不断更新更多的实例演示。

**示例配置文件请参考 `config.py`**

```python
import logging

import leaf
import config

init = leaf.Init()
init.kernel()
init.logging(config.logging)
logger = logging.getLogger("leaf.demo")

# 可选项 - 下面的模块请根据自己需要加载
# 请注意：非稳定版本的模块可能会有变动
# 关于模块之间的相互依赖，请参阅文档
init.server()
init.database(config.database)
init.plugins(config.plugins)
init.weixin(config.weixin)
init.wxpay(config.wxpay)

# 插件管理器
plugins_manager = leaf.modules.plugins

# 获取事件管理器并绑定两个函数到退出事件上
events_manager = leaf.modules.events
whatever_exit = events_manager.event("leaf.exit")
whatever_exit.hook(lambda: print("Goodbye~"))
whatever_exit.hook(plugins_manager.stopall)

# 运行服务器
server = leaf.modules.server

@server.route("/hello/<string:name>")
def greeting(name: str) -> str:
    """来自 Leaf 的问候"""
    logger.log("Visit from client named " + name)
    return "Here's a greeting from Leaf to " + name
    
@leaf.api.wrapper.require("leaf.exit")
@server.route("/goodbye")
def exiting():
    """主动关闭退出"""
    # 手动触发退出事件:
    # 	1. 关闭数据库连接池
    #	2. print("Goodbye~")
    #	3. 关闭所有插件
    whatever_exit.notify()
    return "Goodbye~"
   
leaf.modules.server.run()
```

---

## 特性介绍

### For Users

`Leaf` 希望能够给没有开发能力的普通用户提供一个基础的、易于使用和管理的微信商城系统。
如果您是没有开发经验的普通用户，`Leaf` 可以提供给您：

1. **微信公众平台的接口使用能力**
即使您没有开发经验，也可以在我们的可视化后台中轻松地编辑多媒体文章、设置群发消息、管理用户/组、设置自动回复等等。
2. **主流支付接口的使用能力**
如果您有微信支付及支付宝支付等主流支付接口的使用权限，您可以在我们的后台中轻松配置支付方式，即时应用在您的交易当中。
3. **完善的用户/组/权限管理系统**
`Leaf` 实现了基于角色的用户权限控制，通过在可视化后台中对用户的角色进行编辑，您可以轻松地配置多个用户组以分配工作 —— 管理员、编辑、库存管理员、甚至普通用户都可以进行分组。
4. **产品/库存/订单管理**
`Leaf` 中集成了产品、商品库存、订单管理的功能，您可以轻松地管理 `SKU/SPU` 以及订单等信息。
5. **插件扩展能力**
您可以在我们的项目网站上寻找合适您需求的插件。
通过简单的单击按钮，您就可以启用或者禁用这些扩展，插件也可以使用上述的能力 —— 您可以使用插件设置定时任务，来进行微信推送、也可以使用插件来扩展商城功能，设置促销等等...

---

### For Developers
如果您有开发能力，`Leaf` 则能带给您更多可能，通过简单的二次开发，您可以使用到她的更多高级功能，下面是您可能感兴趣的部分：

#### 功能特性
1. **任务计划支持**
不需要第三方的组件，您可以在开发过程中调用 `leaf.core.schedule` 模块，她可以帮助您实现 *轻量级* 的任务计划调度。
2. **事件机制**
您可以在代码的任何地方创建一个事件实例，通过 `events.hook` 方法可以将您的动作挂载到事件上，当事件发生时您的动作将会自动运行。
3. **日志与错误系统**
`Leaf` 基于 `logging` 包实现了较为完善的日志系统，同时定义的异常基类规范了系统中的异常使用。您只需要在您的代码中继承 `leaf.core.Error` 类，就可以在日志、API网关中得到详细的错误栈信息。
4. **权限控制**
正如上面在介绍所说，`Leaf` 实现了基于用户角色的权限控制，您也可以像系统应用一样定义自己的接入点，并通过简单的装饰器控制。
5. **插件系统**
插件系统是 `Leaf` 扩展性的重要保证。在 `Leaf` 中您可以：
- **热插拔** 地管理插件，代码的更改变动可以仅通过一次插件重入得到部署；
- 插件可以像在`Flask`的应用中设置路由一样，通过简单的装饰器控制视图路径、权限、访问IP等等
- 插件可以调用系统中其余的资源（包括事件调度、日志、微信能力、数据库，甚至是其他插件的资源）

#### 开发特性
1. **关于注释**
我们深知没有注释的代码等于天书这个道理，为了方便您的二次开发，`Leaf` 从核心模块到视图函数都有详细的注释。
2. **关于文档**
对于一些重要的系统功能，`Leaf` 会编写专门的文档进行说明 —— 例如如何开始您的插件开发，必要的地方还会配有插图，用于方便您的理解。
3. **类型提示**
`Python` 从 3.5 版本之后支持了类型提示 `type hinting`，而我们则尽可能的在代码的各个部分使用这项全新功能，配合 `Visual Studio` 等 IDE，帮助您更轻松的开发。
4. **代码风格**
`Leaf` 在开发过程我们尽可能的维持一致的代码风格，并且设置 `commit-Hook` 使用 `PyLint` 进行代码评分 —— 带目前为止，`Leaf` 获得的评分在 **9分** 以上，我们知道评分不能代表一切，但是仍希望能够做的更好。
5. **代码示例**
>古人说： 纸上得来终觉浅，绝知此事要躬行。

我们会编写一些示例代码助于开发者的理解。
例如您可以在 `Leaf` 的任意版本中找到示例插件的代码，相信会更有助您的二次开发。

---

## Other

### Wanted

- `Leaf` 仍在开发阶段，仍有很多不完美的地方，希望大家能够在 `Issue` 中提出，帮助她变得更好。
- `Leaf` 的后端工作已经接近完成，现在需要前端小伙伴们的支持，将它变成一个好看的全栈项目。
- ~~`Leaf` 到现在还没有一个合适的 Logo, 希望各位能够帮助~~ (已实现)

### Todo

1. ~~完善 `JWT Token` 的鉴权流程，实现 `api.wraps.require` 装饰器 - 一周内~~ (已完成)
2. ~~完成用户/组/权限/访问点相关的 `CRUD` 以及视图函数 - 一周内 (2020.2.17 修周假)~~ (已完成)
3. 完成 `SKU/SPU` 的 `CRUD` 以及视图函数 - 一个月内
4. 完成订单模块的 `CRUD` 以及视图函数 - 近期
5. 编写给前端同学的 `API` 文档 - 两个月内 (部分完成)
6. 完善微信公众平台的 `API` 支持 - 两个月内
7. 完成微信支付相关错误码收集 - 两个月内
8. 编写单元测试 - 三个月内
9. 编写给后端同学二次开发的文档 - 三个月内
10. 架设属于 `Leaf` 自己的官网、插件市场 - 有生之年

*To be continued...*

### Contributors

[@guiqiqi](https://github.com/guiqiqi) - `Leaf` 框架及后端支持

[@lsdlab](https://github.com/lsdlab) - 前端及官网展示页面支持

@刘修岩 from *天津大学建筑学院* - `Logo` 制作

~~另外，我们现在已经建立了一个微信讨论组，如果你也想提供 *点子/创意/技术支持/...* 欢迎加入我们~~

### Thanks

`Leaf` 项目的诞生离不开众多开源项目的支持。事实上，我们和他们一样都希望构建一个更好的开源世界。我总是相信：**We can make the world a better place.**

在此特别感谢以下开源项目：
- [python](https://github.com/python/cpython)
- [flask](https://github.com/Legrandin/pycryptodome)
- [mongoengine](https://github.com/MongoEngine/mongoengine)
- [pycryptodome](https://github.com/Legrandin/pycryptodome)

**另外，希望这次疫情快速过去，武汉加油，中国加油！♥**

**祝您使用愉快 ;)**