import os

# 目标文件：首页
target_path = os.path.join("templates", "app", "index.html")

# 修复后的代码
html_content = r"""{% extends "app/base_site.html" %}

{% block title %} 控制面板 {% endblock title %}

{% block content %}
<style>
    /* === 首页对齐强力修复样式 === */
    
    /* 1. 卡片容器：强制高度一致，内容居中 */
    .profile_view {
        min-height: 380px;    /* 固定最小高度，解决框大小不一的问题 */
        display: flex;
        flex-direction: column;
        justify-content: center; /* 内容垂直居中 */
        align-items: center;     /* 内容水平居中 */
        padding: 40px !important;
        border-width: 2px !important;
        border-style: solid !important;
        border-radius: 8px !important;
        background-color: #fff !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s;
    }
    .profile_view:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }

    /* 2. 按钮修复：图标和文字绝对对齐 */
    .btn-role {
        display: flex !important;
        align-items: center !important;      /* 垂直居中关键 */
        justify-content: center !important;  /* 水平居中关键 */
        height: 55px !important;             /* 增加高度，更易点击 */
        font-size: 18px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
        border-radius: 6px !important;
    }
    
    .btn-role i {
        margin-right: 10px;
        font-size: 22px;
        line-height: 1; /* 防止图标行高撑开 */
    }

    /* 3. 文字排版优化 */
    .role-title {
        margin-top: 0;
        margin-bottom: 15px;
        font-weight: 800;
        font-size: 24px;
    }
    .role-desc {
        color: #777; 
        margin-bottom: 30px; 
        font-size: 14px;
        min-height: 40px; /* 确保描述文字占位一致 */
    }
</style>

<div class="right_col" role="main" style="background-color: #f0f3f6; min-height: 90vh;">
  
  <div class="row tile_count">
    <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
      <span class="count_top"><i class="fa fa-clock-o"></i> 系统状态</span>
      <div class="count">运行中</div>
      <span class="count_bottom"><i class="green">Normal </i></span>
    </div>
  </div>

  <div class="row">
      <div class="col-md-12">
          <div class="x_panel" style="background: transparent; border: none; box-shadow: none;">
              <div class="x_title" style="border:none;">
                  <h2>🚀 快速开始 <small>请选择您的角色</small></h2>
                  <div class="clearfix"></div>
              </div>
              <div class="x_content">
                  <div class="row">
                      
                      <div class="col-md-6 col-sm-6 col-xs-12">
                          <div class="well profile_view" style="border-color: #337ab7;">
                              <div class="col-xs-12 bottom text-center">
                                  <div style="font-size: 40px; color: #337ab7; margin-bottom: 15px;">
                                      <i class="fa fa-user-md"></i>
                                  </div>
                                  <h2 class="role-title" style="color: #337ab7;">医院端 (A端)</h2>
                                  <p class="role-desc">上传病例文件、视频源，系统自动加密并抽帧。</p>
                                  
                                  <a href="/labelTask/add" class="btn btn-primary btn-lg btn-block btn-role">
                                      <i class="fa fa-plus-circle"></i> 新建病例任务
                                  </a>
                                  <a href="/labelTask/index" class="btn btn-default btn-block btn-role" style="background: #f9f9f9; border-color:#ccc;">
                                      <i class="fa fa-list"></i> 查看历史任务
                                  </a>
                              </div>
                          </div>
                      </div>

                      <div class="col-md-6 col-sm-6 col-xs-12">
                          <div class="well profile_view" style="border-color: #1abb9c;">
                              <div class="col-xs-12 bottom text-center">
                                  <div style="font-size: 40px; color: #1abb9c; margin-bottom: 15px;">
                                      <i class="fa fa-edit"></i>
                                  </div>
                                  <h2 class="role-title" style="color: #1abb9c;">标注端 (B端)</h2>
                                  <p class="role-desc">下载脱敏图片包，并在本地标注后上传结果。</p>
                                  
                                  <div style="height: 55px; margin-bottom: 15px;"></div>
                                  
                                  <a href="/labelTask/index" class="btn btn-success btn-lg btn-block btn-role">
                                      <i class="fa fa-folder-open"></i> 进入标注工作台
                                  </a>
                              </div>
                          </div>
                      </div>

                  </div>
              </div>
          </div>
      </div>
  </div>
</div>
{% endblock content %}
"""

# 执行覆盖
try:
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ 首页修复完成！已写入: {target_path}")
    print("请回到浏览器首页 (http://127.0.0.1:9824) 并按 [Ctrl + F5] 刷新。")
except Exception as e:
    print(f"❌ 写入失败: {e}")

    