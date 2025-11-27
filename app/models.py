from django.db import models

# 保留核心模型，删除无关模型

class LabelTaskModel(models.Model):
    """
    [A端核心表] 标注任务/病例管理
    """
    sort = models.IntegerField(verbose_name='排序', default=0)
    code = models.CharField(max_length=50, verbose_name='任务编号', unique=True)
    
    # 归属信息
    user_id = models.IntegerField(verbose_name='创建人ID')
    username = models.CharField(max_length=100, verbose_name='创建人')
    
    # 任务基本信息
    name = models.CharField(max_length=50, verbose_name='任务名称')
    remark = models.TextField(verbose_name='备注', null=True, blank=True)
    
    # --- 新增/修改的核心字段 ---
    # 1. 视频源文件（存储在非公开目录，B端无法访问）
    source_video_path = models.CharField(max_length=500, verbose_name='源视频物理路径', null=True, blank=True)
    
    # 2. 加密病例数据（AES加密后的文件路径）
    patient_data_path = models.CharField(max_length=500, verbose_name='加密病例路径', null=True, blank=True)
    
    # 3. 抽帧处理配置
    video_fps = models.IntegerField(verbose_name='抽帧帧率', default=30) # 默认每秒30帧
    is_processed = models.BooleanField(verbose_name='是否已处理', default=False) # 视频是否已转为图片
    
    # 统计信息
    sample_count = models.IntegerField(verbose_name='样本总数', default=0)
    sample_annotation_count = models.IntegerField(verbose_name='已标注数', default=0)

    # 状态与时间
    state = models.IntegerField(verbose_name='状态', default=0) # 0:处理中 1:已就绪 2:已完成
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    create_timestamp = models.IntegerField(verbose_name='时间戳', default=0)
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='最后更新')

    def __repr__(self):
        return self.name

    class Meta:
        db_table = 'xcnvs_label_task'
        verbose_name = '任务与病例'
        verbose_name_plural = '任务与病例'


class LabelTkSampleModel(models.Model):
    """
    [B端核心表] 样本图片/脱敏数据
    B端用户只能接触到此表中的图片，绝对无法关联到 Task 表中的 source_video_path
    """
    sort = models.IntegerField(verbose_name='排序', default=0)
    code = models.CharField(max_length=50, verbose_name='样本编号')
    
    # 关联任务（仅存储Task编号，不物理关联，增加一层隔离）
    task_code = models.CharField(max_length=50, verbose_name='所属任务编号', db_index=True)
    
    # 图片存储（B端可读的静态资源路径）
    # 例如: static/upload/images/TK20231001/img_0001.jpg
    old_filename = models.CharField(max_length=200, verbose_name='脱敏文件名') # 如: img_0001.jpg
    new_filename = models.CharField(max_length=200, verbose_name='相对路径')   # 实际存储路径
    
    # 标注信息（B端上传的结果）
    annotation_content = models.TextField(verbose_name='标注数据', null=True, blank=True) # 存储JSON或XML字符串
    annotation_state = models.IntegerField(verbose_name='标注状态', default=0) # 0:未标注 1:已标注
    annotation_time = models.DateTimeField(verbose_name='标注时间', null=True, blank=True)
    annotation_username = models.CharField(max_length=100, verbose_name='标注员', null=True, blank=True)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    # 冗余字段，为了兼容旧代码可保留，暂不使用
    task_type = models.IntegerField(default=1) # 默认1:图片
    state = models.IntegerField(default=1)

    def __repr__(self):
        return self.code

    class Meta:
        db_table = 'xcnvs_labeltk_sample'
        verbose_name = '样本图片'
        verbose_name_plural = '样本图片'