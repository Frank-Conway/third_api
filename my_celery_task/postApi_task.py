import requests
from .celery import celery_app
from utils.db_helper import handle_result, handle_request_record
from utils.redis_helper import increment_retry_count


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5 * 60)
def call_third_party_api(self, url, data):
    try:
        response = requests.post(url, json=data)
        print(response.status_code)
        response.raise_for_status()
        result = response.json()
        print(result)
        request_id = handle_request_record(url, data, 'success')
        handle_result(result, request_id)
    except Exception as e:
        retry_count = increment_retry_count(url)
        if retry_count < self.max_retries:
            self.retry(exc=e, countdown=self.default_retry_delay)
        else:
            handle_request_record(url, data, 'failed')