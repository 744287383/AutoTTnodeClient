#!/bin/sh
crond -l 9
wget -O /root/ttnode/updateFile.sh https://gitee.com/watermelon_peel/auto-ttnode-client/raw/master/updateFile.sh
chmod 0777 /root/ttnode/updateFile.sh
/root/ttnode/updateFile.sh &
/bin/sh