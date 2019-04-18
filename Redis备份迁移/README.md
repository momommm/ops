[TOC]
# Redis备份迁移

## 前言

刚好接手一个Redis数据迁移的任务，暂时把具体方法书写下来。


### 0x1 环境介绍

备份时需要用到的工具：uredis-redis-port


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
尴尬的事情来了，在实际操作中尝试使用上方命令导入2.8版本的时候，缺提示 ERR Bad data format，而在下线测试的时候，一切正常。
### 0x3 另一款工具的使用
##### 1.下载工具
```
wget https://main.qcloudimg.com/raw/47154504189a8941250f57b60f1e2fcb/redis-port.tgz
```
##### 2.工具介绍
redis-port 是一组开源工具集合，主要用于 Redis 节点间的数据库同步、数据导入、数据导出，支持 Redis 的跨版本数据迁移，工具集中包括以下工具：

- redis-sync：支持在 Redis 实例之间进行数据迁移。
- redis-resotre：支持将 Redis 的备份文件（RDB）导入到指定 Redis 实例。
- redis-dump：支持将 Redis 的数据备份为 RDB 格式文件。
- redis-decode：支持将 Redis 备份文件（RDB）解析为可读的文件。

##### 兼容版本
- 支持源 Redis 2.8，3.0，3.2，4.0 版本。
- 支持目标实例为 Redis 2.8，3.0，3.2，4.0 版本，以及云数据库的所有版本，包括 Redis
单机版（社区）、主从版（社区）、集群版（社区）、主从版（CKV）、集群版（CKV）。

##### 3.导入数据
redis-restore 工具支持将 Redis 的备份文件（RDB）导入到指定 Redis 实例，同时也支持导入 AOF 文件，支持 Redis 2.8、3.0、3.2、4.0 版本的 RDB 文件格式。

参数说明：

-n：并发写入的任务数量，建议不设置或者设置为 CPU 核心数量 * 2。
-i：RDB 文件路径。
-t：目标实例地址，格式为 "password@ip:port"。
-a：AOF 文件路径。
--db=DB：导入的 DB ID，默认为和源实例保持一致。
--unixtime-in-milliseconds=EXPR：导入数据的同时更新 Key 过期时间值。
--help：查看帮助命令。
```
./redis-restore dump.rdb -t 127.0.0.1:6379
```

### 0x4 总结

说一下这个软件使用过程中的坑吧！
- 经过测试，Redis-prot 在导入目标数据库版本高于4.0以上就会失败，原因是高版本RDB数据存储结构不一样
- 腾讯云和Uloud Redis版本全部都是4.0以下（不包含4.0）故可以成功导入数据。