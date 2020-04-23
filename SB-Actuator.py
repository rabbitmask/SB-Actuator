#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\
'''

import argparse
import re
import requests
from multiprocessing import Pool, Manager
from concurrent.futures import ThreadPoolExecutor

'''
是懒惰让我们相遇在此~
感谢Tide_诺言大佬帮忙完善思路，具体exp也可关注其相关文章
一个针对单目标or多目标的spring boot actuator / jolokia 检测脚本
输入格式均为：http:127.0.0.1   or  https://xxx.com
对spring boot 的指纹判断老实说可能不太完善，
所以给出了'-s'参数进行强制payload加载，期待各位小伙伴补充
并发设计采用多进程嵌套异步多线程的方式完成
如有bug，欢迎issue反馈，本脚本仅用于授权测试，笔芯
'''

banner=r'''
  ___________________             _____          __                __                
 /   _____/\______   \           /  _  \   _____/  |_ __ _______ _/  |_  ___________ 
 \_____  \  |    |  _/  ______  /  /_\  \_/ ___\   __\  |  \__  \\   __\/  _ \_  __ \
 /        \ |    |   \ /_____/ /    |    \  \___|  | |  |  // __ \|  | (  <_> )  | \/
/_______  / |______  /         \____|__  /\___  >__| |____/(____  /__|  \____/|__|   
        \/         \/                  \/     \/                \/                   
                                                                      By RabbitMask
'''

requests.packages.urllib3.disable_warnings()



headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",}

executor = ThreadPoolExecutor()

# Spring Boot < 1.5 默认未授权访问所有端点
# Spring Boot >= 1.5 默认只允许访问/health和/info端点，但是此安全性通常被应用程序开发人员禁用
# 另外考虑到人为关闭默认端点开启非默认端点的情况，综上所述，此处采用暴力模式配合异步并发（子进程中嵌套异步子线程）解决。
pathlist=['/autoconfig','/beans','/env','/configprops','/dump','/health','/info','/mappings','/metrics','/shutdown','/trace',]

def getinfo(filepath):
    fr = open(filepath, 'r')
    ips=fr.readlines()
    fr.close()
    return ips

def saveinfo(result):
    if result:
        fw=open('result.txt','a')
        fw.write(result+'\n')
        fw.close()

def sbcheck(ip):
    url= str(ip)
    try:
        r = requests.get(url+ '/404', headers=headers,timeout=10,verify=False)
        if r.status_code==404 or r.status_code==403:
            if 'Whitelabel Error Page' in r.text  or 'There was an unexpected error'in r.text:
                print("It's A Spring Boot Web APP: {}".format(url))
                saveinfo( "It's A Spring Boot Web APP: {}".format(url))
                executor.submit(sb_Actuator,url)
                return 1
    except requests.exceptions.ConnectTimeout:
        return 0.0
    except requests.exceptions.ConnectionError:
        return 0.1


def isSB(ip,q):
    print('>>>>> {}'.format(ip))
    sbcheck(ip)
    q.put(ip)

#Spring Boot 1.x版本端点在根URL下注册。
def sb1_Actuator(url):
    key=0
    for i in pathlist:
        url_tar = url+i
        r = requests.get(url_tar, headers=headers, verify=False)
        if r.status_code==200:
            print("目标站点开启了 {} 端点的未授权访问,路径为：{}".format(i.replace('/',''),url_tar))
            saveinfo("目标站点开启了 {} 端点的未授权访问,路径为：{}".format(i.replace('/',''),url_tar))
            key=1
    return key


#Spring Boot 2.x版本端点移动到/actuator/路径。
def sb2_Actuator(url):
    for i in pathlist:
        url_tar = url+'/actuator'+i
        r = requests.get(url_tar, headers=headers, verify=False)
        if r.status_code==200:
            print("目标站点开启了 {} 端点的未授权访问,路径为：{}".format(i.replace('/',''),url_tar))
            saveinfo("目标站点开启了 {} 端点的未授权访问,路径为：{}".format(i.replace('/', ''), url_tar))


#大多数Actuator仅支持GET请求并仅显示敏感的配置数据,如果使用了Jolokia端点，可能会产生XXE、甚至是RCE安全问题。
#通过查看/jolokia/list 中存在的 Mbeans，是否存在logback 库提供的reloadByURL方法来进行判断。
def sb_Actuator(url):
    try:
        if sb1_Actuator(url)==0:
            sb2_Actuator(url)
        url_tar = url + '/jolokia/list'
        r = requests.get(url_tar, headers=headers, verify=False)
        if r.status_code==200:
            print("目标站点开启了 jolokia 端点的未授权访问,路径为：{}".format(url_tar))
            saveinfo("目标站点开启了 jolokia 端点的未授权访问,路径为：{}".format(url_tar))
            if 'reloadByURL'in r.text:
                print("目标站点开启了 jolokia 端点且存在reloadByURL方法,可进行XXE/RCE测试,路径为：{}".format(url_tar))
                saveinfo("目标站点开启了 jolokia 端点且存在reloadByURL方法,可进行XXE/RCE测试,路径为：{}".format(url_tar))
    except:
        pass


def cscan(curl):
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",curl):
        curls=[]
        for i in range(1, 255):
            curls.append('http://' + str(curl)+'.'+str(i))
            # curls.append('https://' + str(curl) + '.' + str(i))
        poolmana(curls)
    else:
        print("C段格式输入有误，锤你昂w(ﾟДﾟ)w")


def poolmana(ips):
    p = Pool(10)
    q = Manager().Queue()
    for i in ips:
        i=i.replace('\n','')
        p.apply_async(isSB, args=(i,q,))
    p.close()
    p.join()
    print('检索完成>>>>>\n请查看当前路径下文件：result.txt')


def run(filepath):
    ips=getinfo(filepath)
    poolmana(ips)


if __name__ == '__main__':
    print(banner)
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest='url',help="单目标扫描")
    parser.add_argument("-s", "--surl", dest='surl', help="单目标扫描(跳过指纹)")
    parser.add_argument("-c", "--curl", dest='curl', help="C段扫描(HTTP_80)")
    parser.add_argument("-f", "--file", dest='file', help="从文件加载目标")

    args = parser.parse_args()
    if args.url:
        res=sbcheck(args.url)
        if res==1:
            pass
        elif res==0.0:
            print("与目标网络连接异常，timeout默认为10s，请根据网络环境自行更改")
        elif res==0.1:
            print("与目标网络连接异常，目标计算机积极拒绝，无法连接")
        else:
            print("目标未使用spring boot或本脚本识别模块不够完善，如为后者欢迎反馈Issue")
    elif args.surl:
        sb_Actuator(args.surl)
    elif args.curl:
        cscan(args.curl)
    elif args.file:
        run(args.file)
