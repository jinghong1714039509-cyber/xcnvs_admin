import os
import zipfile
from django.http import HttpResponse, StreamingHttpResponse
from django.conf import settings
from app.views.ViewsBase import *
from app.models import LabelTkSampleModel

def download(request):
    """
    B端核心下载接口：打包下载脱敏图片
    URL: /storage/download?type=images&code=TASK_CODE
    """
    params = f_parseGetParams(request)
    download_type = params.get("type")
    task_code = params.get("code")

    if not task_code:
        return HttpResponse("缺少任务编号", status=400)

    if download_type == "images":
        # 1. 查找图片路径
        # 注意：这里我们要找的是 static/upload/images/TASK_CODE 目录
        image_dir = os.path.join(settings.BASE_DIR, "static", "upload", "images", task_code)
        
        if not os.path.exists(image_dir):
            return HttpResponse("该任务没有图片数据或正在处理中", status=404)

        # 2. 创建流式响应 (生成 ZIP)
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{task_code}_images.zip"'

        # 3. 写入 ZIP
        with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(image_dir):
                for file in files:
                    # 只允许图片，双重保险
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        file_path = os.path.join(root, file)
                        # 在ZIP里的文件名：img_001.jpg
                        zf.write(file_path, arcname=file)

        return response

    return HttpResponse("不支持的下载类型", status=400)

def access(request):
    # 简单的文件访问代理 (如果需要)
    return HttpResponse("Access Denied", status=403)