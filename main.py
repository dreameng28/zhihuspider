#coding=utf-8
import os
import time
import requests
import leancloud
from leancloud import Object
from lxml import etree
import re
import multiprocessing
from multiprocessing import Pool, Manager



class ZhihuUser(Object):
    pass


manager = Manager()
urls = manager.list()
poolUrls = manager.list()

def save_urls_to_file():
    global urls_file, urls
    if os.path.exists(urls_file):
        os.remove(urls_file)
    print "\n" + str(len(urls))
    f = file(urls_file, "w")
    f.write(str(urls).replace("[", "").replace("]", "").replace("'", ""))
    f.close()

def read_urls_from_file():
    global urls_file
    if os.path.exists(urls_file):
        f = open(urls_file)
        s = f.read()
        print s
        urls_in_file = s.replace(" ", "").replace("\n", "").split(",")
        f.close()
        return urls_in_file


def get_profile(url):
    zhihuUser = ZhihuUser()
    
    try:
        html = requests.get(url, cookies=cook, headers=headers, timeout=60).content
    
    except requests.exceptions.ConnectionError:
        print "异常02"
        time.sleep(2)
        #写入新爬取的url到文件urls.txt
        save_urls_to_file()
    
    selector = etree.HTML(html)
    #昵称、简介
    profile_1_1 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[1]/div/span[@class="name"]/text()')
    for each1 in profile_1_1:
        print each1 +  ' profile_1'
    
    if len(profile_1_1) > 0:
        zhihuUser.set(profile[0][0], profile_1_1[0])
    
    profile_1_2 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[1]/div/span[@class="bio"]/@title')
    for each1 in profile_1_2:
        print each1 +  ' profile_1'
    
    if len(profile_1_2) > 0:
        zhihuUser.set(profile[0][1], profile_1_2[0])
    
    #头像url
    profile_2 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[1]/img/@src')
    for each1 in profile_2:
        print each1 +  ' profile_2'
    
    if len(profile_2) > 0:
        for i in range(len(profile_2)):
            zhihuUser.set(profile[1][i], profile_2[i])

#所在地、职业
profile_3_1 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span[1]/span[@class="location item"]/@title')
    for each1 in profile_3_1:
        print each1 +  ' profile_3'

if len(profile_3_1) > 0:
    zhihuUser.set(profile[2][0], profile_3_1[0])
    
    profile_3_2 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span[1]/span[@class="business item"]/@title')
    for each1 in profile_3_2:
        print each1 +  ' profile_3'
    
    if len(profile_3_2) > 0:
        zhihuUser.set(profile[2][1], profile_3_2[0])
    
    #性别
    profile_4 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/span[1]/span[@class="item gender"]/i/@class')
    for each1 in profile_4:
        print each1 +  ' profile_4'
    
    if len(profile_4) > 0:
        if profile_4[0] == "icon icon-profile-male":
            zhihuUser.set(profile[3][0], "男")
        elif profile_4[0] == "icon icon-profile-female":
            zhihuUser.set(profile[3][0], "女")

#工作地点、职位
profile_5 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[@data-name="employment"]/span[1]/span/@title')
    for each1 in profile_5:
        print each1 +  ' profile_5'

if len(profile_5) > 0:
    for i in range(len(profile_5)):
        zhihuUser.set(profile[4][i], profile_5[i])
    
    #就读院校、研究方向
    profile_6_1 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[@data-name="education"]/span[1]/span[@class="education item"]/@title')
    for each1 in profile_6_1:
        print each1 +  ' profile_6'
    
    if len(profile_6_1) > 0:
        zhihuUser.set(profile[5][0], profile_6_1[0])
    
    profile_6_2 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[@data-name="education"]/span[1]/span[@class="education-extra item"]/@title')
    for each1 in profile_6_2:
        print each1 +  ' profile_6'
    
    if len(profile_6_2) > 0:
        zhihuUser.set(profile[5][1], profile_6_2[0])
    
    #个人介绍
    profile_7 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/span[1]/span[1]/span/text()')
    if len(profile_7) != 0:
        print profile_7[0].strip() + ' profile_7'
    
    if len(profile_7) > 0:
        zhihuUser.set(profile[6][0], profile_7[0])
    
    #赞同数、感谢数
    profile_8 = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[2]/div[1]/span/strong/text()')
    for each1 in profile_8:
        print each1 + ' profile_8'
    
    if len(profile_8) > 0:
        for i in range(len(profile_8)):
            zhihuUser.set(profile[7][i], int(profile_8[i]))

#擅长话题
profile_9 = selector.xpath('/html/body/div[3]/div[1]/div/div/div[2]/div/div/div[2]/div/h3/a/text()')
    for each1 in profile_9:
        print each1 +  ' profile_9'

if len(profile_9) > 0:
    zhihuUser.set(profile[8][0], profile_9)
    
    profile_10  = re.findall('<i class="zg-icon vote"></i>(.*?)</span>\n<span>', html, re.S)
    for each1 in profile_10:
        print each1.strip() +  ' profile_10'
    
    if len(profile_10) > 0:
        zhihuUser.set(profile[9][0], profile_10)
    
    #    profile_10 = selector.xpath('/html/body/div[3]/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/p/span[1]/text()')
    #    for each1 in profile_10:
    #        print each1.strip() +  ' profile_10'
    try:
        zhihuUser.save()

except Exception as e:
    print '异常03:',e
        time.sleep(2)
        save_urls_to_file()

    #增加爬过的，减少待爬的
    urls.append(url)
    poolUrls.remove(url)

followeesUrlPage = url + '/followees'
    htmlWithFollowees = requests.get(followeesUrlPage, cookies = cook).content
    #    print followeesHtml
    
    nextSelector = etree.HTML(htmlWithFollowees)
    followeesUrls = nextSelector.xpath('//*[@id="zh-profile-follows-list"]/div/div/div[2]/h2/a/@href')
    lock.acquire()
    for each in followeesUrls:
        if (each not in urls) and (each not in poolUrls):
            poolUrls.append(each)
    lock.release()





profile =[['name', 'bio'],
          ['icon'],
          ['location', 'business'],
          ['gender'],
          ['employment', 'position'],
          ['education', 'major'],
          ['self_description'],
          ['agree_num', 'thanks_num'],
          ['topic'],
          ['topic_agree_num']]

leancloud.init('GrpTBDwXyRtDHkAYeRHWdc3u', 'BtN94yX5Yn3fNbzV08mVlxv6')

cook={"Cookie": ' q_c1=78e4ce6bf2614fb8b813d6abe0e2f00d|144721992000|1444819250000;cap_id="NGIyNjg1MTRmYWI1NDhjZWJlOTZhMTI2NDFjNDI1Mjg=|1447730523|ecb378475467d522e7c92485d0b487b26ca5ec3a"; __utma=51854390.688498471.1444883443.1444883443.1444883443.1; __utmz=51854390.1444883443.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|3=entry_date=20151014=1; z_c0="QUFDQXdlNHhBQUFYQUFBQVlRSlZUV2NxY2xZQk5pMkUyUkVPNUZvLUpSX2FMYjlxLUMzdEp3PT0=|1447730535|ec3a878c6ec53ce245bae642ee665890430fe6e7"; unlock_ticket="QUFDQXdlNHhBQUFYQUFBQVlRSlZUVy1rU2xZNGxJbDJyOXF2QWU4SVRucE5idmtySDAwSS1BPT0=|1447730535|5198aff4c56a02b713195e2e935134edc797ce15"'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
beginUrl = 'http://www.zhihu.com/people/dreameng'


#从urls.txt读取已经爬取到的url到urls
urls_file = "urls_file.txt"
if os.path.exists(urls_file):
    urls = read_urls_from_file()
    print urls, len(urls)


#开始爬虫程序
lock = multiprocessing.Lock()
if beginUrl not in urls:
    poolUrls.append(beginUrl)
    try:
        while (len(urls) < 100000) and (len(poolUrls) > 0):
            pool = Pool()
            for i in poolUrls:
                pool.apply_async(get_profile, args=(i,))
            pool.close()
            pool.join()

except Exception as e:
    time.sleep(2)
        print '异常01:',e
    
    finally:
        #写入新爬取的url到文件urls.txt
        save_urls_to_file()
