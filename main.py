import os
import sys
import json
import logging
import tornado.ioloop
import tornado.web
from celery import Celery
from urllib.parse import quote
from celery.result import AsyncResult
from my_celery_task.celery import celery_app
from my_celery_task.postApi_task import call_third_party_api

# # 设置当前目录为系统路径（只需要一次）
# current_dir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(current_dir)

# 配置日志记录
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        url = 'http://127.0.0.1:9888/mysql-version'
        data = ''
        logger.info(f"Calling third-party API at {url}")
        # 异步调用 Celery 任务
        task1 = call_third_party_api.delay(url, data)
        logger.info(f"Task ID: {task1.id}")
        self.write({'status': 'success', 'task_id': task1.id})

    def post(self):
        try:
            body = self.request.body.decode('utf-8')
            data = json.loads(body)
            url = data.get('url', '')
            logger.info(f"Calling third-party API at {url}")
            task2 = call_third_party_api.delay((url, ''))
            logger.info(f"Task ID: {task2.id}")
            self.write({'status': 'success', 'task_id': task2.id})
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            self.set_status(400)
            self.write({'status': 'error', 'message': str(e)})
class TaskStatusHandler(tornado.web.RequestHandler):
    def get(self,id):
        result = AsyncResult(id=id, app=celery_app)
        if result.successful():
            print(result.get())
        if result.failed():
            print('任务失败')
        elif result.status == 'PENDING':
            print('任务正在等待中')
        elif result.status == 'RETRY':
            print('任务正在重试')
        elif result.status == 'STARTED':
            print('任务正在执行中')

def make_app():
    return tornado.web.Application([
        (r"/test", MainHandler),
        (r"/task-status/([a-zA-Z0-9-]+)", TaskStatusHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    logging.info("Server is running at http://127.0.0.1:8888")

    tornado.ioloop.IOLoop.current().start()