甜糖自动采集心愿客户端
```
docker run  -itd --net=host  --name ttnodeclient  --privileged=true --restart=always registry.cn-hangzhou.aliyuncs.com/744287383/autottnodeclient
#创建容器
```
```
docker exec -it ttnodeclient  python3 /root/ttnode/TTnodeLogin.py
#登录甜糖客户端并配置推送消息渠道
```
```
docker exec -it ttnodeclient python3 /root/ttnode/AutoTTnodeClient.py
#手动执行采集心愿,看看有没有消息推送。
```
```
docker exec -it ttnodeclient crontab -e
#自定义执行采集心愿程序的时间，需要懂cron规则（非必须步骤，可以不执行这一步，默认6点30会自动执行采集心愿）
```