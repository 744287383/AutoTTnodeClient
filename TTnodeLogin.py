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
def promotes():
    url="http://tiantang.mogencloud.com/api/v1/promotes?promote_code=123463"
    header={"Content-Type":"application/json","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('POST', url,headers=header)
    data=response.data.decode('utf-8')
#********************************main******************************************
path=sys.path[0]
print("免责声明：\n本程序唯一下载地址：https://www.right.com.cn/forum/thread-4048219-1-1.html 如果你在别的地方下载的，出现问题与作者无关！\n本程序开源，开源自己查阅源码是否有后门。一切个人信息只用于甜糖程序api，请放心使用！，同时禁止转载本相关程序文件！\n禁止使用本程序用于一切商业活动，本程序只供个人学习研究使用。如有侵权请联系作者删除相关内容！\n")
stats=input("接受此免责声明：输入1为接受，输入任意字符为不接受,结束程序\n")
stats=int(stats)
if stats!=1:
    print("谢谢，请24小时删除本程序，程序已结束")
    exit()
    
authorization=""
week=0
PushPlus_token=""
tg_bot_token=""
chat_id=""
DingDing_access_token=""
DingDing_secret=""
iyuu_token=""
QMSG_key=""
Bark_key=""
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
print("\n你的authorization：\n"+authorization+"\n\n")




print("自动提现策略：如果已经实名签约的统一采用银行卡提现；未实名签约的同一采用支付宝提现，支付宝提现最大金额99￥，当账户金额大于等于100￥时默认提现99￥；一周只能提现一次！")
week=input("请输入以下编号开启自动提现功能(其它字符默认不提现,推荐星期三):\n[0]不开启自动提现功能\n[1]星期一提现\n[2]星期二提现\n[3]星期三提现\n[4]星期四提现\n[5]星期五提现\n[6]星期六提现\n[7]星期日提现\n")
weeks=[0,1,2,3,4,5,6,7]
week=int(week)
if week not in weeks:
    week=0
if week!=0:
    print("\n你已选择在星期:"+str(week)+"提现\n")
else:
    print("\n你已选择不开启自动提现\n")



print("\n消息推送渠道(采集成功后发送消息)：请输入下面编号")
print("[1]微信-PUSH+消息推送：官网http://www.pushplus.plus/（作者目前推荐）")
print("[2]Telegram-TG机器人推送：Telegram APP-添加BotFather好友配置机器人（需要国外网络）")
print("[3]钉钉-钉钉群机器人推送：PC端钉钉创建群-群设置-智能群助手-添加机器人")
print("[4]微信-爱语飞飞消息推送：官网https://iyuu.cn/（作者目前推荐）")
print("[5]QQ-QMSG酱消息推送：官网https://qmsg.zendee.cn/")
print("[6]IOS-Bark消息推送：IOS应用商店下载Bark")
num=input("")
num=int(num)
print()
if num==1:
    PushPlus_token=input("请进入http://www.pushplus.plus/微信扫码登录并绑定微信后获取Token!\n请输入你的Push+的Token码：\n")
elif num==2:
    print("Telegram APP-添加BotFather好友配置机器人获取token和chat_id：")
    tg_bot_token=input("请输入机器人Token：\n")
    chat_id=input("请输入chat_id：\n")
elif num==3:
    print("PC端钉钉创建群-群设置-智能群助手-你创建的机器人-获取Webhook：access_token")
    DingDing_access_token=input("请输入钉钉机器人access_token(不是http链接)：\n")
    print("PC端钉钉创建群-群设置-智能群助手-你创建的机器-安全设置-加签(加签码格式：SEC**********)")
    DingDing_secret=input("请输入钉钉机器人加签码secret(加签码的格式是：SEC**********)：\n")
elif num==4:
    print("请进入https://iyuu.cn/微信扫码并绑定微信后获取iyuu_token!\n")
    iyuu_token=input("请输入你的爱语飞飞的iyuu_token码：\n")
elif num==5:
    print("请进入https://qmsg.zendee.cn/QQ登录-扫码添加机器人-管理台-挑选机器人-添加自己的QQ-获取key\n")
    QMSG_key=input("请输入你的QMSG酱的QMSG_key码：\n")
elif num==6:
    print("IOS应用商店下载Bark,打开app获取链接中key\n")
    Bark_key=input("请输入你的Bark的key码：\n")
else:
    print("输入错误程序结束请重新运行程序！")
    exit()
    
    
authorization=authorization.strip()
PushPlus_token=PushPlus_token.strip()
tg_bot_token=tg_bot_token.strip()
chat_id=chat_id.strip()
DingDing_access_token=DingDing_access_token.strip()
DingDing_secret=DingDing_secret.strip()
iyuu_token=iyuu_token.strip()
QMSG_key=QMSG_key.strip()
Bark_key=Bark_key.strip()
config={}
config["authorization"]=authorization
config["week"]=week
config["PushPlus_token"]=PushPlus_token
config["tg_bot_token"]=tg_bot_token
config["chat_id"]=chat_id
config["DingDing_access_token"]=DingDing_access_token
config["DingDing_secret"]=DingDing_secret
config["iyuu_token"]=iyuu_token
config["QMSG_key"]=QMSG_key
config["Bark_key"]=Bark_key
try:
    file=open(path+"/ttnodeConfig.config","w+",encoding="utf-8",errors="ignore")
    file.write(str(config))
    file.flush()
finally:
    if file:
        file.close()
print("已成功写入配置。")
stats=1
stats=input("\n\n是否愿意填写作者的邀请码123463以支持作者？\n[1]支持作者\n[0]不支持作者\n[任意字符]支持作者\n")
stats=str(stats)
if stats=='0':
    print("作者：发际线都高了2cm，你居然不支持我，讨厌你！哼！")
    exit()


promotes()
print("作者：谢谢大老板，祝大老板天天跑满上传，日进斗金，迎娶白富美。")
exit()