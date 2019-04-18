# Prometheus exproter 使用

- mysqld_exporter

### Mysql 监控 

官方文档：https://github.com/prometheus/mysqld_exporter

#### 使用教程
- 创建用户
```
# 创建用户
CREATE USER 'exporter'@'%' IDENTIFIED BY '你的密码' WITH MAX_USER_CONNECTIONS 3;
# 赋予权限
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'%';
```
- 使用Docker启动
```
# 获取镜像
docker pull prom/mysqld-exporter
# 创建容器网络
docker network create my-mysql-network
# 运行容器
docker run -d \
  -p 9104:9104 \
  --network my-mysql-network  \
  -e DATA_SOURCE_NAME="user:password@(地址:3306)/" \
  prom/mysqld-exporter
  
 例子：
 docker run -d \
 -p 9104:9104   \
 --network my-mysql-network  \
 -e DATA_SOURCE_NAME="exporter:3.1415926@(192.168.198.139:3306)/"   \
 prom/mysqld-exporter
 
```
- 验证
```
http://192.168.198.139:9104/metrics
查找：mysql_up 是否等于 1 
1 为正常 0 为异常
```

### Redis 监控
- redis_exporter

#### 使用教程
- 使用Docker启动
```
docker run -d \
--name redis_exporter \
--net host \
-e REDIS_ADDR=IP地址:端口  \
oliver006/redis_exporter
```

### Linux 系统监控
- node-exporter

#### 使用教程
- 使用Docker启动
```
docker run -d \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  quay.io/prometheus/node-exporter \
  --path.rootfs /host
```

### Docker监控

- cadvisor

#### 使用教程

- Dcoker centos 启动
```
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --volume=/cgroup:/cgroup:ro \
  --detach=true \
  --name=cadvisor \
  --privileged=true \
  google/cadvisor:latest
```

- Docker 启动
```
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  google/cadvisor:latest
```