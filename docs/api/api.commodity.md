
 <h1 class="curproject-name"> leaf.commodity </h1> 
 Leaf 的商品库存管理相关 API，由两个部分组成：SKU、SPU

SKU：库存管理单元，指单个商品的相关信息管理
SPU：产品管理单元，包含产品的管理与商品生成等操作


### 公共信息
<p><em>Leaf</em> 拥有完善的 <code data-backticks="1">SKU/SPU</code> 管理系统，开发者可以通过调用 <code data-backticks="1">API</code> 对其进行增删改查操作。</p>
<p>我们所有的 <code data-backticks="1">API</code> 都是 <code data-backticks="1">RESTful</code> 风格的，而认证则使用了基于 <code data-backticks="1">JWT Token</code> 的认证方案（参见用户部分的 <code data-backticks="1">JWT Token</code> 获取接口）</p>
<p>下面介绍这部分 <code data-backticks="1">API</code> 对接需要了解的一些基本概念：</p>
<ul>
<li><code data-backticks="1">ObjectId</code><br>
我们的文档类都有自己的一个唯一 <code data-backticks="1">id</code>, 一般情况下它是一个长度为 <strong>24</strong> 的十六进制字符串，它们看起来像是这样：<code data-backticks="1">5dfdebd0a2ed28fc8397f723</code><br>
在前后端的传输过程中可以直接使用这样的字符串指代对应的商品、产品。</li>
<li>产品类<br>
产品指的是一系列的商品集合，它通过不同的产品参数对应着不同的商品，它的文档结构类似如下：</li>
</ul>
<pre><code>{
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
</code></pre>
<p>每个字段的说明如下：</p>
<table>
<thead>
<tr>
<th align="center">字段</th>
<th align="center">类型</th>
<th align="left">说明</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">id</td>
<td align="center">ObjectId</td>
<td align="left">产品的唯一文档 Id</td>
</tr>
<tr>
<td align="center">name</td>
<td align="center">String</td>
<td align="left">产品名</td>
</tr>
<tr>
<td align="center">description</td>
<td align="center">String</td>
<td align="left">产品描述</td>
</tr>
<tr>
<td align="center">addition</td>
<td align="center">String</td>
<td align="left">产品额外说明</td>
</tr>
<tr>
<td align="center">tags</td>
<td align="center">list[String]</td>
<td align="left">产品标签</td>
</tr>
<tr>
<td align="center">parameters</td>
<td align="center">list[Parameter]</td>
<td align="left">产品参数，下文详述</td>
</tr>
<tr>
<td align="center">onsale</td>
<td align="center">Boolean</td>
<td align="left">是否上架</td>
</tr>
</tbody>
</table>
<ul>
<li>产品参数<br>
产品的不同型号是通过产品内部文档的参数文档定义的，它大概是这样的：</li>
</ul>
<pre><code>"parameters" : [ 
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
</code></pre>
<p>每个字段的说明如下：</p>
<table>
<thead>
<tr>
<th align="center">字段</th>
<th align="center">类型</th>
<th align="left">说明</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">name</td>
<td align="center">String</td>
<td align="left">参数名</td>
</tr>
<tr>
<td align="center">options</td>
<td align="center">List[String]</td>
<td align="left">参数列表</td>
</tr>
</tbody>
</table>
<ul>
<li>商品<br>
商品是每个销售页面的最小单元，它可以由产品根据不同参数生成得到，它的文档结构大概如下：</li>
</ul>
<pre><code>{
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
</code></pre>
<p>下面是每个字段的说明：</p>
<table>
<thead>
<tr>
<th align="center">字段</th>
<th align="center">类型</th>
<th align="left">说明</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">id</td>
<td align="center">ObjectId</td>
<td align="left">商品的唯一文档 Id</td>
</tr>
<tr>
<td align="center">individual</td>
<td align="center">Boolean</td>
<td align="left">商品是否由产品生成而来，是为 <code data-backticks="1">False</code>，否则为 <code data-backticks="1">True</code></td>
</tr>
<tr>
<td align="center">product</td>
<td align="center">ObjectId</td>
<td align="left">如果上面的 <code data-backticks="1">individual</code> 参数为 <code data-backticks="1">False</code>，此处为父产品Id</td>
</tr>
<tr>
<td align="center">name</td>
<td align="center">String</td>
<td align="left">商品名</td>
</tr>
<tr>
<td align="center">attributes</td>
<td align="center">Objects[ String, String ]</td>
<td align="left">商品的详细参数</td>
</tr>
<tr>
<td align="center">description</td>
<td align="center">String</td>
<td align="left">产品描述</td>
</tr>
<tr>
<td align="center">addition</td>
<td align="center">String</td>
<td align="left">产品额外说明</td>
</tr>
<tr>
<td align="center">tags</td>
<td align="center">list[String]</td>
<td align="left">产品标签</td>
</tr>
<tr>
<td align="center">extensions</td>
<td align="center">Objects[ String, String ]</td>
<td align="left">扩展保留字段</td>
</tr>
</tbody>
</table>

# 产品接口

## 根据产品 Id 查找产品信息
<a id=根据产品 Id 查找产品信息> </a>
### 基本信息

**Path：** /commodity/products/{productid}

**Method：** GET

**接口描述：**


### 请求参数
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e0d6c02cc5fa75312a2d958 |  产品 ProductId |

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回信息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> product</span></td><td key=1><span>string</span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品信息JSON字串</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 修改产品信息
<a id=修改产品信息> </a>
### 基本信息

**Path：** /commodity/products/{productid}

**Method：** PUT

**接口描述：**


### 请求参数
**Headers**

| 参数名称  | 参数值  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| Content-Type  |  application/x-www-form-urlencoded | 是  |   |   |
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e572b67357996c8f8b60ae6 |  产品Id ProductId |
**Body**

| 参数名称  | 参数类型  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| name | text  |  是 |  iPhone XR  |  产品名称 |
| description | text  |  否 |  iPhone X 系列贫穷版本  |  产品描述 |
| addition | text  |  否 |  哎呀，真香  |  附加描述 |
| tags | text  |  是 |  ["iPhone", "Apple", "手机", "苹果"]  |  产品标签列表 |



### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回信息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> product</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品JSON信息</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 删除产品
<a id=删除产品> </a>
### 基本信息

**Path：** /commodity/products/{productid}

**Method：** DELETE

**接口描述：**


### 请求参数
**Headers**

| 参数名称  | 参数值  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| Content-Type  |  application/x-www-form-urlencoded | 是  |   |   |
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e0d6c02cc5fa75312a2d958 |  产品Id ProductId |

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回消息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> status</span></td><td key=1><span>boolean</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">操作状态</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 删除产品参数
<a id=删除产品参数> </a>
### 基本信息

**Path：** /commodity/products/{productid}/parameters/{name}

**Method：** DELETE

**接口描述：**


### 请求参数
**Headers**

| 参数名称  | 参数值  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| Content-Type  |  application/x-www-form-urlencoded | 是  |   |   |
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e0d6c02cc5fa75312a2d958 |  产品Id ProductId |
| name |  参数名称 |  颜色 |

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回消息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> parameters</span></td><td key=1><span>string []</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">参数列表</span></td><td key=5><p key=3><span style="font-weight: '700'">item 类型: </span><span>string</span></p></td></tr><tr key=array-351><td key=0><span style="padding-left: 20px"><span style="color: #8c8a8a">├─</span> </span></td><td key=1><span></span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">参数JSON信息</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 删除产品相关所有商品
<a id=删除产品相关所有商品> </a>
### 基本信息

**Path：** /commodity/products/{productid}/goods

**Method：** DELETE

**接口描述：**
<p>该接口用于删除所有由指定产品生成的商品，此操作不可逆</p>


### 请求参数
**Headers**

| 参数名称  | 参数值  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| Content-Type  |  application/x-www-form-urlencoded | 是  |   |   |
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e0d6c02cc5fa75312a2d958 |  产品Id ProductId |

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回信息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> status</span></td><td key=1><span>boolean</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">操作状态</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 增加产品参数
<a id=增加产品参数> </a>
### 基本信息

**Path：** /commodity/products/{productid}/parameters

**Method：** POST

**接口描述：**


### 请求参数
**Headers**

| 参数名称  | 参数值  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| Content-Type  |  application/x-www-form-urlencoded | 是  |   |   |
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e0d6c02cc5fa75312a2d958 |  产品Id |
**Body**

| 参数名称  | 参数类型  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| name | text  |  是 |  颜色  |  产品参数名称 |
| options | text  |  是 |  ["深空灰", "银白色"]  |  详细的参数列表 |



### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回消息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> parameters</span></td><td key=1><span>string []</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">参数列表</span></td><td key=5><p key=3><span style="font-weight: '700'">item 类型: </span><span>string</span></p></td></tr><tr key=array-352><td key=0><span style="padding-left: 20px"><span style="color: #8c8a8a">├─</span> </span></td><td key=1><span></span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">参数JSON信息</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 新建产品
<a id=新建产品> </a>
### 基本信息

**Path：** /commodity/products

**Method：** POST

**接口描述：**


### 请求参数
**Headers**

| 参数名称  | 参数值  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| Content-Type  |  application/x-www-form-urlencoded | 是  |   |   |
**Body**

| 参数名称  | 参数类型  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| name | text  |  是 |  iPhone XR  |  产品名称 |
| description | text  |  否 |  iPhone X 系列贫穷版本  |  产品描述 |
| addition | text  |  否 |  哎呀，真香  |  附加描述 |
| tags | text  |  是 |  ["iPhone", "Apple", "手机", "苹果"]  |  产品标签列表 |



### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回信息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> product</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品JSON信息</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 切换产品上架状态
<a id=切换产品上架状态> </a>
### 基本信息

**Path：** /commodity/products/{productid}/onsale

**Method：** PUT

**接口描述：**


### 请求参数
**Headers**

| 参数名称  | 参数值  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| Content-Type  |  application/x-www-form-urlencoded | 是  |   |   |
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e0d6c02cc5fa75312a2d958 |  产品Id ProductId |
**Body**

| 参数名称  | 参数类型  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| onsale | text  |  是 |  1  |  数值转布尔值 - 0为下架，1为上架 |



### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回消息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> product</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品JSON信息</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 根据产品参数生成商品
<a id=根据产品参数生成商品> </a>
### 基本信息

**Path：** /commodity/products/{productid}/goods

**Method：** POST

**接口描述：**
<p>该接口根据产品的参数选项生成所有可能的商品，例如：</p>
<p>产品参数：</p>
<pre><code>{
    "颜色": ["白色", "红色", "黑色"],
    "大小": ["13寸", "15寸"]
}
</code></pre>
<p>其生成的商品将会有 <code data-backticks="1">2*3=6</code> 种，分别是：</p>
<pre><code>[
    {"颜色": "白色", "大小": "13寸"},
    {"颜色": "白色", "大小": "15寸"},
    {"颜色": "红色", "大小": "13寸"},
    {"颜色": "红色", "大小": "15寸"},
    {"颜色": "黑色", "大小": "13寸"},
    {"颜色": "黑色", "大小": "15寸"},
]
</code></pre>
<p>在产品参数较多时可能会计算时间较长，可使用 <code data-backticks="1">save</code> 参数指定是否立即入库；<br>
不立即入库时可以先让用户进行预览之后再进行入库（可以设置保存按钮重新提交一遍即可）。</p>


### 请求参数
**Headers**

| 参数名称  | 参数值  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| Content-Type  |  application/x-www-form-urlencoded | 是  |   |   |
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e0d6c02cc5fa75312a2d958 |  产品Id ProductId |
**Body**

| 参数名称  | 参数类型  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| save | text  |  是 |  0  |  是否直接入库(或是仅用于生成预览)；数值转布尔 - 1表示保存，0表示不保存 |
| price | text  |  是 |  999.99  |  商品初始价格 |
| inventory | text  |  是 |  999  |  商品初始库存 |
| currency | text  |  否 |  CNY  |  ISO 4217 - 三位货币代码 |



### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回信息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> goods</span></td><td key=1><span>string []</span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">商品信息列表</span></td><td key=5><p key=3><span style="font-weight: '700'">item 类型: </span><span>string</span></p></td></tr><tr key=array-353><td key=0><span style="padding-left: 20px"><span style="color: #8c8a8a">├─</span> </span></td><td key=1><span></span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">商品JSON信息</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 根据产品名称模糊查询
<a id=根据产品名称模糊查询> </a>
### 基本信息

**Path：** /commodity/products/name/{name}

**Method：** GET

**接口描述：**


### 请求参数
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| name |  MacBook |  要模糊查询的名称 |

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回消息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> products</span></td><td key=1><span>string []</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品信息数组</span></td><td key=5><p key=3><span style="font-weight: '700'">item 类型: </span><span>string</span></p></td></tr><tr key=array-354><td key=0><span style="padding-left: 20px"><span style="color: #8c8a8a">├─</span> </span></td><td key=1><span></span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap"></span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 根据产品标签查找产品信息
<a id=根据产品标签查找产品信息> </a>
### 基本信息

**Path：** /commodity/products/tags/{tags}

**Method：** GET

**接口描述：**


### 请求参数
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| tags |  Apple, MacBook |  产品标签 - 以 ',' 分割 |

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回信息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> products</span></td><td key=1><span>string []</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品信息列表</span></td><td key=5><p key=3><span style="font-weight: '700'">item 类型: </span><span>string</span></p></td></tr><tr key=array-355><td key=0><span style="padding-left: 20px"><span style="color: #8c8a8a">├─</span> </span></td><td key=1><span></span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品信息JSON字串</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 获取产品关联商品列表
<a id=获取产品关联商品列表> </a>
### 基本信息

**Path：** /commodity/products/{productid}/goods

**Method：** GET

**接口描述：**


### 请求参数
**路径参数**

| 参数名称 | 示例  | 备注  |
| ------------ | ------------ | ------------ |
| productid |  5e0d6c02cc5fa75312a2d958 |  产品Id ProductId |

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回消息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> goods</span></td><td key=1><span>string []</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">商品列表</span></td><td key=5><p key=3><span style="font-weight: '700'">item 类型: </span><span>string</span></p></td></tr><tr key=array-356><td key=0><span style="padding-left: 20px"><span style="color: #8c8a8a">├─</span> </span></td><td key=1><span></span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">商品JSON信息</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 获取全部产品
<a id=获取全部产品> </a>
### 基本信息

**Path：** /commodity/products

**Method：** GET

**接口描述：**


### 请求参数
**Query**

| 参数名称  |  是否必须 | 示例  | 备注  |
| ------------ | ------------ | ------------ | ------------ |
| count | 是  |  10 |  获取的记录个数 |
| previous | 否  |  5e0d6c02cc5fa75312a2d958 |  上一页最后一条记录 Id |

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回消息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> products</span></td><td key=1><span>string []</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品信息数组</span></td><td key=5><p key=3><span style="font-weight: '700'">item 类型: </span><span>string</span></p></td></tr><tr key=array-357><td key=0><span style="padding-left: 20px"><span style="color: #8c8a8a">├─</span> </span></td><td key=1><span></span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">产品信息JSON字串</span></td><td key=5></td></tr>
               </tbody>
              </table>
            
## 获取全部标签
<a id=获取全部标签> </a>
### 基本信息

**Path：** /commodity/products/tags

**Method：** GET

**接口描述：**
<p>该接口的计算量较大，因此会在后端配置缓存，请咨询后端配置缓存有效时间（默认为 3 小时）。</p>
<p>示例返回：</p>
<pre><code>{
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
</code></pre>


### 请求参数

### 返回数据

<table>
  <thead class="ant-table-thead">
    <tr>
      <th key=name>名称</th><th key=type>类型</th><th key=required>是否必须</th><th key=default>默认值</th><th key=desc>备注</th><th key=sub>其他信息</th>
    </tr>
  </thead><tbody className="ant-table-tbody"><tr key=0-0><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> code</span></td><td key=1><span>number</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回码</span></td><td key=5></td></tr><tr key=0-1><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> message</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回消息</span></td><td key=5></td></tr><tr key=0-2><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> description</span></td><td key=1><span>string</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">返回描述</span></td><td key=5></td></tr><tr key=0-3><td key=0><span style="padding-left: 0px"><span style="color: #8c8a8a"></span> tags</span></td><td key=1><span>object</span></td><td key=2>必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">标签名与数量映射</span></td><td key=5></td></tr><tr key=0-3-0><td key=0><span style="padding-left: 20px"><span style="color: #8c8a8a">├─</span> tag</span></td><td key=1><span>number</span></td><td key=2>非必须</td><td key=3></td><td key=4><span style="white-space: pre-wrap">标签的出现次数</span></td><td key=5></td></tr>
               </tbody>
              </table>
            