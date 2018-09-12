# Wechat_grafana 说明
企业微信对接grafana告警服务(基于web.py框架)

# 使用方法：
### 1、请先注册企业微信：
打开企业微信注册页面：https://work.weixin.qq.com/wework_admin/register_wx?from=myhome  

输入申请信息，微信扫码绑定管理员，在【我的企业】-【企业信息】最末行获取企业id: ww02946fb9034b5649(每个企业id都不同)


### 2、创建企业应用，用于推送信息，创建方法：
打开【应用与小程序】https://work.weixin.qq.com/wework_admin/frame#apps ，选择【应用】，点击【创建应用】，注意：上传应用的logo，设置应用名称，选择可见应用部门范围（注意，这里应用应该属于企业而不是单独某个部门，否则后面创建回话群聊失败，错误码：60011），创建好后点击创建的应用，获取：
AgentId:1000003 #企业ID是1000001，创建子部门顺序加1
Secret:X56RLPUFZYyoaEBCNaZecSkWN-s3_ZRdKMYlK2KJuCA

### 3、安装web.py 
参考：http://webpy.org/install  这里不详细赘述

### 4、clone代码到服务器，修改GetAccessToken.py文件中的企业自定义的信息（这是获取token的必要信息，token是2小时过期一次，这里会获取返回code，过期重新获取）：
    CorpID="ww02946fb9034b5649"
    CorpSecret="jqwFdaSPLJrpoi_YK4M2-XvJp4BXNUGtB0ztEYUEUXo"
    AgentId=1000002
同时修改Alarm_people.txt文件中的告警接收人，如果有多个，请写多行（后期会加入聊天组，企业应用会向该聊天组中推送告警信息，不过得先调用api创建组名，因为信息推送的时候需要使用）
### 5、启动服务
    python WechatServer.py 8080 &

ps: 如果用 supervisorctl管理,请在/etc/supervisord/webchat_grafana.conf中添加：
```
[program:wechat-grafana]  
environment=HOME="/root/Wechat_grafana/"  
command=python /root/Wechat_grafana/WechatServer.py  8080  
directory=/root/Wechat_grafana/  
priority=999  
autostart=true  
startsecs=1  
autorestart=true  
user=root  
```
然后执行:
    supervisorctl reread
    supervisorctl add wechat-grafana


### 6、psotman 访问测试（该步骤可以跳过，只是为了测试）
请求方式：post  
请求地址：http://127.0.0.1:9090/api/model/send_sms/  
请求包体:
```
{"evalMatches":[{"value":100,"metric":"High value","tags":null},{"value":200,"metric":"Higher Value","tags":null}],"imageUrl":"http://grafana.org/assets/img/blog/mixed_styles.png","message":"Someone is testing the alert notification within grafana.","ruleId":0,"ruleName":"Test notification","ruleUrl":"http://grafana.prometheus.qiniu.io:80/","state":"alerting","title":"[Alerting] Test notification"}
```
  
Postman 返回结果：none  并且企业应用中收到告警信息

### 7、grafana上配置告警
打开自己的grafana页面，【设置】-【Alerting】-【Notification channels】 + New Channel  
Name: webchat（自定义）  
Type：webhook  
设置【Webhook settings】url：http://127.0.0.1:9090/api/model/send_sms/   
(ip地址、端口自与启动服务的端口对应，转发地址：/api/model/send_sms/ 与WechatServer.py文件中【设置webpy的接口】对应）  
然后在对应的监控页面中设置告警规则，其中【Alert】-【Notifications】设选中添加的Name为：webchat的告警通道

# 向群聊会话中推送消息 
### 8、首先创建一个群
创建方法参考：https://work.weixin.qq.com/api/doc#13288 ，注意：一个企业中至少包含2个以上用户方可创建群聊会话，请在【通讯录】中添加其他用户（通
过发送邀请给对方，微信或者短信授权登陆）,使用Postman创建群聊会话的参数：  
请求方式： POST（HTTPS）  
请求地址： https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token=ACCESS_TOKEN  
请求包体:  
```
{
    "name" : "告警群",
    "owner" : "User1",
    "userlist" : ["User1","User2"],
    "chatid" : "CHATID"
}
```

### 9、修改代码
取消WechatServer.py文件中该行行首的注释符号: 
 
    SendMsg.sendMessageChat(title, description, ruleUrl, imageUrl)

### 10、重新启动服务
    python WechatServer.py 9090 &  
参考方法6、7步骤进行实际测试，用户daixuan会在【告警群】收到对应的告警通知

