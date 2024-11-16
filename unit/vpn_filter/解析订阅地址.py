import re
import time
from base64 import b64decode
import ping3
import json
import requests
import threading

class Test_AND_OutIp:
    def __init__(self):

        self.share_links = []
        self.test_is_ok_share_links = []
        self.subscription_url = ""

    # 使用ping3 检测ip是否可用,可用保存链接
    def test_ip(self, text, ip):
        try:
            rtt = ping3.ping(ip, unit='ms', timeout=3)  # 超时时间
            if rtt is not None:
                print(f"IP: {ip} 延迟为: {rtt} ms")
                # 把text保存到test_is_ok_share_links
                self.test_is_ok_share_links.append(text)
            else:
                print(f"IP: {ip} 无法连接")
        except ping3.errors.PingError as e:
            print(f"IP: {ip} 无法连接，错误信息: {e}")
        except Exception as e:
            print(f"IP: {ip} 发生未知错误，错误信息: {e}")

    def get_share_links(self):
        try:
            # 获取订阅地址的内容（base64转码后的内容）
            content = requests.get(self.subscription_url,timeout=10).text
        except Exception as e:
            print("请求地址：" + self.subscription_url + "失败,原因:"+str(e))
            return
        if content is None:
            print("请求地址：" + self.subscription_url + "没有实际内容")
            return
        # 解码
        self.share_links = b64decode(content).decode('utf-8').splitlines()
        # 提取ip检测
        for text in self.share_links:
            result = re.search(r'@(.*?):', str(text))
            if result is None:
                # Vmess进行第二次base64解码
                text_split = text.split('://')
                text_decode = b64decode(text_split[1]).decode('utf-8')
                text_decode = text_decode.replace(' ', '')
                print(text_decode)
                jsondata = json.loads(text_decode)

                # 检测ip是否可以用
                self.test_ip(text, jsondata['add'])
            if result:
                print(result.group(1))
                # 检测ip是否可以用
                self.test_ip(text, result.group(1))

    def output_share_links(self):
        if self.test_is_ok_share_links is None:
            return
        # 把test_is_ok_share_links保存到test_is_ok.txt
        TIME = time.strftime("%m-%d%H", time.localtime())
        # 打开static目录下的test_is_ok.txt
        with open(file='static/' + TIME + '_test_is_ok.txt', mode='a') as f:
            for link in self.test_is_ok_share_links:
                f.write(str(link) + '\n')

    def main(self):
        try:
            self.get_share_links()
            self.output_share_links()
        except Exception as e:
            print(e)



def main(subscription_url_list):
    # 创建一个Test_AND_OutIp对象
    test_and_out_ip = Test_AND_OutIp()
    for subscription_url in subscription_url_list:
        test_and_out_ip.subscription_url = subscription_url
        try:
            test_and_out_ip.main()
        except Exception as e:
            print(e)
        print("------------------------完成一个------------------------")
if __name__ == '__main__':

    Subscription_url_list = []  # 订阅地址的url列表
    url = "https://raw.githubusercontent.com/bldst/kexue-subscribe-/refs/heads/main/%E8%AE%A2%E9%98%85%E5%9C%B0%E5%9D%80.txt"
    res = requests.get(url, timeout=10)
    if res.status_code == 200:
        # 去除 \n \r 空格
        print(res.text)
        res = res.text.replace("\n", "")
        # 得到订阅地址列表
        Subscription_url_list = [item for item in res.split("\r") if item]
        print(Subscription_url_list)
    else:
        print("error")
    # 启动线程
    """
    将列表平分给两个线程进行处理
    """
    num_elements = len(Subscription_url_list)
    mid_index = num_elements // 2
    list1 = Subscription_url_list[:mid_index]
    list2 = Subscription_url_list[mid_index:]
    # 创建两个线程
    thread1 = threading.Thread(target=main, args=(list1,))
    thread2 = threading.Thread(target=main, args=(list2,))
    # 启动线程
    thread1.start()
    thread2.start()

    # 等待两个线程都执行完毕
    thread1.join()
    thread2.join()

