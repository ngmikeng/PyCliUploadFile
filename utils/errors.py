
def get_error_message(err_data, err_status):
    err_msg = 'Error occurred.'
    if err_status:
        err_msg += f' Code: {err_status}'
    if err_data:
        if isinstance(err_data, dict):
            if err_data.get('error') is not None:
                msg = err_data.get('error')
                err_msg += f' Error: {msg}.'
            if err_data.get('message') is not None:
                msg = err_data.get('message')
                err_msg += f' Message: {msg}.'
        else:
            err_msg += f' {err_data}'

    return err_msg


def error_response(msg: str, payload=None):
    return {
        'error': True,
        'message': msg,
        'payload': payload
    }