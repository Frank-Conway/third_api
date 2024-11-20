from models import save_result_to_db, save_request_record

def handle_result(result, request_id):
    save_result_to_db(result, request_id)

def handle_request_record(url, data, status):
    return save_request_record(url, data, status)