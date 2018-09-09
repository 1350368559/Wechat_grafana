import urllib2
import json
import ConfigParser
import WriteFile

#class getAccessTokenFromWechat():
def GetAccessTokenFromWechat():
    CorpID="ww02946fb9034b5649"
    CorpSecret="jqwFdaSPLJrpoi_YK4M2-XvJp4BXNUGtB0ztEYUEUXo"
    AgentId=1000002
    conn = urllib2.urlopen("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + CorpID + "&corpsecret=" + CorpSecret )
    getToken = conn.read()
    print getToken
    conn.close()
    result = json.loads(getToken)
    try:
        Accesstoken = result['access_token']
        message = '[token]\nAccessToken=' + Accesstoken + '\n'
        WriteFile.WriteFile('AccessToken.ini', message, 'w')
            
    except:
        Accesstoken = False
        message = 'getAccessTokenFromWechat Error'
        WriteFile.WriteLog('WeChatServer','Error',message,'w')


def GetAccessTokenFromLocal():
    cf = ConfigParser.ConfigParser()
    cf.read('./AccessToken.ini')
    LocalAccessToken = cf.get("token", "AccessToken")
    #cf.close
    return LocalAccessToken

GetAccessTokenFromWechat()
#print GetAccessTokenFromLocal()   
