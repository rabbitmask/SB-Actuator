# SB-Actuator
Spring Boot Actuator未授权访问【XXE、RCE】单/多目标检测

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
                                                                      By RabbitMask

usage: SB-Actuator.py [-h] [-u URL] [-s SURL] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     单目标扫描
  -s SURL, --surl SURL  单目标扫描(跳过指纹)
  -c CURL, --curl CURL  C段扫描(HTTP_80)
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
                                                                      By RabbitMask

It's A Spring Boot Web APP: http://172.19.69.118:9988
目标站点开启了 autoconfig 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/autoconfig
目标站点开启了 beans 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/beans
目标站点开启了 env 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/env
目标站点开启了 configprops 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/configprops
目标站点开启了 dump 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/dump
目标站点开启了 health 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/health
目标站点开启了 info 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/info
目标站点开启了 mappings 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/mappings
目标站点开启了 metrics 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/metrics
目标站点开启了 shutdown 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/shutdown
目标站点开启了 trace 端点的未授权访问,路径为：http://172.19.69.118:9988/actuator/trace
目标站点开启了 jolokia 端点的未授权访问,路径为：http://172.19.69.118:9988/jolokia/list
目标站点开启了 jolokia 端点且存在reloadByURL方法,可进行XXE/RCE测试,路径为：http://172.19.69.118:9988/jolokia/list
```
### 鸣谢
##### [Tide_nuoyan](https://www.jianshu.com/u/58a5f9e596a7)
