from django.urls import path
from .views import UserView
from .views import IndexView
# from .views import NodeView   # 已移除
# from .views import AlarmView  # 已移除
# from .views import MediaView  # 已移除
# from .views import StreamView # 已移除
# from .views import ControlView # 已移除
# from .views import OpenView   # 已移除
from .views import StorageView
# from .views import InnerlView # 已移除
from .views import LabelTaskView
from .views import LabelTkSampleView
# from .views import LabelTkTrainView # 已移除
# from .views import LabelTkPredictView # 已移除

app_name = 'app'

urlpatterns = [
    # 主页功能
    path('', IndexView.index),

    # 登陆退出
    path('captcha', UserView.captcha),
    path('login', UserView.login),
    path('logout', UserView.logout),

    # 用户管理
    path('user/index', UserView.index),
    path('user/add', UserView.add),
    path('user/edit', UserView.edit),
    path('user/postDel', UserView.api_postDel),


    # 节点管理 (已移除)
    # path('node/index', NodeView.index),
    # ...

    # 报警管理 (已移除)
    # path('alarm/index', AlarmView.index),
    # ...

    # 媒体资料管理 (已移除)
    # path('media/index', MediaView.index),
    # ...

    # 节点视频管理 (已移除)
    # path('stream/index', StreamView.index),
    # ...

    # 节点布控管理 (已移除)
    # path('control/index', ControlView.index),
    # ...

    # 标注任务 (核心业务 - A端管理)
    path('labelTask/index', LabelTaskView.index),
    path('labelTask/add', LabelTaskView.add),
    path('labelTask/edit', LabelTaskView.edit),
    path('labelTask/sync', LabelTaskView.api_sync),
    path('labelTask/postDel', LabelTaskView.api_postDel),
    
    # 样本管理 (核心业务 - B端标注)
    path('labelTask/sample', LabelTaskView.sample),
    path('labeltkSample/getInfo', LabelTkSampleView.api_getInfo),
    path('labeltkSample/postSaveAnnotation', LabelTkSampleView.api_postSaveAnnotation),
    path('labeltkSample/postDelAnnotation', LabelTkSampleView.api_postDelAnnotation),
    path('labeltkSample/getIndex', LabelTkSampleView.api_getIndex),
    path('labeltkSample/postAdd', LabelTkSampleView.api_postAdd),
    path('labeltkSample/postDel', LabelTkSampleView.api_postDel),
    
    # 训练/测试 (已移除，后续A端抽帧逻辑写在 LabelTaskView 中)
    # path('labeltkTrain/index', LabelTkTrainView.index),
    # ...

    # 内部接口 (已移除)
    # path('inner/on_stream_not_found', InnerlView.api_on_stream_not_found),

    # 开放接口 (已移除)
    # path('open/getIndex', OpenView.api_getIndex),
    # ...

    # 下载模块 (核心业务 - B端下载脱敏数据)
    path('storage/download', StorageView.download),
    path('storage/access', StorageView.access)
]