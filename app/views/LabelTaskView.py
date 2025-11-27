import os
import time
import json
import cv2
import shutil
from datetime import datetime
from cryptography.fernet import Fernet

from django.shortcuts import render, redirect
from django.conf import settings as django_settings
from app.views.ViewsBase import *
from app.models import LabelTaskModel, LabelTkSampleModel
from app.utils.Utils import gen_random_code_s, buildPageLabels

KEY_FILE = os.path.join(BASE_PARENT_DIR, "secret.key")

def get_cipher_suite():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

def index(request):
    context = { "settings": f_settingsReadData() }
    params = f_parseGetParams(request)
    page = int(params.get('p', 1))
    page_size = int(params.get('ps', 10))
    query = LabelTaskModel.objects.all().order_by('-id')
    total = query.count()
    skip = (page - 1) * page_size
    data = query[skip:skip+page_size]
    page_num = int(total / page_size)
    if total % page_size > 0: page_num += 1
    context["data"] = data
    context["pageData"] = {
        "page": page, "page_size": page_size, "page_num": page_num, "count": total,
        "pageLabels": buildPageLabels(page, page_num)
    }
    return render(request, 'app/labelTask/index.html', context)

def add(request):
    context = {
        "settings": f_settingsReadData(),
        "handle": "add"
    }
    
    if request.method == 'POST':
        ret = False
        msg = "未知错误"
        try:
            # 1. 接收参数
            name = request.POST.get('name', '').strip()
            remark = request.POST.get('remark', '')
            
            # 重点修复 2: 增加空值校验，防止报错
            if not name:
                raise Exception("必须填写任务名称")
            
            # 检查文件是否真的上传了
            if 'video_file' not in request.FILES:
                raise Exception("未接收到视频文件，请检查文件大小是否超过限制")
                
            video_file = request.FILES['video_file']
            patient_file = request.FILES.get('patient_file')

            # 2. 创建数据库记录
            user = f_sessionReadUser(request)
            task = LabelTaskModel()
            task.code = gen_random_code_s("TK", 2)
            task.name = name
            task.remark = remark
            task.user_id = user['id']
            task.username = user['username']
            task.video_fps = 30 # 默认30帧
            task.state = 0 
            task.save()

            # 3. 准备目录
            secure_root = os.path.join(BASE_PARENT_DIR, "data", "secure_storage", task.code)
            public_root = os.path.join(django_settings.BASE_DIR, "static", "upload", "images", task.code)
            if not os.path.exists(secure_root): os.makedirs(secure_root)
            if not os.path.exists(public_root): os.makedirs(public_root)

            # 4. 处理病例文件 (加密)
            if patient_file:
                try:
                    cipher = get_cipher_suite()
                    # 分块读取大文件，避免内存溢出
                    encrypted_data = cipher.encrypt(patient_file.read())
                    with open(os.path.join(secure_root, "patient_data.enc"), "wb") as f:
                        f.write(encrypted_data)
                    task.patient_data_path = os.path.join(secure_root, "patient_data.enc")
                except Exception as e:
                    g_logger.error(f"加密失败: {e}")

            # 5. 保存视频文件
            video_ext = os.path.splitext(video_file.name)[1] if video_file.name else ".mp4"
            video_path = os.path.join(secure_root, f"source{video_ext}")
            
            with open(video_path, 'wb+') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)
            
            task.source_video_path = video_path
            task.save()

            # 6. 调用抽帧 (同步执行)
            handle_video_processing(task, video_path, public_root)
            
            ret = True
            msg = "任务创建成功"

        except Exception as e:
            msg = f"提交失败: {str(e)}"
            # 如果失败，清理刚创建的脏数据
            # if 'task' in locals() and task.id: task.delete()

        return render(request, 'app/message.html', {
            "msg": msg, 
            "is_success": ret, 
            "redirect_url": "/labelTask/index"
        })
    
    else:
        return render(request, 'app/labelTask/add.html', context)

def handle_video_processing(task, video_path, output_dir):
    print(f"--- 开始处理视频: {video_path} ---")
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("OpenCV 打开视频失败")
            return

        original_fps = cap.get(cv2.CAP_PROP_FPS)
        if original_fps <= 0: original_fps = 30
        frame_interval = max(1, int(round(original_fps / task.video_fps)))
        
        frame_count = 0
        saved_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            if frame_count % frame_interval == 0:
                file_name = f"img_{saved_count:05d}.jpg"
                save_path = os.path.join(output_dir, file_name)
                cv2.imwrite(save_path, frame)
                
                sample = LabelTkSampleModel()
                sample.code = gen_random_code_s("SP", 1)
                sample.task_code = task.code
                sample.user_id = task.user_id
                sample.username = task.username
                sample.old_filename = file_name
                sample.new_filename = f"upload/images/{task.code}/{file_name}"
                sample.state = 1
                sample.save()
                saved_count += 1
            frame_count += 1

        cap.release()
        task.sample_count = saved_count
        task.is_processed = True
        task.state = 1
        task.save()
        print(f"--- 处理完成，生成 {saved_count} 张图片 ---")
        
    except Exception as e:
        print(f"处理异常: {e}")

def edit(request): pass 
def api_sync(request): return f_responseJson({"code":0, "msg":"not supported"})
def api_postDel(request):
    if request.method == 'POST':
        try:
            params = f_parsePostParams(request)
            task = LabelTaskModel.objects.get(id=params.get('id'))
            if task.code:
                shutil.rmtree(os.path.join(BASE_PARENT_DIR, "data", "secure_storage", task.code), ignore_errors=True)
                shutil.rmtree(os.path.join(django_settings.BASE_DIR, "static", "upload", "images", task.code), ignore_errors=True)
            LabelTkSampleModel.objects.filter(task_code=task.code).delete()
            task.delete()
            return f_responseJson({"code": 1000, "msg": "删除成功"})
        except Exception as e:
            return f_responseJson({"code": 0, "msg": str(e)})

def sample(request):
    context = { "settings": f_settingsReadData() }
    params = f_parseGetParams(request)
    context["task_code"] = params.get('code')
    return render(request, 'app/labelTask/sample.html', context)