def resp(data, message, code=200):
    return {
        'code': code,
        'data': data,
        'message': message
    }
