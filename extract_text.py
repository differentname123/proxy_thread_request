# coding=utf-8
import os
import sys
import json
import base64
import easyocr


# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'iRNR3ZOTeS7oOcjaaQ4drwFF'

SECRET_KEY = '9wUSInwddyBG01hYvXiro4cimxC2GwNV'


OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"


"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

def get_text(file_name):
    try:
        # 获取access token
        token = fetch_token()

        # 拼接通用文字识别高精度url
        image_url = OCR_URL + "?access_token=" + token

        text = ""

        # 读取测试图片
        file_content = read_file(file_name)

        # 调用文字识别服务
        result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))
        print(result)
        with open("result.txt", 'a') as writer:
            # 解析返回结果
            result_json = json.loads(result)
            for words_result in result_json["words_result"]:
                print(words_result["words"])
                if "（活跃）" in words_result["words"]:
                    writer.write(words_result["words"].split("（活跃）")[0] + os.linesep)

        # 打印文字
        print(text)
    except Exception as e:
        print(e)

def easy_ocr(file_path):
    count = 0
    reader = easyocr.Reader(['ch_sim', 'en'])
    for root_path, _, jpg_name_list in os.walk(file_path):
        for jpg_name in jpg_name_list:
            print(len(jpg_name_list))
            if jpg_name.endswith('.jpg'):
                try:
                    count += 1
                    if count < 1:
                        continue
                    print(root_path + '/' + jpg_name)
                    file_name = (root_path + '/' + jpg_name)
                    result = reader.readtext(file_name)
                    print(result)
                    print(count)
                    with open("result.txt", 'a') as writer:
                        for data in result:
                            writer.write(data[1] + '\n')
                except Exception as e:
                    print("error:%s" % e)


if __name__ == '__main__':

    file_name = "C:/Users/24349/Documents/leidian/Pictures/1654257309401.jpg"
    # get_text(file_name)
    easy_ocr(file_name)