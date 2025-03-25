# ApiTest
#### 介绍
基于python+pytest+allure+requests开发的接口自动化框架

#### 软件架构
基于目前业界比较常见自动化框架封装模式


#### 安装教程

1.  pip install -r requirements.txt


#### 使用说明

1.  安装对应的包之后，在test_data中编写yaml用例
2.  yaml格式需要遵循一定的规则，如下
3.  api_name 接口名称
    api_request 请求信息
    metthod 请求类型
    url 请求接口
    data 请求数据
    headers 请求头
    validate 断言
    sql： sql语句
详细可以参考我给出的例子

```yaml
-
  api_name: 测试查询机型列表接口所有参数正常 # 用例名称
  api_request: # 请求信息
    method: GET # 请求类型
    url: /tcl-template-cms/tpl/machinetab/getAllMachine # 请求接口
    data:
      code: 9653
      licence: 331
      groups: UI5.0
      machineLabel: 0
      tabId: 1
      deployType: 1
    headers:
      X-Csrf-Token: $cache{token}
      Cookie: rhp=https://idsaas.test.leiniao.com; JSESSIONID=$cache{api-token}; return-url=https://idsaas.test.leiniao.com/page/cms-launcher/#/moduleService/machineTabList
      Content-Type: application/x-www-form-urlencoded
      traditional: "true"
      User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36
      Accept-Language: en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,es-US;q=0.6,es;q=0.5,pt-PT;q=0.4,pt;q=0.3,it-IT;q=0.2,it;q=0.1,zh-CN;q=0.1,zh;q=0.1,ar-IL;q=0.1,ar;q=0.1,ru-RU;q=0.1,ru;q=0.1,zh-TW;q=0.1,en-US;q=0.1,es-ES;q=0.1,smn-FI;q=0.1,smn;q=0.1,hy-AM;q=0.1,hy;q=0.1
      Accept-Encoding: gzip, deflate, br
  validate: #断言
    code:
      jsonpath: $.code
      type: ==
      value: 100000
      AssertType:
    status_code:
      jsonpath: $.status_code
      type: ==
      value: 200
      AssertType:
    msg:
      jsonpath: $.msg
      type: ==
      value: OK
      AssertType:
    name:
      jsonpath: $.data[0].name
      type: ==
      value: TCL-CN-MT9653-C78G
      AssertType:
  sql:
```
4、自定义方法以及变量的使用
