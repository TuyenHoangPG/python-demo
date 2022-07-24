def unauthorized(message=""):
    return {"data": None, "message": message}, 401


def forbidden(message=""):
    return {"data": None, "message": message}, 403


def error_bad_request(message=""):
    return {"data": None, "message": message}, 400


def error_not_found(message=""):
    return {"data": None, "message": message}, 404


def error_server_error(message=""):
    return {"data": None, "message": message}, 500


def success_created(data={}):
    return {"data": data, "message": "Success!"}, 201


def success(data={}):
    return {"data": data, "message": "Success!"}, 200
