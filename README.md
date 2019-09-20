# Ops Platform
[TOC]
# 只用于学习交流
* 效果图
![avatar](https://s2.ax1x.com/2019/09/02/nPQrEF.jpg)
![avatar](https://s2.ax1x.com/2019/09/02/nPYlxH.jpg)
![nPzHDP.jpg](https://s2.ax1x.com/2019/09/02/nPzHDP.jpg)
* 更多效果图 -> https://github.com/Shadow-linux/ops-for-study/blob/master/docs/ops_instructions.md

## 一、概述
> 基础架构

* 存储：
    * MySQL 5.6   关系存储
    * Open-Falcon 0.2  时序存储
* 后端:
    * Django 2.0.1
    * djangorestframework 3.7.7
    * djangorestframework-jwt 1.11.0
* 前端:
    * Vue.js 2.5.10
    * IViwe 3.4.0   https://www.iviewui.com, https://github.com/iview/iview-admin


> Develop

* 前端
```
cd ${WORK_SPACE}/webpge
npm run dev
```
* 后端
    1. 可以使用pycharm ，设置 （recommand）
    ![nEXaDI.jpg](https://s2.ax1x.com/2019/09/04/nEXaDI.jpg)
    2. 直接通过原生命令启动

```
python3.6 manage.py 0.0.0.0:8001
```


## 二、编码规范

> Django 编码规范

1. 什么 Restful Api: http://www.ruanyifeng.com/blog/2018/10/restful-api-best-practices.html
2. 务必使用Class ViewSet 或 API View, 这个是django-restframework 提供的一个封装view，它主动关联了 DB数据， 且符合Restful Api规范, 其提供了以下的常用方法:
   * mixins.CreateModelMixin  == post 
   * mixins.RetrieveModelMixin ==  get(single)
   * mixins.UpdateModelMixin  == put, patch
   * mixins.DestroyModelMixin == delete
   * mixins.ListModelMixin == get(list) 
   * `不懂请结合现有代码自行研究`： https://www.django-rest-framework.org/tutorial/quickstart/ 
3. 数据库表名手动指定，不要使用默认，且根据模块设置表明
    * 如 users 模块, 则命名为 users_account
4. 代码优雅简洁
    * 如代码务必能简单明了的说明，功能复杂时尽量采用分而治之，不要出现过于臃肿的代码，尽量做到 “代码即注释及说明”。
    * 如把DB 的关系数据处理，使用 Django Rest Framework 的 Serializer ，https://www.django-rest-framework.org/api-guide/serializers/
    * 如把view.py 的简洁，复杂逻辑不应完整写在view，而是独立文件或文件夹，并清晰命名该功能
5. 注释明确优美
    * 如 UserRegister, 所有viewset, 及view 的注释会被 `public.operation.middleware.GlobalOperatingLogMiddleware` 劫持，记录该HTTP请求的注释，会自动按照方法记录到数据;
```python
class UsersRegisterViewSet(CreateModelMixin, viewsets.GenericViewSet):
        """
        create:
            用户注册
        """
        serializer_class = UsersRegisterSerializer
        queryset = UsersAccount.objects.all()
        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            del data['password']
            return Response(data, status=status.HTTP_201_CREATED)
 ```
    * 其余注释，如虽功能实现，逻辑混沌时务必写上注释， '#' 开头后空格后开始写注释
6. 尽可能利用Django造好的轮子，及已经存在的轮子
    * public.util 下的各种功能, ansible, 常用工具，时间处理等
    * message 下的发送功能
    * monitor 下的 falcon 及 urlooker api的复杂封装

> 代码风格

**Python**
1. 按照`PEP8`的编程风格，使用pycharm 时开启代码风格严格检查
    * https://www.python.org/dev/peps/pep-0008/
    * 如，新的函数和类是空格两行
    * 如，变量是需要小写，横杠连接
    * 简单来说，开启pycharm严格检查后，右边滚动条位置不应该出现大量白色的 " - " 检查提醒，而是在滚动条顶部出现绿色的 " ☑️"

**Js**
1. 只需要跟着babelrc 的限制规则即可，每次编译不符合规范则会提示你的格式错误，务必处理为suceess， 不能让其处于warning状态。

## 三、模块设计及划分
> 大模块分为 Public, Private

* public:  通常定义通常贯通全站的使用，且易于迁移，没有强关系
    * common: 一些小的功能，划分不成一个完整的大模块，就放此；
    * message: 信息发送相关，模版信息等；
    * operation: 操作记录等;
    * openapi: 是对外开放的一些api，只需登陆即可调用，(后面可做一个单独权限控制)；
    * permission: 所有权限都放在该模块，其他模块由此调用
    * users: 用户模块
    * util: 工具文件，并不是一个人模块
* private: 用于定义，比较私有化的设计，根据不同公司和单独功能来设计
    * activity: 业务相关功能（名字没起好，后面根据喜好改改）
    * apps: 应用管理相关
    * cmdb: 资产数
        * aliyun：阿里云
        * native：本地机房
        * cmdb_common:  适用于通用的的基础类
    * code_publish: 代码发布
    * monitor: 监控相关, 逻辑相对复杂, 数据源来自falcon， 所以falcon的工作原理，即插件编写的原理不能忽视
        * third_party： 是一个第三方服务的监控，划分了不同模块做数据收集分析及告警发送，留意algorithm.py 的简单算法
            * \__init__.py 总入口
        * falcon_api.py
            * 主要是对于falcon api 的封装，但是falcon api极其不人性化，所以进行了大量的封装;
            * 文档: http://api.open-falcon.com
        * app_alive.py
            * 关于app alive 监控
            * 流程: urlooker -> open-falcon
* ops
    * setting.py: 你懂的(django setting )
    * urls.conf: url 都集中管理于此，整个文件通过逻辑分割，（请后面维护的同学，遵循里面的逻辑划分）
* deploy.conf: 配置文件

> 页面权限校验

* 为了所有API ，在每个请求的时候会带一个 pp 的头部，该头部是`MD5`加密的，到服务端后，配对做校验；
    * 优点： 是所有API 提供了重用的方法；
    * 缺点：未结合时间加入`MD5` 做校验（后面为了加强安全性，可以加上时间校验）
 * 详细查看，文件: public.permission.perms
* 添加新权限，可参照文档 `${WORK_SPACE}/docs/更改站点web权限流程.md`






