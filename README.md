# Leaf - 开源微信商城系统框架

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAD8UlEQVRoge2YTWhcVRSAv3MnaSY/SqlSNEVTartppBZN8Ye2aYwTNUh3jQqCKEoWbqKWtO6yakmoNOBWFF0EaSsFu3CKiROjRUu7aaOpolQ0hEhpQQ1pJpP37nExVUnnzcx7uS9DC/NtZjj3/N775t1zBqpUqXJbI/G4UeHg6HaD6VLlMYEtQDPQCPjANYEZFc4ZOOklvx5nYMDGEdm9gP2j20xCRoDWsCaKnlYv8RLvdlx1DZ9wsh441WD8Nd8BD0QxE2SzEd2lqU0fMj6uLikYF+OahcZdwIaV2KrweE12Z5dLfHAsQOW/5Ges0VaLbQEmw9pbeMIlPrgWYPXO/DdJc/ipKQZTv6NyPLwDucMlPkCNq4M8+gzvjG4lJ/OI7ovHZzhiKoANxsoPsXmLgNMjdCvgtGd2qHMYGC6lY/rH+hCOltLRibo+dJlOFmQStYdlT+5kSf/h060oSdAdiHyqE8nXSimWPoGDmc1GdT/oTmAj+dagkgiqR3Us+YV0Zn8LUih6Aon+L/catRdAe8m3CZVO/l+aSNBbbDG4gLfHWlR0BGhYrazySLiGTvT5YkuBBZhafYtK7Ljqrzc+y8XapJnGe4IWgk9ApdspsXD8aa137EYa28pqG+/hQHGBpC+zlojd5QqYN8gLHHn6ip5pWg8aZsO2BAkLC0h624lt0FmGRWUa5X1recgbfPI0AL43DDSVtRZZFyQueI0mMPdGbNB/EuSQr94oQ6lZkFDmqhi+qjuC6ouholitDxIXFKCq6yIcwIi9vvgq73UvhjXQM03r8XJ7mDD9iD4S1g7Ra0HiggJEyWqI/BUyWm9eZrDb028amvH9A8Be4D5KTXreEvkNijqImdkgadBNHFjpTVhV+wYDnZ5matvwvTTIXREziobxLwSKbxb4Yn4u50uUswylLmmGJAlzYtWThwXql6aCFgrfQpev/gjMl/Kmwvd567oulJYYEixHWtpYClooLOB4j69wtozDfIHKRtfMQuBh7aFii4E3saDHQrk2q96OeyC90rF0vngKAVj0E2Bm1dIqTRa4BPoRxrZJe/aDUsrB88Bg6i85MPa6wmdFdcozLO2Lb67QNjRFHwF/sPNzC50KGeD6aieyUpx6noBZNirOp3SrzsShqWQBM4i2grkfuBiX00oWkJbduSlpX5hG9ERcTt3+S1OZi9CUPauZNQ9Sm/gb3/b8b++GWwFivyVM65qnGSOT+Mvm+Gmn+Dg+QrI7NwUS7tYuZA5NnHKJD3H8Bhqzr4B+HNHqMshz0jH/h2v42GZfHa/dAWYfwqMILSh3A3Ugc6heQfgF9BwmkWZ24bz04McVu0qVKrcx/wCMzkVJcJCK+gAAAABJRU5ErkJggg==) ![License](https://img.shields.io/badge/License-Apache2-yellow?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAADYElEQVRIidWVTWjcVRTFf+dNEqRYaGJodJoUMnFlkGhcuomoUbHCVKkLKWJbcKMLoVYr9WOYCoIxiAtdVKi2VBdF2xQVtKFIbEEKLaSLoEKmTaqNaWqjFgnY5v+Oi5lJ5iMJxp0H3ua9e8+597777oP/O7TS4Viuu6klmctaygK9QHvpaBpx2lFfpC+v+1z7zt5YtcBULvM40QNIGVzcc8nBhhAgGgQTJrywIT9+7F8JOEf4NXZ+DXqwtDUJPm4454QZhKW43iH0yHo4wEZLYAZvyxd2iXI4ywhceq1zWOIBkIk+6AaOEKudFhCQzaMph23GjaDBdL7wYrVJTVkkFclBDro/JKxbpooQscyXCXGv0DywczqX2bSkwFiuu4nogaKjDwKTgnZLefCaZUWKZRiNxI+EidHveQupOoGWZC4LygCTDj5K8KvAZJRPguZWEijCX0XzMygz3d25uU6AoM0CjI+DoiN/mviyzOEY1Shpu9EBoQ9x2BoJDTV5RIjDADaP1QnY9BoIQaMVTnMAIbAVkw3QLGiT/KTsp4oEiqkQLsxfT06l75x4NgS1hah3ygyVUaQBiL5Slzz0BSAG3QsORE4G+T7DvqYQTt+SG7+2aF2YAWaWEgAgMVJN8wYcQZAgsJAA6aYS+aU9XR1K+V2gvxTRCdu7N7x54afKNp0CSKXUWisarW8NBPkU0ncAMkMV5KOIJwRrBWsRWQV9f2lPV8eigDgD4MR315VI+tTW4Qizhj8wR5TSKwClyFtsziTWthuw3XAWaFaKwQUBRR9zkawfXPUAA3EexUPgZ8BPW/74BzpmS8f9AhL4QIpXU/g34P3i2/dDC0SzqTVDgkKAjSI8UpvFqlG8x8VIu3Nj10G7XLzAHTY9K/nfxcTNRQpOGEjBcwlqBbUCzwNY+qaqFOl84ajw2xAbgsIbFptqy1XG36TaAWzvBn4X3NMI+wPsF/SCr1raueS4nnbmLVsvYWNxETyMGQ3iMkA0bQqhJ4k61LF3fKTUSRcreWIIHe258V9W+HC6sooeMNwuIFI528tfD1fS+fPrAaZez1SN9HT+vKBmXFcZ5ApDt04336HgLYZPBD8CfwHXQGPgA8Y7lvMvo+4lV6L0135WWv8Jy2awemhEjn1y7AONlHf/ASAydLsGpZYoAAAAAElFTkSuQmCC) ![Pylint](https://img.shields.io/badge/Pylint-9+%2F10-brightgreen) ![TypeHints](https://img.shields.io/badge/TypeHints-support-green) ![pypi](https://img.shields.io/badge/Pypi-v1.0.6-orange)

![Logo](https://github.com/guiqiqi/leaf/blob/dev/docs/logo-bar.png?raw=true)

`Leaf` 旨在实现一个对普通用户易用、对开发者友好的 *轻型* 开源 CMS 框架；`Leaf` 基于 `Python3.5+` 构建，后端使用 `Flask` 作为基础框架、`mongoengine` 进行数据库建模。

我们希望能减少普通用户搭建微信商城的成本，同时为有开发能力的朋友提供更多样化的功能。

**`Leaf` 当前的开发仍在进行当中，最新的代码变动请参考 `dev` 分支**

---

## 安装及部署

### 安装

提供两种安装方式：
- 手动安装：从本项目下载代码到您的目录，运行 `python setup.py install`
- 自动安装：运行 `pip install wxleaf`

**请注意，在正式版本发布之前，在代码分支 `dev`, `beta` 的代码都不可用于生产环境**

在正式版本的 `release` 之前，*推荐* 使用手动安装模式（自动安装的包仍会不定期更新）

---

### 部署

`Leaf` 的部署很简单，只需四个步骤：

1. 创建一个您的项目文件夹，用于保存您项目相关的文件
2. 编写配置文件 - 可以直接参考项目 `config.py` 进行修改即可
3. 编写运行文件 - 参考 `run.py` 内的注释，选择自己需要加载的模块即可
4. 使用 `Gunicorn ` 进行部署，示例命令：

```shell
gunicorn -w 4 -b 0.0.0.0:80 run:server --daemon
```

更多的参数配置请参考 `Gunicorn` 的[官方使用文档](https://docs.gunicorn.org/en/stable/)。

同时，我们也建议您在生产环境中使用 `Nginx` 作为代理转发，提升静态资源的访问性能。

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

**示例代码将会在 `demo` 文件夹中不断更新**，您也可以在 `Leaf` 的任意版本中找到示例插件（`Access Token` 中控插件）的代码，相信会更有助您的二次开发。

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