#coding=utf-8
'''
Created on 2018-5-24
@author: daixuan
'''
import urllib2
import GetAccessToken
import json
import WriteFile
import time
import sys

def messageBody(touser,title,description,ruleUrl,imageUrl):
    message = {
        "touser":touser,
               #"toparty": PartyID1,
               #"totag": totag,
               "msgtype": "news",
                   "agentid": 1000002,
                   "news" : {
                   "articles" : [
                       {
                           "title" : title,
                           "description" : description,
                           "url" : ruleUrl,
                           "picurl" : imageUrl,
                           "btntxt":"更多"
                       }
                    ]
               }
        }
    return message

def messageBodyChat(title,description,ruleUrl,imageUrl):
    message = {
        "chatid": "DoraSreInsideTest",
        "msgtype": "news",
        "news" : {
            "articles" : [
                {
                   "title" : title,
                   "description" : description,
                   "url" : ruleUrl,
                   "picurl" : imageUrl,
                   "btntxt":"更多"
               }
            ]
           }
        }
    return message




def postMsg(url, data):
    data = json.dumps(data,ensure_ascii=False)
    req = urllib2.Request(url)
    req.add_header('encoding', 'utf-8')
    resp = urllib2.urlopen(req,data)
    return resp.read()

def sendMessage(user,title,description,ruleUrl,imageUrl):
    accessToken =  GetAccessToken.GetAccessTokenFromLocal()   
    posturl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+ accessToken    
    sendResult = postMsg(posturl ,messageBody(user.encode('utf-8'),title,description,ruleUrl,imageUrl))
    code = str(json.loads(sendResult)['errcode'])
    #code = '0'
    if code == '0':
        WriteFile.WriteLog('SendMessage','Info','UserName:' +user + ' |1_SendMessage:' + title,'a')
        WriteFile.WriteLog('SendMessage','OKINFO_1',str(messageBody(user,title,description,ruleUrl,imageUrl)),'a')
        #return 'OK'
    elif code == '42001':
        GetAccessToken.GetAccessTokenFromWechat()
        accessToken =  GetAccessToken.GetAccessTokenFromLocal()
        posturl =  'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+ accessToken
        time.sleep(1)
        postMsg(posturl ,messageBody(user,title,description,ruleUrl,imageUrl))
        WriteFile.WriteLog('SendMessage','Wran','UserName:' +user + ' |SendMessage:' + title + ' |Errorcode:'+code,'a')
    elif code == '40014':
        GetAccessToken.GetAccessTokenFromWechat()
        accessToken =  GetAccessToken.GetAccessTokenFromLocal()
        posturl =  'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+ accessToken
        time.sleep(1)
        postMsg(posturl ,messageBody(user,title,description,ruleUrl,imageUrl))
        WriteFile.WriteLog('SendMessage','Wran','UserName:' +user + ' |SendMessage:' + title + ' |Errorcode:'+code,'a')
    else:
        WriteFile.WriteLog('SendMessage','Error','UserName:' +user + ' |SendMessage:' + title + ' |Errorcode:'+code,'a')
        WriteFile.WriteLog('SendMessage','ErrorINFO1',user,'a')



# def sendMessageChat(title,description,ruleUrl,imageUrl):
#     accessToken =  GetAccessToken.GetAccessTokenFromLocal()
#     #posturl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+ accessToken
#     posturl = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token='+ accessToken
#     sendResult = postMsg(posturl ,messageBodyChat(title,description,ruleUrl,imageUrl))
#     code = str(json.loads(sendResult)['errcode'])
#     #code = '0'
#     if code == '0':
#         WriteFile.WriteLog('SendMessage','Info','UserName:'  + ' |1_SendMessage:' + title,'a')
#         #WriteFile.WriteLog('SendMessage','OKINFO_1',str(messageBody(title,description,ruleUrl,imageUrl)),'a')
#         #return 'OK'
#     elif code == '42001':
#         GetAccessToken.GetAccessTokenFromWechat()
#         accessToken =  GetAccessToken.GetAccessTokenFromLocal()
#         posturl =  'https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token='+ accessToken
#         time.sleep(1)
#         postMsg(posturl ,messageBody(title,description,ruleUrl,imageUrl))
#         WriteFile.WriteLog('SendMessage','Wran','UserName:'  + ' |SendMessage:' + title + ' |Errorcode:'+code,'a')
#     elif code == '40014':
#         GetAccessToken.GetAccessTokenFromWechat()
#         accessToken =  GetAccessToken.GetAccessTokenFromLocal()
#         posturl =  'https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token='+ accessToken
#         time.sleep(1)
#         postMsg(posturl ,messageBody(title,description,ruleUrl,imageUrl))
#         WriteFile.WriteLog('SendMessage','Wran','UserName:'  + ' |SendMessage:' + title + ' |Errorcode:'+code,'a')
#     else:
#         WriteFile.WriteLog('SendMessage','Error','UserName:'  + ' |SendMessage:' + title + ' |Errorcode:'+code,'a')
#


        #WriteFile.WriteLog('SendMessage','ErrorINFO1','a')


#sendMessageChat('[Alerting] Test notification','High value:100 Higher Value:200','http://grafana.prometheus.qiniu.io:80/','http://grafana.org/assets/img/blog/mixed_styles.png')