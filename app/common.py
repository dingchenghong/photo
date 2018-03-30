def true_return(data, message):
    return {
        'code': 200,
        'data': data,
        'message': message
    }


def false_return(data, message):
    print(message)
    return {
        'code': 400,
        'data': data,
        'message': message
    }
