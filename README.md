# SB-Actuator
Spring Boot Actuator未授权访问【XXE、RCE】单/多目标检测

```
V 1.1更新日志
增加针对env端点的深度检测：
    Spring Boot 1.x版本环境属性覆盖和XStream反序列化导致的RCE
    Spring Boot 2.x版本H2配置不当导致的RCE
C段查询修改为基于CIDR查询：
    提供了格式判定检测，您需要正确输入CIDR格式
    如：192.168.1.0/24  默认探测开启80/443端口

V 1.2更新日志
增加针对jolokia端点的JNDI注入检测：
    通过正则createJNDIRealm方法实现
调整针对env端点的深度检测：
    环境属性覆盖和XStream反序列化导致的RCE检测加入2.*版本支持
    实践表明，此两种RCE利用方式同样适用于2.*版本，data需以json形式发送
```
```
python SB-Actuator.py -h
```
```
  ___________________             _____          __                __
 /   _____/\______   \           /  _  \   _____/  |_ __ _______ _/  |_  ___________
 \_____  \  |    |  _/  ______  /  /_\  \_/ ___\   __\  |  \__  \\   __\/  _ \_  __ \
 /        \ |    |   \ /_____/ /    |    \  \___|  | |  |  // __ \|  | (  <_> )  | \/
/_______  / |______  /         \____|__  /\___  >__| |____/(____  /__|  \____/|__|
        \/         \/                  \/     \/                \/
                                                                      By RabbitMask | V 1.2

usage: sb.py [-h] [-u URL] [-s SURL] [-c CIDR] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     单目标扫描
  -s SURL, --surl SURL  单目标扫描(跳过指纹)
  -c CIDR, --cidr CIDR  CIDR扫描(80/443)
  -f FILE, --file FILE  从文件加载目标
```
```
python SB-Actuator.py -u http://172.19.69.118:9988
```
```

  ___________________             _____          __                __
 /   _____/\______   \           /  _  \   _____/  |_ __ _______ _/  |_  ___________
 \_____  \  |    |  _/  ______  /  /_\  \_/ ___\   __\  |  \__  \\   __\/  _ \_  __ \
 /        \ |    |   \ /_____/ /    |    \  \___|  | |  |  // __ \|  | (  <_> )  | \/
/_______  / |______  /         \____|__  /\___  >__| |____/(____  /__|  \____/|__|
        \/         \/                  \/     \/                \/
                                                                      By RabbitMask | V 1.2

It's A Spring Boot Web APP: http://172.19.69.118:9988
目标站点开启了 env 端点且eureka.client.serviceUrl.defaultZone属性开启,可进行XStream反序列化RCE测试,路径为：http://172.19.69.118:9988/actuator/env
目标站点开启了 jolokia 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/jolokia/list
目标站点开启了 jolokia 端点且存在reloadByURL方法,可进行XXE/RCE测试,路径为：http://172.19.69.118:9988/actuator/jolokia/list
目标站点开启了 jolokia 端点且存在createJNDIRealm方法,可进行JNDI注入RCE测试,路径为：http://172.19.69.118:9988/actuator/jolokia/list
目标站点开启了 autoconfig 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/autoconfig
目标站点开启了 beans 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/beans
目标站点开启了 configprops 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/configprops
目标站点开启了 dump 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/dump
目标站点开启了 health 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/health
目标站点开启了 info 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/info
目标站点开启了 mappings 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/mappings
目标站点开启了 metrics 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/metrics
目标站点开启了 shutdown 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/shutdown
目标站点开启了 trace 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/trace
```
### 鸣谢
##### [Tide_nuoyan](https://www.jianshu.com/u/58a5f9e596a7)
