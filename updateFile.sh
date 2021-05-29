#!/bin/sh
sleep $(($RANDOM%60))
curl -L https://gitee.com/watermelon_peel/auto-ttnode-client/raw/master/AutoTTnodeClient.py -o /root/ttnode/AutoTTnodeClient.py 
sleep $(($RANDOM%60))
curl -L https://gitee.com/watermelon_peel/auto-ttnode-client/raw/master/TTnodeLogin.py -o /root/ttnode/TTnodeLogin.py  
sleep $(($RANDOM%60))
curl -L https://gitee.com/watermelon_peel/auto-ttnode-client/raw/master/crontab.list   -o /root/ttnode/crontab.list
sleep $(($RANDOM%60))
curl -L https://gitee.com/watermelon_peel/auto-ttnode-client/raw/master/updateFile.sh   -o /root/ttnode/updateFile.sh
sleep $(($RANDOM%60))
chmod 0777 /root/ttnode/updateFile.sh
str=$(sed -n '/\/root\/ttnode\/AutoTTnodeClient\.py/p'  /var/spool/cron/crontabs/root)
num=${#str}
if [ $num -gt 10 ];then
sed -i '/\/root\/ttnode\/AutoTTnodeClient\.py/d' /root/ttnode/crontab.list
echo -e "\n$str" >> /root/ttnode/crontab.list
fi

crontab /root/ttnode/crontab.list
echo "更新定时任务文件"
