import requests
url = "https://nodefree.githubrowcontent.com/2024/11/20241110.txt"
res = requests.get(url, timeout=10)
if res.status_code == 200:
    print(res.text)