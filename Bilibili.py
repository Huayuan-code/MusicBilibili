# -*- coding: gbk -*-
from ast import Try
import requests  # 导入用于发送HTTP请求的requests库
from bs4 import BeautifulSoup # 导入用于解析HTML的BeautifulSoup库
import re
import json
from mutagen.id3 import ID3, TIT2, APIC
import subprocess 
import os


user_cookie = ""
save_path = ""

def search(keyword):
# 网址
    url = "https://search.bilibili.com/all?vt=53655423&keyword="
    url += keyword
    url += "&page=1"
    # 设置请求头，用于模拟浏览器发送请求
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # 发送 HTTP 请求并获取响应内容
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 解析搜索结果
    items = soup.find_all("div", class_="bili-video-card__info __scale-disable")
 
    result = []
    for item in items:
        # 提取视频标题
        title = item.find('h3', class_='bili-video-card__info--tit').text
        #print(title)
    
        # 提取视频链接
        url = item.find('a', href=True)['href']
        #print(url)
        result.append((title, url) )
    return result

def getMp3(url):
    
    headers = {
            # Referer 防盗链 告诉服务器你请求链接是从哪里跳转过来的
            "Referer": "https://www.bilibili.com",
            #"Referer": url,
            # User-Agent 用户代理, 表示浏览器/设备基本身份信息
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Cookie": user_cookie
    }

    response = requests.get(url=url, headers=headers)
    html = response.text
    #print(html)
    # 解析数据: 提取视频标题
       
    # 提取视频信息
    try: 
        info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
    except Exception:
        return
    replace_chars = '|:<>?*"\\/'   
    translation_table = str.maketrans(replace_chars, '_' * len(replace_chars)) 
    title = re.findall('title="(.*?)"', html)[0]
    title = title.translate(translation_table) 
    title= title.replace("/", "_")
    title= title.replace("|", "_")
    title= title.replace(".", "_")
    if save_path != "":
        title = save_path + '\\' + title
    print(title)
    if(os.path.exists(title + ".mp3")):
        print("already exists")
        return

    # 提取音频链接
    json_data = json.loads(info)
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
    #print(audio_url)
    # 获取音频内容

    try: 
        audio_content = requests.get(url=audio_url, headers=headers).content
    except:
        return
    # 保存数据
    with open(title + 'temp.mp3', mode='wb') as a:
        a.write(audio_content)

    #获取作者列表
    try:
        soup = soup = BeautifulSoup(response.text, "lxml")
        authordata = soup.find_all('a', class_ = "staff-name is-vip")
        updata = soup.find_all('a', class_ = "up-name is_vip")
        #print(authordata)
        authorliststr = ""
        for a in authordata:
            print("staffmember:" + a.text)
            authorliststr = authorliststr + a.text + ";"
        for u in updata:
            uu =  re.sub(r"[\\\/:*?<>|\n\ ]","",u.text)
            print("up:" + uu)
            authorliststr = authorliststr + uu + ";"
    except:
        print("author error")
        return

    #获取封面
    try:
        soup = BeautifulSoup(response.text, "lxml")
        coverdata = soup.find_all('meta', itemprop = 'image')
        print(coverdata)
        coverurl =  "https:" + re.findall('//.*@', coverdata[0]['content'])[0]
        print(coverurl)
        coverurl = re.sub(r'[@]', "", coverurl)
        print(coverurl)
        coverurl2 = "https:" + re.findall('//.*\.png', coverdata[0]['content'])[0]
    except:
        print("no cover")
        return


    cmd = f"ffmpeg -i \"{title}temp.mp3\" -metadata TIT3=\"{title}\" -metadata artist=\"{authorliststr}\" \"{title}.mp3\""  
    result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
    print("数据写入成功！")
    os.remove(f"{title}temp.mp3")

    cover_content = requests.get(url=coverurl,headers=headers).content
    with open (title + ".jpg", mode = "wb") as f :
        f.write(cover_content)

    with open(title + ".jpg", 'rb') as img:
        audio = ID3(title + ".mp3")
        audio.update_to_v23()
        audio['APIC'] = APIC(
            encoding = 0,
            mime = 'image/jpg',
            type = 3,
            data = img.read()
        )
        audio.save()
    os.remove(f"{title}.jpg")

    




def analyse_favorlist(ml_id):
    print("af")
    headers = {
            # Referer 防盗链 告诉服务器你请求链接是从哪里跳转过来的
            "Referer": "https://www.bilibili.com",
            #"Referer": url,
            # User-Agent 用户代理, 表示浏览器/设备基本身份信息
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Cookie": user_cookie
    }
    result =[]
    for i in range(1, 100):
        try:
            url = 'https://api.bilibili.com/medialist/gateway/base/spaceDetail?media_id=' + ml_id + '&pn='+ str(i) +'&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
            html = requests.get(url=url, headers=headers)
            i = i + 1
            print(f"i={i}")
            res = json.loads(html.text)
            len_video = len(res['data']['medias'])
            print(f"len={len_video}")
            for id in range(0,len_video):
                if not res['data']['medias'][id]['title'] == '已失效视频':
                    result.append((res['data']['medias'][id]['title'], res['data']['medias'][id]['bvid']))
                    print(res['data']['medias'][id]['title'])
                    print(res['data']['medias'][id]['bvid'])
        except Exception:     
            print("bbbb")
            break

    return result
  
def analyse_uplist(up_id):
    
    headers = {
            # Referer 防盗链 告诉服务器你请求链接是从哪里跳转过来的
            "Referer": "https://www.bilibili.com",
            #"Referer": url,
            # User-Agent 用户代理, 表示浏览器/设备基本身份信息
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Cookie": user_cookie
    }
    result =[]
    for i in range(1, 100):
        try:
            #&ps=30&tid=0&pn=3&keyword=&order=pubdate
            url = 'https://api.bilibili.com/x/space/arc/search?mid=' + up_id + '&ps=30&tid=0&pn=' + str(i) + '&keyword=&order=pubdate&jsonp=jsonp&platform=web&web_location=1550101&order_avoided=true&dm_img_list=[]' 
            html = requests.get(url=url, headers=headers)
            i = i + 1
            print(f"i={i}")
            res = json.loads(html.text)
            len_video = len(res['data']['list']['vlist'])
            print(f"len={len_video}")
            for id in range(0,len_video):
                if not res['data']['list']['vlist'][id]['title'] == '已失效视频':
                    result.append((res['data']['list']['vlist'][id]['title'], res['data']['list']['vlist'][id]['bvid']))
                    print(res['data']['list']['vlist'][id]['title'])
                    print(res['data']['list']['vlist'][id]['bvid'])
        except Exception as e:     
            print(f"An error occurred: {e.__class__.__name__}")  
            print(res)
    # 打印堆栈跟踪  
            #traceback.print_exc()
            break

    return result

#https://api.bilibili.com/x/space/wbi/arc/search?mid=698029620&ps=30&tid=0&pn=3&keyword=&order=pubdate
        