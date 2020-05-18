
以下是 _Leaf_ 的现有的所有错误代码及其描述:

| 错误代码 | 错误描述 | 所属模块 |
| :----: | | :----: | :----: |
| 10010 | 非法的 ObjectId 字符串 | leaf.api.error |
| 10011 | 项目达到最大注册数量限制 | leaf.core.events |
| 10012 | 非法根节点名称 | leaf.core.events |
| 10013 | 非法事件名称 | leaf.core.events |
| 10014 | 未找到对应的事件 | leaf.core.events |
| 10015 | 无法找到该用户的Id验证文档 | leaf.rbac.error |
| 10016 | 创建/更新身份验证-密码验证失败 | leaf.rbac.error |
| 10017 | 根据给定的文档索引无法查找到身份验证文档 | leaf.rbac.error |
| 10018 | 根据给定信息找不到用户 | leaf.rbac.error |
| 10019 | 用户初始化已经完成 | leaf.rbac.error |
| 10020 | 根据给定的信息找不到访问点文档 | leaf.rbac.error |
| 10021 | 根据给定的信息找不到用户组文档 | leaf.rbac.error |
| 10022 | 您所给定的用户索引信息已经被绑定 | leaf.rbac.error |
| 10023 | 您所给定的用户索引类型已经被绑定 - 且当前策略不允许多绑定 | leaf.rbac.error |
| 10024 | 不能删除根据 用户Id 创建的认证文档 | leaf.rbac.error |
| 10025 | 根据给定信息找不到对应的产品 | leaf.selling.error |
| 10026 | 找不到对应的产品参数信息 | leaf.selling.error |
| 10027 | 产品参数信息发现重复 | leaf.selling.error |
| 10028 | 根据给定信息找不到对应的商品 | leaf.selling.error |
| 10029 | 不允许给定的货币类型进行交易 | leaf.selling.error |
| 10030 | 不能用空商品列表创建订单 | leaf.selling.error |
| 10031 | 商品货币类型不统一 | leaf.selling.error |
| 10032 | 试图创建订单的商品已经停售 | leaf.selling.error |
| 10033 | 所选商品库存不足 | leaf.selling.error |
| 10034 | 无法找到支付平台通知到的订单 | leaf.selling.error |
| 10101 | 插件载入时出错 | leaf.plugins.error |
| 10102 | 没有找到对应的插件 | leaf.plugins.error |
| 10103 | 插件 init 函数错误 | leaf.plugins.error |
| 10104 | 插件运行期间出现错误 | leaf.plugins.error |
| 11001 | 该状态码已经被使用, 请更换状态码 | leaf.core.algorithm.fsm |
| 11002 | 当前状态不接受发生的指定事件 | leaf.core.algorithm.fsm |
| 11003 | 根据当前状态和事件不能确定转移的目标状态 | leaf.core.algorithm.fsm |
| 12001 | 对消息体的签名验证出现错误 | leaf.weixin.error |
| 12002 | 在消息体加密过程中出现错误 | leaf.weixin.error |
| 12003 | 在消息体解密过程中发生错误 | leaf.weixin.error |
| 12004 | 消息体不正确(键缺少/数据类型非法) | leaf.weixin.error |
| 12111 | JWT Token 头部格式错误/不支持 | leaf.rbac.error |
| 12112 | JWT Token 格式错误 | leaf.rbac.error |
| 12113 | JWT Token 的签名计算错误 - 检查secret是否与算法匹配 | leaf.rbac.error |
| 12114 | JWT Token 签名验证错误 | leaf.rbac.error |
| 12115 | JWT Token 过期 | leaf.rbac.error |
| 12116 | 在 HTTP Header 信息中没有发现 JWT Token 信息 | leaf.rbac.error |
| 13001 | 身份验证错误 | leaf.rbac.error |
| 13003 | 传入的例外用户组无法被识别/用户ID错误 | leaf.rbac.error |
| 13004 | 访问点名称冲突 | leaf.rbac.error |
| 13005 | 未定义的用户索引类型 | leaf.rbac.error |