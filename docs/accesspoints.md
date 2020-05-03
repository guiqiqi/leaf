
以下是 _Leaf_ 现有的所有接入点信息及其介绍:

| 接入点代码 | 接入点描述 | 接入点路径 | 允许的请求方式 |
| :------ | | :---- | | :----- | | :----------- |
| leaf.views.rbac.user.get | 批量获取用户信息 | /rbac/users | HEAD, OPTIONS, GET |
| leaf.views.rbac.user.get | 根据用户 ID 查询用户 | /rbac/users/<string:userid> | HEAD, OPTIONS, GET |
| leaf.views.rbac.user.get | 根据用户 Index 查询用户 | /rbac/users/<string:indexid>/<string:index> | HEAD, OPTIONS, GET |
| leaf.views.rbac.user.update | 更新用户 informations 信息 | /rbac/users/<string:userid>/informations | PUT, OPTIONS |
| leaf.views.rbac.user.create | 创建一个用户的接口调用顺序如下: | /rbac/users | POST, OPTIONS |
| leaf.views.rbac.user.update | 更新一个用户的状态 | /rbac/users/<string:userid>/status | PUT, OPTIONS |
| leaf.views.rbac.user.update | 将用户添加至用户组 | /rbac/users/<string:userid>/groups/<string:groupid> | POST, OPTIONS |
| leaf.views.rbac.user.update | 为指定用户增加一个索引信息 | /rbac/users/<string:userid>/indexs | POST, OPTIONS |
| leaf.views.rbac.user.update | 删除用户的一种指定索引 | /rbac/users/<string:userid>/indexs/<string:typeid> | OPTIONS, DELETE |
| leaf.views.rbac.user.delete | 删除某一个用户 | /rbac/users/<string:userid> | OPTIONS, DELETE |
| leaf.views.rbac.user.update | 将用户从组中移除 | /rbac/users/<string:userid>/groups/<string:groupid> | OPTIONS, DELETE |
| leaf.views.rbac.user.update | 更新用户头像 | /rbac/users/avatar/<string:userid> | POST, OPTIONS |
| leaf.views.rbac.user.update | 删除用户头像 | /rbac/users/avatar/<string:userid> | OPTIONS, DELETE |
| leaf.views.rbac.group.query | 根据给定的 id 查找用户组 | /rbac/groups/<string:groupid> | HEAD, OPTIONS, GET |
| leaf.views.rbac.group.list | 列出所有的用户组信息 | /rbac/groups | HEAD, OPTIONS, GET |
| leaf.views.rbac.group.query | 根据名称查找指定的用户组 | /rbac/groups/name/<string:name> | HEAD, OPTIONS, GET |
| leaf.views.rbac.group.delete | 删除某一个特定的用户组 | /rbac/groups/<string:groupid> | OPTIONS, DELETE |
| leaf.views.rbac.group.add | "增加一个用户组 | /rbac/groups | POST, OPTIONS |
| leaf.views.rbac.group.update | 更新某一个用户组的信息 | /rbac/groups/<string:groupid> | PUT, OPTIONS |
| leaf.views.rbac.group.edituser | 编辑用户组中的用户: | /rbac/groups/<string:groupid>/users | PUT, OPTIONS |
| leaf.views.rbac.auth.create | 根据用户的某一个 index 创建 Auth 文档 | /rbac/auths/<string:userid>/<string:typeid> | POST, OPTIONS |
| leaf.views.rbac.atuh.update | 更新用户的认证文档状态 | /rbac/auths/<string:index>/status | PUT, OPTIONS |
| leaf.views.rbac.auth.delete | 删除用户的某一种认证方式 | /rbac/auths/<string:userid>/<string:index> | OPTIONS, DELETE |
| leaf.views.rbac.auth.get | 查询用户的索引与认证文档的对应状态 | /rbac/auths/<string:userid> | HEAD, OPTIONS, GET |
| leaf.views.rbac.auth.update | 更新用户密码 | /rbac/auths/<string:userid>/password | PUT, OPTIONS |
| leaf.views.rbac.accesspoint.query | 根据指定的名称查找相关的访问点信息 | /rbac/accesspoints/<string:pointname> | HEAD, OPTIONS, GET |
| leaf.views.rbac.accesspoint.get | 返回所有的访问点信息 | /rbac/accesspoints | HEAD, OPTIONS, GET |
| leaf.views.rbac.accesspoint.delete | 删除某一个访问点信息 | /rbac/accesspoints/<string:pointname> | OPTIONS, DELETE |
| leaf.views.rbac.accesspoint.create | 创建一个访问点信息 | /rbac/accesspoints | POST, OPTIONS |
| leaf.views.rbac.accesspoint.update | 更新某一个访问点信息 | /rbac/accesspoints/<string:pointname> | PUT, OPTIONS |
| leaf.views.rbac.accesspoint.update | 为指定的 AccessPoint 管理特权用户 | /rbac/accesspoints/<string:pointname>/exceptions | PUT, OPTIONS |
| leaf.views.commodity.product.get | 批量获取产品信息 | /commodity/products | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.get | 根据产品ID查找产品 | /commodity/products/<string:productid> | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.get | 根据产品名查找全部相关的的产品 | /commodity/products/name/<string:name> | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.get | 根据产品标签查找产品 | /commodity/products/tags/<string:tags> | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.get | 查询全部的标签以及个数 | /commodity/products/tags | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.delete | 删除一个指定的产品 | /commodity/products/<string:productid> | OPTIONS, DELETE |
| leaf.views.commodity.product.update | 删除一个指定的产品参数 | /commodity/products/<string:productid>/parameters/<string:name> | OPTIONS, DELETE |
| leaf.views.commodity.product.update | 增加一个产品参数 | /commodity/products/<string:productid>/parameters | POST, OPTIONS |
| leaf.views.commodity.product.update | 更新产品在售状态 | /commodity/products/<string:productid>/onsale | PUT, OPTIONS |
| leaf.views.commodity.product.create | 创建一个产品 | /commodity/products | POST, OPTIONS |
| leaf.views.commodity.product.update | 更新产品信息 | /commodity/products/<string:productid> | PUT, OPTIONS |
| leaf.views.commodity.product.get | 获取当前产品已经生成的所有商品列表 | /commodity/products/<string:productid>/goods | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.update | 生成商品列表 | /commodity/products/<string:productid>/goods | POST, OPTIONS |
| leaf.views.commodity.product.update | 清除所有的生成商品 | /commodity/products/<string:productid>/goods | OPTIONS, DELETE |
| leaf.views.commodity.product.get | 查询所有的独立商品 | /commodity/goods | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.get | 根据标签查询所有的独立商品 | /commodity/goods/tags/<string:tags> | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.get | 根据名称查询所有的独立商品 | /commodity/goods/name/<string:name> | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.update | 更新一个特定的产品信息 | /commodity/goods/<string:goodid> | PUT, OPTIONS |
| leaf.views.commodity.product.create | 创建一个独立商品 | /commodity/goods | POST, OPTIONS |
| leaf.views.commodity.product.update | 更改商品标签 | /commodity/goods/<string:goodid>/tags | PUT, OPTIONS |
| leaf.views.commodity.product.update | 更新商品在售状态 | /commodity/goods/<string:goodid>/onsale | PUT, OPTIONS |
| leaf.views.commodity.product.get | 查询一个指定的商品信息 | /commodity/goods/<string:goodid> | HEAD, OPTIONS, GET |
| leaf.views.commodity.product.delete | 删除一个指定的商品 | /commodity/goods/<string:goodid> | OPTIONS, DELETE |