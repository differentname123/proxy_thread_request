# -- coding: utf-8 --
"""
:authors:
    zhuxiaohu@baidu.com
:create_date:
    2022/6/10 12:57 下午
:last_date:
    2022/6/10 12:57 下午
:description:
    
"""
import time
import traceback

import requests

max_waite_time = 600

def load_proxy():
    print "start load proxy"

    proxy_list = []
    all_proxy_set = set()
    index = 0
    with open("text/all_proxy.txt") as lines:
        for proxy in lines:
            ip_port = proxy.strip()
            index += 1
            print "%s (%s) test" % (index, ip_port)


            check_ip_port_result = check_proxy(ip_port)
            second_check_ip_port_result = check_little_empire(ip_port)
            if check_ip_port_result and second_check_ip_port_result:
                proxy_list.append(proxy)
            if check_ip_port_result or second_check_ip_port_result:
                all_proxy_set.add(proxy)

    with open("text/proxy.txt", 'w') as writer:
        writer.writelines(proxy_list)

    with open("text/all_proxy.txt", 'w') as writer:
        writer.writelines(all_proxy_set)
    print "finish load %s conect all %s" % (len(proxy_list), len(all_proxy_set))


def check_little_empire(ip_port):
    result = False
    proxy = {"http": "http://" + ip_port}
    url = "http://46.51.252.220:82/api/login?a=n&v=1.26.0&u_c=unknown&cl_t=fantasy&p_e=cXdlcjEyMzQ=&fm=bin&e_e=5pW05a655L6d54S25LiR"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.55 Safari/537.36',
    }
    exe_time = 0
    retyr_time = 1
    while result == False:
        try:

            response = requests.get(url, headers=headers, proxies=proxy, timeout= 5)
            if "ios" in response.content:
                result = True
                # print response.content
                break
        except Exception as e:
            print "check_ip_port error %s" % traceback.format_exc()
        exe_time += 1
        if exe_time > retyr_time:
            break



    return result


def check_proxy(ip_port):
    result = False
    proxy = {"http": "http://" + ip_port}
    url = "http://www.baidu.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.55 Safari/537.36',
    }
    exe_time = 0
    retyr_time = 1
    while result == False:
        try:

            response = requests.get(url, headers=headers, proxies=proxy, timeout= 5)
            if "全球领先的中文搜索引擎" in response.content:
                result = True
                break
        except Exception as e:
            print "check_ip_port error %s" % traceback.format_exc()

        exe_time += 1
        if exe_time > retyr_time:
            break



    return result

def fun():

    count = 2
    ip_port_set = set()
    start_page_number = 333448
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.55 Safari/537.36',
    }

    for i in range(count):
        try:
            page_number = start_page_number - i
            url = "https://www.zdaye.com/dayProxy/ip/%s.html" % page_number

            response = requests.get(url, headers=headers)
            data = response.content
            data_line_list = data.split('\n')

            for data_line in data_line_list:
                if "立即检测该代理IP_" in data_line:
                    key_seg = data_line.split("立即检测该代理IP_")[1]
                    ip_port = key_seg.split("是否可用")[0]
                    ip_port_set.add(ip_port + '\n')

            url = "https://www.zdaye.com/dayProxy/ip/%s/3.html" % page_number

            response = requests.get(url, headers=headers)
            data = response.content
            data_line_list = data.split('\n')

            for data_line in data_line_list:
                if "立即检测该代理IP_" in data_line:
                    key_seg = data_line.split("立即检测该代理IP_")[1]
                    ip_port = key_seg.split("是否可用")[0]
                    ip_port_set.add(ip_port + '\n')

            url = "https://www.zdaye.com/dayProxy/ip/%s/2.html" % page_number

            response = requests.get(url, headers=headers)
            data = response.content
            data_line_list = data.split('\n')

            for data_line in data_line_list:
                if "立即检测该代理IP_" in data_line:
                    key_seg = data_line.split("立即检测该代理IP_")[1]
                    ip_port = key_seg.split("是否可用")[0]
                    ip_port_set.add(ip_port + '\n')
        except Exception as e:
            print e

    with open("text/proxy.txt", 'w') as writer:
        writer.writelines(ip_port_set)
    print ip_port_set

def get_proxy_ip():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.55 Safari/537.36',
    }

    url = "https://proxy.seofangfa.com/"
    try:

        response = requests.get(url, headers=headers)
        data = response.content
        ip_port_list = []
        for line in data.split('\n'):
            if "</td><td>" in line:
                port = line.split("</td><td>")[1]
                ip_data = line.split("</td><td>")[0].split("<tr><td>")[1]
                ip_port = "%s:%s\n" % (ip_data, port)
                ip_port_list.append(ip_port)
        with open("text/all_proxy.txt", 'a') as writer:
            writer.writelines(ip_port_list)
    except Exception as e:
        print "get_proxy_ip error %s" % traceback.format_exc()

    url = "http://www.66ip.cn/index.html"
    import re

    try:

        response = requests.get(url, headers=headers)
        data = response.content
        ip_result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}</td><td>\d+\b", data)
        ip_port_list = []
        for line in ip_result:
            line = line.strip()
            if "</td><td>" in line:
                port = line.split("</td><td>")[1]
                ip_data = line.split("</td><td>")[0]
                ip_port = "%s:%s\n" % (ip_data, port)
                ip_port_list.append(ip_port)
        with open("text/all_proxy.txt", 'a') as writer:
            writer.writelines(ip_port_list)
    except Exception as e:
        print "get_proxy_ip error %s" % traceback.format_exc()


    url = "http://www.ip3366.net/"
    try:
        count_index = 0
        response = requests.get(url, headers=headers)
        data = response.content
        ip_port_list = []
        data_arr = data.split('\n')
        while count_index < len(data_arr):
            line = data_arr[count_index]
            ip_result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
            if len(ip_result) == 1:
                count_index += 1
                port = data_arr[count_index].split("</td>")[0].split("<td>")[1].strip()
                ip_data = ip_result[0]
                ip_port = "%s:%s\n" % (ip_data, port)
                ip_port_list.append(ip_port)
            count_index += 1


        with open("text/all_proxy.txt", 'a') as writer:
            writer.writelines(ip_port_list)
    except Exception as e:
        print "get_proxy_ip error %s" % traceback.format_exc()

    url = "http://www.kxdaili.com/dailiip/1/1.html"
    try:
        count_index = 0
        response = requests.get(url, headers=headers)
        data = response.content
        ip_port_list = []
        data_arr = data.split('\n')
        while count_index < len(data_arr):
            line = data_arr[count_index]
            ip_result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
            if len(ip_result) == 1:
                count_index += 1
                port = data_arr[count_index].split("</td>")[0].split("<td>")[1].strip()
                ip_data = ip_result[0]
                ip_port = "%s:%s\n" % (ip_data, port)
                ip_port_list.append(ip_port)
            count_index += 1


        with open("text/all_proxy.txt", 'a') as writer:
            writer.writelines(ip_port_list)
    except Exception as e:
        print "get_proxy_ip error %s" % traceback.format_exc()


    url = "http://ip.yqie.com/ipproxy.htm"
    try:
        count_index = 0
        response = requests.get(url, headers=headers)
        data = response.content
        ip_port_list = []
        data_arr = data.split('\n')
        while count_index < len(data_arr):
            line = data_arr[count_index]
            ip_result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
            if len(ip_result) == 1:
                count_index += 1
                port = data_arr[count_index].split("</td>")[0].split("<td>")[1].strip()
                ip_data = ip_result[0]
                ip_port = "%s:%s\n" % (ip_data, port)
                ip_port_list.append(ip_port)
            count_index += 1


        with open("text/all_proxy.txt", 'a') as writer:
            writer.writelines(ip_port_list)
    except Exception as e:
        print "get_proxy_ip error %s" % traceback.format_exc()


    url = "https://www.89ip.cn/"
    try:
        count_index = 0
        ip_flag = False
        response = requests.get(url, headers=headers)
        data = response.content
        ip_port_list = []
        data_arr = data.split('\n')
        while count_index < len(data_arr):
            line = data_arr[count_index]
            ip_result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
            if len(ip_result) == 1:
                count_index += 2
                port = data_arr[count_index].split("</td>")[0].strip()
                ip_data = ip_result[0]
                ip_port = "%s:%s\n" % (ip_data, port)
                ip_port_list.append(ip_port)
            count_index += 1


        with open("text/all_proxy.txt", 'a') as writer:
            writer.writelines(ip_port_list)
    except Exception as e:
        print "get_proxy_ip error %s" % traceback.format_exc()

    url = "https://free.kuaidaili.com/free/intr"
    try:
        count_index = 0
        ip_flag = False
        response = requests.get(url, headers=headers)
        data = response.content
        ip_port_list = []
        data_arr = data.split('\n')
        while count_index < len(data_arr):
            line = data_arr[count_index]
            ip_result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
            if len(ip_result) == 1:
                count_index += 1
                new_line = data_arr[count_index]
                port = new_line.split("</td>")[0].split(">")[1].strip()
                ip_data = ip_result[0]
                ip_port = "%s:%s\n" % (ip_data, port)
                ip_port_list.append(ip_port)
            count_index += 1


        with open("text/all_proxy.txt", 'a') as writer:
            writer.writelines(ip_port_list)
    except Exception as e:
        print "get_proxy_ip error %s" % traceback.format_exc()


    url = "https://free.kuaidaili.com/free/"
    try:

        response = requests.get(url, headers=headers)
        data = response.content
        ip_port_list = []
        ip_data = 0
        for line in data.split('\n'):
            if "<td data-title=\"IP\">" in line:
                ip_data = line.split(">")[1].split("<")[0]
            if "<td data-title=\"PORT\">" in line:
                port = line.split(">")[1].split("<")[0]
                ip_port = "%s:%s\n" % (ip_data, port)
                ip_port_list.append(ip_port)
                pass
        with open("text/all_proxy.txt", 'a') as writer:
            writer.writelines(ip_port_list)
    except Exception as e:
        print "get_proxy_ip error %s" % traceback.format_exc()

    all_proxy_set = set()
    with open("text/all_proxy.txt") as lines:
        for proxy in lines:
            all_proxy_set.add(proxy)

    with open("text/all_proxy.txt", 'w') as writer:
        writer.writelines(all_proxy_set)

def keep_load_proxy():
    time_ok = True
    while True:
        now_time = time.time()
        try:
            get_proxy_ip()
            if time_ok:
                befor_time = time.time()
                load_proxy()
                time_ok = False
            time.sleep(60)
            print "waite for 10s"
        except Exception as e:
            print e
        if now_time - befor_time > max_waite_time:
            print "update proxy"
            time_ok = True


if __name__ == "__main__":
    print "start get proxy"
    # fun()
    keep_load_proxy()
