#encoding:UTF-8
__author__ = 'DX'

import io
import sys
import urllib
import urllib.request as ur
import urllib.response
import urllib.error

import json
import random
import os


#html post请求头部信息
headers_str = '''Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50
Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'''


def headers_dx():
    header = headers_str.split('\n')
    length = len(header)
    return header[random.randint(1,length-1)]

def getdata():

    # headers={
        
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

    #     # 'User-Agent': 'Mozilla / 4.0(compatible;MSIE6.0;Windows NT 5.1)'

    # }

    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
    url = "https://www.zhihu.com/api/v3/explore/guest/feeds"
   
    request=ur.Request(url)
    request.add_header('user-agent',headers_dx())
    response=ur.urlopen(request)
    html_byte=response.read()

    # data = urllib.request.urlopen(url，headers=headers).read()

    data = json.loads(html_byte.decode('utf-8'))
    x = data['data']
    # data_max = len(x)

    return (x)


def zhihu():

    post_count = 0
    
    zhihu_post = []

    for index, i in enumerate(getdata()):

        post = ZhiHu_Post()
        
        try:
            
            if(post_count < 12):

                post.post_author=(i['target']['author']['name'])
                post.post_title=(i['target']['question']['title'])
                post.post_target_url=("https://www.zhihu.com/question/"+str(i['target']['question']['id'])+"/answer/"+str(i['target']['id']))
                post_img_url=(i['target']['author']['avatar_url'])

                # print("index:"+str(post_count))
                # print ("标题："+post.post_title+"---作者："+post.post_author+"url:"+post.post_target_url+"图片--img:"+post.post_img_url)

                post_count = post_count + 1

                #保存发表用户图片
                save_img(post_img_url,'dx_{0}'.format(str(index)))

                #转存数据
                post.post_img_url= '/static/blog/images/zhihu/dx_{0}.jpg'.format(str(index))
                
                #知乎数据列表
                zhihu_post.append(post)

            else:
                break

        except KeyError as e:
            continue

    # print ("作者："+T[0][0]+"---标题："+T[1][0]+"url:"+T[2][0]+"图片--img:"+T[3][0])

    return (zhihu_post)


def save_img(img_url,file_name,file_path='blog\\static\\blog\\images\\zhihu'):

    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        if not os.path.exists(file_path):
            print ('文件夹',file_path,'不存在，重新建立')
            # os.makedirs(file_path)

        file_suffix = os.path.splitext(img_url)[1]
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
        urllib.request.urlretrieve(img_url,filename=filename)

    except IOError as e:
        print ('文件操作失败',e)
    except Exception as e:
        print ('错误 ：',e)



class ZhiHu_Post():

    post_author = ''
    post_title = ''
    post_img_url = '' 
    post_target_url = '' 

