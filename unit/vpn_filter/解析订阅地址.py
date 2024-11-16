import re
import time
from base64 import b64decode
import ping3
import json
import requests


class Test_AND_OutIp:
    def __init__(self):

        self.share_links = []
        self.need_test_ip = []
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
        # 打开111.txt
        # with open('111.txt', 'r') as f:
        #     content = f.read()
        content = requests.get(self.subscription_url).text
        if content is None:
            print("请求地址：" + self.subscription_url + "失败")
            return
        self.share_links = b64decode(content).decode('utf-8').splitlines()
        # 提取ip检测
        for text in self.share_links:
            result = re.search(r'@(.*?):', str(text))
            if result is None:
                # Vmess进行第二次base64解码
                print(text)
                text_split = text.split('://')
                text_decode = b64decode(text_split[1]).decode('utf-8')
                text_decode=text_decode.replace(' ', '')
                print(text_decode)
                jsondata = json.loads(text_decode)
                # need_test_ip.append(json['add'])
                # 检测ip是否可以用
                self.test_ip(text, jsondata['add'])
            if result:
                print(result.group(1))
                # 检测ip是否可以用
                self.test_ip(text, result.group(1))
                self.need_test_ip.append(result.group(1))

    def output_share_links(self):
        # 把test_is_ok_share_links保存到111_test_is_ok.txt
        with open('111_test_is_ok.txt', 'a') as f:
            for link in self.test_is_ok_share_links:
                f.write(str(link) + '\n')

    def main(self):
        self.get_share_links()
        self.output_share_links()


def main(subscription_url):
    test_and_out_ip = Test_AND_OutIp()
    test_and_out_ip.subscription_url = subscription_url
    test_and_out_ip.main()


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
    for i in Subscription_url_list:
        main(i)
