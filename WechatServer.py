#coding=utf-8
'''
Created on 2018-5-24
@author: daixuan
'''
import web
import time,datetime
import SendMsg
import sys
import urllib

reload(sys)
#sys.setdefaultencoding('utf8')

#把null内容改为默认为空
global null
null=''

#设置webpy的接口
urls = (
        "/api/model/send_sms/", "send_sms",
        "/check_service","send_sms",
        )
#启动app服务
app = web.application(urls, globals())

#定义写日志
ISOTIMEFORMAT='%Y-%m-%d %X'
def WriteLog(mess):
    today = datetime.date.today()
    logfile = open('./' +str(today)  + '.log','a')
    wrtmsg = str( time.strftime( ISOTIMEFORMAT, time.localtime() )) + '\n' + mess+'\n  \n'
    logfile.write(wrtmsg)
    logfile.close()

class send_sms:
    def GET(self):
        aaa = "{\"status\": \"OK\"}"
        return aaa



    def POST(self):
        dic1=dict(eval(web.data()))
        print dic1
        print type(dic1)

        if 'evalMatches' in dic1:
            if len(dic1['evalMatches']) == 0:
                description=null
            if len(dic1['evalMatches']) == 1:
                description = dic1['evalMatches'][0]['metric'] + ':' + str(dic1['evalMatches'][0]['value'])
            elif len(dic1['evalMatches']) == 2:
                description=dic1['evalMatches'][0]['metric']+ ':' +str(dic1['evalMatches'][0]['value']) + ' ' + \
                            dic1['evalMatches'][1]['metric']+ ':' +str(dic1['evalMatches'][1]['value'])
                #'disk.mean { device: sda1 host: cs19 } 59.7020874503disk.mean { host: cs21 device: sdb1 } 54.4980140058'
            elif len(dic1['evalMatches']) == 2:
                description = dic1['evalMatches'][0]['metric'] + ':' + str(dic1['evalMatches'][0]['value']) + ' ' + \
                              dic1['evalMatches'][1]['metric'] + ':' + str(dic1['evalMatches'][1]['value']) + ' ' + \
                              dic1['evalMatches'][2]['metric'] + ':' + str(dic1['evalMatches'][2]['value'])
            elif len(dic1['evalMatches']) > 2:
                description = dic1['evalMatches'][0]['metric'] + ':' + str(dic1['evalMatches'][0]['value']) + ' ' + \
                              dic1['evalMatches'][1]['metric'] + ':' + str(dic1['evalMatches'][1]['value']) + ' ' + \
                              dic1['evalMatches'][2]['metric'] + ':' + str(dic1['evalMatches'][2]['value'])
        else:
            description=null

        print 'description'
        print description

        if 'message' in dic1:
            message=dic1["message"] #"$host $device 磁盘用量超过85%，请注意是否集群健康"
            print 'message'
            print message
        else:
            message=null

        if 'ruleName' in dic1:
            ruleName=dic1["ruleName"] #"======CS磁盘用量预警alert，超过80%======"
            print ruleName
        else:
            ruleName=null

        if 'ruleUrl' in dic1:
            ruleUrl=dic1["ruleUrl"] #"http://localhost:3000/dashboard/db/schema-registry-cs?fullscreen&edit&tab=alert&panelId=13"
            print 'ruleUrl'
            print ruleUrl
        else:
            ruleUrl=null

        if 'title' in dic1:
            title=dic1["title"] #[Alerting] ======CS磁盘用量预警alert，超过80%======
            print 'title'
            print title
        else:
            title=null

        if 'imageUrl' in dic1:
            imageUrl=dic1["imageUrl"] #"http://grafana.org/assets/img/blog/mixed_styles.png"
            print 'imageUrl'
            print imageUrl
        else:
            imageUrl=null

        f = open("./Alarm_people.txt", "r")
        flag=1
        while True:
            line = f.readline()
            if line:  # 或者用 if line != "":
                SendMsg.sendMessage(line.strip(), title, description, ruleUrl, imageUrl)
                if flag==1:
#                    SendMsg.sendMessageChat(title, description, ruleUrl, imageUrl)
                    flag=0
            else:
                break
        f.close()

        #SendMsg.sendMessage('daixuan',title, description, ruleUrl, imageUrl)
        #PostStatus = "{\"status\": \"OK\"}"
        #return PostStatus
 
if __name__ == "__main__":
    app.run()


