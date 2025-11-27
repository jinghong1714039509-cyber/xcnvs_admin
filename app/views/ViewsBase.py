import os
import time
import platform
import requests
from datetime import datetime, timedelta
import json
from django.http import HttpResponse
from framework.settings import (BASE_DIR, PROJECT_UA,PROJECT_BUILT,PROJECT_VERSION, PROJECT_FLAG,PROJECT_ADMIN_START_TIMESTAMP,TIMEOUT,
                                PROJECT_SUPPORT_XCMS_MIN_VERSION,PROJECT_SUPPORT_V3_MIN_VERSION)

# 移除无关工具引用
# from app.utils.ZLMediaKit import ZLMediaKit
from app.utils.Settings import Settings
from app.utils.Config import Config
from app.utils.Logger import CreateLogger
from app.utils.OSSystem import OSSystem
from app.utils.Database import Database
# from app.utils.AiInterfaceUtils import AiInterfaceUtils
# from app.utils.PgSQLVectorUtils import PgSQLVectorUtils
from app.models import *

# BASE_DIR # xcnvs_admin目录的位置
BASE_PARENT_DIR = os.path.dirname(BASE_DIR)  # BASE_PARENT_DIR是软件根目录的位置
g_filepath_config_json = os.path.join(BASE_PARENT_DIR, "config.json")
g_filepath_config_ini = os.path.join(BASE_PARENT_DIR, "config.ini")
g_filepath_settings_json = os.path.join(BASE_DIR, "settings.json")

g_config = Config(filepath=g_filepath_config_json)
g_settings = Settings(filepath=g_filepath_settings_json)

__log_dir = os.path.join(BASE_PARENT_DIR, "log")
if not os.path.exists(__log_dir):
    os.makedirs(__log_dir)
g_logger = CreateLogger(filepath=os.path.join(__log_dir, "xcnvs_admin%s.log" % (datetime.now().strftime("%Y%m%d-%H%M%S"))),
                        is_show_console=False,
                        log_debug=g_config.logDebug)

g_logger.info("%s v%s,%s" % (PROJECT_UA,PROJECT_VERSION, PROJECT_FLAG))
g_logger.info(PROJECT_BUILT)
g_logger.info("g_filepath_config_json=%s" % g_filepath_config_json)
g_logger.info("g_filepath_config_ini=%s" % g_filepath_config_ini)
g_logger.info("g_filepath_settings_json=%s" % g_filepath_settings_json)
g_logger.info("config.json:%s" % g_config.getStr())
g_logger.info("settings.json:%s" % g_settings.getStr())
g_logger.info("logDebug=%d" % g_config.logDebug)

g_osSystem = OSSystem()
# g_aiInterfaceUtils = AiInterfaceUtils(logger=g_logger, config=g_config) # 移除
# g_pgSQLVectorUtils = PgSQLVectorUtils(logger=g_logger, config=g_config) # 移除
# g_zlm = ZLMediaKit(logger=g_logger, config=g_config) # 移除
g_database = Database(logger=g_logger)

g_session_key_user = "user"
g_session_key_captcha = "captcha"

def f_parseGetParams(request):
    params = {}
    try:
        for k in request.GET:
            params.__setitem__(k, request.GET.get(k))
    except Exception as e:
        params = {}

    return params

def f_parsePostParams(request):
    params = {}
    for k in request.POST:
        params.__setitem__(k, request.POST.get(k))

    # 接收json方式上传的参数
    if not params:
        try:
            params = request.body.decode('utf-8')
            params = json.loads(params)
        except Exception as e:
            params = {}

    return params

def f_parseRequestIp(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR') # 备用方案
    except Exception as e:
        g_logger.error("f_parseRequestIp() error: %s"%str(e))
        ip = "0.0.0.0"
    return ip

def f_parseRequestPort(request):
    return 0

def readUser(request):
    user = request.session.get(g_session_key_user)
    return user

def f_sessionReadUser(request):
    user = request.session.get(g_session_key_user)
    return user

def f_sessionReadUserId(request):
    try:
        user_id = f_sessionReadUser(request).get("id")
    except:
        user_id = 0
    return user_id

def f_sessionLogout(request):
    if request.session.has_key(g_session_key_user):
        del request.session[g_session_key_user]
    if request.session.has_key(g_session_key_captcha):
        del request.session[g_session_key_captcha]

def f_checkRequestSafe(request):
    ret = False
    msg = "未知错误"
    # 检查请求是否安全
    user_id = f_sessionReadUserId(request)
    if user_id:
        ret = True
        msg = "success"
    else:
        headers = request.headers
        Safe = headers.get("Safe")
        if Safe and Safe == g_config.xcnvsSafe:
            ret = True
            msg = "success"
        else:
            msg = "safe verify error"
    return ret,msg

def f_readSampleCountAndAnnotationCount(task_code):
    sample_count = g_database.select("select count(id) as count from xcnvs_labeltk_sample where task_code='%s'" % task_code)
    sample_count = int(sample_count[0]["count"])
    sample_annotation_count = g_database.select(
        "select count(id) as count from xcnvs_labeltk_sample where task_code='%s' and annotation_state=1" % task_code)
    sample_annotation_count = int(sample_annotation_count[0]["count"])

    return sample_count, sample_annotation_count

def f_responseJson(res):
    def json_dumps_default(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    return HttpResponse(json.dumps(res, default=json_dumps_default), content_type="application/json")

def f_settingsReadData():
    return g_settings.data

# 下方关于 Node 同步和 ZLMediaKit 的逻辑已全部移除