from celery import Celery
from urllib.parse import quote

password = 'zh@123'
# 对密码进行URL编码
encoded_password = quote(password)

broker_url = f"redis://:{encoded_password}@localhost:6379/0"
# result_backend = f"redis://:{encoded_password}@localhost:6379/1"
result_backend = 'db+mysql://root:123456@localhost/zhihe'

# 创建 Celery 实例
celery_app = Celery(
    'test',
    broker=broker_url,
    backend=result_backend,
    include=['my_celery_task.postApi_task',]
)

celery_app.conf.timezone = 'Asia/Shanghai'
celery_app.conf.enable_utc = False

### 定时任务配置 ######
# 每隔5秒，爬一次百度
# from datetime import timedelta
# celery_app.conf.beat_schedule = {
#     'low-task': {
#         'task': 'my_celery_task.user_task.send_email',
#         'schedule': timedelta(seconds=5),
#         'args': ('aaaaa',),  # 没有参数传递
#     }
# }