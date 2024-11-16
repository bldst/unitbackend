from django.conf import settings
from django.http import HttpResponse
import os


def get_subscription(request):
      # 获取项目的BASE_DIR（项目根目录），settings.BASE_DIR就是项目根目录的绝对路径
    base_dir = settings.BASE_DIR
    # 假设static文件夹在项目根目录下，拼接出文件的实际路径
    file_path = os.path.join(base_dir,'vpn_filter/static', '11-1704_test_is_ok.txt')
    print(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            # 创建HttpResponse对象，设置响应内容类型为'text/plain'，表示纯文本
            response = HttpResponse(file_content, content_type='text/plain')

            return response
    except FileNotFoundError:
        return HttpResponse("文件未找到", status=404)
