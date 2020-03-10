# leaf.rbac

Leaf 开发文档与测试 - RBAC 部分

Leaf 实现了基于角色的权限管理系统，通过用户组的方式对用户分类并给予不同的角色。
Leaf 支持动态的更改接口所需要的权限，并提供了相应的接口。
下面分为四个部分对这个部分的 API 进行说明：用户、用户组、认证、访问点。

## Public Information
_Leaf_ 实现了基于角色的权限管理系统，通过用户组的方式对用户分类并给予不同的角色；在 `RBAC` 的管理框架中涉及到了四个子类：

| 类名 | 说明 | 用途 |
| --- | --- | --- |
| `User` | 用户类 | 用户信息存储 |
| `Group` | 用户组类 | 用于分组用户，同时也机遇用户所在组权限 |
| `Authentication` | 认证类 | 用于认证用户登录 |
| `AccessPoint` | 接入点类 | 用于动态的控制每一个 `API` 所需要的访问权限 |

我们所有的 `API` 都是 `RESTful` 风格的，而认证则使用了基于 `JWT Token` 的认证方案。

下面是一些**重要的概念**：

* `ObjectId`
我们的文档类都有自己的一个唯一 `id`, 一般情况下它是一个长度为 **24** 的十六进制字符串，它们看起来像是这样：`5dfdebd0a2ed28fc8397f723`
在前后端的传输过程中可以直接使用这样的字符串指代对应的用户、用户组。
* 角色与用户组
每一个用户组文档中都包含有一个 `permission` 值，用以指代该用户组的权限，而用户组中的用户就拥有这个等级的权限（角色）
* 访问点
访问点是我们用来对接口进行动态权限管理的工具，每一个访问点 `AccessPoint` 文档中都类似这样：

```
{
    "_id" : "leaf.plugins.wxtoken.get",
    "required" : 3,
    "strict" : false,
    "description" : "获取微信接口Token权限",
    "exception" : []
}
```

访问点的 `id` 表示访问点名称（这里是少数不使用 `ObjectId` 的地方），全局且唯一；
`required` 表示需要的权限值 - 对应用户组的组权限；
`strict` 表示是否启用严格认证，当启用后，仅指定的权限值用户可以访问；
`exception` 存储了例外用户，这些用户可以无视权限认证直接访问该接口

* 个人信息与扩展
和其他的 `CMS` 框架有所不同，在 _Leaf_ 中为了保证高扩展性，每一个用户的个人信息并不是由数据库中的某个字段直接进行存储的，而是类似 `JSON` 文档一般，所以在用户个人信息的更新过程中请直接在 `POST` 的 `form` 中提交所有的个人信息键值对，类似这样：

```
{
    "用户昵称": "桂小方",
    "年龄": 20,
    "有女朋友吗": "简直是在做梦",
    ...
}
```

而在几乎所有的文档中都保留了一个扩展信息字典，用以方便后期的扩展。

* 用户索引
用户索引指的是用以对用户进行查找、鉴权文档创建的信息，它看起来像是这样：

```
{
    "typeid" : "0C6B4A2B8AAEDDBC",
    "value" : "桂小方",
    "description" : "用户名索引",
    "extension" : {}  /* 用于存储扩展信息 */
}
```

每一个索引都有自己的 `typeid` 作为索引值，而 `value` 则表示索引的真正值
在 **查询索引类型信息** 接口中可以通过 `API` 来获取所有后端允许的索引信息：

```
"Id": ["1B4E705F3305F7FB", "通过用户ID索引"],
"Mail": ["EAC366AD5FEA1B28", "通过邮件索引"],
"Name": ["0C6B4A2B8AAEDDBC", "通过用户名索引"],
"Phone": ["5E4BC1ABDDAACA4A", "通过手机号索引"]
...
```

而在提交时请携带索引的 `typeid` 与 `value` 值。
而每一个用户都有一个通过 `Id` 的索引，此索引**不能被删除/修改**。

* 认证文档
一个认证文档通俗的说就是一种**登陆方式**，在用户创建好对应的索引信息之后可以用索引来创建认证文档

以上就是四类接口中基础概念的介绍，下面是接口文档 :)

---

### /jwts/{token}

#### POST
##### Summary:

请求 JWT-Token

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| token | path | 用户的认证令牌 | Yes | string |
| password | formData | 用户口令 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /auths/{userid}/{typeid}

#### POST
##### Summary:

创建认证文档

##### Description:

在创建身份文档时需要使用用户的口令（也就是密码）来进行验证，不正确时会返回认证错误信息。

在创建认证文档之后就可以通过给定的索引信息登录了。

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 userid | Yes | string |
| typeid | path | 用户索引 typeid | Yes | string |
| password | formData | 用户认证口令 - 需要和之前的认证口令保持一致 | No | string |
| description | formData | 当不给给定时，使用系统内部描述代替 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /auths/{userid}/{index}

#### DELETE
##### Summary:

删除用户某认证文档

##### Description:

不能够删除以用户 `userid` 创建的认证文档

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 userid | Yes | string |
| index | path | 用户用以创建认证文档的索引值 | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /auths/{userid}/password

#### PUT
##### Summary:

更改密码

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 userid | Yes | string |
| current | formData | 用户当前密码 | No | string |
| new | formData | 用户新密码 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /auths/{index}/status

#### PUT
##### Summary:

更新认证文档状态

##### Description:

认证文档状态即指的是登陆方式是否被禁用，一旦设置为 `false` 用户便无法通过这种方式登录

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| index | path | 用户用于创建认证文档的索引值 | Yes | string |
| status | formData | 更新之后认证文档状态 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /auths/{userid}

#### GET
##### Summary:

查询认证与索引映射

##### Description:

返回信息示例：
```
{
  "code": 0,
  "message": "success",
  "description": "成功",
  "auths": [
    [
      "{\"typeid\": \"1B4E705F3305F7FB\", \"value\": \"5dfdebd0a2ed28fc8397f723\", \"description\": \"\\u901a\\u8fc7\\u7528\\u6237ID\\u7d22\\u5f15\", \"extension\": {}}",
      true
    ],
    [
      "{\"typeid\": \"0C6B4A2B8AAEDDBC\", \"value\": \"\\u6842\\u5c0f\\u65b9\", \"description\": \"\\u7528\\u6237\\u540d\\u7d22\\u5f15\", \"extension\": {}}",
      false
    ],
    [
      "{\"typeid\": \"EAC366AD5FEA1B28\", \"value\": \"guiqiqi187@gmail.com\", \"description\": \"\\u901a\\u8fc7\\u90ae\\u4ef6\\u7d22\\u5f15\", \"extension\": {\"verified\": false}}",
      false
    ]
  ]
}
```

这个 `API` 用于查询用户的索引是否被用来创建登陆文档

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 userid | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /accesspoints

#### POST
##### Summary:

创建接入点

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| pointname | formData | 接入点名称 | No | string |
| required | formData | 接入点所需权限值 - 整型 | No | string |
| strict | formData | 是否启用严格模式 - 布尔型数值 | No | string |
| description | formData | 接入点描述 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### GET
##### Summary:

获取所有接入点

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
|		|			| 			|			|		|

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /accesspoints/{pointname}

#### DELETE
##### Summary:

删除接入点

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| pointname | path | 接入点 pointname | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### PUT
##### Summary:

更新接入点

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| pointname | path | 接入点名称 pointname | Yes | string |
| required | formData | 接入点所需权限值 - 整型 | No | string |
| strict | formData | 是否启用严格模式 - 布尔型数值 | No | string |
| description | formData | 接入点描述 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### GET
##### Summary:

查询接入点

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| pointname | path | 接入点名称 | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /accesspoints/{pointname}/exceptions

#### PUT
##### Summary:

管理接入点特权用户

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| pointname | path | 接入点名称 pointname | Yes | string |
| users | formData | 特权用户列表 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/avatar/{userid}

#### POST
##### Summary:

设置用户头像

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | userid | Yes | string |
| avatar | formData | 头像文件 | No | file |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### GET
##### Summary:

获取用户头像

##### Description:

使用该接口的 HTTP 状态码意义：

* 404: 该用户未设置头像
* 304: 用户头像未更新
* 200: 判断是否为 `JSON` 错误描述

该接口直接返回用户头像文件，并使用 `If-Modified-Since` HTTP头判断请求的文件是否更新。

另外，该接口不需要权限认证。

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | userid | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### DELETE
##### Summary:

删除用户头像

##### Description:

当返回 `True` 时说明头像已被删除。

当返回 `False` 时说明用户未曾设置头像。

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | userid | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users

#### GET
##### Summary:

批量获取用户

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| previous | query | 上次获取到的最后一个 userid | No | string |
| count | query | 需要获取的个数 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### POST
##### Summary:

创建用户

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| password | formData | 用户密码 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/{userid}

#### GET
##### Summary:

查询单个用户 - 根据 userid

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | userid | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### DELETE
##### Summary:

删除用户

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 userid | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/{typeid}/{index}

#### GET
##### Summary:

查询用户 - 根据用户 index

##### Description:

用户的 UserIndex 指的是用户索引，调用此API所需的信息有：

* index.typeid - 索引的类型id，一串随机字符串
* index.value - 索引值，例如用户名之类的索引

具体的介绍请参照说明文档的 `RBAC` 部分，开发者可以通过调用 `api.rbac.other.indexs` 来获取所有的用户索引介绍。

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| typeid | path | 查询的 Index-Type-Id | Yes | string |
| index | path | 查询的 Index-Value | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/{userid}/groups/{groupid}

#### POST
##### Summary:

加入用户组

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 Id | Yes | string |
| groupid | path | 用户组 Id | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### DELETE
##### Summary:

移出用户组

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 Id | Yes | string |
| groupid | path | 用户组 Id | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/{userid}/indexs

#### POST
##### Summary:

为用户新增索引

##### Description:

返回值示例：

```
{
  "code": 0,
  "message": "success",
  "description": "成功",
  "user": [
    "{\"typeid\": \"1B4E705F3305F7FB\", \"value\": \"5dfdebd0a2ed28fc8397f723\", \"description\": \"\\u901a\\u8fc7\\u7528\\u6237ID\\u7d22\\u5f15\", \"extension\": {}}",
    "{\"typeid\": \"0C6B4A2B8AAEDDBC\", \"value\": \"\\u6842\\u5c0f\\u65b9\", \"description\": \"\\u7528\\u6237\\u540d\\u7d22\\u5f15\", \"extension\": {}}",
    "{\"typeid\": \"EAC366AD5FEA1B28\", \"value\": \"guiqiqi187@gmail.com\", \"description\": \"\\u901a\\u8fc7\\u90ae\\u4ef6\\u7d22\\u5f15\", \"extension\": {\"verified\": false}}"
  ]
}
```

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 userid | Yes | string |
| typeid | formData | 索引类型 Id | No | string |
| value | formData | 索引值 | No | string |
| extension | formData | 扩展信息JSON字串 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/{userid}/informations

#### PUT
##### Summary:

更新用户个人信息

##### Description:

调用此API时请直接将所有的信息以键值对的形式保存在 \`form\` 中即可

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户的 userid | Yes | string |
| 名字 | formData | 任意参数对 | No | string |
| 性别 | formData | 任意参数对 | No | string |
| 女朋友 | formData | 任意参数对 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/{userid}/status

#### PUT
##### Summary:

更新用户状态

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 userid | Yes | string |
| status | formData | 更新之后的用户状态 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/{userid}/indexs/{typeid}

#### DELETE
##### Summary:

删除用户特定索引

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| userid | path | 用户 userid | Yes | string |
| typeid | path | 指定的索引类型 | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /users/indexs

#### GET
##### Summary:

查询索引类型信息

##### Description:

返回值类似如下：

```
{
  "code": 0,
  "message": "success",
  "description": "成功",
  "indexs": {
    "Id": [
      "1B4E705F3305F7FB",
      "通过用户ID索引"
    ],
    "Mail": [
      "EAC366AD5FEA1B28",
      "通过邮件索引"
    ],
    "Name": [
      "0C6B4A2B8AAEDDBC",
      "通过用户名索引"
    ],
    "Phone": [
      "5E4BC1ABDDAACA4A",
      "通过手机号索引"
    ]
  }
}
```

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
|      |            |             |          |        |



##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /groups

#### POST
##### Summary:

创建用户组

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| name | formData | 用户组名称 | No | string |
| permission | formData | 用户组权限 - 整形 | No | string |
| description | formData | 用户组描述 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### GET
##### Summary:

批量获取用户组

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
|		|			|				|		|		|

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /groups/{groupid}

#### DELETE
##### Summary:

删除用户组

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| groupid | path | 用户组 groupid | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### PUT
##### Summary:

更新用户组信息

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| groupid | path | 用户组 groupid | Yes | string |
| name | formData | 新的用户组名称 | No | string |
| permission | formData | 新的用户组权限 | No | string |
| description | formData | 新的用户组描述 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### GET
##### Summary:

查询单个用户组 - 根据 groupid

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| groupid | path | 用户组 groupid | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /groups/{groupid}/users

#### PUT
##### Summary:

更新用户列表

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| groupid | path | 用户组 groupid | Yes | string |
| users | formData | 用户 userid 列表 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /groups/name/{name}

#### GET
##### Summary:

查询单个用户组 - 根据 name

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| name | path | 用户组名 | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |
