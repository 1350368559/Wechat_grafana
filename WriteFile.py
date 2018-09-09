#coding=utf-8
'''
Created on 2018-5-24
@author: daixuan
'''
import datetime,time


ISOTIMEFORMAT='%Y-%m-%d %X'
def WriteFile(filename,mess,writetype):
    #today = datetime.date.today()
    logfile = open('./' + filename  ,writetype)
    #wrtmsg = str( time.strftime( ISOTIMEFORMAT, time.localtime() )) + '\n' + mess+'\n  \n'
    logfile.write(mess)
    logfile.close()


ISOTIMEFORMAT='%Y-%m-%d %X'
def WriteLog(filename,logtype,mess,writetype):
    today = datetime.date.today()
    logfile = open('./logs/' + filename + str(today)  + '.log',writetype)
    wrtmsg = str( time.strftime( ISOTIMEFORMAT, time.localtime() )) + ' [' +  logtype + ']: ' + mess+   '\n'
    logfile.write(wrtmsg)
    logfile.close()
