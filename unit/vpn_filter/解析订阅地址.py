import re
from base64 import b64decode
import ping3
import json


class Test_AND_OutIp:
    def __init__(self):

        self.share_links = []
        self.need_test_ip = []
        self.test_is_ok_share_links = []

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
        with open('111.txt', 'r') as f:
            content = f.read()
        self.share_links = b64decode(content).decode('utf-8').splitlines()
        # 提取ip检测
        for text in self.share_links:
            result = re.search(r'@(.*?):', str(text))
            if result is None:
                # Vmess进行第二次base64解码
                print(text)
                text_split = text.split('://')
                text_decode = b64decode(text_split[1]).decode('utf-8').splitlines()
                jsondata = json.loads(text_decode[0])
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
        with open('111_test_is_ok.txt', 'w') as f:
            for link in self.test_is_ok_share_links:
                f.write(str(link) + '\n')

    def main(self):
        self.get_share_links()
        self.output_share_links()


def main():
    test_and_out_ip = Test_AND_OutIp()
    test_and_out_ip.main()


if __name__ == '__main__':
    main()
