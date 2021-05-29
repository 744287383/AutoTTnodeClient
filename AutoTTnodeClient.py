#!/usr/bin/python3
#coding=utf-8
import urllib3
import json
import datetime as dt
import time
import sys
import logging
import traceback
import random
import hmac
import hashlib
import base64
import urllib.parse
'''
特别声明:
本程序只有甜糖客户端和plus+ telegram的相关的api的访问，请仔细查阅程序安全性。
本程序仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断.
本脚本的唯一下载地址https://www.right.com.cn/forum/thread-4048219-1-1.html  其它地方下载的可能存在危险，概不负责。
对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.
请勿将本程序的任何内容用于商业或非法目的，否则后果自负.

如果任何单位或个人认为本程序可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关程序.
任何以任何方式查看此程序的人或直接或间接使用该程序的使用者都应仔细阅读此声明。作者保留随时更改或补充此免责声明的权利。
一旦使用并复制了任何相关程序，则视为您已接受此免责声明.
您使用或者复制了本程序且本人制作的任何脚本，则视为已接受此声明，请仔细阅读
您必须在下载后的24小时内从计算机或手机中完全删除以上内容.
'''
def HandleException( excType, excValue, tb):
	ErrorMessage = traceback.format_exception(excType, excValue, tb)  # 异常信息
	logging.exception('ErrorMessage: %s' % ErrorMessage)  # 将异常信息记录到日志中
	str=[]
	for item in ErrorMessage:
		str.append(item)
        
	msg_content=[]
	msg_content.append("程序运行错误，请暂停使用程序，手动领取星愿，截图错误消息推送，并联系程序开发者！-三只松鼠")
	msg_content.append("ErrorMessage:")
	msg_content.append(str)
	msg_content.append(end)
	sendMSG("[甜糖星愿]程序错误警报",msg_content)
	return

sys.excepthook = HandleException #全局错误异常处理！

path=sys.path[0] #脚本所在目录
logging.basicConfig(filename=path + '/AutoTTnodeClient.log',format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.DEBUG)
logging.debug("日志开始")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
####################以下内容请不要乱动，程序写得很菜，望大佬手下留情#########################################
devices=''
inactivedPromoteScore=0
msgTitle="[甜糖星愿]星愿日结详细"
msg="\n"

def sendPushPlus(text,desp):#发送PushPlus代码
    url="http://www.pushplus.plus/send"
    header={"Content-Type":"application/json"}
    body_json={"token":PushPlus_token,"title":text,"content":desp,"template":"html"}
    encoded_body=json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=200:
       print("sendPushPlus方法请求失败，结束程序")
       logging.debug("sendPushPlus方法请求失败，结束程序")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)
    print("消息已经推送至PushPlus，请注意查验！")
    return

def sendPlusPlus(text,desp):#发送PlusPlus代码(旧版)
    url="http://pushplus.hxtrip.com/send"
    header={"Content-Type":"application/json"}
    body_json={"token":plusplus_token,"title":text,"content":desp,"template":"html"}
    encoded_body=json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=200:
       print("sendPlusPlus方法请求失败，结束程序")
       logging.debug("sendPlusPlus方法请求失败，结束程序")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)
    print("消息已经推送至PlusPlus，请注意查验！")
    return    
def sendTelegram(desp):#发送Telegram代码
    url="https://api.telegram.org/bot"+tg_bot_token+"/sendMessage"
    header={"Content-Type":"application/json"}
    body_json={"chat_id":chat_id,"text":desp}
    encoded_body=json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=200:
       print("sendTelegram方法请求失败，结束程序，请确保连接了外国网络！")
       logging.debug("sendTelegram方法请求失败，结束程序，请确保连接了外国网络！")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)
    print("消息已经推送至TG机器人，请注意查验！")
    return

def sendDingDing(desp):#发送Telegram代码
    url="https://oapi.dingtalk.com/robot/send?access_token="+DingDing_access_token
    if len(DingDing_secret)>10:
        timestamp = str(round(time.time() * 1000))
        secret_enc = DingDing_secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, DingDing_secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        url=url+"&timestamp="+str(timestamp)+"&sign="+sign
    header={"Content-Type":"application/json"}
    body_json={"msgtype": "text", "text":{"content":desp}}
    encoded_body=json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=200:
       print("sendDingDing方法请求失败，结束程序")
       logging.debug("sendDingDing方法请求失败，结束程序，请确保连接了外国网络！")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)
    print("消息已经推送至钉钉群机器人，请注意查验！")
    return
def sendIYUU(text,desp):#发送PlusPlus代码
    url="http://iyuu.cn/"+iyuu_token+".send"
    header={"Content-Type":"application/x-www-form-urlencoded"}
    body_json="text="+text+"&desp="+desp
    encoded_body=body_json.encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=200:
       print("sendIYUU方法请求失败，结束程序")
       logging.debug("sendIYUU方法请求失败，结束程序")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)
    print("消息已经推送至爱语飞飞公众号，请注意查验！")
    return
    
def sendQMSG(desp):#发送Telegram代码
    url="https://qmsg.zendee.cn/send/"+QMSG_key
    header={"Content-Type":"application/x-www-form-urlencoded"}
    body_json="msg="+desp
    encoded_body=body_json.encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=200:
       print("sendQMSG方法请求失败，结束程序，请确保连接了外国网络！")
       logging.debug("sendQMSG方法请求失败，结束程序，请确保连接了外国网络！")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)
    print("消息已经推送至QQ，请注意查验！")
    return

def sendBark(text,desp):#发送PlusPlus代码
    url="http://api.day.app/"+Bark_key+"/"
    header={"Content-Type":"application/x-www-form-urlencoded"}
    body_json="title="+text+"&body="+desp
    encoded_body=body_json.encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=200:
       print("sendBark方法请求失败，结束程序")
       logging.debug("sendBark方法请求失败，结束程序")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)
    print("消息已经推送至Bark，请注意查验！")
    return
def getInitInfo():#甜糖用户初始化信息，可以获取待收取的推广信息数，可以获取账户星星数
    url="http://tiantang.mogencloud.com/web/api/account/message/loading"
    header={"Content-Type":"application/json","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('POST', url,headers=header)
    if response.status!=200:
       print("getInitInfo方法请求失败，结束程序")
       logging.debug("getInitInfo方法请求失败，结束程序")
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)
    if data['errCode']!=0:
        print("发送推送微信，authorization已经失效")
        msg_content=[]
        msg_content.append("甜糖登录状态已经失效，请通过手机号码和验证码进行重新生成配置")
        msg_content.append("docker版运行下面命令：")
        item=[]
        item.append("docker exec  autottnode python3 /root/ttnode/TTnodeLogin.py")
        msg_content.append(item)
        msg_content.append("源码版运行下面命令：")
        item=[]
        item.append("python3 /你文件的路径/TTnodeLogin.py")
        msg_content.append(item)
        msg_content.append(end)
        sendMSG("[甜糖星愿]-Auth失效通知",msg_content)
        exit()
    data=data['data']

    return data

def getDevices():#获取当前设备列表，可以获取待收的星星数
    url="http://tiantang.mogencloud.com/api/v1/devices?page=1&type=2&per_page=200"
    header={"Content-Type":"application/json","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('GET', url,headers=header)
    if response.status!=200:
        print("getDevices方法请求失败，结束程序")
        logging.debug("getDevices方法请求失败，结束程序")
        raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)
    if data['errCode']!=0:
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API可能已经变更，请暂停使用程序！")


    data=data['data']['data']
    if len(data)==0:
        msg_content=[]
        msg_content.append("该账号尚未绑定设备，请绑定设备后再运行！")
        msg_content.append(end)
        sendMSG("[甜糖星愿]获取设备失败通知",msg_content)
        exit()
    return data
    
def getDevice_logs():#获取设备日志
    url="http://tiantang.mogencloud.com/api/v1/device_logs?page=1&per_page=200"
    header={"Content-Type":"application/json","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('GET', url,headers=header)
    if response.status!=200:
        print("getDevice_logs方法请求失败，结束程序")
        logging.debug("getDevice_logs方法请求失败，结束程序")
        raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)
    if data['errCode']!=0:
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API可能已经变更，请暂停使用程序！")


    data=data['data']['data']
    return data


def promote_score_logs(score):#收取推广奖励星星
    global msg
    if score==0:
        
        return "[推广奖励]0-🌟",0
    url="http://tiantang.mogencloud.com/api/v1/promote/score_logs"
    header={"Content-Type":"application/json","authorization":authorization}
    body_json={'score':score}
    encoded_body=json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
       print("promote_score_logs方法请求失败，结束程序")
       logging.debug("promote_score_logs方法请求失败，结束程序")
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        
        return "[推广奖励]0-🌟(收取异常)",0
    data=data['data']
    #发送微信推送，啥设备，获取了啥星星数
    return "[推广奖励]"+str(score)+"-🌟",score

def score_logs(device_id,score,name):#收取设备奖励
    global msg
    if score==0:
        return "["+name+"]0-🌟",0
    url="http://tiantang.mogencloud.com/api/v1/score_logs"
    header={"Content-Type":"application/json","authorization":authorization}
    body_json={'device_id':device_id,'score':score}
    encoded_body=json.dumps(body_json).encode('utf-8')
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
       print("score_logs方法请求失败，结束程序")
       logging.debug("score_logs方法请求失败，结束程序")
       raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        return "["+name+"]0-🌟(收取异常)",0
    data=data['data']
    return "["+name+"]"+str(score)+"-🌟",score

def sign_in():#签到功能
	url="http://tiantang.mogencloud.com/web/api/account/sign_in"
	header={"Content-Type":"application/json","authorization":authorization}
	http = urllib3.PoolManager()
	response= http.request('POST', url,headers=header)
	if response.status!=201 and response.status!=200:
		print("sign_in方法请求失败，结束程序")
		logging.debug("sign_in方法请求失败，结束程序")
		raise Exception("响应状态码:"+str(response.status)+"\n请求url:"+url+"\n消息:API出现异常，请暂停使用程序！")
	data=response.data.decode('utf-8')
	data=json.loads(data)
	global msg

	if data['errCode']!=0:
		
		return "[签到奖励]0-🌟(失败:"+data['msg']+")",0

	

	return "[签到奖励]"+str(data['data'])+"-🌟",data['data']

    
def readConfig(filePath):#读取配置文件
	try:
		file=open(filePath,"a+",encoding="utf-8",errors="ignore")
		file.seek(0)
		result=file.read()
	finally:
		if file:
			file.close()
			print("文件流已经关闭")

	return result
def zfb_withdraw(bean):#支付宝提现
    url="http://tiantang.mogencloud.com/api/v1/withdraw_logs"
    score=bean["score"]
    score=score-score%100
    real_name=bean["real_name"]
    card_id=bean["card_id"]
    bank_name="支付宝"
    sub_bank_name=""
    type="zfb"
    
    if score<1000:
        return "[自动提现]支付宝提现失败，星愿数不足1000",""
    if score>=10000:
        score=9900
    body_json="score="+str(score)+"&real_name="+real_name+"&card_id="+card_id+"&bank_name="+bank_name+"&sub_bank_name="+sub_bank_name+"&type="+type
    encoded_body=body_json.encode('utf-8')
    header={"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
        logging.debug("withdraw_logs方法请求失败")
        return "[自动提现]支付宝提现失败，请关闭自动提现等待更新并及时查看甜糖客户端app的账目",""
       
    data=response.data.decode('utf-8')
    data=json.loads(data)
    if data['errCode']==403002:
        logging.debug("[自动提现]支付宝提现失败，"+data['msg'])
        return "[自动提现]支付宝提现失败，"+data['msg'],""
    if data['errCode']!=0:
        print(""+data['msg']+str(score))
        logging.debug(""+data['msg']+str(score))
        return "[自动提现]支付宝提现失败，请关闭自动提现等待更新并及时查看甜糖客户端app的账目",""

    data=data['data']
    zfbID=data['card_id']
    pre=zfbID[0:4]
    end=zfbID[len(zfbID)-4:len(zfbID)]
    zfbID=pre+"***"+end
    item=[]
    item.append("提现方式：支付宝")
    item.append("支付宝号："+zfbID)
    return "[自动提现]扣除"+str(score)+"-🌟",item
    
def yhk_withdraw(bean):#银行卡提现
    url="http://tiantang.mogencloud.com/api/v2/withdraw_logs"
    score=bean["score"]
    score=score-score%100
    real_name=bean["real_name"]
    card_id=bean["card_id"]
    bank_name=bean["bank_name"]
    sub_bank_name=bean["sub_bank_name"]
    type="bank_card"
    
    if score<1000:
        return "[自动提现]银行卡提现失败，星愿数不足1000",""
    body_json="score="+str(score)+"&real_name="+real_name+"&card_id="+card_id+"&bank_name="+bank_name+"&sub_bank_name="+sub_bank_name+"&type="+type
    encoded_body=body_json.encode('utf-8')
    header={"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
        logging.debug("withdraw_logs方法请求失败")
        return "[自动提现]银行卡提现失败，请关闭自动提现等待更新并及时查看甜糖客户端app的账目",""
       
    data=response.data.decode('utf-8')
    data=json.loads(data)
    if data['errCode']==403002:
        logging.debug("[自动提现]银行卡提现失败，"+data['msg'])
        return "[自动提现]银行卡提现失败，"+data['msg'],""
    if data['errCode']!=0:
        print(""+data['msg']+str(score))
        logging.debug(""+data['msg']+str(score))
        return "[自动提现]银行卡提现失败，请关闭自动提现等待更新并及时查看甜糖客户端app的账目",""

    data=data['data']
    yhkID=data['card_id']
    pre=yhkID[0:4]
    end=yhkID[len(yhkID)-4:len(yhkID)]
    yhkID=pre+"****"+end
    item=[]
    item.append("提现方式：银行卡")
    item.append("银行卡号："+yhkID)
    return "[自动提现]扣除"+str(score)+"-🌟",item
    
def withdraw_type(userInfo):#根据用户是否签约来决定提现方式
	isEContract=userInfo['isEContract']
	bean={}
	if isEContract:
		#已经实名签约的采用银行卡提现
		bankCardList=userInfo['bankCardList']#获取支付宝列表
		if len(bankCardList)==0:
			withdraw_str="[自动提现]银行卡提现失败，原因是未绑定银行卡，请绑定一张银行卡"
			return withdraw_str,""
		else:
			bean["score"]=userInfo['score']
			bean["real_name"]=bankCardList[0]['name']
			bean["card_id"]=bankCardList[0]['bankCardNum']
			bean["bank_name"]=bankCardList[0]['bankName']
			bean["sub_bank_name"]=bankCardList[0]['subBankName']
			withdraw_str,item=yhk_withdraw(bean)
			return withdraw_str,item
	else:
		#未实名签约采用支付宝提现
		zfbList=userInfo['zfbList']#获取支付宝列表
		if len(zfbList)==0:
			withdraw_str="[自动提现]支付提现失败，原因是未绑定支付宝号，请绑定支付宝账户"
			return withdraw_str,""
		else:
			bean["score"]=userInfo['score']
			bean["real_name"]=zfbList[0]['name']
			bean["card_id"]=zfbList[0]['account']
			withdraw_str,item=zfb_withdraw(bean)
			return withdraw_str,item

def sendMSG(title,content):

    if len(plusplus_token)>10:    #(旧版pushplus)
        msgContent=""
        num=0
        for item in content:
            num=num+1
            if len(content)==num:
                msgContent=msgContent+"<hr style='border: 2px dashed #ccc'>"
            if isinstance(item,list):
                for i in item:
                    msgContent=msgContent+"|------"+i+"<br>"
            else:
                msgContent=msgContent+""+item+"<br>"
        sendPlusPlus(title,msgContent)
        
    if len(PushPlus_token)>10:    #(新版pushplus)
        msgContent=""
        num=0
        for item in content:
            num=num+1
            if len(content)==num:
                msgContent=msgContent+"<hr style='border: 2px dashed #ccc'>"
            if isinstance(item,list):
                for i in item:
                    msgContent=msgContent+"|------"+i+"<br>"
            else:
                msgContent=msgContent+""+item+"<br>"
        sendPushPlus(title,msgContent)
        
    if len(tg_bot_token)>10 and len(chat_id)!=0:#(tg推送)
        msgContent=title+"\n\n"
        num=0
        for item in content:
            num=num+1
            if len(content)==num:
                msgContent=msgContent+"\n"
            if isinstance(item,list):
                for i in item:
                    msgContent=msgContent+"|----"+i+"\n"
            else:
                msgContent=msgContent+""+item+"\n"
        sendTelegram(msgContent)
    if len(DingDing_access_token)>10:#(钉钉推送)
        msgContent=title+"\n\n"
        num=0
        for item in content:
            num=num+1
            if len(content)==num:
                msgContent=msgContent+"\n"
            if isinstance(item,list):
                for i in item:
                    msgContent=msgContent+"|----"+i+"\n"
            else:
                msgContent=msgContent+""+item+"\n"
        sendDingDing(msgContent)
        
    if len(iyuu_token)>10:#(爱语飞飞推送)
        msgContent=""
        num=0
        for item in content:
            num=num+1
            if len(content)==num:
                msgContent=msgContent+"***\n"
            if isinstance(item,list):
                for i in item:
                    msgContent=msgContent+">"+i+"\n"
            else:
                msgContent=msgContent+item+"\n"
        sendIYUU(title,msgContent)
        
    if len(QMSG_key)>10:#(QMSG酱推送)
        msgContent=title+"\n\n"
        num=0
        for item in content:
            num=num+1
            if len(content)==num:
                msgContent=msgContent+"\n"
            if isinstance(item,list):
                for i in item:
                    msgContent=msgContent+"|----"+i+"\n"
            else:
                msgContent=msgContent+""+item+"\n"
        sendQMSG(msgContent)

    if len(Bark_key)>10:#(Bark推送)
        msgContent=""
        num=0
        for item in content:
            num=num+1
            if len(content)==num:
                msgContent=msgContent+"\n"
            if isinstance(item,list):
                for i in item:
                    msgContent=msgContent+"|----"+i+"\n"
            else:
                msgContent=msgContent+""+item+"\n"
        sendBark(title,msgContent)
	
#*********************************main***********************************************************************************
#*********************************读取配置*************************************
end="注意:以上统计仅供参考，一切请以甜糖客户端APP为准。填写邀请码123463支持作者！"
config=readConfig(path+"/ttnodeConfig.config")
print("config:"+config)

if len(config)==0:
	print("错误提示ttnodeConfig.config为空，请重新运行ttnodeconfig.py")
	logging.debug("错误提示ttnodeConfig.config为空，请重新运行ttnodeconfig.py")
	exit()

config=eval(config)#转成字典
#获取甜糖授权码
authorization=config.get("authorization","")
#获取Push+(新版)推送授权码
PushPlus_token=config.get("PushPlus_token","")
#获取Push+(旧版)推送授权码
plusplus_token=config.get("plusplus_token","")
#获取Telegram机器人推送授权码
tg_bot_token=config.get("tg_bot_token","")
chat_id=config.get("chat_id","")
#获取钉钉群机器人access_token和secret推送授权码
DingDing_access_token=config.get("DingDing_access_token","")
DingDing_secret=config.get("DingDing_secret","")
#获取爱语飞飞推送渠道iyuu_token授权码
iyuu_token=config.get("iyuu_token","")
#获取QMSG酱推送渠道QMSG_key授权码
QMSG_key=config.get("QMSG_key","")
#获取Bark推送渠道Bark_key授权码
Bark_key=config.get("Bark_key","")
#提现配置参数
week=config.get("week",0)
if len(authorization)==0:
	print("错误提示authorization为空，请重新运行ttnodeconfig.py")
	exit()

week=int(week)

#*********************************错峰延时执行*************************************
sleep_time=random.randint(1,200)
print("错峰延时执行"+str(sleep_time)+"秒，请耐心等待")
logging.debug("错峰延时执行"+str(sleep_time)+"秒，请耐心等待")
time.sleep(sleep_time)
#*********************************获取用户信息*************************************
content=[]
data=getInitInfo()
inactivedPromoteScore=data['inactivedPromoteScore']
time.sleep(1)
devices=getDevices()#获取设备列表信息
#*********************************收取星星*************************************

sign_in_msg,sign_in_score=sign_in()#收取签到收益
promote_score_msg,promote_score=promote_score_logs(inactivedPromoteScore)#收取推广收益
time.sleep(1)
score_info=[]
devices_score=0
for device in devices:
    string,device_score=score_logs(device['hardware_id'],device['inactived_score'],device['alias'])#收取设备收益
    devices_score=devices_score+device_score
    score_info.append(string)
    sleep_time=random.randint(1,4)
    time.sleep(sleep_time)
#*********************************获取时间戳*************************************
day_time=int(time.mktime(dt.date.today().timetuple()))
device_infos=getDevice_logs()
billing_bandwidth=0
for device_info in device_infos:
    if day_time>=device_info['completed_at']:
        break
    billing_bandwidth=billing_bandwidth+device_info['billing_bandwidth']
billing_bandwidth=billing_bandwidth/1024
billing_bandwidth=round(billing_bandwidth,2)
billing_bandwidth="[结算带宽]"+str(billing_bandwidth)+"Mbps"
#*********************************自动提现*************************************
withdraw=""
now_week=dt.datetime.now().isoweekday()#获取今天是星期几返回1-7
now_week=int(now_week)
items=[]
if week==now_week:
    userInfo=getInitInfo()
    withdraw,items=withdraw_type(userInfo)
      
#*********************************收益统计并发送微信消息*************************************
total=0
accountScore=0
total=sign_in_score+promote_score+devices_score
total_str="[日总收益]"+str(total)+"-🌟"
nowdata=getInitInfo()
accountScore=nowdata['score']
nickName="[账户昵称]"+nowdata['nickName']
accountScore_str="[账户星愿]"+str(accountScore)+"-🌟"
now_time = dt.datetime.now().strftime('%F %T')
now_time_str="[当前时间]"+now_time

content.append(now_time_str)
content.append(nickName)
content.append(billing_bandwidth)
content.append(accountScore_str)
content.append(total_str)
total_info_str=[]
total_info_str.append(sign_in_msg)
total_info_str.append(promote_score_msg)
total_info_str.append("[设备收益]"+str(devices_score)+"-🌟")
content.append(total_info_str)


if week==now_week:
    content.append(withdraw)
    if len(items)!=0:
        content.append(items)
content.append("[设备详细]：")
content.append(score_info)
content.append(end)
sendMSG(msgTitle,content)




'''
time.sleep(2)

title="[甜糖星愿]Push+推送渠道失效通知"
content=[]
content.append("旧版pushplus即将失效。")
content.append("pushplus推送通知已更换成最新。请在 http://www.pushplus.plus/ 获取新的token 。")
content.append("请进入下方链接教程，运行第二句命令重新登录甜糖并配置推送新版推送渠道。")
content.append(["https://www.right.com.cn/forum/thread-4087719-1-1.html"])
content.append("如没使用该推送渠道或已经更新过新版Push+的token的请忽略本通知，本消息提醒3天！")
sendMSG(title,content)
'''
exit()
