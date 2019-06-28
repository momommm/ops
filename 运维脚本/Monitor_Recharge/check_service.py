# -*- coding:utf-8 -*-
import re
import commands
import configparser
import logging 
import json
import requests



logging.basicConfig(level=logging.INFO,  
                    filename='./send_log.txt',  
                    filemode='a',  
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 


cf = configparser.ConfigParser()
cf.read("./send_mess.ini")
num = cf.get("Globle", "num")
mess = cf.get("Globle", "mess")
sendServer = cf.get("Globle", "sendServer")
i=0
while True:
	retcode, ret = commands.getstatusoutput('# 这里写sql')
	if retcode != 0:
     logging.warning("数据库链接失败")
	   i+=1
     if i >=3:
        content = "海外充值收入的监控告警发生错误，请联系运维查看"
        r = requests.post(sendServer,  data={'number': num, 'content': content})
        exit()
        continue
  break
try:
    result = re.search(r'\d+', ret).group()
    if int(result) != 0:
       logging.info("6小时内充值人数为 %d" % int(result))
    else:
       r = requests.post(sendServer,  data={'number': num, 'content': mess})
       rej = r.json()
       if rej['RetCode'] == 0:
           logging.warning("已发送错误信息")
except Exception as e:
     logging.error("错误： %s" % e)
     content = "海外充值收入的监控告警发生错误，请联系运维查看"
     r = requests.post(sendServer,  data={'number': num, 'content': content})
