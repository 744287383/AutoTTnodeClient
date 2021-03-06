#!/usr/bin/python3
#coding=utf-8
import urllib3
import json
import datetime as dt
import time
import sys
def getCode(phone):#获取验证码！
    url="http://tiantang.mogencloud.com/web/api/login/code"
    body_json="phone="+phone
    encoded_body=body_json.encode('utf-8')
    http = urllib3.PoolManager()
    header={"Content-Type":"application/x-www-form-urlencoded"}
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
       print("getCode方法请求失败，结束程序")

       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        print("请输入正确的手机号码！")
        exit()
    data=data['data']
    return

def getAuthorization(phone,authCode):#获取Authorization
    url="http://tiantang.mogencloud.com/web/api/login"
    body_json="phone="+phone+"&authCode="+authCode
    encoded_body=body_json.encode('utf-8')
    header={"Content-Type":"application/x-www-form-urlencoded"}
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
       print("getAuthorization方法请求失败，结束程序")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        print("验证码错误!等待1分钟后重新运行再次获取验证码！\n")
        exit()
    data=data['data']

    return data['token']

#********************************main******************************************
path=sys.path[0]
print("免责声明：\n本程序唯一下载地址：https://www.right.com.cn/forum/thread-4048219-1-1.html 如果你在别的地方下载的，出现问题与作者无关！\n本程序开源，开源自己查阅源码是否有后门。一切个人信息只用于甜糖程序api，请放心使用！，同时禁止转载本相关程序文件！\n禁止使用本程序用于一切商业活动，本程序只供个人学习研究使用。如有侵权请联系作者删除相关内容！\n")
stats=input("接受此免责声明：输入1为接受，输入任意字符为不接受,结束程序\n")
if stats!='1':
	exit()
    
authorization=""
week=0
plusplus_token=""
tg_bot_token=""
chat_id=""

phonenum=input("请输入手机号码回车键提交:\n")
phonenum=str(phonenum)
if len(phonenum)!=11:
    print("请输入正确的手机号码!!请重新运行")
    exit()
getCode(phonenum)
print("验证码发送成功请耐心等待！\n")
authCode=input("请确保你输入验证码短信是甜糖发的验证码短信，以免造成经济损失，概不负责。\n请输入验证码：\n")
authCode=str(authCode)
if len(authCode)!=6:
    print("请输入正确的验证码!!请重新运行")
    exit()
authorization=getAuthorization(phonenum,authCode)
print("你的authorization：\n\n"+authorization+"\n\n")



print("自动提现策略：如果已经实名签约的统一采用银行卡提现；未实名签约的同一采用支付宝提现，支付宝提现最大金额99￥，当账户金额大于等于100￥时默认提现99￥；一周只能提现一次！")
week=input("\n\n请输入以下编号开启自动提现功能(其它字符默认不提现):\n[0]不开启自动提现功能\n[1]星期一提现\n[2]星期二提现\n[3]星期三提现\n[4]星期四提现\n[5]星期五提现\n[6]星期六提现\n[7]星期日提现\n")
weeks=[0,1,2,3,4,5,6,7]
week=int(week)
if week not in weeks:
    week=0
if week!=0:
    print("\n你已选择在星期:"+str(week)+"提现\n")
else:
    print("\n你已选择不开启自动提现\n")



print("消息推送渠道：请输入下面编号")
print("[1]PLUS+推送：官网http://pushplus.hxtrip.com/（作者推荐）")
print("[2]Telegram机器人推送：Telegram APP-添加BotFather好友配置机器人")
num=input("")
if num=='1':
    plusplus_token=input("请进入http://pushplus.hxtrip.com微信扫码登录并绑定微信后获取Token!\n请输入你的Plus+的Token码：\n")
if num=='2':
    print("Telegram APP-添加BotFather好友配置机器人获取token和chat_id：\n")
    tg_bot_token=input("请输入机器人Token：\n")
    chat_id=input("请输入chat_id：\n")
else:
    print("输入错误程序结束请重新运行程序！")
    exit()
authorization=authorization.strip()
plusplus_token=plusplus_token.strip()
tg_bot_token=tg_bot_token.strip()
chat_id=chat_id.strip()
config={}
config["authorization"]=authorization
config["week"]=week
config["plusplus_token"]=plusplus_token
config["tg_bot_token"]=tg_bot_token
config["chat_id"]=chat_id
try:
    file=open(path+"/ttnodeConfig.config","w+",encoding="utf-8",errors="ignore")
    file.write(str(config))
    file.flush()
finally:
    if file:
        file.close()
print("已经配置成功了，请用python执行sendTTnodeMSG.py文件，以及配置定时程序。填写邀请码123463支持作者！")
exit()