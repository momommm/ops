[TOC]
# Redis备份迁移

## 前言

刚好接手一个Redis数据迁移的任务，暂时把具体方法书写下来。


### 0x1 环境介绍

备份时需要用到的工具：**uredis-redis-port**


机房 | 版本 | 网络环境
---|---|---
Ucloud | Redis 3.2 | 内网
腾讯云 | Redis 2.8 | 内网

### 0x2 工具使用

##### 1.Redis同步导入导出(rsync)
```
./uredis-redis-port sync --psync -f source_ip:source_port -P PASSWORD -t dest_ip:dest_port -A PASSWORD
```

PS：由于使用的是云商提供的Redis数据库，并无外网权限，所以无法使用 rsync 进行同步。

##### 2.Redis导出RDB数据文件
```
./uredis-redis-port dump -f source_ip:source_port -P PASSWORD -o save.rdb
```
##### 3.Redis导入RDB数据文件
```
./uredis-redis-port restore -i save.rdb -t dest_ip:dest_port -A PASSWORD
```
**尴尬的事情来了，在实际操作中尝试使用上方命令导入2.8版本的时候，缺提示 ERR Bad data format，而在下线测试的时候，一切正常。**


### 0x3 另一款工具的使用
##### 1.下载工具
```
wget http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/attach/66006/cn_zh/1531121747155/redis-port%282%29?spm=a2c4e.11153940.blogcont394417.12.6e0e90c8Dbhgw3
```
文档中名字：**redis-port-aliyun**

注意此工具只适合导入Redis 3.0版本以下的数据
>官方地址:https://yq.aliyun.com/articles/394417

```
./redis-port  restore  
  --input=x/dump.rdb  --target=dst_host:dst_port   
  --auth=dst_password  [--filterkey="str1|str2|str3"]
  [--targetdb=DB] [--rewrite] [--bigkeysize=SIZE]
  [--logfile=REDISPORT.LOG]

  参数说明：

    x/dump.rdb : 云redis备份集的dump文件路径

    dst_host : 自建redis域名（或者ip）

    dst_port : 自建redis端口

    dst_password : 自建redis密码

    str1|str2|str3 : 过滤具有str1或str2或str3的key

    DB : 欲同步入自建redis的db

    rewrite : 覆盖已经写入的key

     bigkeysize=SIZE : 当写入的value大于SIZE时，走大key写入模式
```



### 0x4 总结

说一下这个软件使用过程中的坑吧！
- 经过测试，Redis-prot 在导入目标数据库版本高于4.0以上就会失败，原因是高版本RDB数据存储结构不一样
- 腾讯云和Uloud Redis版本全部都是4.0以下（不包含4.0）故可以成功导入数据。
