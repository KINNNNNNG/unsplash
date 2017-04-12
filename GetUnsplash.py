'''
Created on 2016年11月1日

@author: K
'''
#encoding UTF-8

import urllib.request
import re
from PIL import Image
import os,time,glob,sys
import requests


def get_filename():#获得文件下下的文件名
    filenames = []
    os.chdir(r'F:\\Users\K\Pictures\Wallpapers')
    for filename in glob.glob("*.jpg"):
        filenames.append(filename)
    return filenames

def testname(filename):#测试下载文件是否存在
    f = get_filename()
    for x in f:
        if x == filename:
            x =1
            break
        else:
            x = 0
    if x == 1:
        return 1
    else:
        return 0

def getUrlName(x):
    url = 'https://unsplash.com/napi/photos'
    params = {
        'page': x,
        'per_page': '12',
        'order_by': 'latest'
    }
    hears = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'accept-version': 'v1',
        'authorization': 'Client-ID d69927c7ea5c770fa2ce9a2f1e3589bd896454f7068f689d8e41a25b54fa6042',
        'Connection': 'keep-alive',
        'Host': 'unsplash.com',
        'Referer': 'https://unsplash.com/new',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    data = requests.get(url=url, params=params, headers=hears)
    name = []
    durl = []
    wh = []
    for i in data.json():
        name.append(i['id'])
        durl.append(i['links']['download'])
        if(i['height']<i['width'] or i['height']==i['width']):
            wh.append(0)
        else:
            wh.append(1)
    return durl,name,wh

def get_p():
    n=1
    m = True
    while(m):
        local = 'F:\\users\K\Pictures\Wallpapers\\'
        url,name,wh = getUrlName(n)
        y=0
        x=0
        temp = 0
        for p in name :
           print(p)
           y+=1
        print(y)
        while x<len(name):
            d_url = url[x]
            if testname(name[x]+'.jpg')==0 and wh[x]==0:
                print()
                print(d_url)
                urllib.request.urlretrieve(d_url, local+name[x]+'.jpg', reporthook=(report))
            else:
                print()
                if wh[x]==1:
                    print(name[x]+'.jpg'+'长宽不符')
                else:
                    print(name[x]+'.jpg'+'重名')
                temp +=1
                if temp==len(name):
                    m=False
            x += 1
        n+=1
        print()


def report(count, blockSize, totalSize):#显示下载壁纸进度
  percent = int(count*blockSize*100/totalSize)
  sys.stdout.write("\r%d%%" % percent + ' complete')
  sys.stdout.flush()


# def remove_p():#删除不规范壁纸
#     f_n = get_filename()
#     for filename in f_n:
#         fb = 'F:\\Users\K\Pictures\Wallpapers\\' + filename
#         fb = str(fb)
#         filenames = open(fb, 'rb')
#         img = Image.open(filenames)
#         filenames.close()
#         imgsize = img.size
#         if (imgsize[0] <= imgsize[1]) or (imgsize[0]<1920 and imgsize[1]<1080):
#             os.remove(filename)
#             print("删除" + filename)

nowtime = time.localtime(time.time())#现在的时间

def delTime():#在这之前的时间一个月，删除壁纸
    del_mon = nowtime.tm_mon - 1
    if del_mon<=0:
        del_year = nowtime.tm_year - 1
        del_mon = 12+del_mon
    else:
        del_year = nowtime.tm_year
    return del_year,del_mon

def delfile(): #删除两个月前的壁纸（仅一个月）
    filename = get_filename()
    for x in filename:
        filemtime = os.stat('F:\\Users\K\Pictures\\Wallpapers\\' + x).st_mtime
        filetime = time.localtime(filemtime)
        del_year, del_mon = delTime()
        if filetime.tm_year == del_year and filetime.tm_mon == del_mon:
            remove = x
            os.remove('F:\\Users\K\Pictures\\Wallpapers\\' + remove)
            print(x)
            print(str(filetime.tm_year) + "." + str(filetime.tm_mon) + "." + str(filetime.tm_mday))


if __name__ == "__main__":
    delfile()
    # remove_p()
    get_p()
