
'''
在 Web 应用程序中处理 API 调用时可能发生的错误。

'''

import json, logging, inspect, functools
#基础错误，如类型、数据错误
class APIError(Exception):
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

#输入值错误或者无效
class APIValueError(APIError):
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)


class APIResourceNotFoundError(APIError):
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)

#权限错误
class APIPermissionError(APIError):
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)