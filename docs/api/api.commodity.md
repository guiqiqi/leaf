# leaf.commodity
Leaf 的商品库存管理相关 API，由两个部分组成：SKU、SPU

SKU：库存管理单元，指单个商品的相关信息管理
SPU：产品管理单元，包含产品的管理与商品生成等操作

## Public Information
_Leaf_ 拥有完善的 `SKU/SPU` 管理系统，开发者可以通过调用 `API` 对其进行增删改查操作。

我们所有的 `API` 都是 `RESTful` 风格的，而认证则使用了基于 `JWT Token` 的认证方案（参见用户部分的 `JWT Token` 获取接口）

下面介绍这部分 `API` 对接需要了解的一些基本概念：

* `ObjectId`
我们的文档类都有自己的一个唯一 `id`, 一般情况下它是一个长度为 **24** 的十六进制字符串，它们看起来像是这样：`5dfdebd0a2ed28fc8397f723`
在前后端的传输过程中可以直接使用这样的字符串指代对应的商品、产品。
* 产品类
产品指的是一系列的商品集合，它通过不同的产品参数对应着不同的商品，它的文档结构类似如下：

```
{
    "_id" : ObjectId("5e0d6c02cc5fa75312a2d958"),
    "name" : "Macbook 2019",
    "description" : "苹果公司2019年最新笔记本电脑",
    "addition" : "这可能是全球最香的笔记本电脑",
    "tags" : [ 
        "macbook", 
        "笔记本", 
        "apple", 
        "苹果", 
        "电脑"
    ],
    "parameters" : [ 
        // 产品参数
    ],
    "onsale" : true
}
```

每个字段的说明如下：

| 字段 | 类型 | 说明 |
| :---: | :---: | :--- |
| id | ObjectId | 产品的唯一文档 Id |
| name | String | 产品名 |
| description | String | 产品描述 |
| addition | String | 产品额外说明 |
| tags | list[String] | 产品标签 |
| parameters | list[Parameter] | 产品参数，下文详述 |
| onsale | Boolean | 是否上架 |

* 产品参数
产品的不同型号是通过产品内部文档的参数文档定义的，它大概是这样的：

```
"parameters" : [ 
    {
        "name" : "屏幕",
        "options" : [ 
            "13寸", 
            "15寸", 
            "16寸"
        ]
    }, 
    {
        "name" : "内存",
        "options" : [ 
            "8GB", 
            "16GB", 
            "32GB", 
            "64GB"
        ]
    }, 
    {
        "name" : "硬盘",
        "options" : [ 
            "128GB", 
            "256GB", 
            "512GB", 
            "1TB", 
            "3TB"
        ]
    }, 
    {
        "name" : "颜色",
        "options" : [ 
            "深空灰", 
            "银白色"
        ]
    }, 
    {
        "name" : "TouchBar",
        "options" : [ 
            "有", 
            "无"
        ]
    }
]
```

每个字段的说明如下：

| 字段 | 类型 | 说明 |
| :---: | :---: | :--- |
| name | String | 参数名 |
| options | List[String] | 参数列表 |

* 商品
商品是每个销售页面的最小单元，它可以由产品根据不同参数生成得到，它的文档结构大概如下：

```
{
    "_id" : ObjectId("5e573a2e716ca42ad6a19ade"),
    "individual" : false,
    "product" : ObjectId("5e0d6c02cc5fa75312a2d958"),
    "name" : "Macbook 2019",
    "attributes" : {
        "TouchBar" : "有",
        "屏幕" : "13寸",
        "内存" : "8GB",
        "硬盘" : "128GB",
        "颜色" : "深空灰"
    },
    "description" : "苹果公司2019年最新笔记本电脑",
    "addition" : "这可能是全球最香的笔记本电脑",
    "tags" : [ 
        "macbook", 
        "笔记本", 
        "apple", 
        "苹果", 
        "电脑"
    ],
    "extensions" : {}
}
```

下面是每个字段的说明：

| 字段 | 类型 | 说明 |
| :---: | :---: | :--- |
| id | ObjectId | 商品的唯一文档 Id |
| individual | Boolean | 商品是否由产品生成而来，是为 `False`，否则为 `True` |
| product | ObjectId | 如果上面的 `individual` 参数为 `False`，此处为父产品Id |
| name | String | 商品名 |
| attributes | Objects[ String, String ] | 商品的详细参数 |
| description | String | 产品描述 |
| addition | String | 产品额外说明 |
| tags | list[String] | 产品标签 |
| extensions | Objects[ String, String ] | 扩展保留字段 |

---

### /products/{productid}

#### GET
##### Summary:

根据产品 Id 查找产品信息

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品 ProductId | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### PUT
##### Summary:

修改产品信息

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品Id ProductId | Yes | string |
| name | formData | 产品名称 | No | string |
| description | formData | 产品描述 | No | string |
| addition | formData | 附加描述 | No | string |
| tags | formData | 产品标签列表 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### DELETE
##### Summary:

删除产品

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品Id ProductId | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /products/{productid}/parameters/{name}

#### DELETE
##### Summary:

删除产品参数

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品Id ProductId | Yes | string |
| name | path | 颜色 | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /products/{productid}/goods

#### DELETE
##### Summary:

删除产品相关所有商品

##### Description:

该接口用于删除所有由指定产品生成的商品，此操作不可逆

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品Id ProductId | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### POST
##### Summary:

根据产品参数生成商品

##### Description:

该接口根据产品的参数选项生成所有可能的商品，例如：

产品参数：
```
{
    "颜色": ["白色", "红色", "黑色"],
    "大小": ["13寸", "15寸"]
}
```

其生成的商品将会有 `2*3=6` 种，分别是：
```
[
    {"颜色": "白色", "大小": "13寸"},
    {"颜色": "白色", "大小": "15寸"},
    {"颜色": "红色", "大小": "13寸"},
    {"颜色": "红色", "大小": "15寸"},
    {"颜色": "黑色", "大小": "13寸"},
    {"颜色": "黑色", "大小": "15寸"},
]
```

在产品参数较多时可能会计算时间较长，可使用 `save` 参数指定是否立即入库；
不立即入库时可以先让用户进行预览之后再进行入库（可以设置保存按钮重新提交一遍即可）。

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品Id ProductId | Yes | string |
| save | formData | 是否直接入库(或是仅用于生成预览)；数值转布尔 - 1表示保存，0表示不保存 | No | string |
| price | formData | 商品初始价格 | No | string |
| inventory | formData | 商品初始库存 | No | string |
| currency | formData | ISO 4217 - 三位货币代码 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### GET
##### Summary:

获取产品关联商品列表

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品Id ProductId | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /products/{productid}/parameters

#### POST
##### Summary:

增加产品参数

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品Id | Yes | string |
| name | formData | 产品参数名称 | No | string |
| options | formData | 详细的参数列表 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /products

#### POST
##### Summary:

新建产品

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| name | formData | 产品名称 | No | string |
| description | formData | 产品描述 | No | string |
| addition | formData | 附加描述 | No | string |
| tags | formData | 产品标签列表 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

#### GET
##### Summary:

获取全部产品

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| count | query | 获取的记录个数 | No | string |
| previous | query | 上一页最后一条记录 Id | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /products/{productid}/onsale

#### PUT
##### Summary:

切换产品上架状态

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| productid | path | 产品Id ProductId | Yes | string |
| onsale | formData | 数值转布尔值 - 0为下架，1为上架 | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /products/name/{name}

#### GET
##### Summary:

根据产品名称模糊查询

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| name | path | 要模糊查询的名称 | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /products/tags/{tags}

#### GET
##### Summary:

根据产品标签查找产品信息

##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| tags | path | 产品标签 - 以 ',' 分割 | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |

### /products/tags

#### GET
##### Summary:

获取全部标签

##### Description:

该接口的计算量较大，因此会在后端配置缓存，请咨询后端配置缓存有效时间（默认为 3 小时）。

示例返回：
```
{
  "code": 0,
  "message": "success",
  "description": "成功",
  "tags": {
    "macbook": 1,
    "笔记本": 1,
    "apple": 1,
    "苹果": 1,
    "电脑": 1
  }
}
```

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
|		|			|				|		|		|

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | object |
